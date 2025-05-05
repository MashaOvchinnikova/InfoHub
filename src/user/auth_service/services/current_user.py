import uuid

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

import logging
from src.user.auth_service.models.schemas.user_auth import TokenPayload, UserResponse
from src.user.auth_service.utils.jwt_handler import AuthorizationToken
from src.user.auth_service.database import database
from src.user.auth_service.models.domain.user_auth import UserAuth

# Настройка логирования
logger = logging.getLogger(__name__)


def get_current_user(token_data: TokenPayload = Depends(AuthorizationToken()),
                     session: Session = Depends(database.get_session)) -> UserResponse:
    """
    Возвращает модель текущего аутентифицированного пользователя

    Применение
    __________
    Используйте эту функцию в качестве зависимости в Depends().

    Результатом создания зависимости будет объект UserAuth с инф-ей о пользователе

    Пример
    ______
        @user_router.get('/user')
    def get_current_user(user: UserAuth = Depends(get_current_user)) \
        -> UserAuth:
    return user

    :param token_data: содержимое jwt токена из заголовка Authorization запроса
    :param session: сессия для подключения к бд
    :return: Модель оператора или клиента в зависимости от роли, зашитой в токене
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Недействительные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = uuid.UUID(token_data.sub)
    # Получение пользователя из БД
    user: UserAuth = session.query(UserAuth).filter(UserAuth.user_id == user_id).first()
    if user is None:
        logger.warning(f"Пользователь с ID {user_id} не найден")
        raise credentials_exception

    # Проверка активности пользователя
    if not user.is_active or user.is_blocked:
        logger.warning(f"Пользователь {user_id} неактивен или заблокирован")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Аккаунт неактивен или заблокирован"
        )

    return UserResponse.model_validate(user)
