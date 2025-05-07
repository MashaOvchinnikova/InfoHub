"""
Основной роутер для сервиса профилей пользователей.
"""
from fastapi import APIRouter

from src.user.profile_service.api.routers.profile import router as profile_router
from src.user.profile_service.api.routers.interest import router as interest_router
# from src.user.profile_service.api.routers.user_interest import router as user_interest_router
from src.user.profile_service.api.routers.activity import router as activity_router

# Создание основного роутера
router = APIRouter()

# Регистрация маршрутов
router.include_router(profile_router)
router.include_router(interest_router)
router.include_router(activity_router)
# router.include_router(user_interest_router)