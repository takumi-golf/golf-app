import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
import plotly.express as px
import plotly.graph_objects as go

def display_club_summary(recommendations: Dict[str, Any]):
    # 総額表示（上部に移動）
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <div style='font-size: 1.2rem; color: #666666; margin-bottom: 0.5rem;'>推奨セット総額</div>
        <div style='font-size: 2.5rem; color: #2c5282; font-weight: bold;'>
            ¥{:,}～{:,}
        </div>
    </div>
    """.format(
        int(recommendations['total_price'] * 0.9),
        int(recommendations['total_price'] * 1.1)
    ), unsafe_allow_html=True)
    
    st.subheader("推奨クラブセット")
    
    # 全クラブの情報を一つのリストにまとめる
    club_data = []
    
    # ドライバー
    if recommendations['driver']['recommended_models']:
        driver = recommendations['driver']['recommended_models'][0]
        club_data.append({
            "クラブ": "1W",
            "メーカー": driver['brand'],
            "モデル": driver['model'],
            "価格": f"¥{driver['price']:,.0f}",
            "カスタマイズ": f"シャフト: {driver['shaft']} {driver['shaft_flex']}",
            "特徴": driver['features'],
            "購入リンク": f"https://example.com/driver/{driver['brand']}/{driver['model']}"
        })
    
    # フェアウェイウッド
    if recommendations['woods']:
        for wood in recommendations['woods']:
            loft = int(wood['loft'])
            if loft == 15:
                club_name = "3W"
            elif loft == 18:
                club_name = "5W"
            elif loft == 21:
                club_name = "7W"
            else:
                club_name = f"{loft}°FW"
            
            club_data.append({
                "クラブ": club_name,
                "メーカー": wood['brand'],
                "モデル": wood['model'],
                "価格": f"¥{wood['price']:,.0f}",
                "カスタマイズ": f"シャフト: {wood['shaft']} {wood['shaft_flex']}",
                "特徴": wood['features'],
                "購入リンク": f"https://example.com/wood/{wood['brand']}/{wood['model']}"
            })
    
    # アイアン
    if recommendations['irons']:
        # アイアンセットの情報を取得
        first_iron = recommendations['irons'][0]
        last_iron = recommendations['irons'][-1]
        
        # セットの範囲を決定
        start_num = int(first_iron['club'].replace('アイアン', ''))
        end_num = int(last_iron['club'].replace('アイアン', ''))
        
        # 10番以上の場合はウェッジの名称に変更
        if end_num >= 10:
            if end_num == 10:
                end_name = "PW"
            elif end_num == 11:
                end_name = "SW"
            elif end_num == 12:
                end_name = "LW"
            else:
                end_name = f"{end_num}°"
        else:
            end_name = str(end_num)
        
        club_data.append({
            "クラブ": f"{start_num}～{end_name}",
            "メーカー": first_iron['brand'],
            "モデル": first_iron['model'],
            "価格": f"¥{sum(iron['price'] for iron in recommendations['irons']):,.0f}",
            "カスタマイズ": f"シャフト: {first_iron['shaft']} {first_iron['shaft_flex']}",
            "特徴": first_iron['features'],
            "購入リンク": f"https://example.com/iron/{first_iron['brand']}/{first_iron['model']}"
        })
    
    # ウェッジ
    if recommendations['wedges']:
        for wedge in recommendations['wedges']:
            club_number = wedge['club'].replace('ウェッジ', '')
            if club_number == "ピッチング":
                club_name = "PW"
            elif club_number == "サンド":
                club_name = "SW"
            elif club_number == "ロブ":
                club_name = "LW"
            else:
                club_name = f"{club_number}°"
            
            club_data.append({
                "クラブ": club_name,
                "メーカー": wedge['brand'],
                "モデル": wedge['model'],
                "価格": f"¥{wedge['price']:,.0f}",
                "カスタマイズ": f"シャフト: {wedge['shaft']} {wedge['shaft_flex']}",
                "特徴": wedge['features'],
                "購入リンク": f"https://example.com/wedge/{wedge['brand']}/{wedge['model']}"
            })
    
    # パター
    if recommendations['putter']:
        putter = recommendations['putter']
        club_data.append({
            "クラブ": "PT",
            "メーカー": putter['brand'],
            "モデル": putter['model'],
            "価格": f"¥{putter['price']:,.0f}",
            "カスタマイズ": "最適な長さと重さに調整",
            "特徴": putter['features'],
            "購入リンク": f"https://example.com/putter/{putter['brand']}/{putter['model']}"
        })
    
    # 表を表示
    if club_data:
        df = pd.DataFrame(club_data)
        
        # リンクをクリック可能な形式に変換
        for i, row in df.iterrows():
            st.markdown(f"""
            <div style='margin-bottom: 1rem; padding: 1rem; background-color: #f8f9fa; border-radius: 8px;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                    <h3 style='margin: 0; color: #2c5282;'>{row['クラブ']} - {row['メーカー']} {row['モデル']}</h3>
                    <a href='{row['購入リンク']}' target='_blank' style='background-color: #2c5282; color: white; padding: 0.5rem 1rem; border-radius: 4px; text-decoration: none;'>購入ページへ</a>
                </div>
                <div style='display: flex; flex-direction: column; gap: 0.5rem;'>
                    <p style='margin: 0.2rem 0;'><strong>価格:</strong> {row['価格']}</p>
                    <p style='margin: 0.2rem 0;'><strong>カスタマイズ:</strong> {row['カスタマイズ']}</p>
                    <p style='margin: 0.2rem 0;'><strong>特徴:</strong> {row['特徴']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # クラブ本数の表示
        total_clubs = len(club_data)
        st.markdown(f"""
        <div style='text-align: center; font-size: 16px; color: #666666; margin-top: 1rem;'>
            推奨クラブ本数: {total_clubs}本（最大14本まで持てます）
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("条件に合うクラブが見つかりませんでした")

def display_price_comparison(recommendations: Dict[str, Any]):
    st.subheader("価格比較")
    
    # 予算別の推奨セットを表示
    st.markdown("### 予算別推奨セット")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### コスパ重視")
        st.markdown("""
        - 中古品や前年モデルを中心に
        - 実績のある定番モデル
        - 総額: ¥150,000〜
        """)
    
    with col2:
        st.markdown("#### 新作重視")
        st.markdown("""
        - 最新モデルを中心に
        - 最新テクノロジー搭載
        - 総額: ¥300,000〜
        """)
    
    with col3:
        st.markdown("#### 予算重視")
        st.markdown("""
        - 入門モデルを中心に
        - 必要最小限のセット
        - 総額: ¥100,000〜
        """)

def display_fitting_analysis(user_data: Dict[str, Any], recommendations: Dict[str, Any]):
    st.subheader("フィッティング解析")
    
    # スイングの悩みに基づく鉛テープの位置
    if 'weight_position' in recommendations:
        st.markdown("### スイング改善アドバイス")
        st.markdown(f"""
        現在のスイングの悩み: **{user_data.get('swing_issue', '未指定')}**
        
        推奨される鉛テープの位置: **{recommendations['weight_position']}**
        
        <div style='text-align: center;'>
            <img src='https://example.com/weight_position.png' style='width: 300px;'>
        </div>
        """, unsafe_allow_html=True)
    
    # ユーザープロファイルの可視化
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ユーザープロファイル")
        profile_data = pd.DataFrame({
            "項目": ["身長", "体重", "年齢", "性別", "ハンディキャップ"],
            "値": [
                f"{user_data['height']}cm",
                f"{user_data['weight']}kg",
                f"{user_data['age']}歳",
                "男性" if user_data['gender'] == "male" else "女性",
                f"{user_data['handicap']}" if user_data['handicap'] else "未設定"
            ]
        })
        st.table(profile_data)
    
    with col2:
        if user_data['head_speed']:
            st.markdown("### スイングデータ")
            swing_data = pd.DataFrame({
                "項目": ["ヘッドスピード", "ボールスピード", "打ち出し角度"],
                "値": [
                    f"{user_data['head_speed']}m/s",
                    f"{user_data['ball_speed']}m/s" if user_data['ball_speed'] else None,
                    f"{user_data['launch_angle']}°" if user_data['launch_angle'] else None
                ]
            })
            st.table(swing_data)

# ページ設定
st.set_page_config(
    page_title="ぴったりゴルフ",
    page_icon="🏌️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# スタイル設定
st.markdown("""
    <style>
    html {
        scroll-behavior: smooth;
    }
    .main-header {
        background: linear-gradient(135deg, #1a472a, #2d5a3f);
        padding: 1rem 0;
        margin-bottom: 2rem;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    .header-title {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #f8f8f8;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        letter-spacing: 1px;
    }
    .section-title {
        color: #1a472a;
        font-weight: 700;
        font-size: 1.6rem;
        margin: 2rem 0 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e8e8e8;
    }
    .input-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.8rem;
        font-weight: 500;
        color: #333333;
    }
    .required {
        color: #c62828;
        font-weight: bold;
    }
    .search-button {
        display: flex;
        justify-content: center;
        margin: 3rem 0;
    }
    .stButton > button {
        width: 100%;
        padding: 1.2rem;
        font-size: 1.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #1a472a, #2d5a3f);
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2d5a3f, #1a472a);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    .expander-header {
        font-weight: 600;
        color: #1a472a;
        font-size: 1.2rem;
    }
    .stExpander {
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-radius: 8px;
        margin-bottom: 1rem;
        background-color: #f8f8f8;
    }
    .stExpander > div {
        padding: 1rem;
    }
    .stSlider > div > div > div {
        background-color: #f0f0f0;
    }
    .stSlider > div > div > div > div {
        color: #1a472a;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.5rem;
        background-color: #f8f8f8;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stSlider > div > div > div > div:first-child,
    .stSlider > div > div > div > div:last-child {
        color: #333333;
        font-size: 1.1rem;
        font-weight: 500;
        padding: 0.3rem 0.5rem;
    }
    .stSlider > div > div > div > div:first-child::before,
    .stSlider > div > div > div > div:last-child::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 4px;
        z-index: -1;
    }
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 2rem;
    }
    .stRadio > div > label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }
    .stRadio > div > label > div {
        margin-right: 0.5rem;
    }
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# タイトル
st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="header-title">
                <div class="main-title">ぴったりゴルフ</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Font Awesomeの追加
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
""", unsafe_allow_html=True)

# 基本情報セクション
st.markdown('<div class="section-title">基本情報</div>', unsafe_allow_html=True)

# 2カラムレイアウトで基本情報を配置
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-label"><span class="required">*</span>身長</div>', unsafe_allow_html=True)
    height = st.slider("身長 (cm)", 150, 200, 170, label_visibility="collapsed")
    
    st.markdown('<div class="input-label"><span class="required">*</span>体重</div>', unsafe_allow_html=True)
    weight = st.slider("体重 (kg)", 40, 120, 65, label_visibility="collapsed")

with col2:
    st.markdown('<div class="input-label"><span class="required">*</span>年齢</div>', unsafe_allow_html=True)
    age = st.slider("年齢", 18, 80, 45, label_visibility="collapsed")
    
    st.markdown('<div class="input-label"><span class="required">*</span>性別</div>', unsafe_allow_html=True)
    gender = st.radio("性別", ["男性", "女性"], label_visibility="collapsed", horizontal=True)

# 詳細情報セクション
st.markdown('<div class="section-title">詳細情報</div>', unsafe_allow_html=True)

# ゴルフ経験
with st.expander("ゴルフ経験", expanded=False):
    st.markdown('<div class="input-label">アベレージスコア</div>', unsafe_allow_html=True)
    average_score = st.number_input(
        "アベレージスコア（例：100）", 
        min_value=60, 
        max_value=150, 
        value=100,
        label_visibility="visible"
    )

# ドライバースイングデータ
with st.expander("ドライバースイングデータ", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="input-label">ヘッドスピード</div>', unsafe_allow_html=True)
        head_speed = st.number_input(
            "ヘッドスピード (m/s)（例：45.0）", 
            min_value=30.0, 
            max_value=70.0, 
            value=45.0,
            step=0.5,
            label_visibility="visible"
        )
        
        st.markdown('<div class="input-label">ボールスピード</div>', unsafe_allow_html=True)
        ball_speed = st.number_input(
            "ボールスピード (m/s)（例：60.0）", 
            min_value=40.0, 
            max_value=100.0, 
            value=60.0,
            step=0.5,
            label_visibility="visible"
        )
    
    with col2:
        st.markdown('<div class="input-label">打ち出し角度</div>', unsafe_allow_html=True)
        launch_angle = st.number_input(
            "打ち出し角度 (度)（例：12.0）", 
            min_value=5.0, 
            max_value=20.0, 
            value=12.0,
            step=0.5,
            label_visibility="visible"
        )

# スイングの悩み
with st.expander("スイングの悩み", expanded=False):
    swing_issue = st.selectbox(
        "現在のスイングの悩みを選択してください",
        ["なし", "スライス", "フック", "低い弾道", "高い弾道"]
    )

# 予算設定
with st.expander("予算設定", expanded=False):
    budget_preference = st.selectbox(
        "予算の優先度を選択してください",
        ["コスパ重視", "新作重視", "予算重視"]
    )

# レコメンデーション生成ボタン
st.markdown('<div class="search-button">', unsafe_allow_html=True)
if st.button("最適なクラブセットを検索", type="primary", use_container_width=True):
    # プログレスバーとスピナーを表示
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # APIリクエストのためのデータ準備
    user_data = {
        "height": height,
        "weight": weight,
        "age": age,
        "gender": "male" if gender == "男性" else "female",
        "handicap": None,
        "average_score": average_score if average_score else None,
        "head_speed": head_speed if head_speed else None,
        "ball_speed": ball_speed if ball_speed else None,
        "launch_angle": launch_angle if launch_angle else None,
        "swing_issue": swing_issue if swing_issue != "なし" else None,
        "budget_preference": {
            "コスパ重視": "cost_performance",
            "新作重視": "latest",
            "予算重視": "budget"
        }[budget_preference]
    }
    
    try:
        # 進捗表示の更新
        progress_bar.progress(20)
        status_text.text("ユーザーデータを分析中...")
        
        # APIにリクエスト送信
        progress_bar.progress(40)
        status_text.text("AIが最適なクラブを検索中...")
        response = requests.post("http://localhost:8000/recommend", json=user_data)
        
        progress_bar.progress(60)
        status_text.text("レコメンデーションを生成中...")
        
        if response.status_code == 200:
            recommendations = response.json()
            
            progress_bar.progress(80)
            status_text.text("結果を表示中...")
            
            progress_bar.progress(100)
            status_text.text("完了！")
            
            # ゴルフらしい演出
            st.markdown("""
            <div style='text-align: center; margin-top: 1rem;'>
                <div style='font-size: 2rem; color: #1a472a;'>🎯 ホールインワン！</div>
                <div style='margin-top: 1rem;'>
                    <span style='font-size: 1.5rem;'>🏌️</span>
                    <span style='font-size: 1.2rem; color: #666;'>あなたにぴったりのクラブが見つかりました！</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ゴルフボールのアニメーション
            st.markdown("""
            <style>
            @keyframes golfBall {
                0% { transform: translateX(0) translateY(0); }
                50% { transform: translateX(100px) translateY(-50px); }
                100% { transform: translateX(200px) translateY(0); }
            }
            .golf-ball {
                animation: golfBall 1s ease-in-out;
                display: inline-block;
                font-size: 2rem;
            }
            .result-section {
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.5s ease-out, transform 0.5s ease-out;
            }
            .result-section.visible {
                opacity: 1;
                transform: translateY(0);
            }
            </style>
            <div style='text-align: center; margin-top: 1rem;'>
                <div class='golf-ball'>⛳</div>
            </div>
            <script>
            setTimeout(() => {
                document.querySelector('.result-section').classList.add('visible');
            }, 1000);
            </script>
            """, unsafe_allow_html=True)
            
            # 結果表示
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.header("あなたに最適なクラブセット")
            
            # タブで結果を整理
            tabs = st.tabs(["クラブセット概要", "価格比較", "フィッティング解析"])
            
            with tabs[0]:
                display_club_summary(recommendations)
                
            with tabs[1]:
                display_price_comparison(recommendations)
                
            with tabs[2]:
                display_fitting_analysis(user_data, recommendations)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("レコメンデーションの生成中にエラーが発生しました。")
            
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
    finally:
        # プログレスバーをクリア
        progress_bar.empty()
        status_text.empty()
st.markdown('</div>', unsafe_allow_html=True) 