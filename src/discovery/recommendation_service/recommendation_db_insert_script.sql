-- ===============================================================
-- recommendation_service
-- ===============================================================

-- Персональные рекомендации для пользователей
INSERT INTO user_recommendations (recommendation_id, user_id, source_id, recommendation_type, relevance_score, explanation, interests, created_at, updated_at, is_shown, is_clicked) VALUES
('ae5e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 'personalized', 0.85, 'На основе вашего интереса к программированию', ARRAY['3c5e8c5a-9231-4934-9178-953249f78c2e'::uuid, 'fa1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d'::uuid], '2023-03-01', '2023-03-01', 3, 1),
('be6e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174001', 'd0e1f2a3-b4c5-d6e7-f8a9-b0c1d2e3f4a5', 'trending', 0.75, 'Популярно среди пользователей с похожими интересами', ARRAY['3c5e8c5a-9231-4934-9178-953249f78c2e'::uuid, '1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b'::uuid], '2023-03-01', '2023-03-01', 2, 0),
('ce7e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174002', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 'interest_based', 0.92, 'Соответствует вашему интересу к машинному обучению', ARRAY['7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f'::uuid], '2023-03-05', '2023-03-05', 1, 1),
('de8e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174003', 'f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1', 'personalized', 0.68, 'На основе вашего интереса к фронтенду и дизайну', ARRAY['4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a'::uuid, '9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'::uuid], '2023-03-10', '2023-03-10', 2, 0),
('ee9e8c5a-9231-4934-9178-953249f78c2e', '123e4567-e89b-12d3-a456-426614174004', 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', 'similar', 0.79, 'Похоже на источники, которые вы просматривали ранее', NULL, '2023-03-15', '2023-03-15', 4, 2);

-- Похожие источники
INSERT INTO similar_sources (similar_id, source_id, similar_source_id, similarity_score, similarity_reasons, created_at, updated_at) VALUES
('af5e8c5a-9231-4934-9178-953249f78c2e', 'aaf4c61d-f067-4470-9a8d-baaf9a28f23f', 'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 0.75, '{"common_tags": ["python", "программирование"], "common_users": 5}', '2023-03-01', '2023-03-01'),
('bf6e8c5a-9231-4934-9178-953249f78c2e', 'b90c0d12-7c1e-4588-9fb0-3a4a30e92401', 'b8c9d0e1-f2a3-b4c5-d6e7-f8a9b0c1d2e3', 0.85, '{"common_tags": ["javascript", "фронтенд"], "common_users": 7}', '2023-03-05', '2023-03-05'),
('cf7e8c5a-9231-4934-9178-953249f78c2e', 'd4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'a2b3c4d5-e6f7-a8b9-c0d1-e2f3a4b5c6d7', 0.65, '{"common_tags": ["микросервисы", "DevOps"], "common_users": 3}', '2023-03-10', '2023-03-10'),
('df8e8c5a-9231-4934-9178-953249f78c2e', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 'e0f1a2b3-c4d5-e6f7-a8b9-c0d1e2f3a4b5', 0.70, '{"common_tags": ["базы данных"], "common_users": 4}', '2023-03-15', '2023-03-15');

-- Популярные источники
INSERT INTO popular_sources (popular_id, source_id, view_count, save_count, share_count, rating_avg, rating_count, popularity_score, time_period, category, created_at, updated_at) VALUES
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
INSERT INTO interest_recommendations (recommendation_id, interest_id, source_id, relevance_score, created_at, updated_at) VALUES
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
INSERT INTO user_preferences (preference_id, user_id, liked_sources, disliked_sources, viewed_sources, interest_weights, content_type_preferences, created_at, updated_at) VALUES
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
