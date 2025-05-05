import os
import logging
from alembic.config import Config
from alembic import command

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


service_path = os.path.dirname(os.path.abspath(__file__))
migration_path = os.path.join(service_path, 'migrations')
alembic_ini = os.path.join(service_path, 'alembic.ini')


def run_migrations():
    """Запуск миграций до последней версии."""
    alembic_cfg = Config(alembic_ini)
    command.upgrade(alembic_cfg, "head")
    logger.info("Database migrations completed successfully")


if __name__ == "__main__":
    run_migrations()
