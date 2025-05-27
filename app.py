from flask import Flask, request, jsonify, send_file
from tweetcapture import TweetCapture
import asyncio
import os
import tempfile
import uuid
from datetime import datetime
import traceback
import base64

app = Flask(__name__)

# 配置
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'message': 'TweetCapture API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/screenshot', methods=['POST'])
def screenshot_tweet():
    """截图推文接口"""
    try:
        # 获取请求参数
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # 可选参数
        mode = data.get('mode', 3)
        night_mode = data.get('night_mode', 0)
        wait_time = data.get('wait_time', 5.0)
        show_parent_tweets = data.get('show_parent_tweets', False)
        show_parent_limit = data.get('show_parent_limit', -1)
        show_mentions = data.get('show_mentions', 0)
        radius = data.get('radius', 15)
        scale = data.get('scale', 1.0)
        lang = data.get('lang', '')
        
        # 隐藏媒体选项
        hide_photos = data.get('hide_photos', False)
        hide_videos = data.get('hide_videos', False)
        hide_gifs = data.get('hide_gifs', False)
        hide_quotes = data.get('hide_quotes', False)
        hide_link_previews = data.get('hide_link_previews', False)
        hide_all = data.get('hide_all', False)
        
        # 返回格式
        return_format = data.get('format', 'file')  # 'file' or 'base64'
        
        # 创建临时文件
        temp_dir = tempfile.gettempdir()
        filename = f"tweet_{uuid.uuid4().hex}.png"
        filepath = os.path.join(temp_dir, filename)
        
        # 创建TweetCapture实例
        tweet = TweetCapture(
            mode=mode,
            night_mode=night_mode,
            show_parent_tweets=show_parent_tweets,
            parent_tweets_limit=show_parent_limit,
            show_mentions_count=show_mentions,
            overwrite=True,
            radius=radius,
            scale=scale
        )
        
        # 设置配置
        if lang:
            tweet.set_lang(lang)
        tweet.set_wait_time(wait_time)
        
        # 设置Chrome驱动路径（Docker环境）
        tweet.set_chromedriver_path('/usr/bin/chromedriver')
        
        # 隐藏媒体设置
        if hide_all:
            tweet.hide_all_media()
        else:
            tweet.hide_media(hide_link_previews, hide_photos, hide_videos, hide_gifs, hide_quotes)
        
        # 添加Chrome选项（无头模式）
        tweet.add_chrome_argument('--headless')
        tweet.add_chrome_argument('--no-sandbox')
        tweet.add_chrome_argument('--disable-dev-shm-usage')
        tweet.add_chrome_argument('--disable-gpu')
        tweet.add_chrome_argument('--window-size=1920,1080')
        
        # 执行截图
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result_path = loop.run_until_complete(tweet.screenshot(url, filepath))
            
            if return_format == 'base64':
                # 返回base64编码的图片
                with open(result_path, 'rb') as f:
                    image_data = f.read()
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
                
                # 清理临时文件
                if os.path.exists(result_path):
                    os.remove(result_path)
                
                return jsonify({
                    'success': True,
                    'image': image_base64,
                    'format': 'png'
                })
            else:
                # 返回文件
                return send_file(
                    result_path,
                    mimetype='image/png',
                    as_attachment=True,
                    download_name=f'tweet_screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                )
        finally:
            loop.close()
            
    except Exception as e:
        # 清理临时文件
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

@app.route('/screenshot', methods=['GET'])
def screenshot_tweet_get():
    """GET方式截图推文接口（简化版）"""
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'URL parameter is required'}), 400
        
        mode = int(request.args.get('mode', 3))
        night_mode = int(request.args.get('night_mode', 0))
        
        # 添加调试日志
        print(f"DEBUG: Received parameters - URL: {url}, mode: {mode}, night_mode: {night_mode}")
        
        # 创建临时文件
        temp_dir = tempfile.gettempdir()
        filename = f"tweet_{uuid.uuid4().hex}.png"
        filepath = os.path.join(temp_dir, filename)
        
        # 创建TweetCapture实例
        tweet = TweetCapture(mode=mode, night_mode=night_mode, overwrite=True)
        tweet.set_chromedriver_path('/usr/bin/chromedriver')
        
        print(f"DEBUG: TweetCapture created with mode={tweet.mode}, night_mode={tweet.night_mode}")
        
        # 添加Chrome选项
        tweet.add_chrome_argument('--headless')
        tweet.add_chrome_argument('--no-sandbox')
        tweet.add_chrome_argument('--disable-dev-shm-usage')
        tweet.add_chrome_argument('--disable-gpu')
        tweet.add_chrome_argument('--window-size=1920,1080')
        
        # 执行截图
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result_path = loop.run_until_complete(tweet.screenshot(url, filepath))
            return send_file(
                result_path,
                mimetype='image/png',
                as_attachment=True,
                download_name=f'tweet_screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            )
        finally:
            loop.close()
            
    except Exception as e:
        # 清理临时文件
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 