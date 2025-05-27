#!/usr/bin/env python3
"""
TweetCapture Web API 测试脚本
"""

import requests
import json
import base64
import os
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8080"  # 本地测试
# BASE_URL = "https://your-app.railway.app"  # Railway部署后的URL

def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_screenshot_post():
    """测试POST截图接口"""
    print("\n📸 测试POST截图接口...")
    
    # 测试数据
    test_data = {
        "url": "https://twitter.com/jack/status/20",
        "mode": 1,
        "night_mode": 0,
        "format": "file"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/screenshot",
            json=test_data,
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 保存图片
            filename = f"test_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ 截图保存为: {filename}")
            return True
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ POST截图测试失败: {e}")
        return False

def test_screenshot_base64():
    """测试base64格式返回"""
    print("\n🔢 测试base64格式返回...")
    
    test_data = {
        "url": "https://twitter.com/jack/status/20",
        "mode": 0,
        "format": "base64"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/screenshot",
            json=test_data,
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'image' in data:
                # 解码并保存base64图片
                image_data = base64.b64decode(data['image'])
                filename = f"test_base64_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                with open(filename, 'wb') as f:
                    f.write(image_data)
                print(f"✅ base64图片保存为: {filename}")
                return True
            else:
                print(f"❌ 响应中没有图片数据: {data}")
                return False
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ base64测试失败: {e}")
        return False

def test_screenshot_get():
    """测试GET截图接口"""
    print("\n🌐 测试GET截图接口...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/screenshot",
            params={
                "url": "https://twitter.com/jack/status/20",
                "mode": 2,
                "night_mode": 1
            },
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            filename = f"test_get_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ GET截图保存为: {filename}")
            return True
        else:
            print(f"❌ GET请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ GET截图测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n⚠️ 测试错误处理...")
    
    # 测试缺少URL参数
    try:
        response = requests.post(f"{BASE_URL}/screenshot", json={})
        print(f"缺少URL - 状态码: {response.status_code}")
        if response.status_code == 400:
            print("✅ 正确返回400错误")
        else:
            print("❌ 错误处理不正确")
            
        # 测试无效URL
        response = requests.post(f"{BASE_URL}/screenshot", json={"url": "invalid-url"})
        print(f"无效URL - 状态码: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("🚀 开始测试TweetCapture Web API")
    print(f"测试目标: {BASE_URL}")
    print("=" * 50)
    
    tests = [
        ("健康检查", test_health_check),
        ("POST截图", test_screenshot_post),
        ("base64格式", test_screenshot_base64),
        ("GET截图", test_screenshot_get),
        ("错误处理", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！API工作正常。")
    else:
        print("⚠️ 部分测试失败，请检查服务状态。")

if __name__ == "__main__":
    main() 