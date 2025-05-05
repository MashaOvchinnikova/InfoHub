import os
from alembic.config import Config
from alembic import command

service_path = os.path.dirname(os.path.abspath(__file__))
alembic_ini = os.path.join(service_path, 'alembic.ini')


def create_migration(message):
    """
    Создает новую миграцию.

    Args:
        message: Сообщение для миграции
    """
    print(f"Создание миграции '{message}' в {service_path}...")
    alembic_cfg = Config(alembic_ini)
    command.revision(alembic_cfg, autogenerate=True, message=message)
    print(f"Миграция '{message}' успешно создана")


if __name__ == "__main__":
    create_migration("Create tables for auth service")

