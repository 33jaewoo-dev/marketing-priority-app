import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Inbound Marketing Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; }
h1, h2, h3, .logo-text { font-family: 'Outfit', sans-serif !important; }

.stApp { background: #f1f5f9; }

section[data-testid="stSidebar"] > div {
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
}

/* 카드 */
.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
    margin-bottom: 16px;
}

/* 국가 카드 */
.country-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    border-top: 4px solid #e2e8f0;
    transition: transform 0.15s, box-shadow 0.15s;
    height: 100%;
}
.country-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.country-card.high  { border-top-color: #ef4444; }
.country-card.medium { border-top-color: #f59e0b; }
.country-card.low   { border-top-color: #3b82f6; }

/* 배지 */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
    letter-spacing: 0.04em;
}
.badge.high   { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; }
.badge.medium { background: #fffbeb; color: #d97706; border: 1px solid #fcd34d; }
.badge.low    { background: #eff6ff; color: #2563eb; border: 1px solid #93c5fd; }

/* 섹션 라벨 */
.label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 12px;
}

/* 신호 행 */
.sig-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #f1f5f9;
    font-size: 13px;
}
.sig-name { color: #475569; font-weight: 500; }
.sig-desc { font-size: 11px; color: #94a3b8; margin-top: 2px; }
.up   { color: #16a34a; font-weight: 700; font-family: 'Outfit', sans-serif; }
.down { color: #dc2626; font-weight: 700; font-family: 'Outfit', sans-serif; }
.neu  { color: #d97706; font-weight: 700; font-family: 'Outfit', sans-serif; }

/* 액션 아이템 */
.action-item {
    background: #f8fafc;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    border-left: 3px solid #e2e8f0;
}
.action-item.high-border   { border-left-color: #ef4444; }
.action-item.medium-border { border-left-color: #f59e0b; }
.action-item.low-border    { border-left-color: #3b82f6; }
.action-title { font-size: 13px; font-weight: 600; color: #1e293b; margin-bottom: 4px; }
.action-desc  { font-size: 12px; color: #64748b; line-height: 1.5; }

/* stat 수치 */
.stat-val {
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
    line-height: 1;
}
.stat-label { font-size: 11px; color: #94a3b8; margin-top: 4px; }

/* 결과 박스 */
.result-box {
    border-radius: 20px;
    padding: 36px 24px;
    text-align: center;
    border: 2px solid #e2e8f0;
    background: #ffffff;
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    letter-spacing: 0.02em !important;
    height: 52px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(59,130,246,0.3) !important;
}

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: #e2e8f0;
    border-radius: 10px;
    padding: 3px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #64748b !important;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #0f172a !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}

/* 라디오 */
div[data-testid="stRadio"] label {
    font-size: 14px !important;
    color: #334155 !important;
}

hr { border-color: #e2e8f0 !important; margin: 16px 0 !important; }

/* 슬라이더 색상 */
.stSlider [data-baseweb="slider"] { color: #3b82f6 !important; }
</style>
""", unsafe_allow_html=True)

# ── 상수 ──────────────────────────────────────────────────────────
FLAGS    = {'중국':'🇨🇳','일본':'🇯🇵','대만':'🇹🇼','미국':'🇺🇸','홍콩':'🇭🇰'}
CNAME    = {'중국':'China','일본':'Japan','대만':'Taiwan','미국':'USA','홍콩':'Hong Kong'}
PCOLOR   = {'High':'#ef4444','Medium':'#f59e0b','Low':'#3b82f6'}
PBORDER  = {'High':'high','Medium':'medium','Low':'low'}
COLORS   = ['#3b82f6','#ef4444','#10b981','#f59e0b','#8b5cf6']

CHART = dict(
    template='plotly_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(248,250,252,0.6)',
    font=dict(family='Inter', color='#64748b', size=12),
    margin=dict(l=0,r=0,t=8,b=0),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
    xaxis=dict(gridcolor='#f1f5f9', linecolor='#e2e8f0', tickfont=dict(size=11)),
    yaxis=dict(gridcolor='#f1f5f9', linecolor='#e2e8f0', tickfont=dict(size=11)),
)

# ── 모델 학습 ─────────────────────────────────────────────────────
@st.cache_resource(show_spinner="🔄 AI 모델 초기화 중...")
def load_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder

    base = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base,'full_dataset.csv'), encoding='utf-8', dtype={'year_month':str})

    FEATURES = [
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
    df_c = df[FEATURES+['priority_label']].dropna()
    X, y = df_c[FEATURES], df_c['priority_label']
    le = LabelEncoder(); y_enc = le.fit_transform(y)
    rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight='balanced')
    rf.fit(X, y_enc)
    fi = pd.DataFrame({'feature':FEATURES,'importance':rf.feature_importances_}).sort_values('importance',ascending=False)
    return rf, le, FEATURES, fi

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    df  = pd.read_csv(os.path.join(base,'full_dataset.csv'),  encoding='utf-8', dtype={'year_month':str})
    sat = pd.read_csv(os.path.join(base,'satisfaction_data.csv'), encoding='utf-8')
    hsp = pd.read_csv(os.path.join(base,'hallyu_spending.csv'),   encoding='utf-8', dtype={'year_month':str})
    hid = pd.read_csv(os.path.join(base,'hallyu_industry.csv'),   encoding='utf-8', dtype={'year_month':str})
    df['year_month'] = df['year_month'].astype(str).str.strip()
    return df, sat, hsp, hid

model, le, FEATURES, feat_imp = load_model()
df, sat_df, hallyu_df, hallyu_ind = load_data()
latest_month = df['year_month'].max()
ym_disp = f"{latest_month[:4]}.{latest_month[4:]}"

# ── 사이드바 ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 24px;">
      <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:800;
                  color:#0f172a;line-height:1.2;letter-spacing:-0.02em;">
        Inbound Marketing<br/><span style="color:#3b82f6;">Intelligence</span>
      </div>
      <div style="font-size:10px;color:#94a3b8;margin-top:6px;letter-spacing:0.1em;text-transform:uppercase;">
        Korea Tourism AI Platform
      </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", ["📊  Overview","🔮  Priority Engine","👤  Market Profiles","📈  Analytics"],
                    label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px;color:#94a3b8;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">
      Latest Data
    </div>
    <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;color:#0f172a;">{ym_disp}</div>
    <div style="font-size:11px;color:#94a3b8;margin-top:2px;">Korea Tourism Datalab</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:12px;color:#64748b;line-height:2;">
      <b style="color:#334155;">Model</b><br/>Random Forest · 74% Acc<br/>
      <b style="color:#334155;">Data</b><br/>KTO · SNS · Hallyu Index<br/>
      <b style="color:#334155;">Markets</b><br/>🇨🇳 🇯🇵 🇹🇼 🇺🇸 🇭🇰
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page == "📊  Overview":
    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">
      마케팅 우선순위 대시보드
    </h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">
      방한 외국인 빅데이터 + SNS 관심도 기반 실시간 국가별 마케팅 우선순위 추천
    </p>
    """, unsafe_allow_html=True)

    latest = df[df['year_month']==latest_month].sort_values('priority_score', ascending=False)
    st.markdown(f'<div class="label">Current Priority Ranking — {ym_disp}</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (_, row) in enumerate(latest.iterrows()):
        lbl = row.get('priority_label','N/A')
        flag = FLAGS.get(row['country'],'')
        cn   = CNAME.get(row['country'], row['country'])
        mom  = row.get('visitor_mom_growth', 0) or 0
        clr  = PCOLOR.get(lbl,'#888')
        rank = ['1st','2nd','3rd','4th','5th'][i]
        with cols[i]:
            st.markdown(f"""
            <div class="country-card {PBORDER.get(lbl,'low')}">
              <div style="font-size:10px;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">{rank}</div>
              <div style="font-size:40px;line-height:1;margin-bottom:10px;">{flag}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;">{cn}</div>
              <span class="badge {PBORDER.get(lbl,'low')}">{lbl}</span>
              <div style="margin-top:14px;padding-top:12px;border-top:1px solid #f1f5f9;display:flex;justify-content:space-between;font-size:12px;">
                <div>
                  <div style="color:#94a3b8;margin-bottom:2px;">Score</div>
                  <div style="font-family:'Outfit',sans-serif;font-weight:700;color:{clr};">{row['priority_score']:.3f}</div>
                </div>
                <div style="text-align:right;">
                  <div style="color:#94a3b8;margin-bottom:2px;">MoM</div>
                  <div style="font-weight:600;color:{'#16a34a' if mom>0 else '#dc2626'};">{'+' if mom>0 else ''}{mom*100:.1f}%</div>
                </div>
              </div>
              <div style="margin-top:8px;font-size:11px;color:#94a3b8;">{int(row['visitor_count']):,} visitors</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    import plotly.express as px
    import plotly.graph_objects as go

    df_p = df.copy()
    df_p['date'] = df_p['year_month'].apply(lambda x: f"{x[:4]}-{x[4:]}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="label">Monthly Visitor Trends</div>', unsafe_allow_html=True)
        fig = px.line(df_p, x='date', y='visitor_count', color='country',
                      color_discrete_sequence=COLORS,
                      labels={'visitor_count':'Visitors','date':'','country':''})
        fig.update_traces(line=dict(width=2.5))
        fig.update_layout(height=300, **CHART)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="label">SNS Engagement Trends</div>', unsafe_allow_html=True)
        fig2 = px.line(df_p, x='date', y='engagement', color='country',
                       color_discrete_sequence=COLORS,
                       labels={'engagement':'Engagement','date':'','country':''})
        fig2.update_traces(line=dict(width=2.5))
        fig2.update_layout(height=300, **CHART)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="label">Positive Sentiment (%) — 55% = Neutral Threshold</div>', unsafe_allow_html=True)
        fig3 = px.line(df_p, x='date', y='positive_pct', color='country',
                       color_discrete_sequence=COLORS,
                       labels={'positive_pct':'Positive %','date':'','country':''})
        fig3.update_traces(line=dict(width=2.5))
        fig3.add_hline(y=55, line_dash='dash', line_color='#94a3b8', annotation_text='Neutral')
        fig3.update_layout(height=280, **CHART)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown('<div class="label">Feature Importance — Top 10</div>', unsafe_allow_html=True)
        fi_disp = feat_imp.head(10).copy()
        fi_disp['feature'] = fi_disp['feature'].str.replace('_',' ').str.title()
        fig4 = px.bar(fi_disp, x='importance', y='feature', orientation='h',
                      color='importance', color_continuous_scale=['#dbeafe','#3b82f6','#1e40af'])
        fig4.update_layout(height=280, showlegend=False, coloraxis_showscale=False, **CHART)
        fig4.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="label">Model Performance</div>', unsafe_allow_html=True)
    m = st.columns(5)
    for col, lbl, val, sub in [
        (m[0],"Algorithm","Random Forest","200 estimators · depth 10"),
        (m[1],"Test Accuracy","74.0%","80/20 split · stratified"),
        (m[2],"High F1 Score","0.86","Precision 82% · Recall 91%"),
        (m[3],"Training Samples","336","2018.11 → 2025.08"),
        (m[4],"Input Features","29 vars","Visitor + SNS + Hallyu"),
    ]:
        with col:
            st.markdown(f"""
            <div class="card" style="padding:18px 20px;">
              <div style="font-size:10px;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">{lbl}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:19px;font-weight:700;color:#0f172a;">{val}</div>
              <div style="font-size:11px;color:#94a3b8;margin-top:4px;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PRIORITY ENGINE
# ══════════════════════════════════════════════════════════════════
elif page == "🔮  Priority Engine":
    import plotly.express as px
    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">
      Priority Engine
    </h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">
      최신 지표를 입력하면 AI가 마케팅 우선순위와 맞춤 전략을 제안합니다
    </p>
    """, unsafe_allow_html=True)

    country_sel = st.selectbox("분석 국가 선택",['중국','일본','대만','미국','홍콩'],
                                format_func=lambda x:f"{FLAGS[x]}  {CNAME[x]}")
    cd = df[df['country']==country_sel].sort_values('year_month').iloc[-1]

    tab1, tab2, tab3 = st.tabs(["🧳  방문객 지표","📱  SNS 지표","⚙️  거시환경"])
    with tab1:
        c1,c2,c3 = st.columns(3)
        with c1:
            visitor_count = st.number_input("이번 달 방문객",value=int(cd['visitor_count']),step=1000)
            visitor_lag1  = st.number_input("전월 방문객",value=int(cd['visitor_lag1']),step=1000)
        with c2:
            visitor_lag2  = st.number_input("2개월 전",value=int(cd['visitor_lag2']),step=1000)
            visitor_lag3  = st.number_input("3개월 전",value=int(cd['visitor_lag3']),step=1000)
        with c3:
            visitor_3m_avg = st.number_input("3개월 이동평균",value=float(cd['visitor_3m_avg']),step=1000.0)
            visitor_6m_avg = st.number_input("6개월 이동평균",value=float(cd['visitor_6m_avg']),step=1000.0)
        country_share = st.number_input("전체 방한객 중 해당국 비율",value=float(cd['country_share']),step=0.001,format="%.4f")

    with tab2:
        c1,c2 = st.columns(2)
        with c1:
            buzz_volume       = st.number_input("버즈 볼륨 (SNS 언급량)",value=int(cd['buzz_volume']),step=100)
            engagement        = st.number_input("인게이지먼트",value=int(cd['engagement']),step=1000)
        with c2:
            potential_exposure = st.number_input("잠재 노출량",value=int(cd['potential_exposure']),step=10000)
            positive_pct = st.slider("긍정 감성 비율 (%)",0.0,100.0,float(cd['positive_pct']),0.5,
                                     help="40% 미만 시 50% 페널티 / 55% 미만 시 25% 페널티")
        negative_pct = 100.0 - positive_pct
        if positive_pct < 40:
            st.error("🚨 긍정 감성 40% 미만 — 외교 이슈 또는 심각한 부정 여론. 우선순위 점수에 50% 페널티 적용.")
        elif positive_pct < 55:
            st.warning("⚠️ 긍정 감성 55% 미만 — 불안정한 여론. 우선순위 점수에 25% 페널티 적용.")

    with tab3:
        c1,c2,c3 = st.columns(3)
        with c1: month = st.selectbox("기준 월",list(range(1,13)),index=int(cd['month'])-1)
        with c2: exchange_rate = st.number_input("환율 (원화 기준)",value=float(cd['exchange_rate']),step=1.0)
        with c3: oil_price     = st.number_input("유가 (USD/배럴)",value=float(cd['oil_price']),step=1.0)

    # 파생변수
    vmom  = (visitor_count-visitor_lag1)/visitor_lag1 if visitor_lag1 else 0
    vvs3  = visitor_count/visitor_3m_avg if visitor_3m_avg else 1
    vstd  = float(cd.get('visitor_rolling_std',0) or 0)
    bl1   = float(cd.get('buzz_lag1',buzz_volume) or buzz_volume)
    el1   = float(cd.get('engagement_lag1',engagement) or engagement)
    exl1  = float(cd.get('exposure_lag1',potential_exposure) or potential_exposure)
    bmom  = (buzz_volume-bl1)/bl1 if bl1 else 0
    emom  = (engagement-el1)/el1 if el1 else 0
    exmom = (potential_exposure-exl1)/exl1 if exl1 else 0
    epv   = engagement/visitor_count if visitor_count else 0
    bpv   = buzz_volume/visitor_count if visitor_count else 0
    b3m   = float(cd.get('buzz_3m_avg',buzz_volume) or buzz_volume)
    bvs3  = buzz_volume/b3m if b3m else 1
    qtr   = (month-1)//3+1
    peak  = 1 if month in [3,4,5,9,10] else 0
    hc    = float(cd.get('hallyu_spend_count',0) or 0)
    hl1   = float(cd.get('hallyu_lag1',hc) or hc)
    hmom  = (hc-hl1)/hl1 if hl1 else 0
    hpv   = hc/visitor_count if visitor_count else 0

    inp = {
        'visitor_count':visitor_count,'visitor_lag1':visitor_lag1,
        'visitor_lag2':visitor_lag2,'visitor_lag3':visitor_lag3,
        'visitor_mom_growth':vmom,'visitor_3m_avg':visitor_3m_avg,
        'visitor_6m_avg':visitor_6m_avg,'visitor_vs_3m_avg':vvs3,
        'visitor_rolling_std':vstd,'country_share':country_share,
        'buzz_volume':buzz_volume,'engagement':engagement,
        'potential_exposure':potential_exposure,
        'buzz_mom_growth':bmom,'engagement_mom_growth':emom,
        'exposure_mom_growth':exmom,'engagement_per_visitor':epv,
        'buzz_per_visitor':bpv,'buzz_vs_3m_avg':bvs3,
        'positive_pct':positive_pct,'negative_pct':negative_pct,
        'hallyu_spend_count':hc,'hallyu_mom_growth':hmom,
        'hallyu_per_visitor':hpv,'month':month,'quarter':qtr,
        'is_peak_season':peak,'exchange_rate':exchange_rate,'oil_price':oil_price,
    }

    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("🔮  우선순위 분석 실행", use_container_width=True):
        idf = pd.DataFrame([inp])
        for col in FEATURES:
            if col not in idf.columns: idf[col] = 0
        Xin   = idf[FEATURES]
        pred  = model.predict(Xin)[0]
        proba = model.predict_proba(Xin)[0]
        lbl   = le.inverse_transform([pred])[0]
        clr   = PCOLOR[lbl]
        flag  = FLAGS[country_sel]
        cn    = CNAME[country_sel]

        st.markdown('<div class="label">Analysis Results</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns([1.1, 1, 1.2])

        with r1:
            tags = []
            if peak:                tags.append("✨ 성수기")
            if positive_pct < 55:  tags.append("⚠️ 감성 페널티")
            if vmom < -0.15:       tags.append("🔴 급락 감지")
            tag_html = " &nbsp;".join([f'<span style="background:#f1f5f9;border-radius:6px;padding:3px 8px;font-size:11px;color:#475569;">{t}</span>' for t in tags])

            st.markdown(f"""
            <div class="result-box" style="border-top:4px solid {clr};">
              <div style="font-size:52px;margin-bottom:12px;">{flag}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;color:#0f172a;margin-bottom:12px;">{cn}</div>
              <span class="badge {PBORDER[lbl]}" style="font-size:14px;padding:6px 18px;">{lbl} Priority</span>
              <div style="font-family:'Outfit',sans-serif;font-size:48px;font-weight:800;
                          color:{clr};margin:16px 0 4px;letter-spacing:-0.04em;">{int(max(proba)*100)}%</div>
              <div style="font-size:12px;color:#94a3b8;margin-bottom:16px;">Model Confidence</div>
              <div>{tag_html}</div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="label" style="margin-top:0;">Signal Analysis</div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:12px;color:#94a3b8;margin-bottom:14px;line-height:1.5;">
              AI 모델이 우선순위 판단에 사용한 6가지 핵심 신호의 현재 상태입니다.
            </div>
            """, unsafe_allow_html=True)

            def scls(v, t=0.05):
                if v > t:  return "up","▲"
                if v < -t: return "down","▼"
                return "neu","━"

            sigs = [
                ("방문객 증감률", vmom, f"{vmom*100:+.1f}%", "전월 대비 방문객 변화"),
                ("버즈 증감률",   bmom, f"{bmom*100:+.1f}%", "SNS 언급량 전월 대비"),
                ("인게이지먼트 증감", emom, f"{emom*100:+.1f}%", "SNS 반응 전월 대비"),
                ("3개월 평균 대비", vvs3-1, f"{(vvs3-1)*100:+.1f}%", "현재 방문객 vs 3개월 평균"),
                ("긍정 감성", (positive_pct-55)/100, f"{positive_pct:.1f}%", "기준선 55% 이상 = 정상"),
                ("국가 점유율", (country_share-0.2)/0.2, f"{country_share*100:.1f}%", "전체 5개국 중 비율"),
            ]
            html = ""
            for name, val, disp, desc in sigs:
                cls, arrow = scls(val)
                html += f"""
                <div class="sig-row">
                  <div>
                    <div class="sig-name">{name}</div>
                    <div class="sig-desc">{desc}</div>
                  </div>
                  <div class="{cls}">{arrow} {disp}</div>
                </div>"""
            st.markdown(html, unsafe_allow_html=True)

            st.markdown("<br/>", unsafe_allow_html=True)
            for cn_lbl, p in zip(le.classes_, proba):
                c = PCOLOR[cn_lbl]
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
                  <div style="width:64px;font-size:12px;color:#64748b;">{cn_lbl}</div>
                  <div style="flex:1;background:#f1f5f9;border-radius:4px;height:6px;overflow:hidden;">
                    <div style="width:{int(p*100)}%;height:100%;background:{c};border-radius:4px;"></div>
                  </div>
                  <div style="width:36px;text-align:right;font-family:'Outfit',sans-serif;
                              font-size:12px;font-weight:700;color:{c};">{int(p*100)}%</div>
                </div>""", unsafe_allow_html=True)

        with r3:
            clr2 = PCOLOR[lbl]
            border_cls = PBORDER[lbl]
            RECS = {
                'High':   ("적극적 공세 전략","방문객 규모와 SNS 관심도가 모두 높아 최우선 공략 시장입니다.","예산 상향 배정 권고","#fef2f2",
                           [("예산 확대",f"{cn} 전용 광고 예산 전월 대비 20~30% 확대"),
                            ("현지 콘텐츠",f"{flag} 현지 언어 SNS 콘텐츠 집중 제작"),
                            ("인플루언서","팔로워 10만+ 현지 인플루언서 협업 체결"),
                            ("한정 프로모션",f"{cn} 전용 할인·패키지 즉시 런칭")]),
                'Medium': ("유지 및 모니터링","중간 수준이나 상승 가능성이 있어 주시가 필요한 시장입니다.","현행 예산 유지","#fffbeb",
                           [("현행 유지","현재 캠페인 규모 유지 + 주간 지표 모니터링"),
                            ("A/B 테스트","소규모 A/B 테스트로 고성과 메시지 발굴"),
                            ("전환 트리거","MoM +15% 초과 시 즉시 High 전략 전환"),
                            ("콘텐츠 최적화","상위 20% 포맷 중심으로 운영 효율화")]),
                'Low':    ("관망 및 재배분","방문객·SNS 지표 저조. 타 시장에 리소스 집중이 효율적입니다.","예산 최소화 권고","#eff6ff",
                           [("예산 재배분",f"{cn} 예산을 High 우선순위 시장으로 이동"),
                            ("원인 분석","방문객 감소·부정 여론 근본 원인 파악"),
                            ("회복 감시","MoM +10% 회복 시 Medium 전략 전환"),
                            ("리텐션 집중","신규보다 기존 방문자 재방문 유도 프로그램")])
            }
            st.markdown('<div class="label" style="margin-top:0;">Strategic Recommendations</div>', unsafe_allow_html=True)
            title, desc, budget_label, bg, actions = RECS[lbl]
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {clr2}33;border-radius:12px;
                        padding:16px 18px;margin-bottom:14px;">
              <div style="font-family:'Outfit',sans-serif;font-size:16px;font-weight:700;
                          color:{clr2};margin-bottom:6px;">{title}</div>
              <div style="font-size:12px;color:#64748b;line-height:1.5;margin-bottom:10px;">{desc}</div>
              <span style="background:{clr2};color:#fff;border-radius:6px;padding:3px 10px;
                           font-size:11px;font-weight:600;">{budget_label}</span>
            </div>
            """, unsafe_allow_html=True)

            for at, ad in actions:
                st.markdown(f"""
                <div class="action-item {border_cls}-border">
                  <div class="action-title">{at}</div>
                  <div class="action-desc">{ad}</div>
                </div>""", unsafe_allow_html=True)

            # 추가 상황별 액션
            if positive_pct < 40:
                st.markdown(f"""<div class="action-item" style="border-left-color:#dc2626;background:#fef2f2;">
                  <div class="action-title">🚨 위기 커뮤니케이션</div>
                  <div class="action-desc">부정 여론 원인 즉시 파악 및 위기 대응팀 가동</div>
                </div>""", unsafe_allow_html=True)
            if vmom < -0.3:
                st.markdown(f"""<div class="action-item" style="border-left-color:#dc2626;background:#fef2f2;">
                  <div class="action-title">🚨 급락 원인 분석</div>
                  <div class="action-desc">외교·항공·이슈 원인 조사 및 관계 부처 협의</div>
                </div>""", unsafe_allow_html=True)
            if peak:
                st.markdown(f"""<div class="action-item" style="border-left-color:#10b981;background:#f0fdf4;">
                  <div class="action-title">✨ 성수기 타이밍</div>
                  <div class="action-desc">{month}월 성수기 — 캠페인 집행 최적 타이밍입니다</div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# MARKET PROFILES
# ══════════════════════════════════════════════════════════════════
elif page == "👤  Market Profiles":
    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">
      Market Profiles
    </h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">
      국가별 방한 관광객 행태·만족도·한류 소비 심층 분석
    </p>
    """, unsafe_allow_html=True)

    ly = sat_df['year'].max()
    lsat = sat_df[sat_df['year']==ly]

    st.markdown(f'<div class="label">Traveler Profile Summary — {ly}</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, ctry in enumerate(['중국','일본','대만','미국','홍콩']):
        row = lsat[lsat['country']==ctry]
        if row.empty: continue
        r = row.iloc[0]
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="padding:20px 16px;border-top:4px solid {COLORS[i]};text-align:center;">
              <div style="font-size:36px;margin-bottom:8px;">{FLAGS[ctry]}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:14px;font-weight:700;
                          color:#0f172a;margin-bottom:14px;">{CNAME[ctry]}</div>
              {"".join([f'''<div style="display:flex;justify-content:space-between;
                padding:5px 0;border-bottom:1px solid #f8fafc;font-size:12px;">
                <span style="color:#94a3b8;">{k}</span>
                <span style="font-weight:600;color:#0f172a;">{v}</span></div>'''
                for k,v in [
                    ("지출/인",f"${r['spend_per_person_usd']:,.0f}"),
                    ("체재",f"{r['stay_days']}일"),
                    ("재방문율",f"{r['revisit_rate']}%"),
                    ("만족도",f"{r['overall_satisfaction']}%"),
                    ("추천의향",f"{r['recommend_intention']}%"),
                ]])}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    sat_df['yr'] = sat_df['year'].astype(str)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="label">1인 평균 지출 경비 (USD)</div>', unsafe_allow_html=True)
        fig = px.line(sat_df,x='yr',y='spend_per_person_usd',color='country',
                      color_discrete_sequence=COLORS,markers=True,
                      labels={'spend_per_person_usd':'USD','yr':'','country':''})
        fig.update_layout(height=270,**CHART)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="label">재방문율 추이 (%)</div>', unsafe_allow_html=True)
        fig = px.line(sat_df,x='yr',y='revisit_rate',color='country',
                      color_discrete_sequence=COLORS,markers=True,
                      labels={'revisit_rate':'%','yr':'','country':''})
        fig.update_layout(height=270,**CHART)
        st.plotly_chart(fig,use_container_width=True)

    st.markdown('<div class="label">Hallyu Spending Index</div>', unsafe_allow_html=True)
    hplot = hallyu_df.copy()
    hplot['date'] = hplot['year_month'].apply(lambda x: f"{x[:4]}-{x[4:]}")
    c3,c4 = st.columns(2)
    with c3:
        st.markdown('<div class="label">한류 총 소비건수 추이</div>', unsafe_allow_html=True)
        fig = px.line(hplot,x='date',y='total_count',color='country',
                      color_discrete_sequence=COLORS,
                      labels={'total_count':'소비건수','date':'','country':''})
        fig.update_layout(height=270,**CHART)
        st.plotly_chart(fig,use_container_width=True)
    with c4:
        st.markdown('<div class="label">업종별 한류 소비 비율 (최신 기간)</div>', unsafe_allow_html=True)
        liym = hallyu_ind['year_month'].max()
        lind = hallyu_ind[hallyu_ind['year_month']==liym].copy()
        lind['cn'] = lind['country'].map(CNAME)
        fig = px.bar(lind,x='cn',y='ratio',color='industry',barmode='stack',
                     color_discrete_sequence=['#3b82f6','#ef4444','#10b981','#f59e0b','#8b5cf6','#ec4899','#06b6d4','#84cc16','#f97316'],
                     labels={'ratio':'%','cn':'','industry':''})
        fig.update_layout(height=270,**CHART)
        st.plotly_chart(fig,use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════════
elif page == "📈  Analytics":
    import plotly.express as px

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">
      Analytics
    </h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">
      국가·지표별 자유 탐색 및 우선순위 이력 분석
    </p>
    """, unsafe_allow_html=True)

    c1,c2 = st.columns([2,1])
    with c1:
        ctry_f = st.multiselect("국가",['중국','일본','대만','미국','홍콩'],
                                 default=['중국','일본','대만','미국','홍콩'],
                                 format_func=lambda x:f"{FLAGS[x]} {CNAME[x]}")
    with c2:
        MMAP = {'방문객 수':'visitor_count','MoM 성장률':'visitor_mom_growth',
                'SNS 버즈':'buzz_volume','인게이지먼트':'engagement',
                '잠재 노출량':'potential_exposure','긍정 감성(%)':'positive_pct',
                '한류 소비건수':'hallyu_spend_count','우선순위 점수':'priority_score'}
        ml = st.selectbox("지표", list(MMAP.keys()))
        met = MMAP[ml]

    dff = df[df['country'].isin(ctry_f)].copy()
    dff['date'] = dff['year_month'].apply(lambda x: f"{x[:4]}-{x[4:]}")

    fig = px.line(dff,x='date',y=met,color='country',
                  color_discrete_sequence=COLORS,
                  labels={met:ml,'date':'','country':''})
    fig.update_traces(line=dict(width=2.5))
    fig.update_layout(height=340,**CHART)
    st.plotly_chart(fig,use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="label">Priority Label 이력 분포</div>', unsafe_allow_html=True)
        if 'priority_label' in dff.columns:
            lc = dff.groupby(['country','priority_label']).size().reset_index(name='n')
            lc['cn'] = lc['country'].map(lambda x: f"{FLAGS.get(x,'')} {CNAME.get(x,x)}")
            fig2 = px.bar(lc,x='cn',y='n',color='priority_label',barmode='group',
                          color_discrete_map={'High':'#ef4444','Medium':'#f59e0b','Low':'#3b82f6'},
                          labels={'n':'개월','cn':'','priority_label':''})
            fig2.update_layout(height=270,**CHART)
            st.plotly_chart(fig2,use_container_width=True)
    with c2:
        st.markdown('<div class="label">방문객 점유율 추이</div>', unsafe_allow_html=True)
        sd = dff[['date','country','country_share']].dropna()
        fig3 = px.area(sd,x='date',y='country_share',color='country',
                       color_discrete_sequence=COLORS,
                       labels={'country_share':'점유율','date':'','country':''})
        fig3.update_layout(height=270,**CHART)
        st.plotly_chart(fig3,use_container_width=True)

    st.markdown('<div class="label">Raw Data</div>', unsafe_allow_html=True)
    dcols = ['year_month','country','visitor_count','visitor_mom_growth',
             'buzz_volume','engagement','positive_pct','priority_score','priority_label']
    st.dataframe(
        dff[[c for c in dcols if c in dff.columns]]
        .sort_values(['year_month','country'],ascending=[False,True])
        .style.format({'visitor_count':'{:,.0f}','visitor_mom_growth':'{:+.1%}',
                       'buzz_volume':'{:,.0f}','engagement':'{:,.0f}',
                       'positive_pct':'{:.1f}%','priority_score':'{:.3f}'}),
        use_container_width=True, height=380
    )
