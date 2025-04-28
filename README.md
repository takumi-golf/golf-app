# ゴルフフィッティングWebアプリ

このプロジェクトは、AIを活用したゴルフクラブフィッティングWebアプリケーションです。ユーザーの身体特性やスイングデータに基づいて、最適なゴルフクラブをレコメンドします。

## 機能

- ユーザープロファイル入力（身長、体重、年齢、性別など）
- スイングデータ分析（ヘッドスピード、ボールスピード、打ち出し角度など）
- AIベースのクラブレコメンデーション
- 価格比較機能
- フィッティング解析レポート

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

1. ブラウザで `http://localhost:8501` にアクセス
2. サイドバーでユーザー情報を入力
3. 「最適なクラブセットを検索」ボタンをクリック
4. レコメンデーション結果を確認

## 開発者向け情報

### プロジェクト構造

```
golf-fitting-app/
├── app.py              # FastAPIバックエンド
├── frontend.py         # Streamlitフロントエンド
├── requirements.txt    # 依存パッケージ
├── models/            # 機械学習モデル
└── README.md          # ドキュメント
```

### データモデル

- `UserProfile`: ユーザーの基本情報とスイングデータ
- `ClubRecommendation`: 推奨クラブセットの情報

### APIエンドポイント

- `GET /`: ウェルカムメッセージ
- `POST /recommend`: クラブレコメンデーション生成

## ライセンス

MIT License

## 貢献

プロジェクトへの貢献は大歓迎です。IssueやPull Requestをお待ちしています。 