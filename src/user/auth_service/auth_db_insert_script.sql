-- ===============================================================
-- auth_service
-- ===============================================================
-- Добавление пользователей для аутентификации
INSERT INTO user_auth (user_id, email, username, password_hash, is_active, is_admin, is_blocked, created_at, updated_at, last_login_date) VALUES
('123e4567-e89b-12d3-a456-426614174001', 'ivan@example.com','ivan_dev','$2b$12$KhESzFgw.Mf7Ts.YBVm9gu5HZLKkbT4WyXJePVR9M.bzWnbnju33m',true, false, false, '2025-03-03 12:00:00', '2025-03-03 12:00:00', '2025-04-15 15:30:00'),
('123e4567-e89b-12d3-a456-426614174002', 'maria@example.com','maria_designer','$2b$12$P9XgHtS.8xhMt3jYkKKfZeqECQgMGz0wI2.KU7GyWBt.v1JfZuj2.',true, false, false, '2025-03-02 14:30:00', '2025-03-02 14:30:00','2025-04-16 17:45:00'),
('123e4567-e89b-12d3-a456-426614174003', 'alex@example.com','alex_devops','$2b$12$3dCLuKZ.qCdDZ3xz9iAo9eRgFOXHnS4joYWaUHCSt.RKV4aQlQx9S', true, false, false, '2025-01-03 09:15:00', '2025-01-03 09:15:00','2025-04-14 12:20:00'),
('123e4567-e89b-12d3-a456-426614174004', 'olga@example.com','olga_ui','$2b$12$aT5.x8jYUQ5r7U3jh7ZT.G0Lqpw1KjXsHK9QU7wDgc3rnD36gCW',true, false, false, '2025-01-04 11:45:00', '2025-01-04 11:45:00','2025-04-13 14:10:00'),
('123e4567-e89b-12d3-a456-426614174005', 'admin@infohub.com','admin','$2b$12$r7Z5J2SX3LMrV9JD.3wm8usX3fT.wgTJ3appX4vyWjnO4TnzCKpHC', true, true, false, '2025-01-01 00:00:00', '2025-01-01 00:00:00','2025-04-17 09:00:00');