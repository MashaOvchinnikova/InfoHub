-- ===============================================================
-- content_service
-- ===============================================================

-- Добавление тегов
INSERT INTO tag (tag_id, name, description, usage_count) VALUES
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
INSERT INTO source (source_id, title, url, description, thumbnail_url, content_type, publication_date, added_date, added_by, is_verified, is_recommended, avg_rating) VALUES
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
INSERT INTO source_tag (source_tag_id, source_id, tag_id) VALUES
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
INSERT INTO rating (rating_id, user_id, source_id, value, created_date, updated_date) VALUES
('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6e', '123e4567-e89b-12d3-a456-426614174001', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 5, '2023-01-22', '2023-01-22'),
('b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', '123e4567-e89b-12d3-a456-426614174002', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 5, '2023-01-25', '2023-01-25'),
('c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', '123e4567-e89b-12d3-a456-426614174003', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 4, '2023-01-27', '2023-01-27'),
('d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9b', '123e4567-e89b-12d3-a456-426614174004', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 5, '2023-01-30', '2023-01-30'),
('e5f6a7b8-c9d0-e1f2-a3b4-c5d6e7f8a9b1', '123e4567-e89b-12d3-a456-426614174001', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 4, '2023-02-16', '2023-02-16'),
('f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c2', '123e4567-e89b-12d3-a456-426614174002', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 5, '2023-02-18', '2023-02-18'),
('a7b8c9d0-e1f2-a3b4-c5d6-e7f8a9b0c1d3', '123e4567-e89b-12d3-a456-426614174003', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 4, '2023-02-20', '2023-02-20'),
('b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e4', '123e4567-e89b-12d3-a456-426614174001', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 5, '2023-03-12', '2023-03-12'),
('c9d0e1f2-a3b4-c5d6-e7f8-a9b0c1d2e3f5', '123e4567-e89b-12d3-a456-426614174002', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 5, '2023-03-15', '2023-03-15');
