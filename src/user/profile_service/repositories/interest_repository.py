"""
Репозиторий для работы с интересами пользователей в базе данных.
"""
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.moderation.admin_service.database import database
from src.user.profile_service.models.domain.user_profile import Interest
from src.user.profile_service.models.schemas.user_profile import InterestCreate, InterestUpdate

# Настройка логирования
logger = logging.getLogger(__name__)

class InterestRepository:
    """
    Репозиторий для выполнения операций с интересами в БД.
    """
    def __init__(self, db: Session = Depends(database.get_session)) -> None:
        self.db = db

    def get_by_id(self, interest_id: uuid.UUID) -> Optional[Interest]:
        """
        Получение интереса по ID.

        Args:
            interest_id: ID интереса

        Returns:
            Interest | None: Объект интереса или None, если не найден
        """
        return self.db.query(Interest).filter(Interest.interest_id == interest_id).first()

    def get_by_name(self, name: str) -> Optional[Interest]:
        """
        Получение интереса по имени.

        Args:
            name: Имя интереса

        Returns:
            Interest | None: Объект интереса или None, если не найден
        """
        return self.db.query(Interest).filter(Interest.name == name).first()

    def create(self, interest_data: InterestCreate) -> Interest:
        """
        Создание нового интереса.

        Args:
            interest_data: Данные для создания интереса

        Returns:
            Interest: Созданный интерес

        Raises:
            SQLAlchemyError: При ошибке создания интереса
        """
        try:
            db_interest = Interest(
                name=interest_data.name,
                description=interest_data.description,
                parent_id=interest_data.parent_id
            )
            self.db.add(db_interest)
            self.db.commit()
            self.db.refresh(db_interest)
            logger.info(f"Создан интерес: {db_interest.name}")
            return db_interest
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при создании интереса: {e}")
            raise

    def update(self, interest_id: uuid.UUID, interest_data: InterestUpdate) -> Optional[Interest]:
        """
        Обновление интереса.

        Args:
            interest_id: ID интереса
            interest_data: Данные для обновления

        Returns:
            Interest | None: Обновленный интерес или None, если интерес не найден

        Raises:
            SQLAlchemyError: При ошибке обновления интереса
        """
        db_interest = self.get_by_id(interest_id)
        if not db_interest:
            logger.warning(f"Попытка обновления несуществующего интереса: {interest_id}")
            return None

        try:
            update_data = interest_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_interest, key, value)

            self.db.commit()
            self.db.refresh(db_interest)
            logger.info(f"Обновлен интерес: {db_interest.name}")
            return db_interest
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при обновлении интереса: {e}")
            raise

    def delete(self, interest_id: uuid.UUID) -> bool:
        """
        Удаление интереса.

        Args:
            interest_id: ID интереса

        Returns:
            bool: True если интерес успешно удален, иначе False

        Raises:
            SQLAlchemyError: При ошибке удаления интереса
        """
        db_interest = self.get_by_id(interest_id)
        if not db_interest:
            logger.warning(f"Попытка удаления несуществующего интереса: {interest_id}")
            return False

        try:
            self.db.delete(db_interest)
            self.db.commit()
            logger.info(f"Удален интерес: {db_interest.name}")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при удалении интереса: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Interest]:
        """
        Получение списка интересов с пагинацией.

        Args:
            skip: Количество интересов для пропуска
            limit: Максимальное количество интересов для возврата

        Returns:
            List[Interest]: Список интересов
        """
        return self.db.query(Interest).offset(skip).limit(limit).all()

    def get_root_interests(self) -> List[Interest]:
        """
        Получение корневых интересов (без родителя).

        Returns:
            List[Interest]: Список корневых интересов
        """
        return self.db.query(Interest).filter(Interest.parent_id == None).all()

    def get_hierarchy(self) -> List[Interest]:
        """
        Получение иерархии интересов с предзагрузкой дочерних элементов.

        Returns:
            List[Interest]: Список корневых интересов с загруженными дочерними элементами
        """
        return (
            self.db.query(Interest)
            .filter(Interest.parent_id == None)
            .options(joinedload(Interest.children).joinedload(Interest.children))
            .all()
        )

    def get_child_interests(self, parent_id: uuid.UUID) -> List[Interest]:
        """
        Получение дочерних интересов для указанного родительского интереса.

        Args:
            parent_id: ID родительского интереса

        Returns:
            List[Interest]: Список дочерних интересов
        """
        return self.db.query(Interest).filter(Interest.parent_id == parent_id).all()