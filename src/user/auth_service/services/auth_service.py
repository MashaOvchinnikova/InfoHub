"""
Сервисный слой для операций аутентификации и авторизации.
"""
import logging
from datetime import timedelta
from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status

from src.user.auth_service.utils.jwt_handler import jwt_handler
from src.user.auth_service.models.domain.user_auth import UserAuth
from src.user.auth_service.config import settings
from src.user.auth_service.repositories.user_auth_repository import UserAuthRepository

from src.user.auth_service.models.schemas.user_auth import UserCreate, UserLogin, RefreshToken, ChangePassword, \
    UserResponse, Token, MessageResponse

# Настройка логирования
logger = logging.getLogger(__name__)


class AuthService:
    """
    Сервис для операций аутентификации и авторизации.
    """

    def __init__(self, user_repo: UserAuthRepository = Depends(UserAuthRepository)):
        self.user_repo = user_repo

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Регистрация нового пользователя.

        Args:
            user_data: Данные для создания пользователя

        Returns:
        UserResponse: Информация о созданном пользователе

    Raises:
        HTTPException: Если email или имя пользователя уже существуют
        """
        # Проверка, что email уникален
        if self.user_repo.get_by_email(user_data.email):
            logger.warning(f"Попытка регистрации с существующим email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )

        # Проверка, что имя пользователя уникально
        if self.user_repo.get_by_username(user_data.username):
            logger.warning(f"Попытка регистрации с существующим username: {user_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует"
            )

        # Создание пользователя
        try:
            db_user = self.user_repo.create(user_data)
            logger.info(f"Пользователь зарегистрирован успешно: {db_user.email}")
            return UserResponse.model_validate(db_user)
        except Exception as e:
            logger.error(f"Ошибка при регистрации пользователя: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла ошибка при регистрации. Попробуйте позже."
            )

    def authenticate_user(self, login_data: UserLogin) -> Token:
        """
        Аутентификация пользователя.

        Args:
            login_data: Данные для входа пользователя

        Returns:
            Optional[UserAuth]: Пользователь если аутентификация успешна, иначе None
        """
        # Аутентификация пользователя
        user = self.user_repo.authenticate(login_data.email, login_data.password)
        if not user:
            logger.warning(f"Неудачная попытка входа: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Проверка, что пользователь не заблокирован
        if user.is_blocked:
            logger.warning(f"Блокированный пользователь пытается войти: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт заблокирован. Обратитесь к администратору."
            )

        # Проверка, что пользователь активен
        if not user.is_active:
            logger.warning(f"Неактивный пользователь пытается войти: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт неактивен. Проверьте свою почту для активации."
            )

        # Создание токенов
        token_pair = self.create_tokens(user)
        return Token.model_validate(token_pair)

    def refresh_token(self, token_data: RefreshToken) -> Token:
        """
           Обновление токена доступа по refresh токену.

           Args:
               token_data: Refresh токен

           Returns:
               Token: Новые токены доступа и обновления

           Raises:
               HTTPException: Если токен обновления недействителен
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен обновления",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Декодирование токена обновления
            payload = jwt_handler.decode_token(token_data.refresh_token)
            user_id = payload.get("sub")
            token_type = payload.get("type")

            if user_id is None or token_type != "refresh":
                logger.warning("Недействительный refresh токен")
                raise credentials_exception

            # Проверка пользователя
            user = self.user_repo.get_by_id(user_id)
            if not user or not user.is_active or user.is_blocked:
                logger.warning(f"Пользователь недоступен при обновлении токена: {user_id}")
                raise credentials_exception

            # Создание новых токенов
            new_token_pair = self.create_tokens(user)
            logger.info(f"Токен успешно обновлен для пользователя: {user.email}")
            return Token.model_validate(new_token_pair)

        except Exception as e:
            logger.error(f"Ошибка при обновлении токена: {e}")
            raise credentials_exception

    def create_tokens(self, user: UserAuth) -> Dict[str, str]:
        """
        Создание токенов доступа и обновления для пользователя.

        Args:
            user: Объект пользователя

        Returns:
            Dict[str, str]: Словарь с токенами
        """
        access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = jwt_handler.create_access_token(
            subject=str(user.user_id),
            expires_delta=access_token_expires,
            data={"email": user.email, "is_admin": user.is_admin}
        )

        refresh_token = jwt_handler.create_refresh_token(subject=str(user.user_id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def change_user_password(
            self,
            password_data: ChangePassword,
            current_user: UserResponse
    ) -> MessageResponse:
        """
            Изменение пароля текущего пользователя.

            Args:
                password_data: Данные для изменения пароля
                current_user: Текущий аутентифицированный пользователь
            Returns:
                MessageResponse: Сообщение об успешном изменении пароля

            Raises:
                HTTPException: Если текущий пароль неверен
        """
        # Проверка текущего пароля
        user = self.user_repo.authenticate(current_user.email, password_data.current_password)
        if not user:
            logger.warning(f"Неверный текущий пароль при смене пароля: {current_user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текущий пароль неверен"
            )

        # Изменение пароля
        success = self.user_repo.change_password(current_user.user_id, password_data.new_password)
        if not success:
            logger.error(f"Ошибка при изменении пароля: {current_user.email}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла ошибка при изменении пароля"
            )

        logger.info(f"Пароль успешно изменен для пользователя: {current_user.email}")
        message = {"message": "Пароль успешно изменен"}
        return MessageResponse.model_validate(message)