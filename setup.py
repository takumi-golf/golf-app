import os
from pathlib import Path
from config import LOG_DIR, OUTPUT_DIR

def create_directories():
    """必要なディレクトリを作成"""
    directories = [LOG_DIR, OUTPUT_DIR]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"ディレクトリを作成しました: {directory}")
        except Exception as e:
            print(f"ディレクトリの作成に失敗しました: {directory}")
            print(f"エラー: {str(e)}")

if __name__ == "__main__":
    create_directories() 