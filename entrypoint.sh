#!/bin/sh
set -e # 如果任何命令失败，则立即退出

# 脚本接收的第一个参数决定启动哪个服务
COMMAND=$1
shift # 移除第一个参数，其余参数传递给 execaq

echo "Selected command: ${COMMAND}"

# 等待数据库就绪 (可选，但推荐)
# 这里需要根据实际数据库类型调整等待逻辑
# 例如 PostgreSQL:
# until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-user}"; do
#   echo "Waiting for database connection..."
#   sleep 2
# done
# echo "Database is ready."

echo "Running database migrations (Aerich)..."
# 确保 Aerich 和 TortoiseORM 配置能从环境变量或配置文件中正确加载
# Aerich 命令需要能访问到 pyproject.toml 或指定的配置文件
# 如果 pyproject.toml 在 APP_DIR，并且 TORTOISE_ORM 配置路径正确，则可以直接运行
# 注意：aerich 命令可能需要访问源码来发现模型，确保 PYTHONPATH 设置正确
aerich upgrade

echo "Starting service: ${COMMAND}"

if [ "$COMMAND" = "fastapi" ]; then
  # 启动 FastAPI Web 服务
  echo "Starting FastAPI server..."
  # 使用 uvicorn，通过 uv run 启动以利用 uv 的环境管理
  # exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 "$@"
  # 或者直接调用 venv 中的 uvicorn
  exec uvicorn src.main:app --host 0.0.0.0 --port 8000 "$@"
elif [ "$COMMAND" = "worker" ]; then
  # 启动 Celery Worker
  echo "Starting Celery worker..."
  # exec uv run celery -A app.worker_setup.celery_app worker -l INFO -P eventlet -c "${CELERY_WORKER_CONCURRENCY:-4}" "$@"
  exec celery -A app.worker_setup.celery_app worker -l INFO -P eventlet -c "${CELERY_WORKER_CONCURRENCY:-4}" "$@"
elif [ "$COMMAND" = "beat" ]; then
  # 启动 Celery Beat
  echo "Starting Celery beat..."
  # exec uv run celery -A app.worker_setup.celery_app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler "$@"
  exec celery -A app.worker_setup.celery_app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler "$@"
elif [ "$COMMAND" = "flower" ]; then
  # 启动 Celery Flower 监控面板
  echo "Starting Celery Flower..."
  # exec uv run celery -A app.worker_setup.celery_app flower --port=5555 --broker="${CELERY_BROKER_URL}" "$@"
  exec celery -A app.worker_setup.celery_app flower --port=5555 --broker="${CELERY_BROKER_URL}" "$@"
elif [ -z "$COMMAND" ]; then
  # 如果没有提供 COMMAND，可以打印帮助信息或启动默认服务
  echo "No command provided. Exiting or starting default service (not configured)."
  # 例如，可以启动 fastapi 作为默认服务:
  # echo "Starting FastAPI server by default..."
  # exec uvicorn app.main:app --host 0.0.0.0 --port 8000 "$@"
  exit 1 # 或者执行其他逻辑
else
  # 执行作为参数传递的任何其他命令
  echo "Attempting to execute command: $COMMAND with arguments: $@"
  exec "$COMMAND" "$@"
fi
