#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube视频下载和字幕提取脚本
需要安装: pip install yt-dlp
"""

import os
import sys
import yt_dlp

def download_youtube_video(url, output_dir="./downloads"):
    """
    下载YouTube视频和字幕
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 配置选项
    ydl_opts = {
        # 视频格式选择
        'format': 'best[height<=1080]',  # 最高1080p
        
        # 字幕设置
        'writeautomaticsub': True,  # 下载自动生成的字幕
        'subtitleslangs': ['zh-Hans', 'zh-Hant', 'en'],  # 优先中文简体、繁体、英文
        'subtitlesformat': 'srt',  # 字幕格式
        
        # 输出设置
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        
        # 其他选项
        'noplaylist': True,  # 不下载播放列表
        'quiet': False,  # 显示进度
        'no_warnings': False,
    }
    
    try:
        print(f"开始下载: {url}")
        print("-" * 50)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown')
            
            print(f"视频标题: {title}")
            print(f"上传者: {uploader}")
            print(f"时长: {duration//60}分{duration%60}秒")
            print("-" * 50)
            
            # 下载视频和字幕
            ydl.download([url])
            
        print("\n✅ 下载完成!")
        print(f"文件保存在: {os.path.abspath(output_dir)}")
        
        # 列出下载的文件
        files = os.listdir(output_dir)
        if files:
            print("\n下载的文件:")
            for f in files:
                print(f"  - {f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        return False

def download_subtitle_only(url, output_dir="./downloads"):
    """
    只下载字幕，不下载视频
    """
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'writeautomaticsub': True,
        'subtitleslangs': ['zh-Hans', 'zh-Hant', 'en'],
        'subtitlesformat': 'srt',
        'skip_download': True,  # 跳过视频下载
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
    }
    
    try:
        print(f"开始下载字幕: {url}")
        print("-" * 50)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            print(f"视频标题: {title}")
            print("-" * 50)
            
            ydl.download([url])
            
        print("\n✅ 字幕下载完成!")
        
        # 列出字幕文件
        files = [f for f in os.listdir(output_dir) if f.endswith(('.srt', '.vtt'))]
        if files:
            print("\n字幕文件:")
            for f in files:
                print(f"  - {f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        return False

if __name__ == "__main__":
    # YouTube视频URL
    VIDEO_URL = "https://www.youtube.com/watch?v=rWUWfj_PqmM"
    
    print("=" * 60)
    print("YouTube视频下载工具")
    print("=" * 60)
    print()
    print("选择下载模式:")
    print("1. 下载视频 + 字幕")
    print("2. 只下载字幕")
    print()
    
    choice = input("请输入选项 (1/2): ").strip()
    
    if choice == "1":
        download_youtube_video(VIDEO_URL)
    elif choice == "2":
        download_subtitle_only(VIDEO_URL)
    else:
        print("无效选项，默认只下载字幕...")
        download_subtitle_only(VIDEO_URL)
    
    print()
    input("按回车键退出...")
