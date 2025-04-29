import os
from pathlib import Path
from config import ENV_FILE

def read_env():
    """現在の.envファイルの内容を表示"""
    try:
        # 複数のエンコーディングを試す
        encodings = ['utf-8', 'cp932', 'shift_jis', 'utf-16']
        content = None
        
        for encoding in encodings:
            try:
                with open(ENV_FILE, "r", encoding=encoding) as f:
                    content = f.read()
                print(f"エンコーディング {encoding} で読み込み成功")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            raise Exception("適切なエンコーディングが見つかりませんでした")
            
        print("現在の.envファイルの内容:")
        print(content)
    except Exception as e:
        print(f".envファイルの読み込みに失敗しました: {str(e)}")

def update_env(key: str, value: str):
    """指定されたキーの値を更新"""
    try:
        # 現在の内容を読み込む
        encodings = ['utf-8', 'cp932', 'shift_jis', 'utf-16']
        lines = None
        
        for encoding in encodings:
            try:
                with open(ENV_FILE, "r", encoding=encoding) as f:
                    lines = f.readlines()
                print(f"エンコーディング {encoding} で読み込み成功")
                break
            except UnicodeDecodeError:
                continue
        
        if lines is None:
            raise Exception("適切なエンコーディングが見つかりませんでした")
        
        # キーを探して更新
        updated = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                updated = True
                break
        
        # キーが見つからない場合は追加
        if not updated:
            lines.append(f"{key}={value}\n")
        
        # 更新した内容を書き込む（UTF-8で保存）
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"{key}の値を{value}に更新しました")
    except Exception as e:
        print(f".envファイルの更新に失敗しました: {str(e)}")

def delete_env(key: str):
    """指定されたキーを削除"""
    try:
        # 現在の内容を読み込む
        encodings = ['utf-8', 'cp932', 'shift_jis', 'utf-16']
        lines = None
        
        for encoding in encodings:
            try:
                with open(ENV_FILE, "r", encoding=encoding) as f:
                    lines = f.readlines()
                print(f"エンコーディング {encoding} で読み込み成功")
                break
            except UnicodeDecodeError:
                continue
        
        if lines is None:
            raise Exception("適切なエンコーディングが見つかりませんでした")
        
        # キーを含む行を削除
        lines = [line for line in lines if not line.startswith(f"{key}=")]
        
        # 更新した内容を書き込む（UTF-8で保存）
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"{key}を削除しました")
    except Exception as e:
        print(f".envファイルの更新に失敗しました: {str(e)}")

def main():
    """コマンドラインインターフェース"""
    import argparse
    
    parser = argparse.ArgumentParser(description=".envファイルを管理するツール")
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")
    
    # readコマンド
    subparsers.add_parser("read", help="現在の.envファイルの内容を表示")
    
    # updateコマンド
    update_parser = subparsers.add_parser("update", help="指定されたキーの値を更新")
    update_parser.add_argument("key", help="更新するキー")
    update_parser.add_argument("value", help="設定する値")
    
    # deleteコマンド
    delete_parser = subparsers.add_parser("delete", help="指定されたキーを削除")
    delete_parser.add_argument("key", help="削除するキー")
    
    args = parser.parse_args()
    
    if args.command == "read":
        read_env()
    elif args.command == "update":
        update_env(args.key, args.value)
    elif args.command == "delete":
        delete_env(args.key)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 