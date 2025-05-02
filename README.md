# SwingFit Pro - AIゴルフクラブレコメンデーションシステム

SwingFit Proは、ゴルファーの特性に基づいて最適なゴルフクラブを推薦するAIシステムです。

## システム概要

SwingFit Proは、ゴルファーの以下の特性を考慮してクラブを推薦します：

- スイングスピード
- スキルレベル（ハンディキャップ）
- 体格（身長、体重）
- 年齢
- 性別
- 予算
- 好みのブランド

## 技術スタック

### バックエンド
- FastAPI (Python)
- Pydantic (データバリデーション)
- Uvicorn (ASGIサーバー)

### フロントエンド
- React
- Material-UI
- Axios (HTTPクライアント)

## セットアップ方法

### バックエンド
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### フロントエンド
```bash
cd frontend
npm install
npm start
```

## システムアーキテクチャ

### バックエンド

#### データモデル
1. クラブデータベース（`CLUB_DATABASE`）
   - ドライバーとアイアンの2カテゴリ
   - 各クラブの特性：
     - ブランド
     - モデル
     - フレックス
     - ロフト
     - シャフト
     - スイングスピード範囲
     - スキルレベル
     - 価格
     - 特徴

2. リクエストモデル（`RecommendationRequest`）
   ```python
   class RecommendationRequest(BaseModel):
       height: float
       weight: float
       age: int
       gender: str
       handicap: float
       headSpeed: float
       ballSpeed: float
       launchAngle: float
       swingIssue: str
       budget: float
   ```

#### マッチングロジック

1. スキルレベルの計算
   ```python
   def calculate_skill_level(handicap: float) -> str:
       if handicap <= 10:
           return "上級者"
       elif handicap <= 20:
           return "中級者"
       else:
           return "初級者"
   ```

2. スイングスピードのマッチング
   ```python
   def calculate_swing_speed_match(club_speed_range: tuple, user_speed: float) -> float:
       min_speed, max_speed = club_speed_range
       if min_speed <= user_speed <= max_speed:
           return 1.0
       elif user_speed < min_speed:
           return 1.0 - (min_speed - user_speed) / min_speed
       else:
           return 1.0 - (user_speed - max_speed) / max_speed
   ```

3. スキルレベルのマッチング
   ```python
   def calculate_skill_level_match(club_skill: str, user_skill: str) -> float:
       skill_levels = {"初級者": 0, "中級者": 1, "上級者": 2}
       diff = abs(skill_levels[club_skill] - skill_levels[user_skill])
       return 1.0 - (diff * 0.3)
   ```

4. 予算のマッチング
   ```python
   def calculate_budget_match(club_price: float, user_budget: float) -> float:
       if club_price <= user_budget:
           return 1.0
       return max(0.3, 1.0 - (club_price - user_budget) / user_budget)
   ```

5. 総合スコアの計算
   ```python
   weights = {
       "swing_speed": 0.3,
       "skill_level": 0.3,
       "preference": 0.2,
       "budget": 0.2
   }
   ```

### フロントエンド

#### コンポーネント構成
1. `App.js`: アプリケーションのルートコンポーネント
2. `RecommendationForm.js`: ユーザー入力フォームとレコメンデーション表示
3. `client.js`: APIクライアント

#### フォーム項目
- 身長 (cm)
- 体重 (kg)
- 年齢
- 性別
- ハンディキャップ
- ヘッドスピード (m/s)
- ボールスピード (m/s)
- 打ち出し角 (度)
- スイングの課題
- 予算 (円)

## APIエンドポイント

### レコメンデーション生成
```
POST /api/recommendations/
```
- リクエスト: ユーザーの特性データ
- レスポンス: 推薦クラブのリスト（各カテゴリ2つずつ）

### レコメンデーション履歴
```
GET /api/recommendations/history/
```
- レスポンス: 過去のレコメンデーション履歴

### フィードバック
```
POST /api/recommendations/{recommendation_id}/feedback/
```
- リクエスト: フィードバック内容
- レスポンス: 確認メッセージ

## レコメンデーションロジックの詳細

1. ユーザーデータの受信と変換
2. 各クラブタイプ（ドライバー、アイアン）に対して：
   - マッチングスコアの計算
   - スコアの高い順にソート
   - 上位2つのクラブを選択
3. レスポンスの生成と返却

## 今後の改善案

1. データの拡充
   - より多くのクラブモデル
   - 詳細な性能情報
   - ユーザーレビュー

2. マッチングロジックの強化
   - スイングの課題に基づく推薦
   - 年齢・体格に基づく調整
   - 季節・天候の考慮

3. UI/UXの改善
   - レコメンデーション理由の詳細表示
   - クラブ比較機能
   - フィードバック機能の強化

## 注意事項

- バックエンドは`localhost:8000`で動作
- フロントエンドは`localhost:3000`で動作
- CORSは開発環境用に設定済み
- 本番環境では適切なセキュリティ設定が必要

## EC2インスタンスへの接続手順

### 1. キーペアの作成と設定

1. 新しいキーペアを生成（パスフレーズなし）：
```powershell
ssh-keygen -t rsa -b 4096 -f new-golf-recommend-key.pem -N '""'
```

2. キーファイルの権限を設定：
```powershell
icacls new-golf-recommend-key.pem /inheritance:r
icacls new-golf-recommend-key.pem /grant:r "$($env:USERNAME):(R)"
```

3. AWS CLIの認証情報を設定：
```powershell
aws configure
```
以下の情報を入力：
- AWS Access Key ID
- AWS Secret Access Key
- Default region name: ap-northeast-1
- Default output format: json

4. 既存のキーペアを削除：
```powershell
aws ec2 delete-key-pair --key-name golf-recommend-key
```

5. 新しい公開鍵をEC2インスタンスに登録：
```powershell
aws ec2 import-key-pair --key-name golf-recommend-key --public-key-material fileb://new-golf-recommend-key.pem.pub
```

### 2. EC2インスタンスの作成

1. 新しいインスタンスを作成：
```powershell
aws ec2 run-instances --image-id ami-0d52744d6551d851e --instance-type t2.micro --key-name golf-recommend-key --subnet-id subnet-0c8089b48958a36a9 --security-group-ids sg-0db4fcaa3ce0019f8
```

2. インスタンスの状態を確認：
```powershell
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].[InstanceId,PublicIpAddress]' --output text
```

### 3. SSH接続

インスタンスが実行中になったら、SSH接続を試みる：
```powershell
ssh -i new-golf-recommend-key.pem ubuntu@3.112.190.18
```

注意事項：
- インスタンスの起動には約1-2分かかります
- キーファイルは安全に保管し、公開しないようにしてください
- AWSの認証情報は定期的に更新することをお勧めします
- インスタンスのIPアドレスは変更される可能性があります 