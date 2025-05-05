-- Скрипт для заполнения базы данных проекта InfoHub тестовыми данными
-- Порядок заполнения таблиц учитывает зависимости между ними
BEGIN;

-- ===============================================================
-- auth_service
-- ===============================================================

-- Добавление пользователей для аутентификации
INSERT INTO auth_service_schema.user_auth (user_id, email, username, password_hash, is_active, is_admin, is_blocked, created_at, updated_at, last_login_date) VALUES
('123e4567-e89b-12d3-a456-426614174001', 'ivan@example.com', 'ivan_dev', '$2b$12$KhESzFgw.Mf7Ts.YBVm9gu5HZLKkbT4WyXJePVR9M.bzWnbnju33m', true, false, false, '2023-01-01 12:00:00', '2023-01-01 12:00:00', '2023-04-15 15:30:00'),
('123e4567-e89b-12d3-a456-426614174002', 'maria@example.com', 'maria_designer', '$2b$12$P9XgHtS.8xhMt3jYkKKfZeqECQgMGz0wI2.KU7GyWBt.v1JfZuj2.', true, false, false, '2023-01-02 14:30:00', '2023-01-02 14:30:00', '2023-04-16 17:45:00'),
('123e4567-e89b-12d3-a456-426614174003', 'alex@example.com', 'alex_devops', '$2b$12$3dCLuKZ.qCdDZ3xz9iAo9eRgFOXHnS4joYWaUHCSt.RKV4aQlQx9S', true, false, false, '2023-01-03 09:15:00', '2023-01-03 09:15:00', '2023-04-14 12:20:00'),
('123e4567-e89b-12d3-a456-426614174004', 'olga@example.com', 'olga_ui', '$2b$12$aT5.x8jYUQ5r7U3jh7Z/T.G0Lqpw1KjXsHK9QU7wDgc3rnD3/6gCW', true, false, false, '2023-01-04 11:45:00', '2023-01-04 11:45:00', '2023-04-13 14:10:00'),
('123e4567-e89b-12d3-a456-426614174005', 'admin@infohub.com', 'admin', '$2b$12$r7Z5J2SX3LMrV9JD.3wm8usX3fT.wgTJ3appX4vyWjnO4TnzCKpHC', true, true, false, '2023-01-01 00:00:00', '2023-01-01 00:00:00', '2023-04-17 09:00:00');

-- ===============================================================
-- profile_service
-- ===============================================================

-- Добавление профилей пользователей
INSERT INTO profile_service_schema.user_profile (user_id, bio, registration_date, reputation_score) VALUES
('123e4567-e89b-12d3-a456-426614174001', 'Python разработчик с опытом работы более 5 лет. Интересуюсь машинным обучением и обработкой данных.', '2023-01-01 12:00:00', 150),
('123e4567-e89b-12d3-a456-426614174002', 'Frontend разработчик и дизайнер интерфейсов. Специализируюсь на React и UI/UX.', '2023-01-02 14:30:00', 120),
('123e4567-e89b-12d3-a456-426614174003', 'DevOps инженер с опытом работы в крупных проектах. Эксперт по Docker и Kubernetes.', '2023-01-03 09:15:00', 180),
('123e4567-e89b-12d3-a456-426614174004', 'UI/UX дизайнер с художественным образованием. Создаю красивые и удобные интерфейсы.', '2023-01-04 11:45:00', 90),
('123e4567-e89b-12d3-a456-426614174005', 'Администратор платформы. Отвечаю за управление контентом и модерацию.', '2023-01-01 00:00:00', 200);

-- Добавление интересов/категорий
INSERT INTO profile_service_schema.interest (interest_id, name, description, parent_id) VALUES
('f5b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d', 'Разработка', 'Программирование, создание ПО и технологии разработки', NULL),
('1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d', 'Дизайн', 'Проектирование интерфейсов, графический дизайн, UX/UI', NULL),
('2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e', 'DevOps', 'Практики объединения разработки и эксплуатации ПО', NULL),
('3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f', 'Искусственный интеллект', 'Машинное обучение, нейросети и алгоритмы ИИ', NULL),
('4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a', 'Базы данных', 'Проектирование, использование и оптимизация БД', NULL),
('5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b', 'Веб-разработка', 'Разработка веб-приложений и сайтов', 'f5b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d'),
('6f7a8b9c-0d1e-2f3a-4b5c-6d7e8f9a0b1c', 'Мобильная разработка', 'Разработка приложений для мобильных устройств', 'f5b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d'),
('7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d', 'Backend', 'Серверная часть приложений', 'f5b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d'),
('8b9c0d1e-2f3a-4b5c-6d7e-8f9a0b1c2d3e', 'Frontend', 'Клиентская часть приложений', 'f5b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d'),
('9c0d1e2f-3a4b-5c6d-7e8f-9a0b1c2d3e4f', 'UX/UI', 'Дизайн пользовательского опыта и интерфейсов', '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d'),
('0d1e2f3a-4b5c-6d7e-8f9a-0b1c2d3e4f5a', 'Графический дизайн', 'Создание визуальных материалов', '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d'),
('1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b', 'CI/CD', 'Непрерывная интеграция и доставка', '2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e'),
('2f3a4b5c-6d7e-8f9a-0b1c-2d3e4f5a6b7c', 'Контейнеризация', 'Docker, Kubernetes и управление контейнерами', '2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e'),
('3a4b5c6d-7e8f-9a0b-1c2d-3e4f5a6b7c8d', 'Машинное обучение', 'Алгоритмы и методы машинного обучения', '3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f'),
('4b5c6d7e-8f9a-0b1c-2d3e-4f5a6b7c8d9e', 'Нейронные сети', 'Глубокое обучение и нейронные сети', '3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f'),
('5c6d7e8f-9a0b-1c2d-3e4f-5a6b7c8d9e0f', 'SQL', 'Язык структурированных запросов', '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a'),
('6d7e8f9a-0b1c-2d3e-4f5a-6b7c8d9e0f1a', 'NoSQL', 'Нереляционные базы данных', '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a');

-- Добавление связей пользователь-интерес
INSERT INTO profile_service_schema.user_interest (user_interest_id, user_id, interest_id, weight) VALUES
('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', '123e4567-e89b-12d3-a456-426614174001', 'f5b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d', 1.5),
('b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', '123e4567-e89b-12d3-a456-426614174001', '7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d', 2.0),
('c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', '123e4567-e89b-12d3-a456-426614174001', '3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f', 1.8),
('d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', '123e4567-e89b-12d3-a456-426614174001', '3a4b5c6d-7e8f-9a0b-1c2d-3e4f5a6b7c8d', 1.9),
('e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b', '123e4567-e89b-12d3-a456-426614174002', 'f5b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d', 1.2),
('f6a7b8c9-d0e1-2f3a-4b5c-6d7e8f9a0b1c', '123e4567-e89b-12d3-a456-426614174002', '8b9c0d1e-2f3a-4b5c-6d7e-8f9a0b1c2d3e', 2.0),
('a7b8c9d0-e1f2-3a4b-5c6d-7e8f9a0b1c2d', '123e4567-e89b-12d3-a456-426614174002', '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d', 1.7),
('b8c9d0e1-f2a3-4b5c-6d7e-8f9a0b1c2d3e', '123e4567-e89b-12d3-a456-426614174002', '9c0d1e2f-3a4b-5c6d-7e8f-9a0b1c2d3e4f', 1.9),
('c9d0e1f2-a3b4-5c6d-7e8f-9a0b1c2d3e4f', '123e4567-e89b-12d3-a456-426614174003', '2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e', 2.0),
('d0e1f2a3-b4c5-6d7e-8f9a-0b1c2d3e4f5a', '123e4567-e89b-12d3-a456-426614174003', '1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b', 1.8),
('e1f2a3b4-c5d6-7e8f-9a0b-1c2d3e4f5a6b', '123e4567-e89b-12d3-a456-426614174003', '2f3a4b5c-6d7e-8f9a-0b1c-2d3e4f5a6b7c', 1.9),
('f2a3b4c5-d6e7-8f9a-0b1c-2d3e4f5a6b7c', '123e4567-e89b-12d3-a456-426614174004', '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d', 2.0),
('a3b4c5d6-e7f8-9a0b-1c2d-3e4f5a6b7c8d', '123e4567-e89b-12d3-a456-426614174004', '9c0d1e2f-3a4b-5c6d-7e8f-9a0b1c2d3e4f', 2.0),
('b4c5d6e7-f8a9-0b1c-2d3e-4f5a6b7c8d9e', '123e4567-e89b-12d3-a456-426614174004', '0d1e2f3a-4b5c-6d7e-8f9a-0b1c2d3e4f5a', 1.7),
('c5d6e7f8-a9b0-1c2d-3e4f-5a6b7c8d9e0f', '123e4567-e89b-12d3-a456-426614174005', 'f5b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d', 1.2),
('d6e7f8a9-b0c1-2d3e-4f5a-6b7c8d9e0f1a', '123e4567-e89b-12d3-a456-426614174005', '2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e', 1.1),
('e7f8a9b0-c1d2-3e4f-5a6b-7c8d9e0f1a2b', '123e4567-e89b-12d3-a456-426614174005', '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a', 1.3);

-- Добавление активности пользователей
INSERT INTO profile_service_schema.activity (activity_id, user_id, activity_type, entity_type, entity_id, created_date) VALUES
('f8a9b0c1-d2e3-4f5a-6b7c-8d9e0f1a2b3c', '123e4567-e89b-12d3-a456-426614174001', 'view', 'source', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', '2023-03-15 10:30:00'),
('a9b0c1d2-e3f4-5a6b-7c8d-9e0f1a2b3c4d', '123e4567-e89b-12d3-a456-426614174001', 'add', 'source', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', '2023-03-10 14:20:00'),
('b0c1d2e3-f4a5-6b7c-8d9e-0f1a2b3c4d5e', '123e4567-e89b-12d3-a456-426614174001', 'rate', 'source', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', '2023-03-12 16:45:00'),
('c1d2e3f4-a5b6-7c8d-9e0f-1a2b3c4d5e6f', '123e4567-e89b-12d3-a456-426614174001', 'comment', 'source', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', '2023-03-12 16:50:00'),
('d2e3f4a5-b6c7-8d9e-0f1a-2b3c4d5e6f7a', '123e4567-e89b-12d3-a456-426614174002', 'view', 'source', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', '2023-03-20 09:15:00'),
('e3f4a5b6-c7d8-9e0f-1a2b-3c4d5e6f7a8b', '123e4567-e89b-12d3-a456-426614174002', 'add', 'source', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', '2023-02-15 13:20:00'),
('f4a5b6c7-d8e9-0f1a-2b3c-4d5e6f7a8b9c', '123e4567-e89b-12d3-a456-426614174002', 'rate', 'source', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', '2023-03-16 11:30:00'),
('a5b6c7d8-e9f0-1a2b-3c4d-5e6f7a8b9c0d', '123e4567-e89b-12d3-a456-426614174003', 'view', 'source', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', '2023-04-01 15:20:00'),
('b6c7d8e9-f0a1-2b3c-4d5e-6f7a8b9c0d1e', '123e4567-e89b-12d3-a456-426614174003', 'add', 'source', 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', '2023-07-05 10:15:00'),
('c7d8e9f0-a1b2-3c4d-5e6f-7a8b9c0d1e2f', '123e4567-e89b-12d3-a456-426614174003', 'add', 'source', 'd4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', '2023-04-25 09:30:00'),
('d8e9f0a1-b2c3-4d5e-6f7a-8b9c0d1e2f3a', '123e4567-e89b-12d3-a456-426614174004', 'view', 'source', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', '2023-06-25 14:10:00'),
('e9f0a1b2-c3d4-5e6f-7a8b-9c0d1e2f3a4b', '123e4567-e89b-12d3-a456-426614174004', 'add', 'source', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', '2023-06-20 12:30:00'),
('f0a1b2c3-d4e5-6f7a-8b9c-0d1e2f3a4b5c', '123e4567-e89b-12d3-a456-426614174004', 'comment', 'source', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', '2023-06-22 16:40:00');

-- ===============================================================
-- content_service
-- ===============================================================

-- Добавление тегов
INSERT INTO content_service_schema.tag (tag_id, name, description, usage_count) VALUES
('3c5e8c5a-9231-4934-9178-953249f78c2e', 'программирование', 'Статьи, видео и ресурсы по программированию', 15),
('fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d', 'python', 'Материалы по языку программирования Python', 12),
('b32a1c0e-5d9f-4c3b-8a7d-9e0f1c2b3a4d', 'javascript', 'Ресурсы по JavaScript', 10),
('7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', 'машинное обучение', 'Материалы по машинному обучению и искусственному интеллекту', 20),
('4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a', 'дизайн', 'Ресурсы по дизайну интерфейсов и графике', 8),
('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'микросервисы', 'Архитектура микросервисов', 5),
('e5f6a7b8-c9d0-e1f2-a3b4-c5d6e7f8a9b0', 'базы данных', 'Материалы по базам данных и SQL', 7),
('9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'фронтенд', 'Разработка пользовательских интерфейсов', 9),
('5c6d7e8f-9a0b-1c2d-3e4f-5a6b7c8d9e0f', 'бэкенд', 'Серверная разработка', 8),
('1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b', 'DevOps', 'Практики и инструменты DevOps', 6);

-- Добавление источников информации
INSERT INTO content_service_schema.source (source_id, title, url, description, thumbnail_url, content_type, publication_date, added_date, added_by, is_verified, is_recommended, avg_rating) VALUES
('aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 'Основы Python для начинающих', 'https://example.com/python-basics', 'Подробное руководство по основам языка Python для новичков', 'https://example.com/images/python.jpg', 'article', '2023-01-15', '2023-01-20', '123e4567-e89b-12d3-a456-426614174001', true, true, 4.8),
('b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 'JavaScript: Продвинутые концепции', 'https://example.com/advanced-js', 'Глубокое погружение в продвинутые концепции JavaScript', 'https://example.com/images/js.jpg', 'article', '2023-02-10', '2023-02-15', '123e4567-e89b-12d3-a456-426614174002', true, true, 4.5),
('c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 'Введение в машинное обучение с Python', 'https://example.com/ml-intro', 'Базовый курс по машинному обучению с использованием Python', 'https://example.com/images/ml.jpg', 'course', '2023-03-01', '2023-03-10', '123e4567-e89b-12d3-a456-426614174001', true, true, 4.9),
('d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'Микросервисная архитектура в действии', 'https://example.com/microservices', 'Практическое руководство по построению микросервисов', 'https://example.com/images/microservices.jpg', 'book', '2023-04-20', '2023-04-25', '123e4567-e89b-12d3-a456-426614174003', true, false, 4.2),
('e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 'Оптимизация SQL запросов', 'https://example.com/sql-optimization', 'Советы по оптимизации SQL запросов для высокой производительности', 'https://example.com/images/sql.jpg', 'article', '2023-05-05', '2023-05-10', '123e4567-e89b-12d3-a456-426614174002', false, false, 4.0),
('f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 'Дизайн мобильных интерфейсов', 'https://example.com/mobile-ui', 'Лучшие практики дизайна мобильных приложений', 'https://example.com/images/mobile-ui.jpg', 'video', '2023-06-15', '2023-06-20', '123e4567-e89b-12d3-a456-426614174004', true, true, 4.7),
('a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', 'Руководство по CI/CD для DevOps', 'https://example.com/ci-cd-guide', 'Подробное руководство по настройке и использованию CI/CD', 'https://example.com/images/ci-cd.jpg', 'article', '2023-07-01', '2023-07-05', '123e4567-e89b-12d3-a456-426614174003', true, false, 4.3),
('b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 'React: С нуля до продакшена', 'https://example.com/react-guide', 'Полное руководство по React с нуля до продвинутого уровня', 'https://example.com/images/react.jpg', 'course', '2023-08-10', '2023-08-15', '123e4567-e89b-12d3-a456-426614174002', true, true, 4.6),
('c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9', 'FastAPI: Создание высокопроизводительных API', 'https://example.com/fastapi-guide', 'Руководство по созданию API с использованием FastAPI', 'https://example.com/images/fastapi.jpg', 'article', '2023-09-01', '2023-09-05', '123e4567-e89b-12d3-a456-426614174001', false, false, 4.4),
('d0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 'Основы Docker для разработчиков', 'https://example.com/docker-basics', 'Базовое введение в Docker для разработчиков', 'https://example.com/images/docker.jpg', 'video', '2023-10-10', '2023-10-15', '123e4567-e89b-12d3-a456-426614174003', true, true, 4.8);

-- Связи между источниками и тегами
INSERT INTO content_service_schema.source_tag (source_tag_id, source_id, tag_id) VALUES
('11223344-5566-7788-99aa-bbccddeeff00', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', '3c5e8c5a-9231-4934-9178-953249f78c2e'),
('22334455-6677-8899-aabb-ccddeeff0011', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 'fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d'),
('33445566-7788-99aa-bbcc-ddeeff001122', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', '3c5e8c5a-9231-4934-9178-953249f78c2e'),
('44556677-8899-aabb-ccdd-eeff00112233', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 'b32a1c0e-5d9f-4c3b-8a7d-9e0f1c2b3a4d'),
('55667788-99aa-bbcc-ddee-ff0011223344', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f'),
('66778899-aabb-ccdd-eeff-001122334455', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 'fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d'),
('778899aa-bbcc-ddee-ff00-112233445566', 'd4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d'),
('8899aabb-ccdd-eeff-0011-223344556677', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 'e5f6a7b8-c9d0-e1f2-a3b4-c5d6e7f8a9b0'),
('99aabbcc-ddee-ff00-1122-3344556677bb', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a'),
('aabbccdd-eeff-0011-2233-445566778899', 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', '1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b'),
('bbccddee-ff00-1122-3344-556677889900', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', '9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'),
('ccddeeff-0011-2233-4455-6677889900aa', 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9', '5c6d7e8f-9a0b-1c2d-3e4f-5a6b7c8d9e0f'),
('ddeeff00-1122-3344-5566-778899aabbcc', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', '1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b');

-- Оценки источников пользователями
INSERT INTO content_service_schema.rating (rating_id, user_id, source_id, value, created_date, updated_date) VALUES
('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6e', '123e4567-e89b-12d3-a456-426614174001', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 5, '2023-01-22', '2023-01-22'),
('b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', '123e4567-e89b-12d3-a456-426614174002', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 5, '2023-01-25', '2023-01-25'),
('c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', '123e4567-e89b-12d3-a456-426614174003', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 4, '2023-01-27', '2023-01-27'),
('d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9b', '123e4567-e89b-12d3-a456-426614174004', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 5, '2023-01-30', '2023-01-30'),
('e5f6a7b8-c9d0-e1f2-a3b4-c5d6e7f8a9b1', '123e4567-e89b-12d3-a456-426614174001', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 4, '2023-02-16', '2023-02-16'),
('f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c2', '123e4567-e89b-12d3-a456-426614174002', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 5, '2023-02-18', '2023-02-18'),
('a7b8c9d0-e1f2-a3b4-c5d6-e7f8a9b0c1d3', '123e4567-e89b-12d3-a456-426614174003', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 4, '2023-02-20', '2023-02-20'),
('b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e4', '123e4567-e89b-12d3-a456-426614174001', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 5, '2023-03-12', '2023-03-12'),
('c9d0e1f2-a3b4-c5d6-e7f8-a9b0c1d2e3f5', '123e4567-e89b-12d3-a456-426614174002', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 5, '2023-03-15', '2023-03-15');

-- ===============================================================
-- collection_service
-- ===============================================================

-- Добавление коллекций пользователей
INSERT INTO collection_service_schema.collection (collection_id, user_id, name, description, is_public, created_date, updated_date) VALUES
('f1e2d3c4-b5a6-7890-1234-567890abcdef', '123e4567-e89b-12d3-a456-426614174001', 'Python для Data Science', 'Материалы для изучения Python в контексте Data Science', true, '2023-01-25', '2023-01-25'),
('e2d3c4f1-b5a6-7890-1234-567890abcdef', '123e4567-e89b-12d3-a456-426614174002', 'Frontend разработка', 'Ресурсы по современному фронтенду', true, '2023-02-20', '2023-03-15'),
('d3c4f1e2-b5a6-7890-1234-567890abcdef', '123e4567-e89b-12d3-a456-426614174003', 'DevOps инструменты', 'Подборка материалов по DevOps', false, '2023-03-10', '2023-03-10'),
('c4f1e2d3-b5a6-7890-1234-567890abcdef', '123e4567-e89b-12d3-a456-426614174001', 'Мой бэкенд', 'Личная коллекция по бэкенд-разработке', true, '2023-04-05', '2023-04-20'),
('b5a6c4f1-7890-1234-5678-90abcdef1234', '123e4567-e89b-12d3-a456-426614174004', 'UI/UX дизайн', 'Материалы по дизайну интерфейсов', true, '2023-05-12', '2023-05-12');

-- Добавление источников в коллекции
INSERT INTO collection_service_schema.collection_source (collection_source_id, collection_id, source_id, added_date, note) VALUES
('a1b2c3d4-e5f6-7890-1234-567890abcdef', 'f1e2d3c4-b5a6-7890-1234-567890abcdef', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', '2023-01-26', 'Отличный материал для начинающих'),
('b2c3d4a1-e5f6-7890-1234-567890abcdef', 'f1e2d3c4-b5a6-7890-1234-567890abcdef', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', '2023-01-27', 'Хороший старт по ML'),
('c3d4a1b2-e5f6-7890-1234-567890abcdef', 'e2d3c4f1-b5a6-7890-1234-567890abcdef', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', '2023-02-21', 'Важно для понимания JS'),
('d4a1b2c3-e5f6-7890-1234-567890abcdef', 'e2d3c4f1-b5a6-7890-1234-567890abcdef', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', '2023-02-22', NULL),
('e5f6a1b2-7890-1234-5678-90abcdef1234', 'd3c4f1e2-b5a6-7890-1234-567890abcdef', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', '2023-03-11', 'Базовый уровень Docker'),
('f6a1b2e5-7890-1234-5678-90abcdef1234', 'd3c4f1e2-b5a6-7890-1234-567890abcdef', 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', '2023-03-12', 'Полезно для CI/CD пайплайнов'),
('a1b2e5f6-7890-1234-5678-90abcdef1234', 'c4f1e2d3-b5a6-7890-1234-567890abcdef', 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9', '2023-04-06', 'Хороший материал по FastAPI'),
('b2e5f6a1-7890-1234-5678-90abcdef1234', 'b5a6c4f1-7890-1234-5678-90abcdef1234', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', '2023-05-13', 'Полезно для работы с мобильными UI');

-- ===============================================================
-- social_service
-- ===============================================================

-- Подписки пользователей друг на друга
INSERT INTO social_service_schema.subscription (subscription_id, follower_id, followed_id, created_date) VALUES
('a7b8c9d0-e1f2-3456-7890-1234567890ab', '123e4567-e89b-12d3-a456-426614174001', '123e4567-e89b-12d3-a456-426614174002', '2023-01-15'),
('b8c9d0a7-e1f2-3456-7890-1234567890ab', '123e4567-e89b-12d3-a456-426614174002', '123e4567-e89b-12d3-a456-426614174001', '2023-01-16'),
('c9d0a7b8-e1f2-3456-7890-1234567890ab', '123e4567-e89b-12d3-a456-426614174003', '123e4567-e89b-12d3-a456-426614174001', '2023-02-01'),
('d0a7b8c9-e1f2-3456-7890-1234567890ab', '123e4567-e89b-12d3-a456-426614174001', '123e4567-e89b-12d3-a456-426614174003', '2023-02-10'),
('e1f2a7b8-3456-7890-1234-567890abcdef', '123e4567-e89b-12d3-a456-426614174004', '123e4567-e89b-12d3-a456-426614174001', '2023-03-05'),
('f2a7b8e1-3456-7890-1234-567890abcdef', '123e4567-e89b-12d3-a456-426614174004', '123e4567-e89b-12d3-a456-426614174002', '2023-03-15'),
('a7b8e1f2-3456-7890-1234-567890abcdef', '123e4567-e89b-12d3-a456-426614174002', '123e4567-e89b-12d3-a456-426614174004', '2023-04-01');

-- Комментарии к источникам
INSERT INTO social_service_schema.comment (comment_id, user_id, source_id, parent_comment_id, content, created_date, updated_date, is_deleted) VALUES
('ac5e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', NULL, 'Очень полезный материал для новичков в Python!', '2023-01-21', '2023-01-21', false),
('bc6e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174002', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 'ac5e8c5a-9231-4934-9178-953249f78c2e', 'Согласен, особенно понравилась часть про генераторы', '2023-01-22', '2023-01-22', false),
('cc7e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', NULL, 'Отличный глубокий материал по JS!', '2023-02-16', '2023-02-16', false),
('dc8e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174003', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', NULL, 'Хороший вводный курс по ML, но не хватает практики', '2023-03-15', '2023-03-16', false),
('ec9e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174004', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 'dc8e8c5a-9231-4934-9178-953249f78c2e', 'Можно дополнить курсом по практическому ML от Stanford', '2023-03-17', '2023-03-17', false),
('fc0e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', NULL, 'Очень актуальные примеры мобильных интерфейсов', '2023-06-21', '2023-06-21', false),
('ac1e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174003', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', NULL, 'Хорошее введение в Docker, рекомендую начинающим', '2023-10-16', '2023-10-16', false);

-- ===============================================================
-- admin_service
-- ===============================================================

-- Добавление жалоб на источники
INSERT INTO admin_service_schema.complaint (complaint_id, user_id, source_id, reason, description, status, created_date, resolved_date) VALUES
('ad5e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174002', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 'misleading', 'Информация в статье устарела, содержит неактуальные примеры SQL', 'pending', '2023-05-12', NULL),
('bd6e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174003', 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9', 'inappropriate', 'Статья содержит рекламный контент', 'resolved', '2023-09-10', '2023-09-15'),
('cd7e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 'misleading', 'Примеры в статье не работают с последними версиями PostgreSQL', 'pending', '2023-05-15', NULL),
('dd8e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174004', 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9', 'spam', 'Статья содержит множество ссылок на платные курсы', 'rejected', '2023-09-12', '2023-09-16');

-- ===============================================================
-- recommendation_service
-- ===============================================================

-- Персональные рекомендации для пользователей
INSERT INTO recommendation_service_schema.user_recommendations (recommendation_id, user_id, source_id, recommendation_type, relevance_score, explanation, interests, created_at, updated_at, is_shown, is_clicked) VALUES
('ae5e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 'personalized', 0.85, 'На основе вашего интереса к программированию', ARRAY['3c5e8c5a-9231-4934-9178-953249f78c2e'::uuid, 'fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d'::uuid], '2023-03-01', '2023-03-01', 3, 1),
('be6e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 'trending', 0.75, 'Популярно среди пользователей с похожими интересами', ARRAY['3c5e8c5a-9231-4934-9178-953249f78c2e'::uuid, '1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b'::uuid], '2023-03-01', '2023-03-01', 2, 0),
('ce7e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174002', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 'interest_based', 0.92, 'Соответствует вашему интересу к машинному обучению', ARRAY['7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f'::uuid], '2023-03-05', '2023-03-05', 1, 1),
('de8e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174003', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 'personalized', 0.68, 'На основе вашего интереса к фронтенду и дизайну', ARRAY['4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a'::uuid, '9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'::uuid], '2023-03-10', '2023-03-10', 2, 0),
('ee9e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174004', 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', 'similar', 0.79, 'Похоже на источники, которые вы просматривали ранее', NULL, '2023-03-15', '2023-03-15', 4, 2);

-- Похожие источники
INSERT INTO recommendation_service_schema.similar_sources (similar_id, source_id, similar_source_id, similarity_score, similarity_reasons, created_at, updated_at) VALUES
('af5e8c5a-9231-4934-9178-953249f78c2e', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 0.75, '{"common_tags": ["python", "программирование"], "common_users": 5}', '2023-03-01', '2023-03-01'),
('bf6e8c5a-9231-4934-9178-953249f78c2e', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 0.85, '{"common_tags": ["javascript", "фронтенд"], "common_users": 7}', '2023-03-05', '2023-03-05'),
('cf7e8c5a-9231-4934-9178-953249f78c2e', 'd4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', 0.65, '{"common_tags": ["микросервисы", "DevOps"], "common_users": 3}', '2023-03-10', '2023-03-10'),
('df8e8c5a-9231-4934-9178-953249f78c2e', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 0.70, '{"common_tags": ["базы данных"], "common_users": 4}', '2023-03-15', '2023-03-15');

-- Популярные источники
INSERT INTO recommendation_service_schema.popular_sources (popular_id, source_id, view_count, save_count, share_count, rating_avg, rating_count, popularity_score, time_period, category, created_at, updated_at) VALUES
('ef0e8c5a-9231-4934-9178-953249f78c2e', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 1250, 145, 87, 4.8, 98, 8.7, 'monthly', 'programming', '2023-03-01', '2023-03-01'),
('f01e8c5a-9231-4934-9178-953249f78c2e', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 2345, 267, 152, 4.9, 187, 9.2, 'monthly', 'data_science', '2023-03-01', '2023-03-01'),
('f12e8c5a-9231-4934-9178-953249f78c2e', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 1870, 203, 94, 4.7, 132, 8.4, 'monthly', 'design', '2023-03-01', '2023-03-01'),
('f23e8c5a-9231-4934-9178-953249f78c2e', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 1520, 176, 83, 4.6, 121, 8.2, 'monthly', 'frontend', '2023-03-01', '2023-03-01'),
('f34e8c5a-9231-4934-9178-953249f78c2e', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 1430, 164, 79, 4.8, 116, 8.5, 'monthly', 'devops', '2023-03-01', '2023-03-01'),

('f45e8c5a-9231-4934-9178-953249f78c2e', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 5780, 642, 324, 4.8, 412, 8.9, 'all_time', 'programming', '2023-01-01', '2023-03-01'),
('f56e8c5a-9231-4934-9178-953249f78c2e', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 9450, 1032, 583, 4.9, 754, 9.4, 'all_time', 'data_science', '2023-01-01', '2023-03-01'),
('f67e8c5a-9231-4934-9178-953249f78c2e', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 7230, 843, 423, 4.7, 587, 8.6, 'all_time', 'design', '2023-01-01', '2023-03-01'),
('f78e8c5a-9231-4934-9178-953249f78c2e', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 6120, 704, 352, 4.6, 498, 8.3, 'all_time', 'frontend', '2023-01-01', '2023-03-01'),
('f89e8c5a-9231-4934-9178-953249f78c2e', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 5840, 657, 312, 4.8, 473, 8.7, 'all_time', 'devops', '2023-01-01', '2023-03-01'),

('f90e8c5a-9231-4934-9178-953249f78c2e', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 423, 47, 22, 4.8, 36, 8.5, 'weekly', 'programming', '2023-03-01', '2023-03-01'),
('fa1e8c5a-9231-4934-9178-953249f78c2e', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 587, 68, 35, 4.9, 52, 9.0, 'weekly', 'data_science', '2023-03-01', '2023-03-01'),
('fb2e8c5a-9231-4934-9178-953249f78c2e', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 524, 57, 29, 4.7, 46, 8.3, 'weekly', 'design', '2023-03-01', '2023-03-01'),
('fc3e8c5a-9231-4934-9178-953249f78c2e', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 456, 49, 23, 4.6, 42, 8.1, 'weekly', 'frontend', '2023-03-01', '2023-03-01'),
('fd4e8c5a-9231-4934-9178-953249f78c2e', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 438, 51, 26, 4.8, 41, 8.4, 'weekly', 'devops', '2023-03-01', '2023-03-01'),

('fe5e8c5a-9231-4934-9178-953249f78c2e', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 128, 15, 7, 4.8, 12, 8.6, 'daily', 'programming', '2023-03-01', '2023-03-01'),
('ff6e8c5a-9231-4934-9178-953249f78c2e', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 165, 21, 9, 4.9, 17, 9.1, 'daily', 'data_science', '2023-03-01', '2023-03-01'),
('007e8c5a-9231-4934-9178-953249f78c2e', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 142, 17, 8, 4.7, 14, 8.2, 'daily', 'design', '2023-03-01', '2023-03-01'),
('018e8c5a-9231-4934-9178-953249f78c2e', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 134, 16, 7, 4.6, 13, 8.0, 'daily', 'frontend', '2023-03-01', '2023-03-01'),
('029e8c5a-9231-4934-9178-953249f78c2e', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 129, 14, 6, 4.8, 12, 8.3, 'daily', 'devops', '2023-03-01', '2023-03-01');

-- Рекомендации по интересам
INSERT INTO recommendation_service_schema.interest_recommendations (recommendation_id, interest_id, source_id, relevance_score, created_at, updated_at) VALUES
('03ae8c5a-9231-4934-9178-953249f78c2e', '3c5e8c5a-9231-4934-9178-953249f78c2e', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 0.92, '2023-03-01', '2023-03-01'),
('04be8c5a-9231-4934-9178-953249f78c2e', '3c5e8c5a-9231-4934-9178-953249f78c2e', 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9', 0.85, '2023-03-01', '2023-03-01'),
('05ce8c5a-9231-4934-9178-953249f78c2e', 'fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 0.89, '2023-03-01', '2023-03-01'),
('06de8c5a-9231-4934-9178-953249f78c2e', 'fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 0.87, '2023-03-01', '2023-03-01'),
('07ee8c5a-9231-4934-9178-953249f78c2e', '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 0.95, '2023-03-01', '2023-03-01'),
('08fe8c5a-9231-4934-9178-953249f78c2e', '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 0.91, '2023-03-01', '2023-03-01'),
('090e8c5a-9231-4934-9178-953249f78c2e', '9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 0.83, '2023-03-01', '2023-03-01'),
('0a1e8c5a-9231-4934-9178-953249f78c2e', '1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 0.88, '2023-03-01', '2023-03-01'),
('0b2e8c5a-9231-4934-9178-953249f78c2e', '1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b', 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', 0.86, '2023-03-01', '2023-03-01'),
('0c3e8c5a-9231-4934-9178-953249f78c2e', '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 0.84, '2023-03-01', '2023-03-01');

-- Предпочтения пользователей
INSERT INTO recommendation_service_schema.user_preferences (preference_id, user_id, liked_sources, disliked_sources, viewed_sources, interest_weights, content_type_preferences, created_at, updated_at) VALUES
('0d4e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001',
  ARRAY['aaf4c61d-f067-4470-9a8d-baaf9a28f23f'::uuid, 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f'::uuid, 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9'::uuid],
  ARRAY['e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5'::uuid],
  '{"aaf4c61d-f067-4470-9a8d-baaf9a28f23f": 15, "c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f": 12, "b90c0d12-7c1e-4588-9fb0-3a4a30e92401": 5, "c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9": 8}',
  '{"3c5e8c5a-9231-4934-9178-953249f78c2e": 0.9, "7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f": 0.8, "fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d": 0.6}',
  '{"article": 0.8, "course": 0.9, "video": 0.7, "book": 0.5}',
  '2023-01-15', '2023-03-01'),

('0e5e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174002',
  ARRAY['b90c0d12-7c1e-4588-9fb0-3a4a30e92401'::uuid, 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3'::uuid],
  ARRAY['d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a'::uuid, 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5'::uuid],
  '{"b90c0d12-7c1e-4588-9fb0-3a4a30e92401": 18, "b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3": 14, "c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f": 7}',
  '{"fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d": 0.95, "7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f": 0.65, "4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a": 0.5}',
  '{"article": 0.7, "course": 0.85, "video": 0.6, "book": 0.4}',
  '2023-01-20', '2023-03-01'),

('0f6e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174003',
  ARRAY['d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a'::uuid, 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7'::uuid, 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5'::uuid],
  ARRAY['f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1'::uuid],
  '{"d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a": 10, "a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7": 9, "d0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5": 12}',
  '{"1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b": 0.85, "3c5e8c5a-9231-4934-9178-953249f78c2e": 0.4}',
  '{"article": 0.6, "video": 0.85, "book": 0.7, "course": 0.5}',
  '2023-01-25', '2023-03-01'),

('107e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174004',
  ARRAY['f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1'::uuid, 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3'::uuid],
  ARRAY['e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5'::uuid, 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f'::uuid],
  '{"f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1": 16, "b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3": 11, "a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7": 6}',
  '{"4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a": 0.9, "9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d": 0.85, "fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d": 0.7}',
  '{"video": 0.9, "article": 0.75, "course": 0.8, "book": 0.3}',
  '2023-01-30', '2023-03-01'),

('118e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174005',
  ARRAY['c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f'::uuid, 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f'::uuid, 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9'::uuid],
  ARRAY['b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3'::uuid],
  '{"c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f": 20, "aaf4c61d-f067-4470-9a8d-baaf9a28f23f": 13, "c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9": 9}',
  '{"7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f": 0.95, "3c5e8c5a-9231-4934-9178-953249f78c2e": 0.85}',
  '{"course": 0.95, "article": 0.8, "book": 0.75, "video": 0.6}',
  '2023-02-05', '2023-03-01');

-- ===============================================================
-- search_service
-- ===============================================================

-- Заполнение поискового индекса (денормализованные данные из source и других таблиц)
INSERT INTO search_service_schema.search_index (index_id, source_id, title, description, url, content_type,
                         publication_date, added_date, avg_rating, is_verified, is_recommended,
                         tags, tag_ids, interests, interest_ids, added_by_username,
                         popularity_score, relevance_score, thumbnail_url, created_at, updated_at, search_vector) VALUES
('e2f3a4b5-c6d7-e8f9-a0b1-c2d3e4f5a6b7', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 'Основы Python для начинающих',
 'Подробное руководство по основам языка Python для новичков', 'https://example.com/python-basics',
 'article', '2023-01-15', '2023-01-20', 4.8, true, true,
 ARRAY['python', 'программирование', 'обучение'],
 ARRAY['fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d'::uuid, '3c5e8c5a-9231-4934-9178-953249f78c2e'::uuid],
 ARRAY['Программирование', 'Обучение'],
 ARRAY['5f6a7b8c-9d0e-1f2a-3b4c-5d6e7f8a9b0c'::uuid, 'd2e3f4a5-b6c7-d8e9-f0a1-b2c3d4e5f6a7'::uuid],
 'python_expert', 85.3, 0.95, 'https://example.com/images/python.jpg', '2023-01-20', '2023-01-20',
 'python программирование обучение руководство основы начинающие разработка'),

('f8a9b0c1-d2e3-f4a5-b6c7-d8e9f0a1b2c3', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 'JavaScript: Продвинутые концепции',
 'Глубокое погружение в продвинутые концепции JavaScript', 'https://example.com/advanced-js',
 'article', '2023-02-10', '2023-02-15', 4.5, true, true,
 ARRAY['javascript', 'фронтенд', 'программирование'],
 ARRAY['b32a1c0e-5d9f-4c3b-8a7d-9e0f1c2b3a4d'::uuid, '9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'::uuid, '3c5e8c5a-9231-4934-9178-953249f78c2e'::uuid],
 ARRAY['Веб-разработка', 'Программирование'],
 ARRAY['a7b8c9d0-e1f2-a3b4-c5d6-e7f8a9b0c1d2'::uuid, '5f6a7b8c-9d0e-1f2a-3b4c-5d6e7f8a9b0c'::uuid],
 'js_guru', 78.6, 0.88, 'https://example.com/images/js.jpg', '2023-02-15', '2023-02-15',
 'javascript фронтенд программирование концепции продвинутые разработка веб'),

('a0b1c2d3-e4f5-a6b7-c8d9-e0f1a2b3c4d5', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 'Введение в машинное обучение с Python',
 'Базовый курс по машинному обучению с использованием Python', 'https://example.com/ml-intro',
 'course', '2023-03-01', '2023-03-10', 4.9, true, true,
 ARRAY['машинное обучение', 'python', 'data science'],
 ARRAY['7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f'::uuid, 'fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d'::uuid],
 ARRAY['Искусственный интеллект', 'Анализ данных', 'Программирование'],
 ARRAY['b3c4d5e6-f7a8-b9c0-d1e2-f3a4b5c6d7e8'::uuid, 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9'::uuid, '5f6a7b8c-9d0e-1f2a-3b4c-5d6e7f8a9b0c'::uuid],
 'data_scientist', 92.1, 0.97, 'https://example.com/images/ml.jpg', '2023-03-10', '2023-03-10',
 'машинное обучение python data science искусственный интеллект анализ данных курс введение'),

('b4c5d6e7-f8a9-b0c1-d2e3-f4a5b6c7d8e9', 'd4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'Микросервисная архитектура в действии',
 'Практическое руководство по построению микросервисов', 'https://example.com/microservices',
 'book', '2023-04-20', '2023-04-25', 4.2, true, false,
 ARRAY['микросервисы', 'бэкенд', 'архитектура'],
 ARRAY['a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d'::uuid, '5c6d7e8f-9a0b-1c2d-3e4f-5a6b7c8d9e0f'::uuid],
 ARRAY['Архитектура ПО', 'Программирование'],
 ARRAY['d5e6f7a8-b9c0-d1e2-f3a4-b5c6d7e8f9a0'::uuid, '5f6a7b8c-9d0e-1f2a-3b4c-5d6e7f8a9b0c'::uuid],
 'software_architect', 68.5, 0.82, 'https://example.com/images/microservices.jpg', '2023-04-25', '2023-04-25',
 'микросервисы бэкенд архитектура разработка распределенные системы построение руководство'),

('c8d9e0f1-a2b3-c4d5-e6f7-a8b9c0d1e2f3', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 'Оптимизация SQL запросов',
 'Советы по оптимизации SQL запросов для высокой производительности', 'https://example.com/sql-optimization',
 'article', '2023-05-05', '2023-05-10', 4.0, false, false,
 ARRAY['базы данных', 'SQL', 'оптимизация'],
 ARRAY['e5f6a7b8-c9d0-e1f2-a3b4-c5d6e7f8a9b0'::uuid],
 ARRAY['Базы данных', 'Производительность'],
 ARRAY['e6f7a8b9-c0d1-e2f3-a4b5-c6d7e8f9a0b1'::uuid, 'f7a8b9c0-d1e2-f3a4-b5c6-d7e8f9a0b1c2'::uuid],
 'db_specialist', 65.2, 0.78, 'https://example.com/images/sql.jpg', '2023-05-10', '2023-05-10',
 'базы данных sql оптимизация запросы производительность советы');

-- Заполнение таблицы поисковых запросов
INSERT INTO search_service_schema.search_query (query_id, user_id, query_text, query_params, results_count, execution_time_ms, created_at, ip_address) VALUES
('d0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', '123e4567-e89b-12d3-a456-426614174001', 'python машинное обучение',
 '{"content_type": ["article", "course"], "sort_by": "relevance"}', 8, 120, '2023-03-15 14:35:22', '192.168.1.101'),
('e1f2a3b4-c5d6-e7f8-a9b0-c1d2e3f4a5b6', '123e4567-e89b-12d3-a456-426614174002', 'javascript фреймворки',
 '{"content_type": ["article"], "sort_by": "date_desc"}', 5, 95, '2023-03-20 09:12:45', '192.168.1.102'),
('f2a3b4c5-d6e7-f8a9-b0c1-d2e3f4a5b6c7', '123e4567-e89b-12d3-a456-426614174003', 'микросервисы архитектура',
 '{"content_type": ["book", "article"], "sort_by": "rating_desc"}', 3, 110, '2023-04-10 18:20:33', '192.168.1.103'),
('a3b4c5d6-e7f8-a9b0-c1d2-e3f4a5b6c7d8', '123e4567-e89b-12d3-a456-426614174001', 'sql оптимизация',
 '{"content_type": ["article"], "sort_by": "relevance"}', 6, 88, '2023-05-22 11:45:17', '192.168.1.101'),
('b4c5d6e7-f8a9-b0c1-d2e3-f4a5-b6c7d8e9', '123e4567-e89b-12d3-a456-426614174004', 'дизайн мобильных приложений',
 '{"content_type": ["video"], "sort_by": "rating_desc"}', 4, 102, '2023-06-25 15:30:28', '192.168.1.104'),
('c5d6e7f8-a9b0-c1d2-e3f4-a5b6-c7d8e9f0', '123e4567-e89b-12d3-a456-426614174002', 'react redux tutorial',
 '{"content_type": ["article", "course"], "sort_by": "date_desc"}', 7, 125, '2023-08-18 10:15:09', '192.168.1.102'),
('d6e7f8a9-b0c1-d2e3-f4a5-b6c7-d8e9f0a1', '123e4567-e89b-12d3-a456-426614174003', 'docker kubernetes',
 '{"content_type": ["video", "article"], "sort_by": "relevance"}', 9, 131, '2023-10-20 16:40:51', '192.168.1.103'),
('e7f8a9b0-c1d2-e3f4-a5b6-c7d8-e9f0a1b2', NULL, 'fastapi python',
 '{"content_type": ["article"], "sort_by": "date_desc"}', 3, 78, '2023-09-08 13:22:47', '192.168.1.200');

-- Популярные поисковые запросы
INSERT INTO search_service_schema.popular_search (id, query_text, count, last_searched_at, daily_count, weekly_count, monthly_count, created_at, updated_at) VALUES
('f8a9b0c1-d2e3-f4a5-b6c7-d8e9-f0a1b2c3', 'python машинное обучение', 132, '2023-10-25 14:35:22', 12, 45, 132, '2023-03-15 14:35:22', '2023-10-25 14:35:22'),
('a9b0c1d2-e3f4-a5b6-c7d8-e9f0a1b2c3d4', 'javascript фреймворки', 98, '2023-10-24 11:12:45', 8, 37, 98, '2023-03-20 09:12:45', '2023-10-24 11:12:45'),
('b0c1d2e3-f4a5-b6c7-d8e9-f0a1b2c3d4e5', 'микросервисы архитектура', 56, '2023-10-23 16:40:33', 5, 22, 56, '2023-04-10 18:20:33', '2023-10-23 16:40:33'),
('c1d2e3f4-a5b6-c7d8-e9f0-a1b2c3d4e5f6', 'sql оптимизация', 74, '2023-10-22 09:15:17', 7, 28, 74, '2023-05-22 11:45:17', '2023-10-22 09:15:17'),
('d2e3f4a5-b6c7-d8e9-f0a1-b2c3d4e5f6a7', 'react redux', 115, '2023-10-25 10:45:09', 15, 48, 115, '2023-08-18 10:15:09', '2023-10-25 10:45:09'),
('e3f4a5b6-c7d8-e9f0-a1b2-c3d4e5f6a7b8', 'docker kubernetes', 89, '2023-10-24 14:30:51', 9, 35, 89, '2023-10-20 16:40:51', '2023-10-24 14:30:51'),
('f4a5b6c7-d8e9-f0a1-b2c3-d4e5f6a7b8c9', 'fastapi python', 42, '2023-10-23 11:22:47', 4, 18, 42, '2023-09-08 13:22:47', '2023-10-23 11:22:47'),
('a5b6c7d8-e9f0-a1b2-c3d4-e5f6a7b8c9d0', 'дизайн интерфейсов', 63, '2023-10-22 15:30:28', 6, 25, 63, '2023-06-25 15:30:28', '2023-10-22 15:30:28');

-- Недавние поисковые запросы пользователей
INSERT INTO search_service_schema.user_recent_search (id, user_id, query_text, query_params, created_at) VALUES
('b6c7d8e9-f0a1-b2c3-d4e5-f6a7b8c9d0e1', '123e4567-e89b-12d3-a456-426614174001', 'python data science',
 '{"content_type": ["course", "article"], "sort_by": "relevance"}', '2023-10-25 09:45:12'),
('c7d8e9f0-a1b2-c3d4-e5f6-a7b8c9d0e1f2', '123e4567-e89b-12d3-a456-426614174001', 'машинное обучение основы',
 '{"content_type": ["course"], "sort_by": "rating_desc"}', '2023-10-24 14:30:45'),
('d8e9f0a1-b2c3-d4e5-f6a7-b8c9d0e1f2a3', '123e4567-e89b-12d3-a456-426614174001', 'sql запросы примеры',
 '{"content_type": ["article"], "sort_by": "relevance"}', '2023-10-23 16:20:33'),
('e9f0a1b2-c3d4-e5f6-a7b8-c9d0e1f2a3b4', '123e4567-e89b-12d3-a456-426614174002', 'javascript typescript отличия',
 '{"content_type": ["article"], "sort_by": "date_desc"}', '2023-10-25 10:15:27'),
('f0a1b2c3-d4e5-f6a7-b8c9-d0e1f2a3b4c5', '123e4567-e89b-12d3-a456-426614174002', 'react хуки использование',
 '{"content_type": ["article", "video"], "sort_by": "relevance"}', '2023-10-24 11:40:38'),
('a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6', '123e4567-e89b-12d3-a456-426614174003', 'docker compose руководство',
 '{"content_type": ["article"], "sort_by": "rating_desc"}', '2023-10-25 13:25:19'),
('b2c3d4e5-f6a7-b8c9-d0e1-f2a3b4c5d6e7', '123e4567-e89b-12d3-a456-426614174003', 'микросервисы patterns',
 '{"content_type": ["book", "article"], "sort_by": "relevance"}', '2023-10-24 09:50:42');


-- Подсказки поиска
INSERT INTO search_service_schema.search_suggestion (id, text, type, source_id, weight, usage_count, created_at, updated_at) VALUES
('c3d4e5f6-a7b8-c9d0-e1f2-a3b4c5d6e7f8', 'Python для начинающих', 'title', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 2.5, 48, '2023-01-20', '2023-10-25'),
('d4e5f6a7-b8c9-d0e1-f2a3-b4c5d6e7f8a9', 'машинное обучение', 'interest', NULL, 3.8, 132, '2023-03-10', '2023-10-25'),
('e5f6a7b8-c9d0-e1f2-a3b4-c5d6e7f8a9b0', 'javascript', 'tag', NULL, 3.2, 98, '2023-02-15', '2023-10-24'),
('f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 'SQL оптимизация', 'title', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 1.8, 74, '2023-05-10', '2023-10-22'),
('a7b8c9d0-e1f2-a3b4-c5d6-e7f8a9b0c1d2', 'react', 'tag', NULL, 3.5, 115, '2023-08-15', '2023-10-25'),
('b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 'микросервисы', 'tag', NULL, 2.0, 56, '2023-04-25', '2023-10-23'),
('c9d0e1f2-a3b4-c5d6-e7f8-a9b0c1d2e3f4', 'FastAPI', 'title', 'c4d5e6f7-a8b9-c0d1-e2f3-a4b5c6d7e8f9', 1.9, 42, '2023-09-05', '2023-10-23'),
('d0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 'Docker основы', 'title', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 2.3, 89, '2023-10-15', '2023-10-24');

-- ===============================================================
-- parser_service
-- ===============================================================

-- Добавление задач парсинга
INSERT INTO parser_service_schema.parser_tasks (task_id, title, description, url, task_type, status, params, created_by, created_at, updated_at, started_at, completed_at, error_message, sources_found, sources_created) VALUES
('f1e2d3c4-b5a6-47c8-9d0e-1f2a3b4c5d6e', 'Парсинг блога по Python', 'Сбор статей с популярного блога по Python', 'https://realpython.com', 'website', 'completed', '{"depth": 2, "article_selector": ".article-card", "max_articles": 20}', '123e4567-e89b-12d3-a456-426614174001', '2023-11-01 10:00:00', '2023-11-01 11:30:00', '2023-11-01 10:00:05', '2023-11-01 11:25:30', NULL, 18, 15),

('e2d3c4b5-a6f1-48c9-b0d1-e2f3a4b5c6d7', 'Парсинг RSS канала по JavaScript', 'Получение последних статей из RSS потока', 'https://javascript.info/feed', 'rss', 'completed', '{"max_items": 50, "categories": ["tutorial", "guide"]}', '123e4567-e89b-12d3-a456-426614174002', '2023-11-05 14:30:00', '2023-11-05 14:35:00', '2023-11-05 14:30:10', '2023-11-05 14:34:45', NULL, 12, 10),

('d3c4b5a6-f1e2-49d0-a1b2-c3d4e5f6a7b8', 'Парсинг статьи по микросервисам', 'Сбор данных с конкретной статьи о микросервисах', 'https://microservices.io/patterns/microservices.html', 'single_url', 'completed', '{"extract_images": true, "extract_code": true}', '123e4567-e89b-12d3-a456-426614174003', '2023-11-10 09:00:00', '2023-11-10 09:02:00', '2023-11-10 09:00:05', '2023-11-10 09:01:45', NULL, 1, 1),

('c4b5a6d3-e2f1-4a0b-9c8d-7e6f5a4b3c2d', 'Еженедельное обновление статей по ML', 'Периодический парсинг новых статей по машинному обучению', 'https://machinelearningmastery.com', 'scheduled', 'pending', '{"keywords": ["neural networks", "deep learning", "python", "tensorflow"], "max_articles": 10}', '123e4567-e89b-12d3-a456-426614174001', '2023-11-15 12:00:00', '2023-11-15 12:00:00', NULL, NULL, NULL, 0, 0),

('b5a6c4d3-f1e2-41d0-8c9e-7f6a5b4c3d2e', 'Парсинг форума по базам данных', 'Сбор обсуждений с форума по PostgreSQL и другим СУБД', 'https://postgresql.org/forum', 'website', 'failed', '{"depth": 3, "thread_selector": ".thread-item", "min_replies": 5}', '123e4567-e89b-12d3-a456-426614174002', '2023-11-20 15:45:00', '2023-11-20 16:00:00', '2023-11-20 15:45:10', '2023-11-20 15:55:30', 'Failed to authenticate with the forum website', 0, 0),

('a6b5c4d3-e2f1-42d0-9c8e-1f2a3b4c5d6e', 'Парсинг блога по Frontend', 'Сбор статей по фронтенд-разработке', 'https://css-tricks.com', 'website', 'processing', '{"categories": ["css", "javascript", "html"], "max_pages": 5}', '123e4567-e89b-12d3-a456-426614174004', '2023-11-25 10:30:00', '2023-11-25 10:35:00', '2023-11-25 10:30:15', NULL, NULL, 8, 3),

('9c8d7e6f-5a4b-43c2-b1a0-9d8e7f6a5b4c', 'Парсинг видеокурсов по DevOps', 'Сбор материалов с платформы обучения по DevOps', 'https://kodekloud.com/courses', 'single_url', 'pending', '{"course_type": "free", "extract_syllabus": true}', '123e4567-e89b-12d3-a456-426614174003', '2023-12-01 09:00:00', '2023-12-01 09:00:00', NULL, NULL, NULL, 0, 0),

('8d9c0e1f-2a3b-44c5-d6e7-f8a9b0c1d2e3', 'Парсинг документации Docker', 'Извлечение руководств по Docker', 'https://docs.docker.com/get-started/', 'website', 'completed', '{"depth": 1, "article_selector": ".topic", "exclude_paths": ["/reference", "/engine"]}', '123e4567-e89b-12d3-a456-426614174003', '2023-12-05 14:00:00', '2023-12-05 15:30:00', '2023-12-05 14:00:10', '2023-12-05 15:15:45', NULL, 7, 7),

('7e8f9d0c-1b2a-45c3-d4e5-f6a7b8c9d0e1', 'Парсинг новостей по языку Go', 'Сбор новостей и обновлений о языке Go', 'https://golang.org/blog', 'scheduled', 'pending', '{"posts_per_page": 10, "min_length": 500}', '123e4567-e89b-12d3-a456-426614174001', '2023-12-10 11:00:00', '2023-12-10 11:00:00', NULL, NULL, NULL, 0, 0),

('6f7e8d9c-0b1a-46c2-d3e4-f5a6b7c8d9e0', 'Парсинг учебников по React', 'Сбор учебных материалов по React', 'https://react.dev/learn', 'website', 'completed', '{"sections": ["main-concepts", "hooks", "advanced-guides"], "code_examples": true}', '123e4567-e89b-12d3-a456-426614174002', '2023-12-15 10:00:00', '2023-12-15 11:45:00', '2023-12-15 10:00:05', '2023-12-15 11:30:20', NULL, 15, 12);

-- Добавление запланированных задач парсинга
INSERT INTO parser_service_schema.scheduled_parser_tasks (scheduled_task_id, task_id, schedule_type, schedule_value, is_active, last_run, next_run) VALUES
('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'c4b5a6d3-e2f1-4a0b-9c8d-7e6f5a4b3c2d', 'cron', '0 9 * * 1', true, '2023-11-20 09:00:00', '2023-11-27 09:00:00'),
('b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', '7e8f9d0c-1b2a-45c3-d4e5-f6a7b8c9d0e1', 'interval', '86400', true, '2023-12-10 11:00:00', '2023-12-11 11:00:00'),
('c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', 'c4b5a6d3-e2f1-4a0b-9c8d-7e6f5a4b3c2d', 'cron', '0 12 1,15 * *', false, '2023-11-15 12:00:00', '2023-12-01 12:00:00'),
('d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', '9c8d7e6f-5a4b-43c2-b1a0-9d8e7f6a5b4c', 'cron', '0 0 * * 0', true, NULL, '2023-12-03 00:00:00'),
('e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b', '7e8f9d0c-1b2a-45c3-d4e5-f6a7b8c9d0e1', 'interval', '604800', true, NULL, '2023-12-17 11:00:00');

-- Добавление распарсенных источников
INSERT INTO parser_service_schema.parsed_sources (source_id, task_id, url, title, description, content, thumbnail_url, content_type, publication_date, author, source_site, language, keywords, is_processed, processed_at, created_source_id, created_at) VALUES
('f0e1d2c3-b4a5-46b7-8c9d-0e1f2a3b4c5d', 'f1e2d3c4-b5a6-47c8-9d0e-1f2a3b4c5d6e', 'https://realpython.com/python-async-features/', 'Асинхронное программирование в Python', 'Полное руководство по асинхронному программированию в Python с примерами', 'В этой статье рассматриваются основные концепции асинхронного программирования в Python, включая async/await, asyncio и другие библиотеки...', 'https://realpython.com/images/async-python.jpg', 'article', '2023-10-15', 'John Smith', 'Real Python', 'ru', '["python", "async", "asyncio", "concurrency"]', true, '2023-11-01 11:26:00', 'aaf4c61d-f067-4470-9a8d-baaf9a28f24a', '2023-11-01 10:15:20'),

('e1d2c3b4-a5f0-47b6-9c8d-1e2f3a4b5c6d', 'f1e2d3c4-b5a6-47c8-9d0e-1f2a3b4c5d6e', 'https://realpython.com/python-design-patterns/', 'Шаблоны проектирования в Python', 'Реализация основных шаблонов проектирования на языке Python', 'Шаблоны проектирования - это типовые решения часто встречающихся проблем при разработке ПО. В этой статье мы рассмотрим основные шаблоны и их реализацию на Python...', 'https://realpython.com/images/design-patterns.jpg', 'article', '2023-10-20', 'Mary Johnson', 'Real Python', 'ru', '["python", "design patterns", "oop", "programming"]', true, '2023-11-01 11:27:15', 'aaf4c61d-f067-4470-9a8d-baaf9a28f24b', '2023-11-01 10:18:45'),

('d2c3b4a5-f0e1-48b5-a6c7-2d3e4f5a6b7c', 'e2d3c4b5-a6f1-48c9-b0d1-e2f3a4b5c6d7', 'https://javascript.info/promise-basics', 'Основы работы с промисами в JavaScript', 'Руководство по использованию промисов в JavaScript', 'Промисы (promises) - это специальные объекты в JavaScript, которые представляют результат асинхронной операции. В этой статье мы разберем, как работать с промисами...', 'https://javascript.info/images/promise-basics.png', 'article', '2023-10-25', 'Alex Weber', 'JavaScript.info', 'ru', '["javascript", "promises", "async", "tutorial"]', true, '2023-11-05 14:35:30', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92402', '2023-11-05 14:31:10'),

('c3b4a5d2-e1f0-49b4-a5c6-3d4e5f6a7b8c', 'e2d3c4b5-a6f1-48c9-b0d1-e2f3a4b5c6d7', 'https://javascript.info/async-await', 'Async/Await в JavaScript', 'Глубокое погружение в работу с async/await', 'Async/await - это синтаксический сахар поверх промисов, делающий асинхронный код более читаемым и понятным. В этой статье разберем все нюансы этого механизма...', 'https://javascript.info/images/async-await.png', 'article', '2023-10-27', 'Sarah Brown', 'JavaScript.info', 'ru', '["javascript", "async", "await", "es6"]', true, '2023-11-05 14:36:15', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92403', '2023-11-05 14:32:05'),

('b4a5c3d2-f0e1-4a9b-3c4d-5e6f7a8b9c0d', 'd3c4b5a6-f1e2-49d0-a1b2-c3d4e5f6a7b8', 'https://microservices.io/patterns/microservices.html', 'Введение в шаблоны микросервисной архитектуры', 'Обзор ключевых шаблонов проектирования для микросервисной архитектуры', 'Микросервисная архитектура предлагает ряд шаблонов для решения типичных проблем масштабирования и развертывания. В статье рассматриваются шаблоны агрегации данных, обнаружения сервисов и т.д...', 'https://microservices.io/images/patterns-overview.png', 'article', '2023-10-10', 'Chris Richardson', 'microservices.io', 'ru', '["microservices", "architecture", "patterns", "distributed systems"]', true, '2023-11-10 09:02:10', 'd4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9b', '2023-11-10 09:01:00'),

('a5b4c3d2-e1f0-4b8a-2c3d-4e5f6a7b8c9d', '8d9c0e1f-2a3b-44c5-d6e7-f8a9b0c1d2e3', 'https://docs.docker.com/get-started/overview/', 'Обзор технологии Docker', 'Введение в архитектуру и основные понятия Docker', 'Docker - это платформа для разработки, доставки и запуска приложений в контейнерах. В этом руководстве рассматриваются основные компоненты Docker и их взаимодействие...', 'https://docs.docker.com/images/docker-overview.png', 'article', '2023-11-05', 'Docker Team', 'Docker Documentation', 'ru', '["docker", "containers", "devops", "virtualization"]', true, '2023-12-05 15:16:30', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a6', '2023-12-05 14:20:15'),

('9a8b7c6d-5e4f-4a3b-2c1d-0e9f8a7b6c5d', '8d9c0e1f-2a3b-44c5-d6e7-f8a9b0c1d2e3', 'https://docs.docker.com/get-started/docker-compose/', 'Начало работы с Docker Compose', 'Руководство по использованию Docker Compose для многоконтейнерных приложений', 'Docker Compose - это инструмент для определения и запуска многоконтейнерных приложений Docker. В этом руководстве вы научитесь создавать файл docker-compose.yml и управлять службами...', 'https://docs.docker.com/images/compose-overview.png', 'article', '2023-11-10', 'Docker Team', 'Docker Documentation', 'ru', '["docker", "docker-compose", "containers", "configuration"]', true, '2023-12-05 15:17:45', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a7', '2023-12-05 14:25:30'),

('8b7a6c5d-4e3f-4c2b-1a0d-9e8f7a6b5c4d', '6f7e8d9c-0b1a-46c2-d3e4-f5a6b7c8d9e0', 'https://react.dev/learn/thinking-in-react', 'Мышление в стиле React', 'Руководство по подходу к разработке интерфейсов с помощью React', 'React требует особого подхода к созданию пользовательских интерфейсов. В этом руководстве рассматривается процесс построения компонентной модели интерфейса на основе UI-макета...', 'https://react.dev/images/thinking-in-react.png', 'article', '2023-11-25', 'React Team', 'React Documentation', 'ru', '["react", "components", "frontend", "ui"]', true, '2023-12-15 11:31:10', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e4', '2023-12-15 10:15:40'),

('7c6b5a4d-3e2f-4d1c-0b9a-8d7e6f5c4b3a', '6f7e8d9c-0b1a-46c2-d3e4-f5a6b7c8d9e0', 'https://react.dev/learn/state-management', 'Управление состоянием в React', 'Подробное руководство по работе с состоянием в React-приложениях', 'Состояние - это одна из ключевых концепций в React. В этом руководстве рассматриваются различные подходы к управлению состоянием: от локального состояния компонентов до использования Redux и Context API...', 'https://react.dev/images/state-management.png', 'article', '2023-12-01', 'React Team', 'React Documentation', 'ru', '["react", "state", "hooks", "redux", "context"]', true, '2023-12-15 11:32:05', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e5', '2023-12-15 10:20:15'),

('6d5c4b3a-2e1f-4e0d-9c8b-7a6d5e4f3c2b', 'f1e2d3c4-b5a6-47c8-9d0e-1f2a3b4c5d6e', 'https://realpython.com/python-testing/', 'Тестирование в Python', 'Полное руководство по написанию тестов в Python', 'Тестирование - важнейшая часть разработки программного обеспечения. В этой статье рассматриваются различные фреймворки и подходы к тестированию в Python, включая unittest, pytest и другие инструменты...', 'https://realpython.com/images/testing.jpg', 'article', '2023-10-30', 'Peter Wilson', 'Real Python', 'ru', '["python", "testing", "pytest", "unittest"]', true, '2023-11-01 11:28:30', 'aaf4c61d-f067-4470-9a8d-baaf9a28f24c', '2023-11-01 10:25:10');