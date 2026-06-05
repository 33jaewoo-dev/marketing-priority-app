import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Inbound Marketing Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 커스텀 CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* 전체 배경 */
.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background: #0f1420 !important;
    border-right: 1px solid #1e2640;
}
section[data-testid="stSidebar"] * {
    color: #c8ccd8 !important;
}

/* 헤더 타이포 */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

/* 메트릭 카드 */
.metric-card {
    background: linear-gradient(135deg, #141928 0%, #1a2035 100%);
    border: 1px solid #252d45;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #3d4f7c; }

/* Priority 배지 */
.badge-high {
    background: linear-gradient(135deg, #ff4b4b22, #ff6b6b11);
    border: 1px solid #ff4b4b66;
    color: #ff6b6b;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.05em;
}
.badge-medium {
    background: linear-gradient(135deg, #ffaa0022, #ffcc0011);
    border: 1px solid #ffaa0066;
    color: #ffcc00;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.05em;
}
.badge-low {
    background: linear-gradient(135deg, #4488ff22, #6699ff11);
    border: 1px solid #4488ff66;
    color: #6699ff;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.05em;
}

/* 국가 카드 */
.country-card {
    background: linear-gradient(135deg, #141928, #1a2035);
    border: 1px solid #252d45;
    border-radius: 20px;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.country-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 20px 20px 0 0;
}
.country-card.high::before { background: linear-gradient(90deg, #ff4b4b, #ff8888); }
.country-card.medium::before { background: linear-gradient(90deg, #ffaa00, #ffdd66); }
.country-card.low::before { background: linear-gradient(90deg, #4488ff, #88bbff); }

/* 인사이트 박스 */
.insight-box {
    background: #141928;
    border-left: 3px solid #3d6fff;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 8px 0;
}

/* 결과 카드 */
.result-card {
    border-radius: 20px;
    padding: 32px;
    text-align: center;
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #3d6fff, #5580ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 14px 28px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px #3d6fff44 !important;
}

/* selectbox, number_input */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #141928 !important;
    border: 1px solid #252d45 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
}

/* 구분선 */
hr { border-color: #1e2640 !important; }

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: #0f1420;
    border-radius: 12px;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8890a8;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: #1a2035 !important;
    color: #e8eaf0 !important;
}

/* 데이터프레임 */
.stDataFrame { background: #141928; border-radius: 12px; }

/* 슬라이더 */
.stSlider > div > div { background: #252d45 !important; }

/* 섹션 타이틀 */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #5a6280;
    text-transform: uppercase;
    margin-bottom: 16px;
    margin-top: 8px;
}

/* 수치 강조 */
.big-number {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
}

.signal-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #1e2640;
    font-size: 14px;
}
.signal-label { color: #8890a8; }
.signal-value { font-weight: 600; font-family: 'Syne', sans-serif; }
.signal-up { color: #4dff91; }
.signal-down { color: #ff4b4b; }
.signal-neutral { color: #ffcc00; }
</style>
""", unsafe_allow_html=True)

# ── 상수 ──────────────────────────────────────────────────────────
FLAGS = {'중국': '🇨🇳', '일본': '🇯🇵', '대만': '🇹🇼', '미국': '🇺🇸', '홍콩': '🇭🇰'}
COUNTRY_EN = {'중국': 'China', '일본': 'Japan', '대만': 'Taiwan', '미국': 'USA', '홍콩': 'Hong Kong'}
PRIORITY_COLOR = {'High': '#ff4b4b', 'Medium': '#ffaa00', 'Low': '#4488ff'}
PRIORITY_EMOJI = {'High': '🔴', 'Medium': '🟡', 'Low': '🔵'}
PRIORITY_CSS = {'High': 'high', 'Medium': 'medium', 'Low': 'low'}

# ── 데이터/모델 로드 ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    import numpy as np

    base = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base, 'full_dataset.csv'), encoding='utf-8', dtype={'year_month': str})

    feature_cols = [
        'visitor_count','visitor_lag1','visitor_lag2','visitor_lag3',
        'visitor_mom_growth','visitor_3m_avg','visitor_6m_avg',
        'visitor_vs_3m_avg','visitor_rolling_std','country_share',
        'buzz_volume','engagement','potential_exposure',
        'buzz_mom_growth','engagement_mom_growth','exposure_mom_growth',
        'engagement_per_visitor','buzz_per_visitor','buzz_vs_3m_avg',
        'positive_pct','negative_pct',
        'hallyu_spend_count','hallyu_mom_growth','hallyu_per_visitor',
        'month','quarter','is_peak_season','exchange_rate','oil_price',
    ]

    df_clean = df[feature_cols + ['priority_label']].dropna()
    X = df_clean[feature_cols]
    y = df_clean['priority_label']

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight='balanced')
    model.fit(X, y_enc)

    feat_imp = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    return model, le, feature_cols, feat_imp

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base, 'full_dataset.csv'), encoding='utf-8', dtype={'year_month': str})
    sat = pd.read_csv(os.path.join(base, 'satisfaction_data.csv'), encoding='utf-8')
    hallyu = pd.read_csv(os.path.join(base, 'hallyu_spending.csv'), encoding='utf-8', dtype={'year_month': str})
    hallyu_ind = pd.read_csv(os.path.join(base, 'hallyu_industry.csv'), encoding='utf-8', dtype={'year_month': str})
    df['year_month'] = df['year_month'].astype(str).str.strip()
    return df, sat, hallyu, hallyu_ind

model, le, feature_cols, feat_imp = load_model()
df, sat_df, hallyu_df, hallyu_ind_df = load_data()

# ── 사이드바 ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 24px 0;">
        <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:800;
                    color:#0f172a; letter-spacing:-0.02em; line-height:1.2;">
            Inbound Marketing<br/>
            <span style="color:#3b82f6;">Intelligence</span>
        </div>
        <div style="font-size:11px; color:#94a3b8; margin-top:6px; letter-spacing:0.08em; text-transform:uppercase;">
            Korea Tourism AI Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    page = st.radio("", [
        "📊  Overview",
        "🔮  Priority Engine",
        "👤  Market Profiles",
        "📈  Analytics"
    ], label_visibility="collapsed")

    st.markdown("---")
    latest_month = df['year_month'].max()
    ym_disp = f"{str(latest_month)[:4]}.{str(latest_month)[4:]}"
    st.markdown(f"""
    <div style="font-size:11px; color:#5a6280; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:8px;">
        Latest Data
    </div>
    <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:700; color:#e8eaf0;">
        {ym_disp}
    </div>
    <div style="font-size:12px; color:#5a6280; margin-top:4px;">Korea Tourism Datalab</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px; color:#5a6280; line-height:1.8;">
        <b style="color:#8890a8;">Model</b><br/>Random Forest · 74% Acc<br/><br/>
        <b style="color:#8890a8;">Data Sources</b><br/>
        KTO Visitor Stats<br/>SNS Buzz & Engagement<br/>Hallyu Spending Index<br/><br/>
        <b style="color:#8890a8;">Countries</b><br/>
        🇨🇳 🇯🇵 🇹🇼 🇺🇸 🇭🇰
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page == "📊  Overview":
    st.markdown("""
    <h1 style="font-family:'Syne',sans-serif; font-size:32px; font-weight:800;
               color:#e8eaf0; letter-spacing:-0.03em; margin-bottom:4px;">
        Inbound Marketing Intelligence
    </h1>
    <p style="color:#5a6280; font-size:15px; margin-bottom:32px;">
        방한 외국인 빅데이터 기반 실시간 마케팅 우선순위 추천 시스템
    </p>
    """, unsafe_allow_html=True)

    # 최신 월 우선순위 카드
    latest = df[df['year_month'] == latest_month].copy()
    latest_sorted = latest.sort_values('priority_score', ascending=False)

    st.markdown('<div class="section-title">Current Priority Ranking</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (_, row) in enumerate(latest_sorted.iterrows()):
        label = row.get('priority_label', 'N/A')
        color = PRIORITY_COLOR.get(label, '#888')
        css_cls = PRIORITY_CSS.get(label, 'low')
        flag = FLAGS.get(row['country'], '')
        cname = COUNTRY_EN.get(row['country'], row['country'])
        rank_label = ['1st', '2nd', '3rd', '4th', '5th'][i]
        with cols[i]:
            st.markdown(f"""
            <div class="country-card {css_cls}">
                <div style="font-size:11px; color:#5a6280; letter-spacing:0.1em;
                            text-transform:uppercase; margin-bottom:8px;">{rank_label}</div>
                <div style="font-size:36px; margin-bottom:6px;">{flag}</div>
                <div style="font-family:'Syne',sans-serif; font-size:16px; font-weight:700;
                            color:#e8eaf0; margin-bottom:10px;">{cname}</div>
                <span class="badge-{label.lower()}">{label}</span>
                <div style="margin-top:12px; padding-top:12px; border-top:1px solid #252d45;">
                    <div style="font-size:11px; color:#5a6280;">Score</div>
                    <div style="font-family:'Syne',sans-serif; font-size:20px;
                                font-weight:700; color:{color};">{row['priority_score']:.3f}</div>
                </div>
                <div style="margin-top:8px;">
                    <div style="font-size:11px; color:#5a6280;">Visitors</div>
                    <div style="font-size:13px; font-weight:500; color:#c8ccd8;">{int(row['visitor_count']):,}</div>
                </div>
                <div style="margin-top:6px;">
                    <div style="font-size:11px; color:#5a6280;">MoM Growth</div>
                    <div style="font-size:13px; font-weight:600; color:{'#4dff91' if row.get('visitor_mom_growth',0)>0 else '#ff4b4b'};">
                        {'+' if row.get('visitor_mom_growth',0)>0 else ''}{row.get('visitor_mom_growth',0)*100:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # 차트 섹션
    df_plot = df.copy()
    df_plot['date_str'] = df_plot['year_month'].astype(str).apply(lambda x: f"{x[:4]}-{x[4:]}")

    CHART_TEMPLATE = dict(
        template='plotly_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(248,250,252,0.8)',
        font=dict(family='DM Sans', color='#64748b'),
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=12)),
        xaxis=dict(gridcolor='#e2e8f0', linecolor='#e2e8f0'),
        yaxis=dict(gridcolor='#e2e8f0', linecolor='#e2e8f0'),
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Monthly Visitor Trends</div>', unsafe_allow_html=True)
        fig = px.line(df_plot, x='date_str', y='visitor_count', color='country',
                      color_discrete_sequence=['#3d6fff','#ff4b4b','#4dff91','#ffaa00','#cc44ff'],
                      labels={'visitor_count':'Visitors','date_str':'','country':''})
        fig.update_layout(height=300, **CHART_TEMPLATE)
        fig.update_traces(line=dict(width=2))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">SNS Engagement Trends</div>', unsafe_allow_html=True)
        fig2 = px.line(df_plot, x='date_str', y='engagement', color='country',
                       color_discrete_sequence=['#3d6fff','#ff4b4b','#4dff91','#ffaa00','#cc44ff'],
                       labels={'engagement':'Engagement','date_str':'','country':''})
        fig2.update_layout(height=300, **CHART_TEMPLATE)
        fig2.update_traces(line=dict(width=2))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">Positive Sentiment Trends</div>', unsafe_allow_html=True)
        fig3 = px.line(df_plot, x='date_str', y='positive_pct', color='country',
                       color_discrete_sequence=['#3d6fff','#ff4b4b','#4dff91','#ffaa00','#cc44ff'],
                       labels={'positive_pct':'Positive Sentiment (%)','date_str':'','country':''})
        fig3.update_layout(height=280, **CHART_TEMPLATE)
        fig3.add_hline(y=55, line_dash='dash', line_color='#5a6280', annotation_text='Neutral threshold')
        fig3.update_traces(line=dict(width=2))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">AI Model — Feature Importance</div>', unsafe_allow_html=True)
        feat_disp = feat_imp.head(10).copy()
        feat_disp['feature'] = feat_disp['feature'].str.replace('_', ' ').str.title()
        fig4 = px.bar(feat_disp, x='importance', y='feature', orientation='h',
                      color='importance', color_continuous_scale=['#dbeafe','#3b82f6','#1d4ed8'])
        fig4.update_layout(height=280, showlegend=False, coloraxis_showscale=False, **CHART_TEMPLATE)
        fig4.update_yaxes(categoryorder='total ascending', gridcolor='#e8eaf0')
        st.plotly_chart(fig4, use_container_width=True)

    # 모델 성능 요약
    st.markdown('<div class="section-title">Model Performance</div>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    for col, label, value, sub in [
        (m1, "Algorithm", "Random Forest", "200 estimators"),
        (m2, "Accuracy", "74.0%", "Test set (80/20)"),
        (m3, "High Precision", "82%", "F1: 0.86"),
        (m4, "Training Data", "336 samples", "2018.11 ~ 2025.08"),
        (m5, "Features", "29 variables", "Visitor + SNS + Hallyu"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:11px; color:#94a3b8; letter-spacing:0.1em;
                            text-transform:uppercase; margin-bottom:8px;">{label}</div>
                <div style="font-family:'Syne',sans-serif; font-size:20px;
                            font-weight:700; color:#0f172a;">{value}</div>
                <div style="font-size:12px; color:#64748b; margin-top:4px;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 2: PRIORITY ENGINE
# ══════════════════════════════════════════════════════════════════
elif page == "🔮  Priority Engine":
    st.markdown("""
    <h1 style="font-family:'Syne',sans-serif; font-size:32px; font-weight:800;
               color:#e8eaf0; letter-spacing:-0.03em; margin-bottom:4px;">
        Priority Engine
    </h1>
    <p style="color:#5a6280; font-size:15px; margin-bottom:32px;">
        국가별 최신 지표를 입력하여 마케팅 우선순위와 전략적 액션을 도출합니다
    </p>
    """, unsafe_allow_html=True)

    country_sel = st.selectbox(
        "분석 대상 국가",
        ['중국', '일본', '대만', '미국', '홍콩'],
        format_func=lambda x: f"{FLAGS[x]}  {COUNTRY_EN[x]} ({x})"
    )

    country_data = df[df['country'] == country_sel].sort_values('year_month').iloc[-1]

    st.markdown("<br/>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🧳  방문객 지표", "📱  SNS 지표", "⚙️  거시환경 지표"])

    with tab1:
        st.markdown('<div class="section-title">Visitor Statistics</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            visitor_count = st.number_input("이번 달 방문객 수", value=int(country_data['visitor_count']), step=1000, help="해당 월 실제 입국자 수")
            visitor_lag1 = st.number_input("전월 방문객 수", value=int(country_data['visitor_lag1']), step=1000)
        with c2:
            visitor_lag2 = st.number_input("2개월 전 방문객", value=int(country_data['visitor_lag2']), step=1000)
            visitor_lag3 = st.number_input("3개월 전 방문객", value=int(country_data['visitor_lag3']), step=1000)
        with c3:
            visitor_3m_avg = st.number_input("3개월 이동평균", value=float(country_data['visitor_3m_avg']), step=1000.0)
            visitor_6m_avg = st.number_input("6개월 이동평균", value=float(country_data['visitor_6m_avg']), step=1000.0)
        country_share = st.number_input(
            "전체 방한객 중 해당국 비율 (0~1)",
            value=float(country_data['country_share']), step=0.001, format="%.4f",
            help="해당 국가 방문객 / 전체 5개국 방문객 합계"
        )

    with tab2:
        st.markdown('<div class="section-title">SNS Buzz & Engagement</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            buzz_volume = st.number_input("버즈 볼륨 (SNS 언급 건수)", value=int(country_data['buzz_volume']), step=100,
                                          help="해당 국가의 한국 관광 관련 SNS 언급량")
            engagement = st.number_input("인게이지먼트 (좋아요·댓글·공유)", value=int(country_data['engagement']), step=1000,
                                         help="SNS 게시물에 대한 총 반응 수")
        with c2:
            potential_exposure = st.number_input("잠재 노출량 (팔로워 합산)", value=int(country_data['potential_exposure']), step=10000,
                                                  help="게시물 작성자들의 팔로워 합산 수치")
            positive_pct = st.slider(
                "긍정 감성 비율 (%)",
                min_value=0.0, max_value=100.0,
                value=float(country_data['positive_pct']),
                step=0.5,
                help="한국 관광 관련 SNS 게시물 중 긍정적 내용의 비율. 40% 미만 시 심각한 페널티 부여 (외교 이슈, 부정 여론 등)"
            )
            negative_pct = 100.0 - positive_pct

        # 감성 경고
        if positive_pct < 40:
            st.error("⚠️ 긍정 감성이 40% 미만입니다. 외교 이슈 또는 심각한 부정 여론이 의심됩니다. 우선순위 점수에 50% 페널티가 적용됩니다.")
        elif positive_pct < 55:
            st.warning("⚠️ 긍정 감성이 불안정합니다. 우선순위 점수에 25% 페널티가 적용됩니다.")

    with tab3:
        st.markdown('<div class="section-title">Macroeconomic Indicators</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            month = st.selectbox("기준 월", list(range(1, 13)),
                                  index=int(country_data['month']) - 1,
                                  help="3·4·5·9·10월은 성수기 보너스 적용")
        with c2:
            exchange_rate = st.number_input("환율 (원화 기준)", value=float(country_data['exchange_rate']), step=1.0,
                                             help="원화 약세(높은 환율) 시 외국인 방한 비용 감소 → 소폭 보너스 적용")
        with c3:
            oil_price = st.number_input("유가 (USD/배럴)", value=float(country_data['oil_price']), step=1.0,
                                         help="항공 운임과 연계. 고유가 시 방한 비용 증가")

    # ── 파생변수 자동 계산 ─────────────────────────────────────
    visitor_mom_growth = (visitor_count - visitor_lag1) / visitor_lag1 if visitor_lag1 != 0 else 0
    visitor_vs_3m_avg = visitor_count / visitor_3m_avg if visitor_3m_avg != 0 else 1
    visitor_rolling_std = float(country_data.get('visitor_rolling_std', 0) or 0)
    buzz_lag1 = float(country_data.get('buzz_lag1', buzz_volume) or buzz_volume)
    engagement_lag1 = float(country_data.get('engagement_lag1', engagement) or engagement)
    exposure_lag1 = float(country_data.get('exposure_lag1', potential_exposure) or potential_exposure)
    buzz_mom_growth = (buzz_volume - buzz_lag1) / buzz_lag1 if buzz_lag1 != 0 else 0
    engagement_mom_growth = (engagement - engagement_lag1) / engagement_lag1 if engagement_lag1 != 0 else 0
    exposure_mom_growth = (potential_exposure - exposure_lag1) / exposure_lag1 if exposure_lag1 != 0 else 0
    engagement_per_visitor = engagement / visitor_count if visitor_count != 0 else 0
    buzz_per_visitor = buzz_volume / visitor_count if visitor_count != 0 else 0
    buzz_3m_avg = float(country_data.get('buzz_3m_avg', buzz_volume) or buzz_volume)
    buzz_vs_3m_avg = buzz_volume / buzz_3m_avg if buzz_3m_avg != 0 else 1
    quarter = (month - 1) // 3 + 1
    is_peak_season = 1 if month in [3, 4, 5, 9, 10] else 0
    hallyu_count = float(country_data.get('hallyu_spend_count', 0) or 0)
    hallyu_lag1_val = float(country_data.get('hallyu_lag1', hallyu_count) or hallyu_count)
    hallyu_mom = (hallyu_count - hallyu_lag1_val) / hallyu_lag1_val if hallyu_lag1_val != 0 else 0
    hallyu_per_v = hallyu_count / visitor_count if visitor_count != 0 else 0

    input_data = {
        'visitor_count': visitor_count, 'visitor_lag1': visitor_lag1,
        'visitor_lag2': visitor_lag2, 'visitor_lag3': visitor_lag3,
        'visitor_mom_growth': visitor_mom_growth, 'visitor_3m_avg': visitor_3m_avg,
        'visitor_6m_avg': visitor_6m_avg, 'visitor_vs_3m_avg': visitor_vs_3m_avg,
        'visitor_rolling_std': visitor_rolling_std, 'country_share': country_share,
        'buzz_volume': buzz_volume, 'engagement': engagement,
        'potential_exposure': potential_exposure,
        'buzz_mom_growth': buzz_mom_growth, 'engagement_mom_growth': engagement_mom_growth,
        'exposure_mom_growth': exposure_mom_growth,
        'engagement_per_visitor': engagement_per_visitor, 'buzz_per_visitor': buzz_per_visitor,
        'buzz_vs_3m_avg': buzz_vs_3m_avg,
        'positive_pct': positive_pct, 'negative_pct': negative_pct,
        'hallyu_spend_count': hallyu_count, 'hallyu_mom_growth': hallyu_mom,
        'hallyu_per_visitor': hallyu_per_v,
        'month': month, 'quarter': quarter, 'is_peak_season': is_peak_season,
        'exchange_rate': exchange_rate, 'oil_price': oil_price,
    }

    st.markdown("<br/>", unsafe_allow_html=True)

    if st.button("🔮  우선순위 분석 실행", use_container_width=True):
        input_df = pd.DataFrame([input_data])
        for col in feature_cols:
            if col not in input_df.columns:
                input_df[col] = 0
        X_input = input_df[feature_cols]

        pred = model.predict(X_input)[0]
        proba = model.predict_proba(X_input)[0]
        label = le.inverse_transform([pred])[0]
        color = PRIORITY_COLOR[label]
        flag = FLAGS[country_sel]
        cname = COUNTRY_EN[country_sel]

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Analysis Results</div>', unsafe_allow_html=True)

        res1, res2, res3 = st.columns([1.2, 1, 1.2])

        # 결과 카드
        with res1:
            border_style = f"border: 2px solid {color}44; border-top: 4px solid {color};"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #141928, #1a2035);
                        {border_style} border-radius: 20px; padding: 36px 24px; text-align: center;">
                <div style="font-size:56px; margin-bottom:12px;">{flag}</div>
                <div style="font-family:'Syne',sans-serif; font-size:22px; font-weight:700;
                            color:#e8eaf0; margin-bottom:16px;">{cname}</div>
                <span class="badge-{label.lower()}" style="font-size:16px; padding:8px 24px;">
                    {label} Priority
                </span>
                <div style="margin-top:20px; font-family:'Syne',sans-serif;
                            font-size:42px; font-weight:800; color:{color}; letter-spacing:-0.04em;">
                    {max(proba)*100:.0f}%
                </div>
                <div style="font-size:12px; color:#5a6280; margin-top:4px;">Model Confidence</div>
                <div style="margin-top:20px; padding-top:16px; border-top:1px solid #252d45;">
                    {'⚠️ 성수기 보너스 적용' if is_peak_season else ''}
                    {'<br/>🔴 감성 페널티 적용' if positive_pct < 55 else ''}
                    {'<br/>🔴 급락 충격 감지' if visitor_mom_growth < -0.15 else ''}
                    {'&nbsp;' if is_peak_season==0 and positive_pct >= 55 and visitor_mom_growth >= -0.15 else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 신호 분석 (Signal Analysis)
        with res2:
            st.markdown("""
            <div style="font-family:'Syne',sans-serif; font-size:13px; font-weight:700;
                        color:#5a6280; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:16px;">
                Signal Analysis
            </div>
            <div style="font-size:11px; color:#5a6280; margin-bottom:12px;">
                모델이 우선순위 판단에 활용한 핵심 지표들의 현재 상태입니다.
                각 신호는 전월 대비 방향성과 수치를 나타냅니다.
            </div>
            """, unsafe_allow_html=True)

            def sig_cls(val, threshold=0.05):
                if val > threshold: return "signal-up", "▲"
                elif val < -threshold: return "signal-down", "▼"
                else: return "signal-neutral", "━"

            signals = [
                ("방문객 증감률", visitor_mom_growth, "전월 대비 방문객 변화율", True, 0.05),
                ("버즈 증감률", buzz_mom_growth, "SNS 언급량 전월 대비 변화", True, 0.05),
                ("인게이지먼트 증감", engagement_mom_growth, "SNS 반응 전월 대비 변화", True, 0.05),
                ("3개월 평균 대비", visitor_vs_3m_avg - 1, "현재 방문객이 3개월 평균보다 높으면 ▲", True, 0.05),
                ("긍정 감성", (positive_pct - 55) / 100, f"현재 {positive_pct:.1f}% (기준선 55%)", True, 0),
                ("국가 점유율", (country_share - 0.2) / 0.2, f"현재 {country_share*100:.1f}%", True, 0),
            ]

            html_signals = ""
            for name, val, desc, _, thresh in signals:
                cls, arrow = sig_cls(val, thresh)
                display_val = f"{val*100:+.1f}%" if name not in ["긍정 감성", "국가 점유율"] else f"{'+' if val>0 else ''}{val*100:.1f}%"
                if name == "긍정 감성":
                    display_val = f"{positive_pct:.1f}%"
                elif name == "국가 점유율":
                    display_val = f"{country_share*100:.1f}%"
                html_signals += f"""
                <div class="signal-row">
                    <div>
                        <div class="signal-label">{name}</div>
                        <div style="font-size:10px; color:#3a4260;">{desc}</div>
                    </div>
                    <div class="signal-value {cls}">{arrow} {display_val}</div>
                </div>
                """
            st.markdown(html_signals, unsafe_allow_html=True)

            # Confidence breakdown
            st.markdown("<br/>", unsafe_allow_html=True)
            for cls_name, prob in zip(le.classes_, proba):
                c = PRIORITY_COLOR[cls_name]
                pct = int(prob * 100)
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <div style="width:70px; font-size:12px; color:#8890a8;">{cls_name}</div>
                    <div style="flex:1; background:#1a2035; border-radius:4px; height:6px; overflow:hidden;">
                        <div style="width:{pct}%; height:100%; background:{c}; border-radius:4px;"></div>
                    </div>
                    <div style="width:40px; text-align:right; font-size:12px;
                                font-family:'Syne',sans-serif; font-weight:600; color:{c};">{pct}%</div>
                </div>
                """, unsafe_allow_html=True)

        # 전략적 권고안
        with res3:
            st.markdown("""
            <div style="font-family:'Syne',sans-serif; font-size:13px; font-weight:700;
                        color:#5a6280; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:16px;">
                Strategic Recommendations
            </div>
            """, unsafe_allow_html=True)

            # 상황별 맞춤 액션 생성
            actions_by_label = {
                'High': {
                    'headline': '적극적 공세 전략',
                    'desc': '방문객 규모와 SNS 관심도가 모두 높아 최우선 공략 시장입니다.',
                    'budget': '예산 상향 배정 권고',
                    'actions': [
                        ("예산 확대", f"{cname} 전용 광고 예산을 전월 대비 20~30% 확대하세요."),
                        ("현지 언어 캠페인", f"{flag} 현지 언어 콘텐츠 제작 및 인플루언서 협업을 강화하세요."),
                        ("채널 집중", "가장 버즈가 높은 SNS 채널에 리소스를 집중 투입하세요."),
                        ("프로모션 런칭", f"{cname} 타겟 한정 프로모션(할인·패키지)을 즉시 런칭하세요."),
                    ]
                },
                'Medium': {
                    'headline': '유지 및 모니터링 전략',
                    'desc': '현재 중간 수준이나 상승 가능성이 있어 주시가 필요한 시장입니다.',
                    'budget': '현행 예산 유지',
                    'actions': [
                        ("현행 유지", "현재 캠페인 규모를 유지하되 성과 지표를 주간 단위로 모니터링하세요."),
                        ("테스트 캠페인", "소규모 A/B 테스트로 반응률이 높은 메시지를 탐색하세요."),
                        ("트리거 설정", "방문객 증가율 +15% 초과 시 즉시 High 전략으로 전환하세요."),
                        ("콘텐츠 최적화", "기존 콘텐츠 중 인게이지먼트 상위 20% 포맷을 확대 운영하세요."),
                    ]
                },
                'Low': {
                    'headline': '관망 및 리소스 재배분 전략',
                    'desc': '현재 방문객 및 SNS 지표가 낮아 타 시장에 리소스를 집중하는 것이 효율적입니다.',
                    'budget': '예산 최소화 권고',
                    'actions': [
                        ("예산 절감", f"{cname} 마케팅 예산을 High 우선순위 국가로 재배분하세요."),
                        ("원인 분석", "방문객 감소 또는 부정 감성의 근본 원인을 분석하세요."),
                        ("회복 모니터링", "MoM 성장률이 +10% 이상 회복 시 Medium 전략으로 전환하세요."),
                        ("리텐션 집중", "신규 유입보다 기존 방문 경험자 재방문 유도 프로그램을 운영하세요."),
                    ]
                }
            }

            # 감성 낮을 때 경고 액션 추가
            extra_actions = []
            if positive_pct < 40:
                extra_actions.append(("🚨 위기 대응", "부정 여론 원인을 즉시 파악하고 위기 커뮤니케이션 팀을 가동하세요."))
            if visitor_mom_growth < -0.3:
                extra_actions.append(("🚨 급락 대응", "방문객 급감 원인(외교·항공·이슈)을 조사하고 관계 부처와 협의하세요."))
            if is_peak_season:
                extra_actions.append(("✨ 성수기 활용", f"현재 성수기({month}월)입니다. 캠페인 집행 타이밍을 지금 잡으세요."))

            rec = actions_by_label[label]

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}11, {color}08);
                        border: 1px solid {color}33; border-radius: 16px; padding: 20px; margin-bottom: 16px;">
                <div style="font-family:'Syne',sans-serif; font-size:16px; font-weight:700;
                            color:{color}; margin-bottom:6px;">{rec['headline']}</div>
                <div style="font-size:13px; color:#8890a8; line-height:1.5;">{rec['desc']}</div>
                <div style="margin-top:10px; padding: 6px 12px; background:{color}22;
                            border-radius:8px; display:inline-block; font-size:12px;
                            font-weight:600; color:{color};">{rec['budget']}</div>
            </div>
            """, unsafe_allow_html=True)

            all_actions = rec['actions'] + extra_actions
            for title, desc in all_actions:
                icon = "✅" if label == 'High' else ("🔄" if label == 'Medium' else "⏸️")
                if title.startswith("🚨") or title.startswith("✨"):
                    icon = title[:2]
                    title = title[2:].strip()
                st.markdown(f"""
                <div style="background:#141928; border-radius:10px; padding:12px 16px; margin-bottom:8px;
                            border-left: 3px solid {color}66;">
                    <div style="font-size:13px; font-weight:600; color:#e8eaf0; margin-bottom:4px;">
                        {icon} {title}
                    </div>
                    <div style="font-size:12px; color:#8890a8; line-height:1.5;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 3: MARKET PROFILES
# ══════════════════════════════════════════════════════════════════
elif page == "👤  Market Profiles":
    st.markdown("""
    <h1 style="font-family:'Syne',sans-serif; font-size:32px; font-weight:800;
               color:#e8eaf0; letter-spacing:-0.03em; margin-bottom:4px;">
        Market Profiles
    </h1>
    <p style="color:#5a6280; font-size:15px; margin-bottom:32px;">
        국가별 방한 관광객 행태·만족도·한류 소비 심층 분석 (2015~2024)
    </p>
    """, unsafe_allow_html=True)

    CHART_TEMPLATE = dict(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(20,25,40,0.5)',
        font=dict(family='DM Sans', color='#8890a8'),
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(gridcolor='#1e2640'),
        yaxis=dict(gridcolor='#1e2640'),
    )
    COLORS = ['#3d6fff','#ff4b4b','#4dff91','#ffaa00','#cc44ff']

    # 최신연도 프로파일 카드
    latest_year = sat_df['year'].max()
    latest_sat = sat_df[sat_df['year'] == latest_year].copy()

    st.markdown(f'<div class="section-title">Traveler Profile Summary — {latest_year}</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, country in enumerate(['중국', '일본', '대만', '미국', '홍콩']):
        row = latest_sat[latest_sat['country'] == country]
        if row.empty: continue
        row = row.iloc[0]
        with cols[i]:
            st.markdown(f"""
            <div class="country-card" style="border-top: 3px solid {COLORS[i]};">
                <div style="font-size:36px; margin-bottom:8px;">{FLAGS[country]}</div>
                <div style="font-family:'Syne',sans-serif; font-size:15px; font-weight:700;
                            color:#e8eaf0; margin-bottom:14px;">{COUNTRY_EN[country]}</div>
                <div style="text-align:left;">
                    <div style="display:flex; justify-content:space-between; padding:6px 0;
                                border-bottom:1px solid #1e2640; font-size:12px;">
                        <span style="color:#5a6280;">1인 지출</span>
                        <span style="font-weight:600; color:#e8eaf0;">${row['spend_per_person_usd']:,.0f}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0;
                                border-bottom:1px solid #1e2640; font-size:12px;">
                        <span style="color:#5a6280;">체재 기간</span>
                        <span style="font-weight:600; color:#e8eaf0;">{row['stay_days']}일</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0;
                                border-bottom:1px solid #1e2640; font-size:12px;">
                        <span style="color:#5a6280;">재방문율</span>
                        <span style="font-weight:600; color:{COLORS[i]};">{row['revisit_rate']}%</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0;
                                border-bottom:1px solid #1e2640; font-size:12px;">
                        <span style="color:#5a6280;">만족도</span>
                        <span style="font-weight:600; color:#4dff91;">{row['overall_satisfaction']}%</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0; font-size:12px;">
                        <span style="color:#5a6280;">추천 의향</span>
                        <span style="font-weight:600; color:#e8eaf0;">{row['recommend_intention']}%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    sat_df['date_str'] = sat_df['year'].astype(str)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">1인 평균 지출 경비 (USD)</div>', unsafe_allow_html=True)
        fig = px.line(sat_df, x='date_str', y='spend_per_person_usd', color='country',
                      color_discrete_sequence=COLORS, markers=True,
                      labels={'spend_per_person_usd':'USD','date_str':'','country':''})
        fig.update_layout(height=280, **CHART_TEMPLATE)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">재방문율 추이 (%)</div>', unsafe_allow_html=True)
        fig = px.line(sat_df, x='date_str', y='revisit_rate', color='country',
                      color_discrete_sequence=COLORS, markers=True,
                      labels={'revisit_rate':'%','date_str':'','country':''})
        fig.update_layout(height=280, **CHART_TEMPLATE)
        st.plotly_chart(fig, use_container_width=True)

    # 한류 소비 분석
    st.markdown('<div class="section-title">Hallyu Spending Index</div>', unsafe_allow_html=True)
    hallyu_plot = hallyu_df.copy()
    hallyu_plot['date_str'] = hallyu_plot['year_month'].astype(str).apply(lambda x: f"{x[:4]}-{x[4:]}")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">한류 총 소비건수 추이</div>', unsafe_allow_html=True)
        fig = px.line(hallyu_plot, x='date_str', y='total_count', color='country',
                      color_discrete_sequence=COLORS,
                      labels={'total_count':'소비건수','date_str':'','country':''})
        fig.update_layout(height=280, **CHART_TEMPLATE)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">업종별 한류 소비 비율 (최신)</div>', unsafe_allow_html=True)
        latest_ym = hallyu_ind_df['year_month'].max()
        latest_ind = hallyu_ind_df[hallyu_ind_df['year_month'] == latest_ym].copy()
        latest_ind['country_en'] = latest_ind['country'].map(COUNTRY_EN)
        fig = px.bar(latest_ind, x='country_en', y='ratio', color='industry',
                     barmode='stack',
                     color_discrete_sequence=['#3d6fff','#ff4b4b','#4dff91','#ffaa00',
                                              '#cc44ff','#ff6644','#44ddff','#ffdd44','#88ff44'],
                     labels={'ratio':'비율(%)','country_en':'','industry':''})
        fig.update_layout(height=280, **CHART_TEMPLATE)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 4: ANALYTICS
# ══════════════════════════════════════════════════════════════════
elif page == "📈  Analytics":
    st.markdown("""
    <h1 style="font-family:'Syne',sans-serif; font-size:32px; font-weight:800;
               color:#e8eaf0; letter-spacing:-0.03em; margin-bottom:4px;">
        Analytics
    </h1>
    <p style="color:#5a6280; font-size:15px; margin-bottom:32px;">
        국가·지표별 자유 탐색 및 우선순위 이력 분석
    </p>
    """, unsafe_allow_html=True)

    CHART_TEMPLATE = dict(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(20,25,40,0.5)',
        font=dict(family='DM Sans', color='#8890a8'),
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(gridcolor='#1e2640'),
        yaxis=dict(gridcolor='#1e2640'),
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        country_filter = st.multiselect(
            "국가 선택",
            ['중국', '일본', '대만', '미국', '홍콩'],
            default=['중국', '일본', '대만', '미국', '홍콩'],
            format_func=lambda x: f"{FLAGS[x]} {COUNTRY_EN[x]}"
        )
    with c2:
        metric_map = {
            '방문객 수': 'visitor_count',
            'MoM 성장률': 'visitor_mom_growth',
            'SNS 버즈': 'buzz_volume',
            '인게이지먼트': 'engagement',
            '잠재 노출량': 'potential_exposure',
            '긍정 감성(%)': 'positive_pct',
            '한류 소비건수': 'hallyu_spend_count',
            '우선순위 점수': 'priority_score',
        }
        metric_label = st.selectbox("지표 선택", list(metric_map.keys()))
        metric = metric_map[metric_label]

    df_filtered = df[df['country'].isin(country_filter)].copy()
    df_filtered['date_str'] = df_filtered['year_month'].astype(str).apply(lambda x: f"{x[:4]}-{x[4:]}")

    fig = px.line(df_filtered, x='date_str', y=metric, color='country',
                  color_discrete_sequence=['#3d6fff','#ff4b4b','#4dff91','#ffaa00','#cc44ff'],
                  labels={metric: metric_label, 'date_str': '', 'country': ''},
                  title='')
    fig.update_layout(height=350, **CHART_TEMPLATE)
    fig.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Priority Label 이력 분포</div>', unsafe_allow_html=True)
        if 'priority_label' in df_filtered.columns:
            label_count = df_filtered.groupby(['country', 'priority_label']).size().reset_index(name='count')
            label_count['country_flag'] = label_count['country'].apply(lambda x: f"{FLAGS.get(x,'')} {COUNTRY_EN.get(x,x)}")
            PRIORITY_COLOR_MAP = {'High': '#ff4b4b', 'Medium': '#ffaa00', 'Low': '#4488ff'}
            fig2 = px.bar(label_count, x='country_flag', y='count', color='priority_label',
                          color_discrete_map=PRIORITY_COLOR_MAP, barmode='group',
                          labels={'count':'개월 수','country_flag':'','priority_label':''})
            fig2.update_layout(height=280, **CHART_TEMPLATE)
            st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">방문객 점유율 추이</div>', unsafe_allow_html=True)
        share_data = df_filtered[['date_str','country','country_share']].dropna()
        fig3 = px.area(share_data, x='date_str', y='country_share', color='country',
                       color_discrete_sequence=['#3d6fff','#ff4b4b','#4dff91','#ffaa00','#cc44ff'],
                       labels={'country_share':'점유율','date_str':'','country':''})
        fig3.update_layout(height=280, **CHART_TEMPLATE)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">Raw Data</div>', unsafe_allow_html=True)
    display_cols = ['year_month', 'country', 'visitor_count', 'visitor_mom_growth',
                    'buzz_volume', 'engagement', 'positive_pct', 'priority_score', 'priority_label']
    st.dataframe(
        df_filtered[[c for c in display_cols if c in df_filtered.columns]]
        .sort_values(['year_month', 'country'], ascending=[False, True])
        .style.format({
            'visitor_count': '{:,.0f}',
            'visitor_mom_growth': '{:+.1%}',
            'buzz_volume': '{:,.0f}',
            'engagement': '{:,.0f}',
            'positive_pct': '{:.1f}%',
            'priority_score': '{:.3f}',
        }),
        use_container_width=True,
        height=400
    )
