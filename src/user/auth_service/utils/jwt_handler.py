"""
Обработчик JWT токенов для управления черным списком и проверки токенов.
"""
import logging
from typing import Dict, List, Optional, Any

import redis
from jose import jwt, JWTError

import base64
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, Depends
from starlette import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request


from src.user.auth_service.config import settings
from src.user.auth_service.models.schemas.user_auth import TokenPayload

# Настройка логирования
logger = logging.getLogger(__name__)


def validate_token(token: str) -> TokenPayload | HTTPException:
    """
    Валидирует содержимое jwt токена, проверяет, не истек ли срок действия токена
    :param token: закодированный jwt токен
    :return: содержимое jwt токена, либо HTTPException, если валидация не прошла или токен просрочен
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Недействительные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt_handler.decode_token(token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            logger.warning("Недействительный токен: отсутствует sub или неверный тип")
            raise credentials_exception

        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            logger.warning("Недействительный токен: срок действия токена истек")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        token_data = TokenPayload(sub=user_id, exp=payload.get("exp"), type=token_type)
        return token_data

    except JWTError as e:

        logger.error(f"Ошибка декодирования JWT: {e}")

        raise credentials_exception


class AuthorizationToken(HTTPBearer):
    """
    Используется для проверки и валидации токена в заголовке Authorization запросов

    Применение
    __________
    Создайте объект класса и используйте этот объект в качестве зависимости в Depends().

    Результатом создания зависимости будет объект TokenPayload с содержимым jwt токена.

    Пример
    ______
    def get_current_user(token_data: TokenPayload = Depends(AuthorizationToken()):
        ...
    """
    def __init__(self, auto_error: bool = True):
        super(AuthorizationToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> TokenPayload | HTTPException:
        """
        Проверяет наличие и валидирует токен в заголовке Authorization запросов.
        :param request: запрос
        :return: содержимое токена, либо HTTPException, если токена нет или валидация не прошла
        """
        credentials: HTTPAuthorizationCredentials = await super(AuthorizationToken, self).__call__(request)
        token_payload = validate_token(credentials.credentials)
        return token_payload


class JWTHandler:
    """
    Обработчик JWT токенов с поддержкой черного списка.
    """

    def __init__(self, redis_url: str = None):
        """
        Инициализация обработчика JWT токенов.

        Args:
            redis_url: URL для подключения к Redis (для хранения черного списка токенов)
        """
        self.use_blacklist = False
        self.redis_client = None

        # Если указан URL Redis, настраиваем поддержку черного списка
        if redis_url:
            try:
                self.redis_client = redis.from_url(redis_url)
                self.use_blacklist = True
                logger.info("Поддержка черного списка токенов включена")
            except Exception as e:
                logger.error(f"Ошибка подключения к Redis: {e}")

    def create_access_token(
            self,
            subject: str,
            expires_delta: Optional[timedelta] = None,
            data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Создание JWT токена доступа.

        Args:
            subject: Идентификатор пользователя
            expires_delta: Время жизни токена
            data: Дополнительные данные для включения в токен

        Returns:
            str: JWT токен
        """
        to_encode = {}
        if data:
            to_encode.update(data)

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({
            "exp": expire,
            "sub": str(subject),
            "type": "access",
            "iat": datetime.utcnow()
        })

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    def create_refresh_token(self, subject: str) -> str:
        """
        Создание JWT токена обновления.

        Args:
            subject: Идентификатор пользователя

        Returns:
            str: JWT токен обновления
        """
        expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "refresh",
            "iat": datetime.utcnow()
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Декодирование и проверка JWT токена.

        Args:
            token: JWT токен

        Returns:
            Dict[str, Any]: Декодированные данные из токена

        Raises:
            JWTError: Если токен недействителен
        """
        # Проверка токена в черном списке
        if self.use_blacklist and self.is_token_blacklisted(token):
            logger.warning("Попытка использования токена из черного списка")
            raise JWTError("Token is blacklisted")

        # Декодирование токена
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload

    def blacklist_token(self, token: str) -> bool:
        """
        Добавление токена в черный список.

        Args:
            token: JWT токен

        Returns:
            bool: True если токен добавлен в черный список, иначе False
        """
        pass

jwt_handler = JWTHandler()