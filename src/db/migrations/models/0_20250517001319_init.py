from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "auth_user" (
    "userid" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(128) NOT NULL,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_superuser" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "auth_user"."userid" IS '用户ID';
COMMENT ON COLUMN "auth_user"."username" IS '用户名';
COMMENT ON COLUMN "auth_user"."hashed_password" IS '密码';
COMMENT ON COLUMN "auth_user"."email" IS '邮箱';
COMMENT ON COLUMN "auth_user"."is_active" IS '是否激活';
COMMENT ON COLUMN "auth_user"."is_superuser" IS '是否超级用户';
COMMENT ON COLUMN "auth_user"."created_at" IS '创建时间';
COMMENT ON COLUMN "auth_user"."updated_at" IS '更新时间';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
