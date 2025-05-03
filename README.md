# SwingFit Pro - AIゴルフクラブレコメンデーションシステム

## 概要
SwingFit Proは、ユーザーのスイングデータやプレースタイル、身体的特徴に基づき、最適なゴルフクラブセット（14本）をAIが自動で提案するWebアプリケーションです。国内外のプロ・アマチュアのクラブセッティングデータや最新のゴルフ理論をもとに、ユーザー属性ごとに最適なクラブ構成を選定します。

## 特徴
- ユーザー属性（ヘッドスピード・ハンディキャップ・年齢・性別）ごとに最適な14本セットを自動生成
- 国内外のプロ・アマチュアのデータをもとにした10パターンのクラブセッティング
- クラブ種別・ブランド・モデル・ロフト・シャフト・フレックスなど詳細なスペックを提案
- セット詳細画面ではブランドごとのロゴ画像や色分けで視覚的に分かりやすく表示
- UI/UXは30〜50代ゴルファー向けに最適化
- CORSやAPIエンドポイントの柔軟な設定

## 技術スタック
- フロントエンド: React, Material-UI, Axios, React Router DOM
- バックエンド: FastAPI, Pydantic
- その他: ブランドロゴ画像（SVG/PNG）

## セットアップ手順
### 1. バックエンド
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # (Windows)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. フロントエンド
```bash
cd frontend
npm install
npm start
```

### 3. ブランドロゴ画像の配置
`frontend/public/brand-logos/` ディレクトリを作成し、主要ブランドのSVG/PNGロゴ（例: `titleist.svg`, `taylormade.svg`, `callaway.svg` など）を配置してください。

## 画面構成
- トップ画面：ユーザー情報入力フォーム＋おすすめクラブセット一覧（簡易表示）
- セット詳細画面：14本すべてのクラブをブランドロゴ・色分け・スペック付きでリッチに表示

## APIエンドポイント
- `POST /api/recommendations/` : レコメンデーション生成
- `GET /api/recommendations/history/` : 履歴取得
- `POST /api/recommendations/{id}/feedback/` : フィードバック送信

## カスタマイズ例
- ブランドロゴ画像の追加・差し替え
- 推薦ロジックのパターン追加や重み調整
- UIテーマやレイアウトの変更

## 今後の拡張例
- クラブ比較・お気に入り登録機能
- PDF/印刷用レイアウト
- より詳細なマッチングスコアやフィードバック分析

## 注意事項
- 本システムは開発・検証用途です。実際のクラブ購入時は必ずフィッティングや試打を推奨します。
- CORS設定やAPIエンドポイントは運用環境に合わせて調整してください。

---
ご質問・ご要望はいつでもお知らせください！ 