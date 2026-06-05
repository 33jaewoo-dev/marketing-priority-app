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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Outfit', sans-serif !important; }
.stApp { background: #f1f5f9; }
section[data-testid="stSidebar"] > div { background:#ffffff; border-right:1px solid #e2e8f0; }

.card { background:#ffffff; border-radius:16px; padding:24px; box-shadow:0 1px 3px rgba(0,0,0,0.08); margin-bottom:16px; }
.country-card { background:#ffffff; border-radius:16px; padding:20px 16px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.08); border-top:4px solid #e2e8f0; }
.country-card.high   { border-top-color:#ef4444; }
.country-card.medium { border-top-color:#f59e0b; }
.country-card.low    { border-top-color:#3b82f6; }

.badge { display:inline-block; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700; font-family:'Outfit',sans-serif; letter-spacing:0.04em; }
.badge.high   { background:#fef2f2; color:#dc2626; border:1px solid #fca5a5; }
.badge.medium { background:#fffbeb; color:#d97706; border:1px solid #fcd34d; }
.badge.low    { background:#eff6ff; color:#2563eb; border:1px solid #93c5fd; }

.lbl { font-size:10px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#94a3b8; margin-bottom:12px; }

.sig-row { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9; font-size:13px; }
.sig-name { color:#475569; font-weight:500; }
.sig-desc { font-size:11px; color:#94a3b8; margin-top:2px; }
.up   { color:#16a34a; font-weight:700; font-family:'Outfit',sans-serif; }
.down { color:#dc2626; font-weight:700; font-family:'Outfit',sans-serif; }
.neu  { color:#d97706; font-weight:700; font-family:'Outfit',sans-serif; }

.act { background:#f8fafc; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:3px solid #e2e8f0; }
.act.high-b   { border-left-color:#ef4444; }
.act.medium-b { border-left-color:#f59e0b; }
.act.low-b    { border-left-color:#3b82f6; }
.act-title { font-size:13px; font-weight:600; color:#1e293b; margin-bottom:4px; }
.act-desc  { font-size:12px; color:#64748b; line-height:1.5; }

.result-box { border-radius:20px; padding:36px 24px; text-align:center; border:2px solid #e2e8f0; background:#ffffff; }

.stButton > button {
    background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%) !important;
    color:#fff !important; border:none !important; border-radius:12px !important;
    font-family:'Outfit',sans-serif !important; font-weight:600 !important;
    font-size:15px !important; height:52px !important;
}
.stButton > button:hover { opacity:0.92 !important; transform:translateY(-1px) !important; }

.stTabs [data-baseweb="tab-list"] { background:#e2e8f0; border-radius:10px; padding:3px; gap:2px; }
.stTabs [data-baseweb="tab"] { border-radius:8px; color:#64748b !important; font-weight:500; }
.stTabs [aria-selected="true"] { background:#ffffff !important; color:#0f172a !important; box-shadow:0 1px 3px rgba(0,0,0,0.1) !important; }
hr { border-color:#e2e8f0 !important; margin:16px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────
FLAG_URL = {
    '중국': 'https://flagcdn.com/w40/cn.png',
    '일본': 'https://flagcdn.com/w40/jp.png',
    '대만': 'https://flagcdn.com/w40/tw.png',
    '미국': 'https://flagcdn.com/w40/us.png',
    '홍콩': 'https://flagcdn.com/w40/hk.png',
}
def flag_img(country, w=32):
    return f'<img src="{FLAG_URL.get(country,"")}" width="{w}" style="border-radius:3px;display:block;margin:0 auto;">'

CNAME  = {'중국':'China','일본':'Japan','대만':'Taiwan','미국':'USA','홍콩':'Hong Kong'}
PCOLOR = {'High':'#ef4444','Medium':'#f59e0b','Low':'#3b82f6'}
PBDR   = {'High':'high','Medium':'medium','Low':'low'}
COLORS = ['#3b82f6','#ef4444','#10b981','#f59e0b','#8b5cf6']

CHART = dict(
    template='plotly_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(248,250,252,0.6)',
    font=dict(family='Inter',color='#64748b',size=12),
    margin=dict(l=0,r=0,t=8,b=0),
    legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(size=11)),
    xaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0',tickfont=dict(size=11)),
    yaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0',tickfont=dict(size=11)),
)

# ── Priority Score 0-100 ──────────────────────────────────────────
def calc_score(inp, df_ref):
    """
    Marketing Attractiveness Score (0–100)
    Higher = more attractive market for budget allocation.
    All 6 factors increase the score continuously.
    External shocks (visitor crash, severe negative sentiment) apply penalties.
    """
    def mm(val, mn, mx):
        if mx == mn: return 0.5
        return float(np.clip((val - mn) / (mx - mn), 0, 1))

    # Factor 1: Visitor Volume (28%)
    f_volume = mm(inp['visitor_count'], df_ref['visitor_count'].min(), df_ref['visitor_count'].max())

    # Factor 2: Visitor Momentum (22%) — MoM growth + vs 3M avg
    mom_n = mm(inp['visitor_mom_growth'], -0.8, 0.8)
    vs3_n = mm(inp['visitor_vs_3m_avg'] - 1, -0.5, 1.0)
    f_momentum = mom_n * 0.6 + vs3_n * 0.4

    # Factor 3: SNS Interest Volume (18%) — engagement is primary signal
    f_sns = mm(inp['engagement'], df_ref['engagement'].min(), df_ref['engagement'].max())

    # Factor 4: SNS Growth (12%) — buzz + engagement MoM
    sg_raw = inp['buzz_mom_growth'] * 0.5 + inp['engagement_mom_growth'] * 0.5
    f_sns_growth = mm(sg_raw, -0.8, 0.8)

    # Factor 5: Hallyu Spending (10%) — actual consumption proxy
    f_hallyu = mm(inp['hallyu_spend_count'], df_ref['hallyu_spend_count'].min(), df_ref['hallyu_spend_count'].max())

    # Factor 6: Positive Sentiment (10%) — linear, always increases score
    f_sentiment = inp['positive_pct'] / 100.0   # 0 → 0.0,  100 → 1.0

    base = (0.28 * f_volume +
            0.22 * f_momentum +
            0.18 * f_sns +
            0.12 * f_sns_growth +
            0.10 * f_hallyu +
            0.10 * f_sentiment)

    # Shock penalty: only when visitor crash (external event like THAAD, COVID)
    vmom = inp['visitor_mom_growth']
    if   vmom < -0.50: shock = 0.40
    elif vmom < -0.30: shock = 0.60
    elif vmom < -0.15: shock = 0.80
    else:              shock = 1.00

    # Severe negative sentiment penalty (< 40% positive)
    sent_penalty = 0.60 if inp['positive_pct'] < 40 else 1.00

    # Bonuses
    peak_b = inp['is_peak_season'] * 0.04
    fx_b   = mm(inp['exchange_rate'], 100, 1600) * 0.02

    score = (base + peak_b + fx_b) * shock * sent_penalty
    return round(float(np.clip(score, 0, 1)) * 100, 1)

# ── Model ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Initializing AI model...")
def load_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder

    base = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base,'full_dataset.csv'), encoding='utf-8', dtype={'year_month':str})

    FEATS = [
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
    dc = df[FEATS+['priority_label']].dropna()
    X, y = dc[FEATS], dc['priority_label']
    le = LabelEncoder(); ye = le.fit_transform(y)
    rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight='balanced')
    rf.fit(X, ye)
    fi = pd.DataFrame({'feature':FEATS,'importance':rf.feature_importances_}).sort_values('importance',ascending=False)
    return rf, le, FEATS, fi

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    df  = pd.read_csv(os.path.join(base,'full_dataset.csv'),  encoding='utf-8', dtype={'year_month':str})
    sat = pd.read_csv(os.path.join(base,'satisfaction_data.csv'), encoding='utf-8')
    hsp = pd.read_csv(os.path.join(base,'hallyu_spending.csv'),   encoding='utf-8', dtype={'year_month':str})
    hid = pd.read_csv(os.path.join(base,'hallyu_industry.csv'),   encoding='utf-8', dtype={'year_month':str})
    df['year_month'] = df['year_month'].astype(str).str.strip()
    return df, sat, hsp, hid

model, le, FEATS, feat_imp = load_model()
df, sat_df, hallyu_df, hallyu_ind = load_data()
latest_month = df['year_month'].max()
ym_disp = f"{latest_month[:4]}.{latest_month[4:]}"

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 24px;">
      <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:800;color:#0f172a;line-height:1.2;letter-spacing:-0.02em;">
        Inbound Marketing<br/><span style="color:#3b82f6;">Intelligence</span>
      </div>
      <div style="font-size:10px;color:#94a3b8;margin-top:6px;letter-spacing:0.1em;text-transform:uppercase;">Korea Tourism AI Platform</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", ["📊  Overview","🔮  Priority Engine","👤  Market Profiles","📈  Analytics"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px;color:#94a3b8;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">Latest Data</div>
    <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;color:#0f172a;">{ym_disp}</div>
    <div style="font-size:11px;color:#94a3b8;margin-top:2px;">Korea Tourism Datalab</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    flag_row = "".join([f'<img src="{FLAG_URL[c]}" width="20" style="border-radius:2px;margin-right:4px;">' for c in ['중국','일본','대만','미국','홍콩']])
    st.markdown(f"""
    <div style="font-size:12px;color:#64748b;line-height:2.2;">
      <b style="color:#334155;">Model</b><br/>Random Forest · 74% Acc<br/>
      <b style="color:#334155;">Data Sources</b><br/>KTO · SNS · Hallyu Index<br/>
      <b style="color:#334155;">Markets</b><br/>{flag_row}
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page == "📊  Overview":
    import plotly.express as px

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">
      Marketing Priority Dashboard</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">
      AI-powered inbound tourism analytics for strategic marketing budget allocation</p>
    """, unsafe_allow_html=True)

    latest = df[df['year_month']==latest_month].sort_values('priority_score',ascending=False)
    st.markdown(f'<div class="lbl">Current Priority Ranking — {ym_disp}</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (_, row) in enumerate(latest.iterrows()):
        lbl  = row.get('priority_label','N/A')
        cn   = CNAME.get(row['country'],row['country'])
        mom  = row.get('visitor_mom_growth',0) or 0
        clr  = PCOLOR.get(lbl,'#888')
        rank = ['1st','2nd','3rd','4th','5th'][i]
        ps   = round(float(row.get('priority_score',0) or 0)*100,1)
        with cols[i]:
            st.markdown(f"""
            <div class="country-card {PBDR.get(lbl,'low')}">
              <div style="font-size:10px;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">{rank}</div>
              <div style="margin-bottom:10px;">{flag_img(row['country'],36)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;">{cn}</div>
              <span class="badge {PBDR.get(lbl,'low')}">{lbl}</span>
              <div style="margin-top:14px;padding-top:12px;border-top:1px solid #f1f5f9;">
                <div style="font-size:11px;color:#94a3b8;margin-bottom:2px;">Attractiveness Score</div>
                <div style="font-family:'Outfit',sans-serif;font-size:24px;font-weight:800;color:{clr};">{ps}<span style="font-size:13px;color:#94a3b8;">/100</span></div>
                <div style="font-size:12px;font-weight:600;color:{'#16a34a' if mom>0 else '#dc2626'};margin-top:4px;">{'▲' if mom>0 else '▼'} {abs(mom*100):.1f}% MoM</div>
                <div style="font-size:11px;color:#94a3b8;margin-top:2px;">{int(row['visitor_count']):,} visitors</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    df_p = df.copy()
    df_p['date'] = df_p['year_month'].apply(lambda x:f"{x[:4]}-{x[4:]}")
    df_p['country_en'] = df_p['country'].map(CNAME)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Monthly Visitor Trends</div>', unsafe_allow_html=True)
        fig = px.line(df_p,x='date',y='visitor_count',color='country_en',
                      color_discrete_sequence=COLORS,labels={'visitor_count':'Visitors','date':'','country_en':''})
        fig.update_traces(line=dict(width=2.5)); fig.update_layout(height=300,**CHART)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">SNS Engagement Trends</div>', unsafe_allow_html=True)
        fig2 = px.line(df_p,x='date',y='engagement',color='country_en',
                       color_discrete_sequence=COLORS,labels={'engagement':'Engagement','date':'','country_en':''})
        fig2.update_traces(line=dict(width=2.5)); fig2.update_layout(height=300,**CHART)
        st.plotly_chart(fig2,use_container_width=True)

    c3,c4 = st.columns(2)
    with c3:
        st.markdown('<div class="lbl">Positive Sentiment (%) — 40% Penalty / 55% Neutral Threshold</div>', unsafe_allow_html=True)
        fig3 = px.line(df_p,x='date',y='positive_pct',color='country_en',
                       color_discrete_sequence=COLORS,labels={'positive_pct':'%','date':'','country_en':''})
        fig3.update_traces(line=dict(width=2.5))
        fig3.add_hline(y=55,line_dash='dash',line_color='#94a3b8',annotation_text='Neutral')
        fig3.add_hline(y=40,line_dash='dot',line_color='#ef4444',annotation_text='Penalty zone')
        fig3.update_layout(height=280,**CHART)
        st.plotly_chart(fig3,use_container_width=True)
    with c4:
        st.markdown('<div class="lbl">Feature Importance — Top 10</div>', unsafe_allow_html=True)
        fi_d = feat_imp.head(10).copy()
        fi_d['feature'] = fi_d['feature'].str.replace('_',' ').str.title()
        fig4 = px.bar(fi_d,x='importance',y='feature',orientation='h',
                      color='importance',color_continuous_scale=['#dbeafe','#3b82f6','#1e40af'])
        fig4.update_layout(height=280,showlegend=False,coloraxis_showscale=False,**CHART)
        fig4.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig4,use_container_width=True)

    st.markdown('<div class="lbl">Model Performance</div>', unsafe_allow_html=True)
    mc = st.columns(5)
    for col,l,v,s in [
        (mc[0],"Algorithm","Random Forest","200 estimators · depth 10"),
        (mc[1],"Test Accuracy","74.0%","80/20 stratified split"),
        (mc[2],"High F1","0.86","Precision 82% · Recall 91%"),
        (mc[3],"Training Data","336 samples","2018.11 – 2025.08"),
        (mc[4],"Input Features","29 variables","Visitor + SNS + Hallyu"),
    ]:
        with col:
            st.markdown(f"""
            <div class="card" style="padding:18px 20px;">
              <div style="font-size:10px;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">{l}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:19px;font-weight:700;color:#0f172a;">{v}</div>
              <div style="font-size:11px;color:#94a3b8;margin-top:4px;">{s}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PRIORITY ENGINE
# ══════════════════════════════════════════════════════════════════
elif page == "🔮  Priority Engine":
    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">
      Priority Engine</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">
      Input current market indicators to receive an AI-generated attractiveness score and strategic recommendations</p>
    """, unsafe_allow_html=True)

    country_sel = st.selectbox("Select Market",['중국','일본','대만','미국','홍콩'],
                                format_func=lambda x:f"{CNAME[x]}")
    cd = df[df['country']==country_sel].sort_values('year_month').iloc[-1]

    t1,t2,t3 = st.tabs(["🧳  Visitor Metrics","📱  SNS Metrics","⚙️  Macro Environment"])
    with t1:
        c1,c2,c3 = st.columns(3)
        with c1:
            visitor_count = st.number_input("Current Month Visitors",value=int(cd['visitor_count']),step=1000)
            visitor_lag1  = st.number_input("Previous Month",value=int(cd['visitor_lag1']),step=1000)
        with c2:
            visitor_lag2  = st.number_input("2 Months Ago",value=int(cd['visitor_lag2']),step=1000)
            visitor_lag3  = st.number_input("3 Months Ago",value=int(cd['visitor_lag3']),step=1000)
        with c3:
            visitor_3m_avg = st.number_input("3M Moving Average",value=float(cd['visitor_3m_avg']),step=1000.0)
            visitor_6m_avg = st.number_input("6M Moving Average",value=float(cd['visitor_6m_avg']),step=1000.0)
        country_share = st.number_input("Market Share (0–1)",value=float(cd['country_share']),step=0.001,format="%.4f",
                                         help="This country's share of total inbound visitors across all 5 markets")

    with t2:
        c1,c2 = st.columns(2)
        with c1:
            buzz_volume        = st.number_input("Buzz Volume (SNS Mentions)",value=int(cd['buzz_volume']),step=100)
            engagement         = st.number_input("Engagement (Likes · Comments · Shares)",value=int(cd['engagement']),step=1000)
        with c2:
            potential_exposure = st.number_input("Potential Exposure (Follower Reach)",value=int(cd['potential_exposure']),step=10000)
            positive_pct = st.slider("Positive Sentiment (%)",0.0,100.0,float(cd['positive_pct']),0.5,
                                     help="% of Korea tourism posts with positive sentiment. Directly increases attractiveness score. Below 40% triggers crisis penalty.")
        negative_pct = 100.0 - positive_pct
        if positive_pct < 40:
            st.error("🚨 Positive sentiment below 40% — geopolitical tension or crisis detected. Score penalty: −40%")
        elif positive_pct < 55:
            st.warning("⚠️ Positive sentiment below 55% — unstable public opinion.")

    with t3:
        c1,c2,c3 = st.columns(3)
        with c1: month = st.selectbox("Reference Month",list(range(1,13)),index=int(cd['month'])-1,
                                       help="Months 3,4,5,9,10 = peak season bonus")
        with c2: exchange_rate = st.number_input("Exchange Rate (KRW)",value=float(cd['exchange_rate']),step=1.0,
                                                   help="Weaker KRW = cheaper for foreign tourists = small attractiveness bonus")
        with c3: oil_price     = st.number_input("Oil Price (USD/barrel)",value=float(cd['oil_price']),step=1.0)

    # Derived features
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
    if st.button("🔮  Run Priority Analysis", use_container_width=True):
        idf = pd.DataFrame([inp])
        for col in FEATS:
            if col not in idf.columns: idf[col]=0
        pred  = model.predict(idf[FEATS])[0]
        proba = model.predict_proba(idf[FEATS])[0]
        lbl   = le.inverse_transform([pred])[0]
        clr   = PCOLOR[lbl]
        cn    = CNAME[country_sel]

        # Attractiveness Score (0-100)
        p_score = calc_score(inp, df)
        prev_s  = round(float(cd.get('priority_score',0.5) or 0.5)*100,1)
        diff    = round(p_score - prev_s, 1)

        if p_score >= 65:   g_clr = '#ef4444'
        elif p_score >= 40: g_clr = '#f59e0b'
        else:               g_clr = '#3b82f6'

        # Score breakdown for transparency
        f_volume   = float(np.clip((inp['visitor_count']-df['visitor_count'].min())/(df['visitor_count'].max()-df['visitor_count'].min()),0,1))
        f_momentum = float(np.clip((vmom+0.8)/1.6,0,1))*0.6 + float(np.clip((vvs3-0.5)/1.5,0,1))*0.4
        f_sns      = float(np.clip((inp['engagement']-df['engagement'].min())/(df['engagement'].max()-df['engagement'].min()),0,1))
        f_sent     = inp['positive_pct']/100.0

        st.markdown('<div class="lbl">Analysis Results</div>', unsafe_allow_html=True)
        r1,r2,r3 = st.columns([1.1,1,1.2])

        with r1:
            tags = []
            if peak:              tags.append("✨ Peak season")
            if positive_pct < 55: tags.append("⚠️ Sentiment penalty")
            if vmom < -0.15:      tags.append("🔴 Visitor crash")
            tag_html = "&nbsp;".join([f'<span style="background:#f1f5f9;border-radius:6px;padding:3px 8px;font-size:10px;color:#475569;">{t}</span>' for t in tags])
            diff_html = f'<span style="color:{"#16a34a" if diff>=0 else "#dc2626"};font-size:12px;font-weight:600;">{"▲" if diff>=0 else "▼"} {abs(diff):.1f} pts vs last month</span>'

            st.markdown(f"""
            <div class="result-box" style="border-top:4px solid {g_clr};">
              <div style="margin-bottom:12px;">{flag_img(country_sel,48)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;color:#0f172a;margin-bottom:12px;">{cn}</div>
              <span class="badge {PBDR[lbl]}" style="font-size:13px;padding:5px 16px;">{lbl} Priority</span>
              <div style="margin:20px 0 6px;">
                <div style="font-size:10px;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;">Market Attractiveness Score</div>
                <div style="font-family:'Outfit',sans-serif;font-size:60px;font-weight:800;color:{g_clr};letter-spacing:-0.04em;line-height:1;">{p_score}</div>
                <div style="font-size:16px;color:#94a3b8;margin-bottom:8px;">/ 100</div>
                <div>{diff_html}</div>
              </div>
              <div style="background:#f1f5f9;border-radius:8px;height:10px;margin:14px 0 6px;overflow:hidden;">
                <div style="width:{p_score}%;height:100%;background:linear-gradient(90deg,{g_clr}88,{g_clr});border-radius:8px;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:#94a3b8;margin-bottom:14px;">
                <span>0</span><span>50</span><span>100</span>
              </div>
              <div style="background:#f8fafc;border-radius:10px;padding:12px;text-align:left;margin-bottom:12px;">
                <div style="font-size:10px;color:#94a3b8;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">Score Breakdown</div>
                {"".join([f'<div style="display:flex;justify-content:space-between;font-size:11px;padding:3px 0;"><span style="color:#64748b;">{n}</span><span style="font-weight:600;color:#0f172a;">{round(v*10,1)}/10</span></div>' for n,v in [("Visitor Volume",f_volume),("Visitor Momentum",f_momentum),("SNS Interest",f_sns),("Sentiment",f_sent)]])}
              </div>
              <div>{tag_html}</div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="lbl" style="margin-top:0;">Signal Analysis</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#94a3b8;margin-bottom:14px;line-height:1.5;">Current status of the 6 key signals driving the attractiveness score.</div>', unsafe_allow_html=True)

            def scls(v,t=0.05):
                if v>t:  return "up","▲"
                if v<-t: return "down","▼"
                return "neu","━"

            sigs = [
                ("Visitor MoM Growth",    vmom,              f"{vmom*100:+.1f}%",      "Month-over-month visitor change"),
                ("Buzz Volume Change",    bmom,              f"{bmom*100:+.1f}%",      "SNS mention volume vs last month"),
                ("Engagement Change",     emom,              f"{emom*100:+.1f}%",      "SNS reactions vs last month"),
                ("vs 3M Average",         vvs3-1,            f"{(vvs3-1)*100:+.1f}%",  "Current visitors vs 3-month avg"),
                ("Positive Sentiment",    (positive_pct-55)/100, f"{positive_pct:.1f}%","Directly adds to attractiveness score"),
                ("Market Share",          (country_share-0.2)/0.2, f"{country_share*100:.1f}%","Share of total 5-market visitors"),
            ]
            html=""
            for name,val,disp,desc in sigs:
                cls,arrow = scls(val)
                html+=f"""<div class="sig-row">
                  <div><div class="sig-name">{name}</div><div class="sig-desc">{desc}</div></div>
                  <div class="{cls}">{arrow} {disp}</div></div>"""
            st.markdown(html, unsafe_allow_html=True)

            st.markdown("<br/>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:11px;color:#94a3b8;margin-bottom:8px;">AI Classification Confidence</div>', unsafe_allow_html=True)
            for cn_l,p in zip(le.classes_,proba):
                c=PCOLOR[cn_l]
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
                  <div style="width:56px;font-size:12px;color:#64748b;">{cn_l}</div>
                  <div style="flex:1;background:#f1f5f9;border-radius:4px;height:6px;overflow:hidden;">
                    <div style="width:{int(p*100)}%;height:100%;background:{c};border-radius:4px;"></div></div>
                  <div style="width:32px;text-align:right;font-family:'Outfit',sans-serif;font-size:12px;font-weight:700;color:{c};">{int(p*100)}%</div>
                </div>""", unsafe_allow_html=True)

        with r3:
            clr2 = PCOLOR[lbl]; bc = PBDR[lbl]; cn2 = CNAME[country_sel]
            RECS = {
                'High':   ("Aggressive Offensive Strategy",
                           "Visitor volume, SNS interest, and sentiment are all strong. Maximum ROI market right now.",
                           "Increase Budget","#fef2f2",
                           [("Budget Expansion",f"Increase {cn2}-specific ad spend by 20–30% vs. last month"),
                            ("Local Language Content",f"Scale up {cn2}-language content production and influencer collabs"),
                            ("Influencer Push","Partner with 100K+ local influencers for peak reach"),
                            ("Exclusive Promotions",f"Launch {cn2}-only discounts and travel packages immediately")]),
                'Medium': ("Monitor & Optimize",
                           "Mid-tier market with upside potential. Watch for momentum signals before scaling.",
                           "Maintain Budget","#fffbeb",
                           [("Hold Steady","Maintain current campaign scale — track weekly KPIs"),
                            ("A/B Testing","Run small creative tests to identify high-performing messages"),
                            ("Trigger Plan","Upgrade to High strategy if MoM growth exceeds +15%"),
                            ("Content Efficiency","Double down on top 20% performing content formats")]),
                'Low':    ("Reallocate & Monitor",
                           "Low volume and/or sentiment. Reallocating resources to stronger markets is more efficient.",
                           "Minimize Budget","#eff6ff",
                           [("Reallocate",f"Shift {cn2} budget to High-priority markets"),
                            ("Root Cause Analysis","Diagnose visitor decline — geopolitical, aviation, or seasonal?"),
                            ("Recovery Trigger","Re-engage when MoM rebounds above +10%"),
                            ("Retention Focus","Target returning visitors rather than new acquisition")])
            }
            st.markdown('<div class="lbl" style="margin-top:0;">Strategic Recommendations</div>', unsafe_allow_html=True)
            title,desc,blbl,bg,actions = RECS[lbl]
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {clr2}33;border-radius:12px;padding:16px 18px;margin-bottom:14px;">
              <div style="font-family:'Outfit',sans-serif;font-size:16px;font-weight:700;color:{clr2};margin-bottom:6px;">{title}</div>
              <div style="font-size:12px;color:#64748b;line-height:1.5;margin-bottom:10px;">{desc}</div>
              <span style="background:{clr2};color:#fff;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:600;">{blbl}</span>
            </div>""", unsafe_allow_html=True)
            for at,ad in actions:
                st.markdown(f"""<div class="act {bc}-b">
                  <div class="act-title">{at}</div>
                  <div class="act-desc">{ad}</div></div>""", unsafe_allow_html=True)
            if positive_pct < 40:
                st.markdown(f"""<div class="act" style="border-left-color:#dc2626;background:#fef2f2;">
                  <div class="act-title">🚨 Crisis Communication</div>
                  <div class="act-desc">Identify root cause of negative sentiment. Activate PR crisis response team immediately.</div></div>""", unsafe_allow_html=True)
            if vmom < -0.30:
                st.markdown(f"""<div class="act" style="border-left-color:#dc2626;background:#fef2f2;">
                  <div class="act-title">🚨 Visitor Crash Response</div>
                  <div class="act-desc">Investigate cause — diplomatic tensions, flight suspensions, or external events. Coordinate with relevant authorities.</div></div>""", unsafe_allow_html=True)
            if peak:
                st.markdown(f"""<div class="act" style="border-left-color:#10b981;background:#f0fdf4;">
                  <div class="act-title">✨ Peak Season Opportunity</div>
                  <div class="act-desc">Month {month} is peak season — optimal timing for campaign launch and budget deployment.</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# MARKET PROFILES
# ══════════════════════════════════════════════════════════════════
elif page == "👤  Market Profiles":
    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">
      Market Profiles</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">
      Traveler behavior, satisfaction, and Hallyu consumption by market (2015–2024)</p>
    """, unsafe_allow_html=True)

    ly = sat_df['year'].max()
    lsat = sat_df[sat_df['year']==ly]
    st.markdown(f'<div class="lbl">Traveler Profile Summary — {ly}</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i,ctry in enumerate(['중국','일본','대만','미국','홍콩']):
        row = lsat[lsat['country']==ctry]
        if row.empty: continue
        r = row.iloc[0]
        with cols[i]:
            rows_html = "".join([f'<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f8fafc;font-size:12px;"><span style="color:#94a3b8;">{k}</span><span style="font-weight:600;color:#0f172a;">{v}</span></div>'
                for k,v in [("Spend/Person",f"${r['spend_per_person_usd']:,.0f}"),("Stay",f"{r['stay_days']} days"),
                             ("Revisit Rate",f"{r['revisit_rate']}%"),("Satisfaction",f"{r['overall_satisfaction']}%"),("Recommend",f"{r['recommend_intention']}%")]])
            st.markdown(f"""
            <div class="card" style="padding:20px 16px;border-top:4px solid {COLORS[i]};text-align:center;">
              <div style="margin-bottom:8px;">{flag_img(ctry,36)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:14px;font-weight:700;color:#0f172a;margin-bottom:14px;">{CNAME[ctry]}</div>
              {rows_html}
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    sat_df['yr'] = sat_df['year'].astype(str)
    sat_df['country_en'] = sat_df['country'].map(CNAME)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Spend per Person (USD)</div>', unsafe_allow_html=True)
        fig = px.line(sat_df,x='yr',y='spend_per_person_usd',color='country_en',color_discrete_sequence=COLORS,markers=True,labels={'spend_per_person_usd':'USD','yr':'','country_en':''})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">Revisit Rate (%)</div>', unsafe_allow_html=True)
        fig = px.line(sat_df,x='yr',y='revisit_rate',color='country_en',color_discrete_sequence=COLORS,markers=True,labels={'revisit_rate':'%','yr':'','country_en':''})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)

    st.markdown('<div class="lbl">Hallyu Spending Index</div>', unsafe_allow_html=True)
    hplot = hallyu_df.copy()
    hplot['date'] = hplot['year_month'].apply(lambda x:f"{x[:4]}-{x[4:]}")
    hplot['country_en'] = hplot['country'].map(CNAME)
    c3,c4 = st.columns(2)
    with c3:
        st.markdown('<div class="lbl">Total Hallyu Transactions</div>', unsafe_allow_html=True)
        fig = px.line(hplot,x='date',y='total_count',color='country_en',color_discrete_sequence=COLORS,labels={'total_count':'Transactions','date':'','country_en':''})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)
    with c4:
        st.markdown('<div class="lbl">Hallyu Category Breakdown (Latest)</div>', unsafe_allow_html=True)
        liym = hallyu_ind['year_month'].max()
        lind = hallyu_ind[hallyu_ind['year_month']==liym].copy()
        lind['cn'] = lind['country'].map(CNAME)
        fig = px.bar(lind,x='cn',y='ratio',color='industry',barmode='stack',
                     color_discrete_sequence=['#3b82f6','#ef4444','#10b981','#f59e0b','#8b5cf6','#ec4899','#06b6d4','#84cc16','#f97316'],
                     labels={'ratio':'%','cn':'','industry':''})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════════
elif page == "📈  Analytics":
    import plotly.express as px

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">
      Analytics</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">
      Explore trends by market and metric</p>
    """, unsafe_allow_html=True)

    df['country_en'] = df['country'].map(CNAME)
    c1,c2 = st.columns([2,1])
    with c1:
        ctry_f = st.multiselect("Markets",['중국','일본','대만','미국','홍콩'],
                                 default=['중국','일본','대만','미국','홍콩'],
                                 format_func=lambda x:CNAME[x])
    with c2:
        MMAP={'Visitor Count':'visitor_count','MoM Growth':'visitor_mom_growth',
              'SNS Buzz':'buzz_volume','Engagement':'engagement',
              'Potential Exposure':'potential_exposure','Positive Sentiment (%)':'positive_pct',
              'Hallyu Transactions':'hallyu_spend_count','Priority Score':'priority_score'}
        ml = st.selectbox("Metric",list(MMAP.keys()))
        met = MMAP[ml]

    dff = df[df['country'].isin(ctry_f)].copy()
    dff['date'] = dff['year_month'].apply(lambda x:f"{x[:4]}-{x[4:]}")

    fig = px.line(dff,x='date',y=met,color='country_en',color_discrete_sequence=COLORS,
                  labels={met:ml,'date':'','country_en':''})
    fig.update_traces(line=dict(width=2.5)); fig.update_layout(height=340,**CHART)
    st.plotly_chart(fig,use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Priority Label History</div>', unsafe_allow_html=True)
        if 'priority_label' in dff.columns:
            lc = dff.groupby(['country_en','priority_label']).size().reset_index(name='n')
            fig2 = px.bar(lc,x='country_en',y='n',color='priority_label',barmode='group',
                          color_discrete_map={'High':'#ef4444','Medium':'#f59e0b','Low':'#3b82f6'},
                          labels={'n':'Months','country_en':'','priority_label':''})
            fig2.update_layout(height=270,**CHART); st.plotly_chart(fig2,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">Market Share Trend</div>', unsafe_allow_html=True)
        sd = dff[['date','country_en','country_share']].dropna()
        fig3 = px.area(sd,x='date',y='country_share',color='country_en',color_discrete_sequence=COLORS,
                       labels={'country_share':'Share','date':'','country_en':''})
        fig3.update_layout(height=270,**CHART); st.plotly_chart(fig3,use_container_width=True)
