"""
Репозиторий для работы с активностями пользователей в базе данных.
"""
import uuid
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.moderation.admin_service.database import database
from src.user.profile_service.models.domain.user_profile import Activity
from src.user.profile_service.models.schemas.user_profile import ActivityCreate

# Настройка логирования
logger = logging.getLogger(__name__)

class ActivityRepository:
    """
    Репозиторий для выполнения операций с активностями пользователей в БД.
    """
    def __init__(self, db: Session = Depends(database.get_session)) -> None:
        self.db = db

    def get_by_id(self, activity_id: uuid.UUID) -> Optional[Activity]:
        """
        Получение активности по ID.

        Args:
            activity_id: ID активности

        Returns:
            Activity | None: Объект активности или None, если не найден
        """
        return self.db.query(Activity).filter(Activity.activity_id == activity_id).first()

    def create(self, activity_data: ActivityCreate) -> Activity:
        """
        Создание новой записи активности.

        Args:
            activity_data: Данные для создания активности

        Returns:
            Activity: Созданная активность

        Raises:
            SQLAlchemyError: При ошибке создания активности
        """
        try:
            db_activity = Activity(
                user_id=activity_data.user_id,
                activity_type=activity_data.activity_type,
                entity_type=activity_data.entity_type,
                entity_id=activity_data.entity_id
            )
            self.db.add(db_activity)
            self.db.commit()
            self.db.refresh(db_activity)
            logger.info(f"Создана активность пользователя {activity_data.user_id}: {activity_data.activity_type}")
            return db_activity
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при создании активности пользователя: {e}")
            raise

    def delete(self, activity_id: uuid.UUID) -> bool:
        """
        Удаление активности.

        Args:
            activity_id: ID активности

        Returns:
            bool: True если активность успешно удалена, иначе False

        Raises:
            SQLAlchemyError: При ошибке удаления активности
        """
        db_activity = self.get_by_id(activity_id)
        if not db_activity:
            logger.warning(f"Попытка удаления несуществующей активности: {activity_id}")
            return False

        try:
            self.db.delete(db_activity)
            self.db.commit()
            logger.info(f"Удалена активность пользователя: {activity_id}")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при удалении активности пользователя: {e}")
            raise

    def get_by_user_id(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Activity]:
        """
        Получение активностей пользователя с пагинацией.

        Args:
            user_id: ID пользователя
            skip: Количество активностей для пропуска
            limit: Максимальное количество активностей для возврата

        Returns:
            List[Activity]: Список активностей пользователя
        """
        return (
            self.db.query(Activity)
            .filter(Activity.user_id == user_id)
            .order_by(desc(Activity.created_date))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_recent_activities(self, user_id: uuid.UUID, days: int = 7) -> List[Activity]:
        """
        Получение недавних активностей пользователя.

        Args:
            user_id: ID пользователя
            days: Количество дней для выборки

        Returns:
            List[Activity]: Список недавних активностей пользователя
        """
        since_date = datetime.utcnow() - timedelta(days=days)
        return (
            self.db.query(Activity)
            .filter(Activity.user_id == user_id, Activity.created_date >= since_date)
            .order_by(desc(Activity.created_date))
            .all()
        )

    def get_activity_count_by_type(self, user_id: uuid.UUID) -> dict:
        """
        Получение количества активностей пользователя по типам.

        Args:
            user_id: ID пользователя

        Returns:
            dict: Словарь с количеством активностей по типам
        """
        results = (
            self.db.query(Activity.activity_type, func.count(Activity.activity_id))
            .filter(Activity.user_id == user_id)
            .group_by(Activity.activity_type)
            .all()
        )
        return {activity_type: count for activity_type, count in results}

    def get_by_entity(self, entity_type: str, entity_id: uuid.UUID) -> List[Activity]:
        """
        Получение активностей, связанных с определенной сущностью.

        Args:
            entity_type: Тип сущности
            entity_id: ID сущности

        Returns:
            List[Activity]: Список активностей для сущности
        """
        return (
            self.db.query(Activity)
            .filter(Activity.entity_type == entity_type, Activity.entity_id == entity_id)
            .order_by(desc(Activity.created_date))
            .all()
        )