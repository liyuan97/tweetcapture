#!/bin/sh

# 设置默认端口
PORT=${PORT:-8080}

echo "Starting TweetCapture API on port $PORT"

# 启动gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --access-logfile - --error-logfile - app:app 