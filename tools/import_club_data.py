import pandas as pd
from sqlalchemy import create_engine
import re

# --- 設定 ---
CSV_PATH = 'golf_club_sets.csv'  # ここにCSVファイル名を指定
DB_URL = 'postgresql+psycopg2://ユーザー名:パスワード@localhost:5432/データベース名'  # ←適宜修正

# --- CSV読み込み ---
df = pd.read_csv(CSV_PATH)

# --- 前処理 ---
def extract_number(val):
    if pd.isnull(val):
        return None
    m = re.search(r'([0-9.]+)', str(val))
    return float(m.group(1)) if m else None

df['クラブ重量'] = df['クラブ重量'].apply(extract_number)
df['シャフト重量'] = df['シャフト重量'].apply(extract_number)
df['ロフト角'] = df['ロフト角'].apply(lambda x: float(str(x).replace('°','')) if pd.notnull(x) else None)
df['ライ角'] = df['ライ角'].apply(lambda x: float(str(x).replace('°','')) if pd.notnull(x) else None)
df['長さ'] = df['長さ'].apply(lambda x: float(str(x).replace('"','')) if pd.notnull(x) else None)
def match_score_to_num(x):
    if '★' in str(x):
        return str(x).count('★')
    try:
        return float(x)
    except:
        return None
df['推奨度'] = df['推奨度'].apply(match_score_to_num)

# --- セット情報抽出 ---
set_cols = [
    'セットID','セット名','ブランド名','モデル年','参考価格','対象ユーザー層',
    'セットの特徴・コンセプト','推奨度','発売日','公式商品ページURL','商品画像URL','備考'
]
sets_df = df[set_cols].drop_duplicates(subset=['セットID']).copy()
sets_df = sets_df.rename(columns={
    'セットID': 'set_id',
    'セット名': 'set_name',
    'ブランド名': 'brand',
    'モデル年': 'model_year',
    '参考価格': 'price',
    '対象ユーザー層': 'target_user',
    'セットの特徴・コンセプト': 'concept',
    '推奨度': 'match_score',
    '発売日': 'release_date',
    '公式商品ページURL': 'official_url',
    '商品画像URL': 'image_url',
    '備考': 'remarks'
})

# --- クラブ情報抽出 ---
club_cols = [
    'セットID','クラブ種別','クラブ名','ロフト角','シャフト名・素材','フレックス','長さ','ライ角',
    'クラブ重量','ヘッド素材','シャフト重量','グリップ名','単品価格','ブランドロゴ画像ファイル名',
    '発売日','公式商品ページURL','商品画像URL','備考'
]
clubs_df = df[club_cols].copy()
clubs_df = clubs_df.rename(columns={
    'セットID': 'set_id',
    'クラブ種別': 'club_type',
    'クラブ名': 'club_name',
    'ロフト角': 'loft',
    'シャフト名・素材': 'shaft',
    'フレックス': 'flex',
    '長さ': 'length',
    'ライ角': 'lie_angle',
    'クラブ重量': 'club_weight',
    'ヘッド素材': 'head_material',
    'シャフト重量': 'shaft_weight',
    'グリップ名': 'grip',
    '単品価格': 'club_price',
    'ブランドロゴ画像ファイル名': 'brand_logo',
    '発売日': 'release_date',
    '公式商品ページURL': 'official_url',
    '商品画像URL': 'image_url',
    '備考': 'remarks'
})

# --- DB接続 ---
engine = create_engine(DB_URL)

# --- インポート ---
sets_df.to_sql('club_sets', engine, if_exists='append', index=False)
clubs_df.to_sql('clubs', engine, if_exists='append', index=False)

print('インポート完了')

# --- README追記用サンプル ---
# このスクリプトは tools/import_club_data.py に配置し、
# 1. golf_club_sets.csv をプロジェクト直下に置く
# 2. DB_URL を自分の環境に合わせて修正
# 3. python tools/import_club_data.py で実行
# でインポートできます。 