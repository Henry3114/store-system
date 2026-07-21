-- 小卖部销售管理系统 - 数据库初始化脚本（参考用）
-- 实际表结构由 SQLAlchemy + Alembic 管理，此文件仅作备用

-- 创建数据库（需要超级用户权限执行）
-- CREATE DATABASE store_system;

-- 表结构将在 Phase 1-3 中通过 Alembic 迁移逐步创建：
--   users         - Phase 1
--   products      - Phase 2
--   inventory_logs- Phase 3
--   orders        - Phase 3
--   order_items   - Phase 3
