import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# --- 多言語辞書 ---
LANG_DICT = {
    'ja': {
        'title': 'SwingFit Pro',
        'subtitle': 'あなたに最適なゴルフクラブセットをAIが提案します',
        'dev_settings': '開発設定',
        'use_dummy': 'ダミーデータを使用',
        'using_dummy': 'ダミーデータを使用中',
        'basic_info': '基本情報',
        'swing_info': 'スイング情報',
        'budget_setting': '予算設定',
        'search_btn': '最適なクラブを探す',
        'recommend_set': '推奨クラブセット',
        'price_comparison': '予算別推奨セット',
        'fitting_analysis': 'フィッティング解析',
        'lang_select': '言語 / Language',
        'recommend_reason': '推奨理由',
        'no_reason': '（推奨理由の情報がありません）',
    },
    'en': {
        'title': 'SwingFit Pro',
        'subtitle': 'AI recommends the best golf club set for you',
        'dev_settings': 'Development Settings',
        'use_dummy': 'Use Dummy Data',
        'using_dummy': 'Using Dummy Data',
        'basic_info': 'Basic Information',
        'swing_info': 'Swing Information',
        'budget_setting': 'Budget Setting',
        'search_btn': 'Find the Best Clubs',
        'recommend_set': 'Recommended Club Set',
        'price_comparison': 'Recommended Sets by Budget',
        'fitting_analysis': 'Fitting Analysis',
        'lang_select': '言語 / Language',
        'recommend_reason': 'Reason for Recommendation',
        'no_reason': '(No recommendation reason available)',
    }
}

# --- テーマカラーパターン ---
THEME_PRESETS = {
    'blue':  { 'main': '#2c5282', 'accent': '#2a4365', 'label': 'ブルー系 / Blue' },
    'green': { 'main': '#2e7d32', 'accent': '#1b5e20', 'label': 'グリーン系 / Green' },
    'red':   { 'main': '#c62828', 'accent': '#8e0000', 'label': 'レッド系 / Red' },
}
DEFAULT_THEME = 'blue'

# --- 言語選択（セッションで管理） ---
def get_lang():
    if 'lang' not in st.session_state:
        st.session_state['lang'] = 'ja'
    return st.session_state['lang']

def set_lang():
    lang = get_lang()
    # サイドバー最上部に20pxの余白を追加
    st.sidebar.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    # サイドバータイトル行をflex rowで配置
    st.sidebar.markdown(
        """
        <div class='sidebar-title-row'>
            <span style='font-size:1.5em; font-weight:800; color:#2c5282;'>SwingFit Pro</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    # 言語セクション全体をラップしてマージン調整
    st.sidebar.markdown("""
    <div id='lang-section' style='margin-bottom: 1.2em;'>
      <strong style='font-size:1.1em;'>言語 / Language</strong>
    </div>
    """, unsafe_allow_html=True)
    lang = st.sidebar.selectbox(
        "言語 / Language",
        options=[('ja', '日本語'), ('en', 'English')],
        format_func=lambda x: x[1],
        index=0 if get_lang() == 'ja' else 1,
        key='lang_select_box',
        label_visibility="collapsed"
    )
    st.session_state['lang'] = lang[0]
    # 言語セクション直後の余白は削除

# --- カスタムテーマCSS（レスポンシブ・ダーク対応） ---
def set_custom_theme():
    st.set_page_config(
        page_title="SwingFit Pro",
        page_icon="⛳",
        layout="wide"
    )
    st.markdown("""
    <style>
        html, body, .main, .block-container {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        .main {
            padding-bottom: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        /* サイドバーのselectboxやラベルの下部マージンを調整 */
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label {
            margin-bottom: 0.7em !important;
        }
        /* selectboxラッパーにもマージン調整 */
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb] {
            margin-bottom: 0.7em !important;
        }
        section[data-testid="stSidebar"] .stSelectbox + div {
            margin-bottom: 0.7em !important;
        }
        .service-title, .service-subtitle, .catchcopy, .main-visual {
            margin-top: 0 !important;
        }
        .stButton > button {
            width: 100%;
            background-color: #2c5282;
            color: white;
            border: none;
            padding: 0.7rem 1.2rem;
            border-radius: 6px;
            font-size: 1.1rem;
        }
        .stButton > button:hover {
            background-color: #2a4365;
        }
        .stSelectbox, .stNumberInput {
            margin-bottom: 1rem;
        }
        .card {
            padding: 1.2rem 1rem 1.2rem 1rem;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .section-header {
            color: #2c5282;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e2e8f0;
        }
        .info-text {
            color: #4a5568;
            font-size: 0.9rem;
        }
        /* --- クラブカードの見やすさ改善 --- */
        .club-card-title {
            font-size: 1.35em !important;
            font-weight: 700 !important;
            color: #2c5282 !important;
            margin: 0 0 0.2em 0 !important;
            line-height: 1.2;
        }
        .club-card-btn {
            background-color: #2c5282;
            color: #fff !important;
            padding: 0.35rem 0.9rem;
            border-radius: 5px;
            font-size: 0.98em;
            font-weight: 600;
            text-decoration: none;
            border: none;
            margin-left: 0.5em;
            transition: background 0.2s;
            display: inline-block;
        }
        .club-card-btn:hover {
            background-color: #2a4365;
            color: #fff !important;
        }
        /* --- サービスタイトル調整 --- */
        .service-title {
            font-size: 2.1em;
            font-weight: 800;
            color: #2c5282;
            margin-bottom: 3em;
            margin-top: 0.2em;
            line-height: 1.15;
            letter-spacing: 0.01em;
        }
        .service-subtitle {
            color: #4a5568;
            font-size: 1.1rem;
            margin-top: 0.1em;
            margin-bottom: 0.5em;
        }
        .catchcopy {
            font-size: 1.3em;
            font-weight: 700;
            color: #2c5282;
            margin: 1.2em 0 1.2em 0;
            letter-spacing: 0.01em;
        }
        .main-visual {
            width: 95%;
            max-width: 420px;
            border-radius: 14px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.13);
            margin-top: calc(2em + 40px);
            margin-bottom: 1.8em;
        }
        @media (max-width: 900px) {
            .main { padding: 0.5rem; }
            .card { padding: 0.7rem; }
            .club-card-title { font-size: 1.1em !important; }
            .service-title { font-size: 1.3em; margin-bottom: 2em; }
        }
        @media (max-width: 600px) {
            .main { padding: 0.1rem; }
            .card { padding: 0.3rem; border-radius: 8px; }
            .club-card-title { font-size: 1em !important; }
            .service-title { font-size: 1.25em; margin-bottom: 1.8em; }
            .service-subtitle { font-size: 0.98em; margin-top: 0.05em; margin-bottom: 0.3em; }
            .catchcopy { font-size: 1.05em; }
            .main-visual { max-width: 98vw; margin-top: calc(1.2em + 40px); margin-bottom: 1.2em; }
        }
        @media (max-width: 600px) {
            .club-card-btn {
                display: block;
                margin: 0.7em auto 0.1em auto;
                width: 90%;
                font-size: 1.05em;
                padding: 0.6em 0;
                text-align: center;
                color: #fff !important;
            }
        }
        .card ul, .card ol {
            margin: 0.5em 0 0.5em 1.2em;
            font-size: 0.98em;
        }
        .card ul {
            padding-left: 1.2em;
            margin-bottom: 0.5em;
        }
        a[role="button"], .stButton > button {
            min-height: 44px;
        }
        body[data-theme=\"dark\"] .card, body[data-theme=\"dark\"] .main {
            background-color: #222831 !important;
            color: #f8f8f2 !important;
        }
        body[data-theme=\"dark\"] .stButton > button {
            background-color: #2c5282;
            color: #f8f8f2;
        }
        body[data-theme=\"dark\"] .stButton > button:hover {
            background-color: #2a4365;
        }
        /* --- ファーストビュー用アニメーション --- */
        .fadein {
            opacity: 0;
            animation: fadein-anim 1.2s ease-in forwards;
        }
        .fadein-img {
            opacity: 0;
            animation: fadein-anim-img 1.2s 0.3s ease-in forwards;
        }
        .fadein-copy {
            opacity: 0;
            animation: fadein-anim 1.2s 0.6s ease-in forwards;
        }
        @keyframes fadein-anim {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadein-anim-img {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(30px); }
        }
        /* バッジ群の上マージンを拡大 */
        .main .service-title + .fadein-img + div {
            margin-top: 1.2em !important;
        }
        .badge-group {
            display: flex;
            justify-content: center;
            gap: 1.2em;
            margin: 1.5em 0 0.8em 0;
            flex-wrap: wrap;
        }
        .badge {
            display: flex;
            align-items: center;
            padding: 0.45em 1.3em;
            border-radius: 2em;
            font-size: 1em;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(44,82,130,0.10);
            background: linear-gradient(90deg, #2c5282 90%, #3a6ea5 100%);
            color: #fff;
            letter-spacing: 0.01em;
            transition: box-shadow 0.2s;
            margin-bottom: 0.3em;
        }
        .badge--green {
            background: linear-gradient(90deg, #2e7d32 90%, #43a047 100%);
        }
        .badge--red {
            background: linear-gradient(90deg, #c62828 90%, #e53935 100%);
        }
        .badge i {
            margin-right: 0.5em;
            font-size: 1.1em;
            opacity: 0.85;
        }
        .badge:hover {
            box-shadow: 0 4px 16px rgba(44,82,130,0.18);
        }
        .step-group {
            display: flex;
            justify-content: center;
            gap: 2em;
            margin: 2em 0 1.2em 0;
            flex-wrap: wrap;
        }
        .step-card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 2px 12px rgba(44,82,130,0.10);
            padding: 1.2em 1.5em 1.1em 1.5em;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 140px;
            max-width: 180px;
            transition: box-shadow 0.2s;
        }
        .step-card:hover {
            box-shadow: 0 4px 24px rgba(44,82,130,0.18);
        }
        .step-num {
            background: #2c5282;
            color: #fff;
            font-weight: 700;
            border-radius: 50%;
            width: 2.2em;
            height: 2.2em;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
            margin-bottom: 0.5em;
            box-shadow: 0 1px 4px rgba(44,82,130,0.10);
        }
        .step-icon {
            font-size: 2em;
            margin-bottom: 0.3em;
        }
        .step-label {
            font-size: 1.05em;
            color: #2c5282;
            font-weight: 600;
            text-align: center;
        }
        /* サイドバー全体のスクロールを完全に無効化 */
        section[data-testid="stSidebar"] {
            overflow-y: hidden !important;
            padding-bottom: 0 !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            height: 100vh !important;
            min-height: 0 !important;
        }
        section[data-testid="stSidebar"] > div:last-child {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .sidebar-content {
            margin-top: -1.5em !important;
        }
        /* 更新履歴のスクロール窓 */
        .sidebar-changelog-scroll {
            max-height: 140px;
            overflow-y: auto;
            padding-right: 0.5em;
        }
        div[data-testid="stLogoSpacer"] {
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        div[data-testid="stSidebarHeader"] {
            margin: 0 !important;
            padding: 0 !important;
            height: auto !important;
            min-height: 0 !important;
        }
        /* サイドバータイトル行をflex配置 */
        .sidebar-title-row {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }
        /* サイドバー折りたたみボタンをタイトル横に */
        div[data-testid="stSidebarCollapseButton"] {
            position: absolute !important;
            right: 0;
            top: 50%;
            transform: translateY(-50%);
            margin: 0 !important;
        }
        /* 箇条書きのポチを左端に寄せる */
        .sidebar-changelog-scroll ul {
            margin-left: 0 !important;
            padding-left: 0.7em !important;
            list-style-position: inside !important;
        }
        .sidebar-changelog-scroll li {
            text-indent: -0.3em !important;
            padding-left: 0 !important;
        }
        /* サイドバー閉じるボタンをサイドバー外側に少しはみ出す */
        div[data-testid="stSidebarCollapseButton"] {
            right: -12px !important;
            z-index: 1002 !important;
        }
        div[data-testid="stSidebarCollapseButton"] > button {
            box-shadow: 0 2px 8px rgba(44,82,130,0.18);
        }
        /* 空のselectboxラベルを非表示に */
        label[data-testid="stWidgetLabel"]:empty {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    # --- Streamlit標準UI非表示 ---
    st.markdown("""
    <style>
    div[data-testid="stToolbar"] {visibility: hidden; height: 0%; position: fixed;}
    div[data-testid="stDecoration"] {visibility: hidden; height: 0%; position: fixed;}
    #MainMenu {visibility: hidden; height: 0%;}
    header {visibility: hidden; height: 0%;}
    footer {visibility: hidden; height: 0%;}
    </style>
    """, unsafe_allow_html=True)

def display_club_summary(recommendations: Dict[str, Any]):
    lang = get_lang()
    # 総額表示（上部に移動）
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem; padding: 1.5rem; background-color: #f8f9fa; border-radius: 12px;'>
        <div style='font-size: 1.2rem; color: #666666; margin-bottom: 0.5rem;'>{'Total Price' if lang=='en' else '推奨セット総額'}</div>
        <div style='font-size: 2.5rem; color: #2c5282; font-weight: bold;'>
            ¥{{:,}}～{{:,}}
        </div>
        <div style='font-size: 0.9rem; color: #666666; margin-top: 0.5rem;'>
            ({'Tax included, shipping not included' if lang=='en' else '税込・送料別'})
        </div>
    </div>
    """.format(
        int(recommendations['total_price'] * 0.9),
        int(recommendations['total_price'] * 1.1)
    ), unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h2 style='color: #2c5282;'>{LANG_DICT[lang]['recommend_set']}</h2>
        <p style='color: #666666;'>{'This is the optimal club set for your play style.' if lang=='en' else 'あなたのプレースタイルに最適なクラブセットです'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 全クラブの情報を一つのリストにまとめる
    club_data = []
    reason_data = []
    
    # ドライバー
    if recommendations['driver']['recommended_models']:
        driver = recommendations['driver']['recommended_models'][0]
        club_data.append({
            "クラブ": "1W" if lang=='ja' else "Driver",
            "メーカー": driver['brand'],
            "モデル": driver['model'],
            "価格": f"¥{driver['price']:,.0f}",
            "カスタマイズ": (f"Shaft: {driver['shaft']} {driver['shaft_flex']}" if lang=='en' else f"シャフト: {driver['shaft']} {driver['shaft_flex']}") ,
            "特徴": driver['features'],
            "購入リンク": f"https://example.com/driver/{driver['brand']}/{driver['model']}",
            "アイコン": "🏌️",
            "推奨理由": driver.get('match_reasons', [])
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
                "購入リンク": f"https://example.com/wood/{wood['brand']}/{wood['model']}",
                "アイコン": "🌲",
                "推奨理由": wood.get('match_reasons', [])
            })
    
    # アイアン
    if recommendations['irons']:
        first_iron = recommendations['irons'][0]
        last_iron = recommendations['irons'][-1]
        start_num = int(first_iron['club'].replace('アイアン', ''))
        end_num = int(last_iron['club'].replace('アイアン', ''))
        
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
            "購入リンク": f"https://example.com/iron/{first_iron['brand']}/{first_iron['model']}",
            "アイコン": "⚡",
            "推奨理由": first_iron.get('match_reasons', [])
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
                "購入リンク": f"https://example.com/wedge/{wedge['brand']}/{wedge['model']}",
                "アイコン": "🎯",
                "推奨理由": wedge.get('match_reasons', [])
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
            "購入リンク": f"https://example.com/putter/{putter['brand']}/{putter['model']}",
            "アイコン": "⛳",
            "推奨理由": putter.get('match_reasons', [])
        })
    
    # 表を表示
    if club_data:
        for club in club_data:
            st.markdown(f"""
            <div style='margin-bottom: 1.2rem; padding: 1.2rem 1rem 1.2rem 1rem; background-color: #ffffff; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.7rem; flex-wrap: wrap;'>
                    <div style='display: flex; align-items: center; gap: 1rem;'>
                        <span style='font-size: 2rem;'>{club['アイコン']}</span>
                        <div>
                            <span class='club-card-title'>{club['クラブ']} - {club['メーカー']} {club['モデル']}</span>
                            <p style='margin: 0.15rem 0 0.1rem 0; color: #666666; font-size:1.05em;'>{club['価格']}</p>
                        </div>
                    </div>
                    <a href='{club['購入リンク']}' target='_blank' class='club-card-btn'>{'Go to Purchase Page' if lang=='en' else '購入ページへ'}</a>
                </div>
                <div style='display: flex; flex-direction: column; gap: 0.5rem; padding: 0.7rem; background-color: #f8f9fa; border-radius: 8px;'>
                    <p style='margin: 0.2rem 0;'><strong>{'Customization' if lang=='en' else 'カスタマイズ'}:</strong> {club['カスタマイズ']}</p>
                    <p style='margin: 0.2rem 0;'><strong>{'Features' if lang=='en' else '特徴'}:</strong> {club['特徴']}</p>
                    <div style='margin-top:0.5rem;'>
                        <strong>{LANG_DICT[lang]['recommend_reason']}:</strong><br/>
                        {('<ul>' + ''.join(f'<li>{reason}</li>' for reason in club['推奨理由']) + '</ul>') if club['推奨理由'] else LANG_DICT[lang]['no_reason']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # クラブ本数の表示
        total_clubs = len(club_data)
        st.markdown(f"""
        <div style='text-align: center; font-size: 16px; color: #666666; margin-top: 1rem; padding: 1rem; background-color: #f8f9fa; border-radius: 8px;'>
            {'Number of recommended clubs' if lang=='en' else '推奨クラブ本数'}: {total_clubs}{' clubs (You can carry up to 14)' if lang=='en' else '本（最大14本まで持てます）'}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No clubs found matching your criteria." if lang=='en' else "条件に合うクラブが見つかりませんでした")

def display_price_comparison(recommendations: Dict[str, Any]):
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h2 style='color: #2c5282;'>予算別推奨セット</h2>
        <p style='color: #666666;'>あなたの予算に合わせた最適な選択肢をご提案します</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='padding: 1.5rem; background-color: #ffffff; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;'>
            <h3 style='color: #2c5282; text-align: center;'>コスパ重視</h3>
            <div style='text-align: center; margin: 1rem 0;'>
                <span style='font-size: 1.5rem; color: #2c5282;'>¥150,000〜</span>
            </div>
            <ul style='color: #666666; padding-left: 1.5rem;'>
                <li>中古品や前年モデルを中心に</li>
                <li>実績のある定番モデル</li>
                <li>コストパフォーマンス重視</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 1.5rem; background-color: #ffffff; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;'>
            <h3 style='color: #2c5282; text-align: center;'>新作重視</h3>
            <div style='text-align: center; margin: 1rem 0;'>
                <span style='font-size: 1.5rem; color: #2c5282;'>¥300,000〜</span>
            </div>
            <ul style='color: #666666; padding-left: 1.5rem;'>
                <li>最新モデルを中心に</li>
                <li>最新テクノロジー搭載</li>
                <li>パフォーマンス重視</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='padding: 1.5rem; background-color: #ffffff; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;'>
            <h3 style='color: #2c5282; text-align: center;'>入門者向け</h3>
            <div style='text-align: center; margin: 1rem 0;'>
                <span style='font-size: 1.5rem; color: #2c5282;'>¥100,000〜</span>
            </div>
            <ul style='color: #666666; padding-left: 1.5rem;'>
                <li>入門モデルを中心に</li>
                <li>必要最小限のセット</li>
                <li>使いやすさ重視</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def display_fitting_analysis(user_data: Dict[str, Any], recommendations: Dict[str, Any]):
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h2 style='color: #2c5282;'>フィッティング解析</h2>
        <p style='color: #666666;'>あなたのプレースタイルに基づく詳細な分析</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 1.5rem; background-color: #ffffff; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #2c5282; text-align: center;'>ユーザープロファイル</h3>
            <div style='margin-top: 1rem;'>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;'>
                    <span style='color: #666666;'>身長</span>
                    <span style='font-weight: bold;'>{height}cm</span>
                </div>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;'>
                    <span style='color: #666666;'>体重</span>
                    <span style='font-weight: bold;'>{weight}kg</span>
                </div>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;'>
                    <span style='color: #666666;'>年齢</span>
                    <span style='font-weight: bold;'>{age}歳</span>
                </div>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;'>
                    <span style='color: #666666;'>性別</span>
                    <span style='font-weight: bold;'>{gender}</span>
                </div>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0;'>
                    <span style='color: #666666;'>ハンディキャップ</span>
                    <span style='font-weight: bold;'>{handicap}</span>
                </div>
            </div>
        </div>
        """.format(
            height=user_data['height'],
            weight=user_data['weight'],
            age=user_data['age'],
            gender=user_data['gender'],
            handicap=user_data['handicap']
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 1.5rem; background-color: #ffffff; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #2c5282; text-align: center;'>スイングデータ</h3>
            <div style='margin-top: 1rem;'>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;'>
                    <span style='color: #666666;'>ヘッドスピード</span>
                    <span style='font-weight: bold;'>{head_speed}m/s</span>
                </div>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;'>
                    <span style='color: #666666;'>ボールスピード</span>
                    <span style='font-weight: bold;'>{ball_speed}m/s</span>
                </div>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0;'>
                    <span style='color: #666666;'>打ち出し角度</span>
                    <span style='font-weight: bold;'>{launch_angle}°</span>
                </div>
            </div>
        </div>
        """.format(
            head_speed=user_data['head_speed'],
            ball_speed=user_data['ball_speed'],
            launch_angle=user_data['launch_angle']
        ), unsafe_allow_html=True)
    
    # スイングの悩みに基づくアドバイス
    if 'weight_position' in recommendations:
        st.markdown("""
        <div style='margin-top: 2rem; padding: 1.5rem; background-color: #ffffff; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #2c5282; text-align: center;'>スイング改善アドバイス</h3>
            <div style='margin-top: 1rem;'>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;'>
                    <span style='color: #666666;'>現在の悩み</span>
                    <span style='font-weight: bold;'>{swing_issues}</span>
                </div>
                <div style='display: flex; justify-content: space-between; padding: 0.5rem 0;'>
                    <span style='color: #666666;'>推奨される鉛テープの位置</span>
                    <span style='font-weight: bold;'>{weight_position}</span>
                </div>
            </div>
            <div style='text-align: center; margin-top: 1rem;'>
                <img src='https://example.com/weight_position.png' style='width: 300px; border-radius: 8px;'>
            </div>
        </div>
        """.format(
            swing_issues=", ".join(user_data['swing_issues']),
            weight_position=recommendations['weight_position']
        ), unsafe_allow_html=True)

def display_header():
    lang = get_lang()
    header_html = (
        f"<div style='text-align: center; padding: 0 0 0.2em 0; margin-top: 0;'>"
        f"<span class='service-title fadein'>{LANG_DICT[lang]['title']}</span><br/>"
        f"<div class='fadein-img'>"
        f"<img src='https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=800&q=80' class='main-visual' alt='golf visual'>"
        f"</div>"
        # バッジ群
        f"<div class='badge-group'>"
        f"<span class='badge'><i>⛳</i>開発者はゴルフ歴25年</span>"
        f"<span class='badge badge--green'><i>👍</i>プロも納得</span>"
        f"<span class='badge badge--red'><i>⭐</i>累計1,000人が体験</span>"
        f"</div>"
        # ストーリー導入文
        f"<div style='font-size:1.1em;color:#2c5282;font-weight:600;margin-bottom:0.7em;'>あなたのゴルフストーリーが、ここから始まる。</div>"
        # 3ステップ案内
        f"<div class='step-group'>"
        f"<div class='step-card'><div class='step-num'>1</div><div class='step-icon'>📝</div><div class='step-label'>プロフィール入力</div></div>"
        f"<div class='step-card'><div class='step-num'>2</div><div class='step-icon'>🤖</div><div class='step-label'>AIが最適クラブを提案</div></div>"
        f"<div class='step-card'><div class='step-num'>3</div><div class='step-icon'>⛳</div><div class='step-label'>あなたに合ったセット完成！</div></div>"
        f"</div>"
        # 下向き矢印ボタン
        f"<a href='#user_input_form_anchor' style='display:inline-block;margin-top:0.5em;animation:arrow-bounce 1.5s infinite;outline:none;' aria-label='入力フォームへ'>"
        f"<span style='font-size:2.2em;color:#2c5282;'>↓</span>"
        f"</a>"
        f"<style>@keyframes arrow-bounce {{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(12px);}}}}</style>"
        f"</div>"
    )
    st.markdown(header_html, unsafe_allow_html=True)

def generate_dummy_recommendations(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """ダミーの推奨クラブデータを生成"""
    brands = ["Titleist", "Callaway", "TaylorMade", "Mizuno", "Ping"]
    shaft_flexes = ["R", "S", "X"]
    lofts = [9.5, 10.5, 12.0]
    
    # --- 推奨理由を生成 ---
    def make_reason(club_type, brand, model):
        lang = get_lang()
        if lang == 'ja':
            base = f"{brand} {model}は"
            if club_type == 'driver':
                return [f"ヘッドスピード{user_data['head_speed']}m/sに最適", f"スライス傾向の方にもおすすめ"]
            elif club_type == 'wood':
                return [f"高弾道設計で飛距離アップ", f"{user_data['play_frequency']}の方に最適"]
            elif club_type == 'iron':
                return [f"打感重視の方におすすめ", f"ハンディキャップ{user_data['handicap']}向け"]
            elif club_type == 'wedge':
                return [f"スピン性能重視", f"多様なアプローチに対応"]
            elif club_type == 'putter':
                return [f"安定したストロークをサポート"]
        else:
            if club_type == 'driver':
                return [f"Optimal for head speed {user_data['head_speed']} m/s", "Recommended for slicers"]
            elif club_type == 'wood':
                return ["High trajectory for more distance", f"Great for {user_data['play_frequency']}"]
            elif club_type == 'iron':
                return ["Recommended for feel-oriented players", f"For handicap {user_data['handicap']}"]
            elif club_type == 'wedge':
                return ["Spin performance focused", "Versatile for various approaches"]
            elif club_type == 'putter':
                return ["Supports stable putting strokes"]
        return []
    # --- ドライバー ---
    driver = {
        "recommended_models": [{
            "brand": random.choice(brands),
            "model": f"Driver {random.choice(lofts)}°",
            "price": random.randint(40000, 60000),
            "shaft": "Graphite Design",
            "shaft_flex": random.choice(shaft_flexes),
            "features": "低重心設計で高弾道・低スピン",
            "match_reasons": make_reason('driver', brands[0], f"Driver {lofts[0]}")
        }]
    }
    # --- フェアウェイウッド ---
    woods = []
    for loft in [15, 18, 21]:
        woods.append({
            "brand": random.choice(brands),
            "model": f"Fairway Wood {loft}°",
            "price": random.randint(30000, 45000),
            "shaft": "Mitsubishi Chemical",
            "shaft_flex": random.choice(shaft_flexes),
            "loft": loft,
            "features": "高弾道・低スピン設計",
            "match_reasons": make_reason('wood', brands[1], f"Fairway Wood {loft}°")
        })
    # --- アイアン ---
    irons = []
    for num in range(5, 10):
        irons.append({
            "club": f"アイアン{num}",
            "brand": random.choice(brands),
            "model": "Iron Set",
            "price": random.randint(15000, 25000),
            "shaft": "Nippon",
            "shaft_flex": random.choice(shaft_flexes),
            "features": "フォージド設計で優れた打感",
            "match_reasons": make_reason('iron', brands[2], "Iron Set")
        })
    # --- ウェッジ ---
    wedges = []
    for wedge_type in ["ピッチング", "サンド", "ロブ"]:
        wedges.append({
            "club": f"{wedge_type}ウェッジ",
            "brand": random.choice(brands),
            "model": f"{wedge_type} Wedge",
            "price": random.randint(20000, 30000),
            "shaft": "True Temper",
            "shaft_flex": random.choice(shaft_flexes),
            "features": "スピン性能に優れた設計",
            "match_reasons": make_reason('wedge', brands[3], f"{wedge_type} Wedge")
        })
    # --- パター ---
    putter = {
        "brand": random.choice(brands),
        "model": "Mallet Putter",
        "price": random.randint(30000, 40000),
        "features": "安定性に優れたマレット型",
        "match_reasons": make_reason('putter', brands[4], "Mallet Putter")
    }
    
    # 総額計算
    total_price = (
        driver["recommended_models"][0]["price"] +
        sum(wood["price"] for wood in woods) +
        sum(iron["price"] for iron in irons) +
        sum(wedge["price"] for wedge in wedges) +
        putter["price"]
    )
    
    # スイング改善アドバイス
    weight_position = "トゥ側" if "スライス" in user_data["swing_issues"] else "ヒール側"
    
    return {
        "driver": driver,
        "woods": woods,
        "irons": irons,
        "wedges": wedges,
        "putter": putter,
        "total_price": total_price,
        "weight_position": weight_position
    }

# APIエンドポイントの設定
API_BASE_URL = "http://localhost:8000/api"

def get_recommendations(user_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        response = requests.post(f"{API_BASE_URL}/recommend", json=user_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"APIリクエストエラー: {str(e)}")
        return None

def display_user_input_form():
    lang = get_lang()
    st.markdown("<a id='user_input_form_anchor'></a>", unsafe_allow_html=True)
    st.sidebar.markdown("### 開発設定")
    use_dummy_data = st.sidebar.checkbox(LANG_DICT[lang]['use_dummy'], value=True)
    st.sidebar.markdown("<div style='margin-bottom:2em;'></div>", unsafe_allow_html=True)
    
    with st.form("user_input_form"):
        # 基本情報セクション
        st.markdown(f"### {LANG_DICT[lang]['basic_info']}")
        col1, col2, col3 = st.columns(3)
    
        with col1:
            height = st.number_input(
                "Height (cm)" if lang=='en' else "身長 (cm)",
                min_value=140, max_value=220, value=170, key="height"
            )
            age = st.number_input(
                "Age" if lang=='en' else "年齢",
                min_value=10, max_value=100, value=30, key="age"
            )
        
        with col2:
            weight = st.number_input(
                "Weight (kg)" if lang=='en' else "体重 (kg)",
                min_value=30, max_value=150, value=65, key="weight"
            )
            gender = st.selectbox(
                "Gender" if lang=='en' else "性別",
                ["Male", "Female"] if lang=='en' else ["男性", "女性"],
                key="gender"
            )
        
        with col3:
            handicap = st.number_input(
                "Handicap" if lang=='en' else "ハンディキャップ",
                min_value=0, max_value=54, value=20, key="handicap",
                help="例：20（初心者30-54）" if lang=='ja' else "e.g. 20 (beginner: 30-54)"
            )
            golf_years = st.number_input(
                "Golf Experience (years)" if lang=='en' else "ゴルフ歴 (年)",
                min_value=0, max_value=50, value=5, key="golf_years"
            )
        
        # スイング情報セクション
        st.markdown(f"### {LANG_DICT[lang]['swing_info']}")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            head_speed = st.number_input(
                "Head Speed (m/s)" if lang=='en' else "ヘッドスピード (m/s)",
                min_value=20.0, max_value=60.0, value=40.0, step=0.5, key="head_speed",
                help="例：40.0（男性平均40-45）" if lang=='ja' else "e.g. 40.0 (average male: 40-45)"
            )
            play_frequency = st.selectbox(
                "Play Frequency" if lang=='en' else "プレー頻度",
                ["1+ times/week", "2-3 times/month", "1 time/month", "Once every few months"] if lang=='en' else ["週1回以上", "月2-3回", "月1回", "数ヶ月に1回"],
                key="play_frequency"
            )
        
        with col5:
            ball_speed = st.number_input(
                "Ball Speed (m/s)" if lang=='en' else "ボールスピード (m/s)",
                min_value=20.0, max_value=100.0, value=50.0, step=0.5, key="ball_speed"
            )
            swing_issues = st.multiselect(
                "Swing Issues" if lang=='en' else "スイングの悩み",
                ["Slice", "Hook", "Fat", "Top", "Lack of Distance", "Direction"] if lang=='en' else ["スライス", "フック", "ダフリ", "トップ", "飛距離不足", "方向性"],
                key="swing_issues"
            )
        
        with col6:
            launch_angle = st.number_input(
                "Launch Angle (°)" if lang=='en' else "打ち出し角度 (°)",
                min_value=0.0, max_value=60.0, value=15.0, step=0.5, key="launch_angle"
            )
            handedness = st.selectbox(
                "Handedness" if lang=='en' else "利き手",
                ["Right", "Left"] if lang=='en' else ["右", "左"],
                key="handedness"
            )
        
        # 予算設定セクション
        st.markdown(f"### {LANG_DICT[lang]['budget_setting']}")
        budget = st.slider(
            "Budget Range (10,000 JPY)" if lang=='en' else "予算範囲 (万円)",
            min_value=10,
            max_value=50,
            value=30,
            step=5,
            key="budget",
            help="例：30（30万円）" if lang=='ja' else "e.g. 30 (300,000 JPY)"
        )
        
        # 送信ボタン
        submit_button = st.form_submit_button(
            LANG_DICT[lang]['search_btn'],
            use_container_width=True,
            type="primary"
        )
        
        if submit_button:
            # 入力データの収集
            user_data = {
                "height": height,
                "weight": weight,
                "age": age,
                "gender": gender,
                "handicap": handicap,
                "golf_years": golf_years,
                "head_speed": head_speed,
                "ball_speed": ball_speed,
                "launch_angle": launch_angle,
                "swing_issues": swing_issues,
                "play_frequency": play_frequency,
                "handedness": handedness,
                "budget": budget * 10000  # 万円から円に変換
            }
            # API呼び出しまたはダミーデータ生成
            with st.spinner("Searching for the best clubs..." if lang=='en' else "最適なクラブを検索中..."):
                if use_dummy_data:
                    recommendations = generate_dummy_recommendations(user_data)
                    st.sidebar.info(LANG_DICT[lang]['using_dummy'])
                else:
                    try:
                        response = requests.post(
                            "http://localhost:8000/api/recommend",
                            json=user_data
                        )
                        response.raise_for_status()
                        recommendations = response.json()
                        st.sidebar.success("Using production API" if lang=='en' else "本番APIを使用中")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error: {str(e)}" if lang=='en' else f"エラーが発生しました: {str(e)}")
                        st.error("API server may not be running." if lang=='en' else "APIサーバーが起動していない可能性があります。")
                        return
            # 結果の表示
            st.session_state['recommendations'] = recommendations
            st.session_state['user_data'] = user_data

def sidebar_quick_guide_and_changelog():
    lang = get_lang()
    # 更新履歴セクションを一時的に非表示に
    return

def main():
    set_custom_theme()
    set_lang()
    sidebar_quick_guide_and_changelog()
    display_header()

    # ユーザー入力フォームを表示
    display_user_input_form()

    # 推奨クラブ・価格比較・分析結果を順番に表示
    if "recommendations" in st.session_state:
        display_club_summary(st.session_state.recommendations)
        display_price_comparison(st.session_state.recommendations)
    if "recommendations" in st.session_state and "user_data" in st.session_state:
        display_fitting_analysis(st.session_state.user_data, st.session_state.recommendations)

if __name__ == "__main__":
    main() 