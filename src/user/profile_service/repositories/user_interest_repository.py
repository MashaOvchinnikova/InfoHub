
"""
Репозиторий для работы с интересами пользователей в базе данных.
"""
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.moderation.admin_service.database import database
from src.user.profile_service.models.domain.user_profile import UserInterest
from src.user.profile_service.models.schemas.user_profile import UserInterestCreate

# Настройка логирования
logger = logging.getLogger(__name__)

class UserInterestRepository:
    """
    Репозиторий для выполнения операций с интересами пользователей в БД.
    """
    def __init__(self, db: Session = Depends(database.get_session)) -> None:
        self.db = db

    def get_by_id(self, user_interest_id: uuid.UUID) -> Optional[UserInterest]:
        """
        Получение связи пользователя с интересом по ID.

        Args:
            user_interest_id: ID связи

        Returns:
            UserInterest | None: Объект связи или None, если не найден
        """
        return self.db.query(UserInterest).filter(UserInterest.user_interest_id == user_interest_id).first()

    def get_by_user_and_interest(self, user_id: uuid.UUID, interest_id: uuid.UUID) -> Optional[UserInterest]:
        """
        Получение связи по ID пользователя и ID интереса.

        Args:
            user_id: ID пользователя
            interest_id: ID интереса

        Returns:
            UserInterest | None: Объект связи или None, если не найден
        """
        return (
            self.db.query(UserInterest)
            .filter(UserInterest.user_id == user_id, UserInterest.interest_id == interest_id)
            .first()
        )

    def create(self, user_interest_data: UserInterestCreate, user_id: uuid.UUID) -> UserInterest:
        """
        Создание новой связи пользователя с интересом.

        Args:
            user_interest_data: Данные для создания связи
            user_id: ID пользователя

        Returns:
            UserInterest: Созданная связь

        Raises:
            SQLAlchemyError: При ошибке создания связи
        """
        try:
            db_user_interest = UserInterest(
                user_id=user_id,
                interest_id=user_interest_data.interest_id,
                weight=user_interest_data.weight
            )
            self.db.add(db_user_interest)
            self.db.commit()
            self.db.refresh(db_user_interest)
            logger.info(f"Создана связь пользователя {user_id} с интересом {user_interest_data.interest_id}")
            return db_user_interest
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при создании связи пользователя с интересом: {e}")
            raise

    def update_weight(self, user_id: uuid.UUID, interest_id: uuid.UUID, weight: float) -> Optional[UserInterest]:
        """
        Обновление веса интереса для пользователя.

        Args:
            user_id: ID пользователя
            interest_id: ID интереса
            weight: Новый вес интереса

        Returns:
            UserInterest | None: Обновленная связь или None, если связь не найдена

        Raises:
            SQLAlchemyError: При ошибке обновления веса
        """
        db_user_interest = self.get_by_user_and_interest(user_id, interest_id)
        if not db_user_interest:
            logger.warning(f"Попытка обновления несуществующей связи: пользователь {user_id}, интерес {interest_id}")
            return None

        try:
            db_user_interest.weight = weight
            self.db.commit()
            self.db.refresh(db_user_interest)
            logger.info(f"Обновлен вес интереса {interest_id} для пользователя {user_id}: {weight}")
            return db_user_interest
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при обновлении веса интереса: {e}")
            raise

    def delete(self, user_id: uuid.UUID, interest_id: uuid.UUID) -> bool:
        """
        Удаление связи пользователя с интересом.

        Args:
            user_id: ID пользователя
            interest_id: ID интереса

        Returns:
            bool: True если связь успешно удалена, иначе False

        Raises:
            SQLAlchemyError: При ошибке удаления связи
        """
        db_user_interest = self.get_by_user_and_interest(user_id, interest_id)
        if not db_user_interest:
            logger.warning(f"Попытка удаления несуществующей связи: пользователь {user_id}, интерес {interest_id}")
            return False

        try:
            self.db.delete(db_user_interest)
            self.db.commit()
            logger.info(f"Удалена связь пользователя {user_id} с интересом {interest_id}")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при удалении связи пользователя с интересом: {e}")
            raise

    def get_by_user_id(self, user_id: uuid.UUID) -> List[UserInterest]:
        """
        Получение всех интересов пользователя.

        Args:
            user_id: ID пользователя

        Returns:
            List[UserInterest]: Список связей пользователя с интересами
        """
        return self.db.query(UserInterest).filter(UserInterest.user_id == user_id).all()

    def get_users_by_interest(self, interest_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[UserInterest]:
        """
        Получение всех пользователей, интересующихся определенной темой.

        Args:
            interest_id: ID интереса
            skip: Количество записей для пропуска
            limit: Максимальное количество записей для возврата

        Returns:
            List[UserInterest]: Список связей пользователей с указанным интересом
        """
        return (
            self.db.query(UserInterest)
            .filter(UserInterest.interest_id == interest_id)
            .offset(skip)
            .limit(limit)
            .all()
        )