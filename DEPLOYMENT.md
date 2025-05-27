# TweetCapture Web API 部署指南

本指南将帮助你将TweetCapture部署为Web API服务，支持Railway平台部署。

## 🚀 快速开始

### 1. Railway部署（推荐）

Railway是一个现代化的部署平台，支持Docker和自动部署。

#### 步骤：

1. **准备代码**
   ```bash
   git clone <your-repo>
   cd tweetcapture
   ```

2. **安装Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

3. **登录Railway**
   ```bash
   railway login
   ```

4. **创建新项目**
   ```bash
   railway new
   ```

5. **部署**
   ```bash
   railway up
   ```

Railway会自动检测`railway.toml`配置文件并使用`Dockerfile.web`构建镜像。

#### 环境变量设置：

在Railway控制台中设置以下环境变量（可选）：

- `PORT`: 端口号（默认8080）
- `AUTH_TOKEN`: Twitter认证令牌（如果需要）

### 2. 本地Docker部署

#### 构建镜像：
```bash
docker build -f Dockerfile.web -t tweetcapture-web .
```

#### 运行容器：
```bash
docker run -p 8080:8080 tweetcapture-web
```

#### 使用docker-compose：
创建`docker-compose.yml`文件：

```yaml
version: '3.8'
services:
  tweetcapture:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    restart: unless-stopped
```

运行：
```bash
docker-compose up -d
```

### 3. 本地开发运行

#### 安装依赖：
```bash
pip install -r requirements.txt
pip install .
```

#### 运行开发服务器：
```bash
python app.py
```

或使用gunicorn：
```bash
gunicorn --bind 0.0.0.0:8080 --workers 1 --timeout 120 app:app
```

## 🔧 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `PORT` | 服务端口 | 8080 | 否 |
| `AUTH_TOKEN` | Twitter认证令牌 | - | 否 |
| `PYTHONUNBUFFERED` | Python输出缓冲 | 1 | 否 |

### Chrome配置

服务会自动配置Chrome浏览器为无头模式，包含以下选项：
- `--headless`: 无头模式
- `--no-sandbox`: 禁用沙箱（Docker环境需要）
- `--disable-dev-shm-usage`: 禁用/dev/shm使用
- `--disable-gpu`: 禁用GPU
- `--window-size=1920,1080`: 设置窗口大小

## 📊 性能优化

### 1. 内存优化
- 使用单个worker进程（`--workers 1`）
- 设置合理的超时时间（`--timeout 120`）
- 及时清理临时文件

### 2. 响应时间优化
- 调整`wait_time`参数（默认5秒）
- 使用适当的截图模式
- 考虑缓存机制

### 3. 并发处理
由于Chrome浏览器的资源消耗，建议：
- 单worker模式运行
- 实现请求队列
- 设置合理的超时时间

## 🔍 监控和日志

### 健康检查
服务提供健康检查端点：
```
GET /
```

### 日志配置
使用gunicorn的日志配置：
```bash
gunicorn --bind 0.0.0.0:8080 \
         --workers 1 \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         app:app
```

### 监控指标
建议监控以下指标：
- 响应时间
- 错误率
- 内存使用
- CPU使用率

## 🛠️ 故障排除

### 常见问题

1. **Chrome启动失败**
   - 确保安装了chromium和chromedriver
   - 检查权限设置
   - 验证Docker环境配置

2. **内存不足**
   - 增加容器内存限制
   - 优化Chrome选项
   - 减少并发请求

3. **截图失败**
   - 检查推文URL有效性
   - 验证网络连接
   - 查看详细错误日志

4. **超时问题**
   - 增加超时时间
   - 优化wait_time参数
   - 检查网络延迟

### 调试模式

在开发环境中启用调试模式：
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

### 日志级别
设置环境变量启用详细日志：
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

## 🔒 安全考虑

### 1. 输入验证
- URL格式验证
- 参数范围检查
- 防止路径遍历

### 2. 资源限制
- 请求大小限制
- 超时设置
- 内存使用限制

### 3. 访问控制
考虑添加：
- API密钥认证
- 速率限制
- IP白名单

## 📈 扩展部署

### 负载均衡
使用nginx进行负载均衡：

```nginx
upstream tweetcapture {
    server app1:8080;
    server app2:8080;
}

server {
    listen 80;
    location / {
        proxy_pass http://tweetcapture;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 容器编排
使用Kubernetes部署：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tweetcapture
spec:
  replicas: 2
  selector:
    matchLabels:
      app: tweetcapture
  template:
    metadata:
      labels:
        app: tweetcapture
    spec:
      containers:
      - name: tweetcapture
        image: tweetcapture-web:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "1Gi"
            cpu: "500m"
```

## 🧪 测试

运行API测试：
```bash
python test_api.py
```

测试特定功能：
```bash
# 测试健康检查
curl http://localhost:8080/

# 测试截图功能
curl -X POST http://localhost:8080/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://twitter.com/jack/status/20"}' \
  --output test.png
```

## 📞 支持

如果遇到问题：
1. 查看日志输出
2. 检查配置文件
3. 验证依赖版本
4. 参考API文档

---

**注意**: 确保遵守Twitter的使用条款和API政策。 