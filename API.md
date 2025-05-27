# TweetCapture Web API

这是TweetCapture的Web API版本，提供HTTP接口来截取推文截图。

## 基础信息

- **基础URL**: `https://your-railway-app.railway.app`
- **内容类型**: `application/json`
- **响应格式**: JSON 或 图片文件

## 接口列表

### 1. 健康检查

**GET** `/`

检查服务是否正常运行。

**响应示例**:
```json
{
  "status": "ok",
  "message": "TweetCapture API is running",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### 2. 截图推文 (POST)

**POST** `/screenshot`

**请求体**:
```json
{
  "url": "https://twitter.com/jack/status/20",
  "mode": 3,
  "night_mode": 0,
  "wait_time": 5.0,
  "show_parent_tweets": false,
  "show_parent_limit": -1,
  "show_mentions": 0,
  "radius": 15,
  "scale": 1.0,
  "lang": "",
  "hide_photos": false,
  "hide_videos": false,
  "hide_gifs": false,
  "hide_quotes": false,
  "hide_link_previews": false,
  "hide_all": false,
  "format": "file"
}
```

**参数说明**:
- `url` (必需): 推文URL
- `mode` (可选): 显示模式 (0-4)，默认3
  - 0: 只显示推文内容和作者
  - 1: 显示转发/点赞数
  - 2: 显示转发/点赞数和时间戳
  - 3: 显示所有内容
  - 4: 只显示时间戳
- `night_mode` (可选): 夜间模式 (0-2)，默认0
  - 0: 浅色模式
  - 1: 深色模式
  - 2: 黑色模式
- `wait_time` (可选): 页面加载等待时间 (1.0-10.0)，默认5.0
- `show_parent_tweets` (可选): 是否显示父推文，默认false
- `show_parent_limit` (可选): 父推文显示限制，默认-1（无限制）
- `show_mentions` (可选): 显示提及数量，默认0
- `radius` (可选): 图片圆角，默认15
- `scale` (可选): 截图缩放 (0.0-14.0)，默认1.0
- `lang` (可选): 浏览器语言代码
- `hide_photos` (可选): 隐藏照片，默认false
- `hide_videos` (可选): 隐藏视频，默认false
- `hide_gifs` (可选): 隐藏GIF，默认false
- `hide_quotes` (可选): 隐藏引用推文，默认false
- `hide_link_previews` (可选): 隐藏链接预览，默认false
- `hide_all` (可选): 隐藏所有媒体，默认false
- `format` (可选): 返回格式 ("file" 或 "base64")，默认"file"

**响应**:
- 当 `format` 为 "file" 时：返回PNG图片文件
- 当 `format` 为 "base64" 时：返回JSON格式的base64编码图片

**base64响应示例**:
```json
{
  "success": true,
  "image": "iVBORw0KGgoAAAANSUhEUgAA...",
  "format": "png"
}
```

### 3. 截图推文 (GET)

**GET** `/screenshot?url=<tweet_url>&mode=<mode>&night_mode=<night_mode>`

简化版的GET接口，只支持基本参数。

**参数**:
- `url` (必需): 推文URL
- `mode` (可选): 显示模式，默认3
- `night_mode` (可选): 夜间模式，默认0

**响应**: PNG图片文件

## 使用示例

### cURL示例

```bash
# 基本截图
curl -X POST "https://your-app.railway.app/screenshot" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://twitter.com/jack/status/20"}' \
  --output screenshot.png

# 获取base64格式
curl -X POST "https://your-app.railway.app/screenshot" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://twitter.com/jack/status/20", "format": "base64"}'

# GET方式
curl "https://your-app.railway.app/screenshot?url=https://twitter.com/jack/status/20&mode=1" \
  --output screenshot.png
```

### Python示例

```python
import requests

# POST请求
response = requests.post('https://your-app.railway.app/screenshot', json={
    'url': 'https://twitter.com/jack/status/20',
    'mode': 1,
    'night_mode': 1
})

if response.status_code == 200:
    with open('screenshot.png', 'wb') as f:
        f.write(response.content)

# 获取base64
response = requests.post('https://your-app.railway.app/screenshot', json={
    'url': 'https://twitter.com/jack/status/20',
    'format': 'base64'
})

if response.status_code == 200:
    data = response.json()
    image_base64 = data['image']
```

### JavaScript示例

```javascript
// 使用fetch API
const response = await fetch('https://your-app.railway.app/screenshot', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://twitter.com/jack/status/20',
    mode: 2,
    night_mode: 0
  })
});

if (response.ok) {
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  // 使用图片URL
}
```

## 错误处理

API会返回适当的HTTP状态码和错误信息：

- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 接口不存在
- `500 Internal Server Error`: 服务器内部错误

**错误响应示例**:
```json
{
  "error": "URL is required"
}
```

## 部署说明

1. 确保Docker环境可用
2. 构建镜像：`docker build -f Dockerfile.web -t tweetcapture-web .`
3. 运行容器：`docker run -p 8080:8080 tweetcapture-web`
4. 或直接部署到Railway平台 