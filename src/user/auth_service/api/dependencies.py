"""
Зависимости для API эндпоинтов.
"""
import logging
from typing import Optional
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.user.auth_service.utils.jwt_handler import JWTHandler
from src.user.auth_service.repositories.user_auth_repository import UserAuthRepository
from src.user.auth_service.models.domain.user_auth import UserAuth
from src.user.auth_service.models.schemas.user_auth import TokenPayload, UserResponse
from src.user.auth_service.services.current_user import get_current_user

# Настройка логирования
logger = logging.getLogger(__name__)

# Настройка OAuth2 для получения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Репозиторий для работы с пользователями
user_repository = UserAuthRepository()


# jwt_handler = JWTHandler()


# async def get_current_user(
#         token: str = Depends(oauth2_scheme)
# ) -> UserAuth:
#     """
#     Получение текущего пользователя по токену.
#
#     Args:
#         token: JWT токен из заголовка
#
#     Returns:
#         UserAuth: Объект пользователя
#
#     Raises:
#         HTTPException: Если токен недействителен или пользователь не найден
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Недействительные учетные данные",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         # Декодирование токена
#         payload = jwt_handler.decode_token(token)
#         user_id: str = payload.get("sub")
#         token_type: str = payload.get("type")
#
#         if user_id is None or token_type != "access":
#             logger.warning("Недействительный токен: отсутствует sub или неверный тип")
#             raise credentials_exception
#
#         token_data = TokenPayload(sub=user_id, exp=payload.get("exp"), type=token_type)
#
#     except JWTError as e:
#         logger.error(f"Ошибка декодирования JWT: {e}")
#         raise credentials_exception


async def get_current_admin(current_user: UserAuth = Depends(get_current_user)) -> UserAuth:
    """
    Проверка, что текущий пользователь - администратор.

    Args:
        current_user: Текущий аутентифицированный пользователь

    Returns:
        UserAuth: Объект пользователя-администратора

    Raises:
        HTTPException: Если пользователь не имеет прав администратора
    """
    if not current_user.is_admin:
        logger.warning(f"Пользователь {current_user.user_id} пытался получить доступ к админ-функциям")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    return current_user


# def get_user_repository() -> UserAuthRepository:
#     """
#     Получение репозитория для работы с пользователями.
#
#     Returns:
#         UserAuthRepository: Репозиторий пользователей
#     """
#     return user_repository
