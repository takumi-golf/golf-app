# ゴルフフィッティングWebアプリ

このプロジェクトは、AIを活用したゴルフクラブフィッティングWebアプリケーションです。ユーザーの身体特性やスイングデータに基づいて、最適なゴルフクラブをレコメンドします。

## 機能

- ユーザープロファイル入力（身長、体重、年齢、性別など）
- スイングデータ分析（ヘッドスピード、ボールスピード、打ち出し角度など）
- AIベースのクラブレコメンデーション
- 価格比較機能
- フィッティング解析レポート

## 自動化機能

### データ収集
- 毎週月曜日の午前3時に自動的にゴルフクラブ情報をスクレイピング
- スクレイピング完了後、Slackに通知
- 収集したデータは`data/golf_clubs.json`に保存

### バックアップ
- 毎日午前2時にデータベースのバックアップを自動実行
- バックアップ完了後、Slackに通知
- バックアップファイルは`backups/`ディレクトリに保存
- 最新10件のバックアップ履歴を`backups/backup_history.json`に記録

### スケジューラの起動方法
```bash
python scripts/scheduler.py
```

## 技術スタック

- バックエンド: FastAPI
- フロントエンド: Streamlit
- 機械学習: scikit-learn
- データ処理: pandas, numpy
- 可視化: matplotlib, seaborn

## セットアップ手順

1. リポジトリのクローン
```bash
git clone [repository-url]
cd golf-fitting-app
```

2. 仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

4. バックエンドサーバーの起動
```bash
uvicorn app:app --reload
```

5. フロントエンドの起動（別のターミナルで）
```bash
streamlit run frontend.py
```

## 使用方法

### 基本的な使用方法

1. ブラウザで `http://localhost:8501` にアクセス
2. サイドバーでユーザー情報を入力
3. 「最適なクラブセットを検索」ボタンをクリック
4. レコメンデーション結果を確認

### 詳細な使用方法

#### ユーザープロファイル入力
- 必須項目：
  - 身長（cm）
  - 体重（kg）
  - 年齢
  - 性別
  - 利き手
- オプション項目：
  - スイングスピード
  - プレイ頻度
  - 現在のハンディキャップ

#### スイングデータ分析
- 入力可能なデータ：
  - ヘッドスピード
  - ボールスピード
  - 打ち出し角度
  - スピン量
  - キャリー距離

#### レコメンデーション結果
- 表示される情報：
  - 推奨クラブセット
  - 各クラブの詳細仕様
  - 価格帯
  - 適合度スコア
  - 代替オプション

## コンポーネント説明

### アプリケーション（app/）
- `main.py`: アプリケーションのエントリーポイント
- `app.py`: FastAPIバックエンド
- `frontend.py`: Streamlitフロントエンド
- `models.py`: データモデル定義
- `schemas.py`: APIスキーマ定義
- `env_manager.py`: 環境変数管理
- `cache_manager.py`: キャッシュ管理

### スクリプト（scripts/）
- `scraper.py`: ゴルフクラブデータ収集
- `slack_bot.py`: Slack通知機能
- `slack_notifier.py`: Slack通知ユーティリティ
- `golf-app.service`: システムサービス設定
- `deploy.sh`: デプロイスクリプト

### 設定（config/）
- `config.py`: メイン設定
- `slack_config.py`: Slack設定
- `email_config.py`: メール設定
- `aws_config.py`: AWS設定

### データベース（db/）
- `database.py`: データベース接続
- `database_partitioning.py`: データベースパーティショニング
- `query_analyzer.py`: クエリ分析
- `query_optimizer.py`: クエリ最適化

### テスト（tests/）
- `performance_tests.py`: パフォーマンステスト
- `run_performance_tests.py`: テスト実行スクリプト
- `init_test_data.py`: テストデータ初期化
- `pytest.ini`: pytest設定

### バックアップ（backups/）
- `backup_utils.py`: バックアップユーティリティ
- `backup_database.py`: データベースバックアップ
- `backup_verifier.py`: バックアップ検証
- `backup_scheduler.ps1`: バックアップスケジューラ

## 開発者向け情報

### プロジェクト構造

```
golf-fitting-app/
├── app/                # アプリケーションコード
├── scripts/            # スクリプト類
├── config/             # 設定ファイル
├── db/                 # データベース関連
├── tests/              # テスト関連
├── logs/               # ログファイル
├── data/               # データファイル
├── backups/            # バックアップファイル
├── models/             # 機械学習モデル
├── output/             # 出力ファイル
├── venv/               # 仮想環境
├── setup.py            # プロジェクトのセットアップ
├── requirements.txt    # 依存パッケージ
└── README.md           # ドキュメント
```

### データモデル

- `UserProfile`: ユーザーの基本情報とスイングデータ
- `ClubRecommendation`: 推奨クラブセットの情報

### APIエンドポイント

- `GET /`: ウェルカムメッセージ
- `POST /recommend`: クラブレコメンデーション生成

## トラブルシューティング

### よくある問題と解決方法

1. バックエンドサーバーが起動しない
   - ポートが使用中でないか確認
   - 依存パッケージが正しくインストールされているか確認

2. フロントエンドが表示されない
   - ブラウザのキャッシュをクリア
   - ポート8501が使用可能か確認

3. データベース接続エラー
   - データベースサーバーが起動しているか確認
   - 接続情報が正しいか確認

## ライセンス

MIT License

## 貢献

プロジェクトへの貢献は大歓迎です。IssueやPull Requestをお待ちしています。

## データベース仕様

### テーブル構造

#### Clubsテーブル
- `id`: 主キー
- `club_id`: ユニークID（文字列）
- `brand`: ブランド名
- `model`: モデル名
- `loft`: ロフト角度（度）
- `shaft`: シャフト名
- `shaft_flex`: シャフトフレックス
- `price`: 価格（円）
- `features`: 特徴（JSON）
- `type`: クラブタイプ
- `specifications`: 仕様（JSON）
- `popularity_score`: 人気スコア
- `created_at`: 作成日時
- `updated_at`: 更新日時
- `is_available`: 在庫状態

### データベース初期化手順

1. データベースの初期化
```bash
python scripts/init_db.py
```

2. サンプルデータの挿入（開発環境用）
```bash
python scripts/insert_sample_data.py
```

3. データベースの状態確認
```bash
python scripts/check_db.py
```

### データベースバックアップ

// ... existing code ... 