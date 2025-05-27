# TweetCapture

Easily take screenshots of tweets/mentions and save them as image.

## Command-Line Usage

```
> pip install tweet-capture
> tweetcapture https://twitter.com/jack/status/20
> tweetcapture -h
```

## Web API Usage

TweetCapture now provides a Web API for HTTP-based screenshot generation.

### Quick Start with Railway

1. Deploy to Railway:
   ```bash
   railway login
   railway new
   railway up
   ```

2. Use the API:
   ```bash
   curl -X POST "https://your-app.railway.app/screenshot" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://twitter.com/jack/status/20"}' \
     --output screenshot.png
   ```

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install .
   ```

2. Run the web server:
   ```bash
   python app.py
   ```

3. Test the API:
   ```bash
   curl -X POST "http://localhost:8080/screenshot" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://twitter.com/jack/status/20"}' \
     --output screenshot.png
   ```

### Docker Usage

```bash
# Build and run web service
docker build -f Dockerfile.web -t tweetcapture-web .
docker run -p 8080:8080 tweetcapture-web

# Or use docker-compose
docker-compose up -d
```

### API Endpoints

- `GET /` - Health check
- `POST /screenshot` - Generate screenshot (full options)
- `GET /screenshot?url=<tweet_url>` - Generate screenshot (simple)

See [API.md](API.md) for detailed API documentation.

## Code Usage Examples

- [Cli](tweetcapture/cli.py)
- [Code Examples](tweetcapture/examples/)
- [Web API](app.py)

## Testing
```
> pip3 install opencv-python numpy
> cd tweetcapture/tests/
> python -m unittest

# Test Web API
> python test_api.py
```

## Original Docker Usage
```
docker run --rm -v $(pwd):/app xacnio/tweetcapture -h
docker run --rm -v $(pwd):/app xacnio/tweetcapture https://twitter.com/jack/status/20
```
- *<font size="1">On Windows: Replace `$(pwd)` with `${PWD}`* (**Powershell**)
- *On Windows: Replace `$(pwd)` with `%cd%`* (**Command Line**)</font>

## Modes

| #   |                                                   |                                                      |
| --- | ------------------------------------------------- | ---------------------------------------------------- |
| 0   | Hide everything outside tweet content and author. | <img src="tweetcapture/assets/mode0.png" width="300"> |
| 1   | Show retweet/like counts.                         | <img src="tweetcapture/assets/mode1.png" width="300"> |
| 2   | Show retweet/like counts and timestamp.           | <img src="tweetcapture/assets/mode2.png" width="300"> |
| 3   | Show everything.                                  | <img src="tweetcapture/assets/mode3.png" width="300"> |
| 4   | Show timestamp.                                   | <img src="tweetcapture/assets/mode4.png" width="300"> |

## Night Modes

| #   |            |                                                      |
| --- | ---------- | ---------------------------------------------------- |
| 0   | Light mode | <img src="tweetcapture/assets/mode4.png" width="300"> |
| 1   | Dark mode  | <img src="tweetcapture/assets/mode1.png" width="300"> |
| 2   | Black mode | <img src="tweetcapture/assets/mode3.png" width="300"> |

## Show Mentions Example
_If the tweet have a very many mentions, there may be problems because "show more" option not supported. The tool can show only first loaded mentions. You can limit mention count on screenshot by using -sc <count> argument_
```
tweetcapture -sm 3 https://twitter.com/Twitter/status/1445078208190291973
```
<details>
    <summary>Image</summary>
    <img src="https://i.imgur.com/IZ0GHl8.png" />
</details>

## Show Parent Tweets Example
```
tweetcapture -sp https://twitter.com/elonmusk/status/1587911540770222081
```
<details>
    <summary>Image</summary>
    <img src="https://i.imgur.com/KrK9N8Y.png" />
</details>
