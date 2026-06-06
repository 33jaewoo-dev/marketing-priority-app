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
.country-card.high   { border-top-color:#4f46e5; }
.country-card.medium { border-top-color:#f59e0b; }
.country-card.low    { border-top-color:#94a3b8; }
.badge { display:inline-block; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700; font-family:'Outfit',sans-serif; letter-spacing:0.04em; }
.badge.high   { background:#eef2ff; color:#4338ca; border:1px solid #a5b4fc; }
.badge.medium { background:#fffbeb; color:#d97706; border:1px solid #fcd34d; }
.badge.low    { background:#f8fafc; color:#64748b; border:1px solid #cbd5e1; }
.conf-strong { background:#dcfce7; color:#15803d; border:1px solid #86efac; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600; }
.conf-moderate { background:#fef9c3; color:#854d0e; border:1px solid #fde047; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600; }
.conf-weak { background:#fee2e2; color:#dc2626; border:1px solid #fca5a5; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600; }
.lbl { font-size:10px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#94a3b8; margin-bottom:12px; }
.sig-row { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9; font-size:13px; }
.up   { color:#16a34a; font-weight:700; font-family:'Outfit',sans-serif; }
.down { color:#dc2626; font-weight:700; font-family:'Outfit',sans-serif; }
.neu  { color:#d97706; font-weight:700; font-family:'Outfit',sans-serif; }
.act { background:#f8fafc; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:3px solid #e2e8f0; }
.act.high-b   { border-left-color:#4f46e5; }
.act.medium-b { border-left-color:#f59e0b; }
.act.low-b    { border-left-color:#94a3b8; }
.act-title { font-size:13px; font-weight:600; color:#1e293b; margin-bottom:4px; }
.act-desc  { font-size:12px; color:#64748b; line-height:1.5; }
.result-box { border-radius:20px; padding:36px 24px; text-align:center; border:2px solid #e2e8f0; background:#ffffff; }
.driver-pill { display:inline-block; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600; margin:2px; }
.driver-pos { background:#eef2ff; color:#4338ca; }
.driver-neg { background:#fef2f2; color:#dc2626; }
.stButton > button {
    background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%) !important;
    color:#fff !important; border:none !important; border-radius:12px !important;
    font-family:'Outfit',sans-serif !important; font-weight:600 !important; font-size:15px !important; height:52px !important;
}
.stButton > button:hover { opacity:0.92 !important; transform:translateY(-1px) !important; }
.stTabs [data-baseweb="tab-list"] { background:#e2e8f0; border-radius:10px; padding:3px; gap:2px; }
.stTabs [data-baseweb="tab"] { border-radius:8px; color:#64748b !important; font-weight:500; }
.stTabs [aria-selected="true"] { background:#ffffff !important; color:#0f172a !important; box-shadow:0 1px 3px rgba(0,0,0,0.1) !important; }
hr { border-color:#e2e8f0 !important; margin:16px 0 !important; }
.insight-box { background:#f0f9ff; border-left:3px solid #0ea5e9; border-radius:0 10px 10px 0; padding:12px 16px; margin:12px 0; font-size:13px; color:#0c4a6e; line-height:1.6; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────
FLAG_URL = {'중국':'https://flagcdn.com/w40/cn.png','일본':'https://flagcdn.com/w40/jp.png',
            '대만':'https://flagcdn.com/w40/tw.png','미국':'https://flagcdn.com/w40/us.png','홍콩':'https://flagcdn.com/w40/hk.png'}
def flag(c, w=32): return f'<img src="{FLAG_URL.get(c,"")}" width="{w}" style="border-radius:3px;display:block;margin:0 auto;">'

CNAME  = {'중국':'China','일본':'Japan','대만':'Taiwan','미국':'USA','홍콩':'Hong Kong'}
PCOLOR = {'High':'#4f46e5','Medium':'#f59e0b','Low':'#64748b'}
PBDR   = {'High':'high','Medium':'medium','Low':'low'}
COLORS = ['#4f46e5','#f59e0b','#10b981','#ef4444','#8b5cf6']
CHART  = dict(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(248,250,252,0.6)',
              font=dict(family='Inter',color='#64748b',size=12),margin=dict(l=0,r=0,t=8,b=0),
              legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(size=11)),
              xaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0'),
              yaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0'))

INDUSTRY_EN = {
    'K-라이프스타일푸드': 'K-Lifestyle Food',
    'K-쇼핑':           'K-Shopping',
    'K-한식':           'K-Food',
    'K-뷰티웰니스':      'K-Beauty & Wellness',
    'K-패션':           'K-Fashion',
    'K-문화체험':        'K-Cultural Experience',
    'K-나이트컬처':      'K-Nightlife',
    'K-스포츠':         'K-Sports',
    'K-공연':           'K-Performances',
}

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

def confidence_label(prob):
    if prob >= 0.65: return "Strong", "conf-strong"
    elif prob >= 0.50: return "Moderate", "conf-moderate"
    else: return "Weak", "conf-weak"

def row_to_full_features(row):
    d = {}
    for f in FEATS:
        val = row.get(f, 0)
        try:    d[f] = float(val) if pd.notna(val) else 0.0
        except: d[f] = 0.0
    return d

def inp_to_full_features(inp_partial):
    return {f: float(inp_partial.get(f, 0) or 0) for f in FEATS}

# ── ML Model ──────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Initializing AI model...")
def load_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

    base = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base,'full_dataset.csv'), encoding='utf-8', dtype={'year_month':str})
    df['year_month'] = df['year_month'].astype(str).str.strip()

    dc = df[FEATS+['priority_label','year_month']].dropna()
    le = LabelEncoder()
    train_mask = dc['year_month'] <= '202412'
    test_mask  = (dc['year_month'] >= '202501') & (dc['year_month'] <= '202508')
    X_train = dc[train_mask][FEATS]; X_test = dc[test_mask][FEATS]
    y_train = le.fit_transform(dc[train_mask]['priority_label'])
    y_test  = le.transform(dc[test_mask]['priority_label'])

    rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight='balanced')
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_acc  = accuracy_score(y_test, rf_pred)
    cm      = confusion_matrix(y_test, rf_pred)
    cr      = classification_report(y_test, rf_pred, target_names=le.classes_, output_dict=True)

    scaler = StandardScaler()
    lr = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    lr.fit(scaler.fit_transform(X_train), y_train)
    lr_acc = accuracy_score(y_test, lr.predict(scaler.transform(X_test)))

    def rule_pred_fn(row):
        if row['visitor_count']>300000 and row['visitor_mom_growth']>0.05: return le.transform(['High'])[0]
        elif row['visitor_count']<100000 or row['visitor_mom_growth']<-0.15: return le.transform(['Low'])[0]
        else: return le.transform(['Medium'])[0]
    rule_acc = accuracy_score(y_test, dc[test_mask].apply(rule_pred_fn, axis=1))

    fi = pd.DataFrame({'feature':FEATS,'importance':rf.feature_importances_}).sort_values('importance',ascending=False)
    metrics = {'rf_acc':rf_acc,'lr_acc':lr_acc,'rule_acc':rule_acc,'cm':cm,'cr':cr,
               'classes':le.classes_,'train_n':len(X_train),'test_n':len(X_test)}
    return rf, le, fi, metrics

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    df  = pd.read_csv(os.path.join(base,'full_dataset.csv'), encoding='utf-8', dtype={'year_month':str})
    sat = pd.read_csv(os.path.join(base,'satisfaction_data.csv'), encoding='utf-8')
    hsp = pd.read_csv(os.path.join(base,'korean_wave_spending.csv'), encoding='utf-8', dtype={'year_month':str})
    hid = pd.read_csv(os.path.join(base,'korean_wave_industry.csv'), encoding='utf-8', dtype={'year_month':str})
    df['year_month'] = df['year_month'].astype(str).str.strip()
    hid['industry_en'] = hid['industry'].map(INDUSTRY_EN).fillna(hid['industry'])
    return df, sat, hsp, hid

model, le, feat_imp, metrics = load_model()
df, sat_df, hallyu_df, hallyu_ind = load_data()
latest_month = df['year_month'].max()
ym_disp = f"{latest_month[:4]}.{latest_month[4:]}"

def get_ml_prediction(inp_full):
    idf = pd.DataFrame([inp_full])[FEATS]
    proba = model.predict_proba(idf)[0]
    pred  = le.inverse_transform(model.predict(idf))[0]
    prob_dict = {cls: proba[i] for i,cls in enumerate(le.classes_)}
    ml_score  = round(prob_dict['High'] * 100, 1)
    return pred, prob_dict, ml_score

def get_market_signals(inp):
    pos = [(n,v) for n,v,t in [
        ('Visitor volume',    inp['visitor_count'],        200000),
        ('Visitor momentum',  inp['visitor_mom_growth'],   0.05),
        ('SNS engagement',    inp['engagement'],           200000),
        ('Buzz volume',       inp['buzz_volume'],          30000),
        ('Positive sentiment',inp['positive_pct'],         65),
        ('Korean Wave spend', inp['hallyu_spend_count'],   200000),
    ] if v > t]
    neg = [(n,v) for n,v,t in [
        ('Visitor crash',     inp['visitor_mom_growth'],  -0.15),
        ('Negative sentiment',inp['positive_pct'],         50),
    ] if v < t]
    return pos[:2], neg[:1]

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 24px;">
      <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:800;color:#0f172a;line-height:1.2;letter-spacing:-0.02em;">
        Inbound Marketing<br/><span style="color:#4f46e5;">Intelligence</span></div>
      <div style="font-size:10px;color:#94a3b8;margin-top:6px;letter-spacing:0.1em;text-transform:uppercase;">Korea Tourism AI Platform</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("", ["📊  Overview","🔮  Priority Engine","💰  Budget Planner",
                          "👤  Market Profiles","📈  Analytics","🔬  Methodology"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px;color:#94a3b8;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">Latest Data</div>
    <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;color:#0f172a;">{ym_disp}</div>
    <div style="font-size:11px;color:#94a3b8;margin-top:2px;">Korea Tourism Data Lab</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    flag_row = "".join([f'<img src="{FLAG_URL[c]}" width="18" style="border-radius:2px;margin-right:3px;">' for c in ['중국','일본','대만','미국','홍콩']])
    st.markdown(f"""
    <div style="font-size:12px;color:#64748b;line-height:2.2;">
      <b style="color:#334155;">Model</b><br/>Random Forest · {metrics['rf_acc']*100:.1f}% Accuracy<br/>
      <b style="color:#334155;">Split</b><br/>Time-based (~2024 train / 2025 test)<br/>
      <b style="color:#334155;">Data</b><br/>KTO · SNS · Korean Wave Index<br/>
      <b style="color:#334155;">Markets</b><br/>{flag_row}
    </div>
    <div style="font-size:11px;color:#94a3b8;margin-top:16px;">Last updated: {ym_disp}</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page == "📊  Overview":
    import plotly.express as px

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">Marketing Priority Dashboard</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:8px;">
      Tourism marketers must decide which inbound markets deserve more campaign budget under limited resources.
      This system supports data-driven market prioritization by combining visitor demand, SNS attention,
      Korean Wave consumption, and macro indicators.</p>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="insight-box"><b>How to use:</b>
    (1) Check ML priority ranking below &nbsp;→&nbsp;
    (2) Review visitor &amp; SNS trends &nbsp;→&nbsp;
    (3) Open <b>Priority Engine</b> for scenario simulation &nbsp;→&nbsp;
    (4) Use <b>Budget Planner</b> for budget allocation recommendations</div>""", unsafe_allow_html=True)

    latest_raw = df[df['year_month']==latest_month].copy()
    if 'ml_priority_score' not in latest_raw.columns or latest_raw['ml_priority_score'].isna().all():
        scores, preds = [], []
        for _, row in latest_raw.iterrows():
            pred, prob_dict, ml_score = get_ml_prediction(row_to_full_features(row))
            scores.append(ml_score); preds.append(pred)
        latest_raw['ml_priority_score'] = scores
        latest_raw['ml_pred_label'] = preds
    latest_sorted = latest_raw.sort_values('ml_priority_score', ascending=False)

    st.markdown(f'<div class="lbl" style="margin-top:16px;">ML Priority Ranking — {ym_disp} · Random Forest · {metrics["rf_acc"]*100:.1f}% Test Accuracy</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (_, row) in enumerate(latest_sorted.iterrows()):
        lbl  = row.get('ml_pred_label', row.get('priority_label','N/A'))
        clr  = PCOLOR.get(lbl,'#888')
        rank = ['1st','2nd','3rd','4th','5th'][i]
        mom  = float(row.get('visitor_mom_growth',0) or 0)
        ms   = float(row.get('ml_priority_score',0) or 0)
        hp   = ms / 100.0
        conf_label, conf_cls = confidence_label(hp)
        inp_s = row_to_full_features(row)
        pos_d, neg_d = get_market_signals(inp_s)
        driver_html = "".join([f'<span class="driver-pill driver-pos">↑ {n}</span>' for n,_ in pos_d])
        driver_html += "".join([f'<span class="driver-pill driver-neg">↓ {n}</span>' for n,_ in neg_d])
        with cols[i]:
            st.markdown(f"""
            <div class="country-card {PBDR.get(lbl,'low')}">
              <div style="font-size:10px;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">{rank}</div>
              <div style="margin-bottom:10px;">{flag(row['country'],36)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:15px;font-weight:700;color:#0f172a;margin-bottom:8px;">{CNAME.get(row['country'],row['country'])}</div>
              <span class="badge {PBDR.get(lbl,'low')}">{lbl}</span>
              <div style="margin-top:12px;padding-top:10px;border-top:1px solid #f1f5f9;">
                <div style="font-size:10px;color:#94a3b8;margin-bottom:2px;">ML Priority Score</div>
                <div style="font-family:'Outfit',sans-serif;font-size:26px;font-weight:800;color:{clr};">{ms:.1f}<span style="font-size:13px;color:#94a3b8;">/100</span></div>
                <div style="font-size:11px;color:#94a3b8;">High Probability: <b style="color:{clr};">{ms:.0f}%</b></div>
                <div style="margin:4px 0;"><span class="{conf_cls}">{conf_label} Confidence</span></div>
                <div style="font-size:11px;font-weight:600;color:{'#16a34a' if mom>0 else '#dc2626'};margin-top:4px;">{'▲' if mom>0 else '▼'} {abs(mom*100):.1f}% MoM</div>
                <div style="font-size:11px;color:#94a3b8;">{int(row.get('visitor_count',0) or 0):,} visitors</div>
              </div>
              <div style="margin-top:10px;padding-top:8px;border-top:1px solid #f1f5f9;text-align:left;">
                <div style="font-size:10px;color:#94a3b8;margin-bottom:4px;">Observable Market Signals</div>
                {driver_html if driver_html else '<span style="font-size:11px;color:#94a3b8;">No dominant signal</span>'}
                <div style="font-size:9px;color:#cbd5e1;margin-top:4px;font-style:italic;">Not causal attribution</div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    df_p = df.copy()
    df_p['date'] = df_p['year_month'].apply(lambda x: f"{x[:4]}-{x[4:]}")
    df_p['Market'] = df_p['country'].map(CNAME)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Monthly Visitor Trends</div>', unsafe_allow_html=True)
        fig = px.line(df_p,x='date',y='visitor_count',color='Market',color_discrete_sequence=COLORS,labels={'visitor_count':'Visitors','date':'','Market':'Market'})
        fig.update_traces(line=dict(width=2.5)); fig.update_layout(height=300,**CHART)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">SNS Engagement Trends</div>', unsafe_allow_html=True)
        fig2 = px.line(df_p,x='date',y='engagement',color='Market',color_discrete_sequence=COLORS,labels={'engagement':'Engagement','date':'','Market':'Market'})
        fig2.update_traces(line=dict(width=2.5)); fig2.update_layout(height=300,**CHART)
        st.plotly_chart(fig2,use_container_width=True)

    c3,c4 = st.columns(2)
    with c3:
        st.markdown('<div class="lbl">Positive Sentiment (%) — Thresholds Used in Proxy Label Construction</div>', unsafe_allow_html=True)
        fig3 = px.line(df_p,x='date',y='positive_pct',color='Market',color_discrete_sequence=COLORS,labels={'positive_pct':'%','date':'','Market':'Market'})
        fig3.update_traces(line=dict(width=2.5))
        fig3.add_hline(y=55,line_dash='dash',line_color='#94a3b8',annotation_text='Neutral')
        fig3.add_hline(y=40,line_dash='dot',line_color='#ef4444',annotation_text='Critical')
        fig3.update_layout(height=280,**CHART); st.plotly_chart(fig3,use_container_width=True)
    with c4:
        st.markdown('<div class="lbl">Feature Importance — Top 10</div>', unsafe_allow_html=True)
        fi_d = feat_imp.head(10).copy()
        fi_d['Feature'] = fi_d['feature'].str.replace('_',' ').str.title()
        fig4 = px.bar(fi_d,x='importance',y='Feature',orientation='h',color='importance',color_continuous_scale=['#e0e7ff','#4f46e5','#3730a3'])
        fig4.update_layout(height=280,showlegend=False,coloraxis_showscale=False,**CHART)
        fig4.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig4,use_container_width=True)
        top3 = feat_imp.head(3)['feature'].str.replace('_',' ').tolist()
        st.markdown(f'<div class="insight-box">The model places the highest weight on <b>{top3[0]}</b>, <b>{top3[1]}</b>, and <b>{top3[2]}</b>, suggesting that both actual tourism demand and digital attention are important for priority classification.</div>', unsafe_allow_html=True)

    st.markdown('<div class="lbl">Model Performance</div>', unsafe_allow_html=True)
    mc = st.columns(5)
    m = metrics
    for col,l,v,s in [
        (mc[0],"Algorithm","Random Forest","200 estimators · depth 10"),
        (mc[1],"Test Accuracy",f"{m['rf_acc']*100:.1f}%","Time-based split"),
        (mc[2],"High Priority F1",f"{m['cr']['High']['f1-score']:.2f}","Prec {:.0f}% · Rec {:.0f}%".format(m['cr']['High']['precision']*100,m['cr']['High']['recall']*100)),
        (mc[3],"Train Period","2018.11 – 2024.12",f"{m['train_n']} samples"),
        (mc[4],"Test Period","2025.01 – 2025.08",f"{m['test_n']} samples"),
    ]:
        with col:
            st.markdown(f"""<div class="card" style="padding:18px 20px;">
              <div style="font-size:10px;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">{l}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:19px;font-weight:700;color:#0f172a;">{v}</div>
              <div style="font-size:11px;color:#94a3b8;margin-top:4px;">{s}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PRIORITY ENGINE
# ══════════════════════════════════════════════════════════════════
elif page == "🔮  Priority Engine":
    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">Priority Engine</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:16px;">
      Adjust market indicators — the Random Forest model predicts marketing priority using all 29 input features.</p>
    """, unsafe_allow_html=True)

    mode = st.radio("", ["📋  Standard Input","⚡  What-If Scenario"], horizontal=True, label_visibility="collapsed")
    st.markdown("<br/>", unsafe_allow_html=True)
    country_sel = st.selectbox("Select Market",['중국','일본','대만','미국','홍콩'],format_func=lambda x:CNAME[x])
    cd = df[df['country']==country_sel].sort_values('year_month').iloc[-1]

    if "Standard" in mode:
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
                visitor_3m_avg = st.number_input("3-Month Moving Average",value=float(cd['visitor_3m_avg']),step=1000.0)
                visitor_6m_avg = st.number_input("6-Month Moving Average",value=float(cd['visitor_6m_avg']),step=1000.0)
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
                                         help="Sentiment ML input signal. Below 40% is historically associated with Low Priority cases.")
            negative_pct = 100.0 - positive_pct
            if positive_pct < 40:
                st.error("🚨 Below 40%: historically associated with Low Priority cases (e.g., geopolitical tensions)")
            elif positive_pct < 50:
                st.warning("⚠️ Below 50%: negative sentiment may suppress predicted priority")
        with t3:
            c1,c2,c3 = st.columns(3)
            with c1: month = st.selectbox("Reference Month",list(range(1,13)),index=int(cd['month'])-1,
                                           help="Months 3, 4, 5, 9, 10 are peak season in historical data")
            with c2: exchange_rate = st.number_input("Exchange Rate (KRW)",value=float(cd['exchange_rate']),step=1.0,
                                                      help="Higher rate = weaker KRW = Korea more affordable for foreign tourists")
            with c3: oil_price = st.number_input("Oil Price (USD/barrel)",value=float(cd['oil_price']),step=1.0,
                                                   help="Higher oil price = higher airfare = historically associated with reduced travel demand")

        vmom = (visitor_count-visitor_lag1)/visitor_lag1 if visitor_lag1 else 0
        vvs3 = visitor_count/visitor_3m_avg if visitor_3m_avg else 1
        vstd = float(cd.get('visitor_rolling_std',0) or 0)
        bl1  = float(cd.get('buzz_lag1',buzz_volume) or buzz_volume)
        el1  = float(cd.get('engagement_lag1',engagement) or engagement)
        exl1 = float(cd.get('exposure_lag1',potential_exposure) or potential_exposure)
        bmom = (buzz_volume-bl1)/bl1 if bl1 else 0
        emom = (engagement-el1)/el1 if el1 else 0
        exmom= (potential_exposure-exl1)/exl1 if exl1 else 0
        epv  = engagement/visitor_count if visitor_count else 0
        bpv  = buzz_volume/visitor_count if visitor_count else 0
        b3m  = float(cd.get('buzz_3m_avg',buzz_volume) or buzz_volume)
        bvs3 = buzz_volume/b3m if b3m else 1
        qtr  = (month-1)//3+1; peak = 1 if month in [3,4,5,9,10] else 0
        hc   = float(cd.get('hallyu_spend_count',0) or 0)
        hl1  = float(cd.get('hallyu_lag1',hc) or hc)
        hmom = (hc-hl1)/hl1 if hl1 else 0
        hpv  = hc/visitor_count if visitor_count else 0

        inp = inp_to_full_features({
            'visitor_count':visitor_count,'visitor_lag1':visitor_lag1,'visitor_lag2':visitor_lag2,
            'visitor_lag3':visitor_lag3,'visitor_mom_growth':vmom,'visitor_3m_avg':visitor_3m_avg,
            'visitor_6m_avg':visitor_6m_avg,'visitor_vs_3m_avg':vvs3,'visitor_rolling_std':vstd,
            'country_share':country_share,'buzz_volume':buzz_volume,'engagement':engagement,
            'potential_exposure':potential_exposure,'buzz_mom_growth':bmom,
            'engagement_mom_growth':emom,'exposure_mom_growth':exmom,
            'engagement_per_visitor':epv,'buzz_per_visitor':bpv,'buzz_vs_3m_avg':bvs3,
            'positive_pct':positive_pct,'negative_pct':negative_pct,
            'hallyu_spend_count':hc,'hallyu_mom_growth':hmom,'hallyu_per_visitor':hpv,
            'month':month,'quarter':qtr,'is_peak_season':peak,
            'exchange_rate':exchange_rate,'oil_price':oil_price,
        })

    else:  # What-If
        st.markdown('<div class="lbl">What-If Scenario Simulator</div>', unsafe_allow_html=True)
        st.markdown("Simulate how changes in market conditions affect the ML priority prediction.")
        cd_full = row_to_full_features(cd)
        c1,c2 = st.columns(2)
        with c1:
            v_chg  = st.slider("Visitor Count Change (%)",   -50,50,0,5)
            s_chg  = st.slider("SNS Engagement Change (%)",  -50,50,0,5)
            bz_chg = st.slider("Buzz Volume Change (%)",     -50,50,0,5)
        with c2:
            se_chg = st.slider("Positive Sentiment Change (pp)", -20,20,0,1)
            oi_chg = st.slider("Oil Price Change (%)",      -30,50,0,5)
            ex_chg = st.slider("Exchange Rate Change (%)",  -20,20,0,2)

        inp = cd_full.copy()
        bvc = inp['visitor_count']
        inp['visitor_count']      = bvc*(1+v_chg/100)
        inp['visitor_mom_growth'] = (inp['visitor_count']-inp['visitor_lag1'])/inp['visitor_lag1'] if inp['visitor_lag1'] else 0
        inp['visitor_vs_3m_avg']  = inp['visitor_count']/inp['visitor_3m_avg'] if inp['visitor_3m_avg'] else 1
        inp['engagement']         = inp['engagement']*(1+s_chg/100)
        inp['buzz_volume']        = inp['buzz_volume']*(1+bz_chg/100)
        inp['positive_pct']       = max(0,min(100,inp['positive_pct']+se_chg))
        inp['negative_pct']       = 100-inp['positive_pct']
        inp['oil_price']          = inp['oil_price']*(1+oi_chg/100)
        inp['exchange_rate']      = inp['exchange_rate']*(1+ex_chg/100)

    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("🤖  Run ML Priority Prediction", use_container_width=True):
        pred, prob_dict, ml_score = get_ml_prediction(inp)
        lbl = pred; clr = PCOLOR[lbl]; cn = CNAME[country_sel]
        conf_label, conf_cls = confidence_label(prob_dict[lbl])

        cd_full_base = row_to_full_features(cd)
        base_pred, base_probs, base_score = get_ml_prediction(cd_full_base)
        diff        = round(ml_score - base_score, 1)
        high_diff   = round((prob_dict['High'] - base_probs['High']) * 100, 1)

        pos_d, neg_d = get_market_signals(inp)
        st.markdown('<div class="lbl">Prediction Results</div>', unsafe_allow_html=True)
        r1,r2,r3 = st.columns([1.1,1,1.2])

        with r1:
            tags = []
            if inp.get('is_peak_season'): tags.append("✨ Peak season")
            if inp.get('positive_pct',50) < 50: tags.append("⚠️ Sentiment risk")
            if inp.get('visitor_mom_growth',0) < -0.15: tags.append("🔴 Visitor drop")
            tag_html  = "&nbsp;".join([f'<span style="background:#f1f5f9;border-radius:6px;padding:3px 8px;font-size:10px;color:#475569;">{t}</span>' for t in tags])
            diff_html = f'<span style="color:{"#16a34a" if diff>=0 else "#dc2626"};font-size:12px;font-weight:600;">{"▲" if diff>=0 else "▼"} {abs(diff):.1f} pts vs baseline</span>'
            pos_pills = "".join([f'<span class="driver-pill driver-pos">↑ {n}</span>' for n,_ in pos_d])
            neg_pills = "".join([f'<span class="driver-pill driver-neg">↓ {n}</span>' for n,_ in neg_d])

            st.markdown(f"""
            <div class="result-box" style="border-top:4px solid {clr};">
              <div style="margin-bottom:12px;">{flag(country_sel,48)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;color:#0f172a;margin-bottom:12px;">{cn}</div>
              <span class="badge {PBDR[lbl]}" style="font-size:13px;padding:5px 16px;">{lbl} Priority</span>
              &nbsp;<span class="{conf_cls}">{conf_label} Confidence</span>
              <div style="margin:18px 0 6px;">
                <div style="font-size:10px;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">ML Priority Score</div>
                <div style="font-size:10px;color:#94a3b8;margin-bottom:4px;">High Priority Probability × 100</div>
                <div style="font-family:'Outfit',sans-serif;font-size:58px;font-weight:800;color:{clr};letter-spacing:-0.04em;line-height:1;">{ml_score}</div>
                <div style="font-size:14px;color:#94a3b8;margin-bottom:6px;">/ 100 &nbsp;·&nbsp; High prob: <b style="color:{clr};">{prob_dict['High']*100:.0f}%</b></div>
                <div>{diff_html}</div>
              </div>
              <div style="background:#f1f5f9;border-radius:8px;height:10px;margin:12px 0 6px;overflow:hidden;">
                <div style="width:{ml_score}%;height:100%;background:linear-gradient(90deg,{clr}88,{clr});border-radius:8px;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:#94a3b8;margin-bottom:14px;"><span>0</span><span>50</span><span>100</span></div>
              <div style="margin-bottom:10px;">{pos_pills}{neg_pills}</div>
              <div>{tag_html}</div>
            </div>""", unsafe_allow_html=True)

            # What-if interpretation
            if "What" in mode:
                direction = "remains" if pred == base_pred else f"changes from {base_pred} to {pred}"
                high_dir  = "increases" if high_diff >= 0 else "decreases"
                changes = []
                if v_chg != 0: changes.append(f"visitor count ({'+' if v_chg>0 else ''}{v_chg}%)")
                if s_chg != 0: changes.append(f"SNS engagement ({'+' if s_chg>0 else ''}{s_chg}%)")
                if se_chg != 0: changes.append(f"sentiment ({'+' if se_chg>0 else ''}{se_chg}pp)")
                if bz_chg != 0: changes.append(f"buzz volume ({'+' if bz_chg>0 else ''}{bz_chg}%)")
                change_str = ", ".join(changes) if changes else "no significant changes"
                st.markdown(f"""<div class="insight-box" style="margin-top:12px;font-size:12px;">
                  <b>Scenario interpretation:</b> Under this scenario, {cn} {direction}, and the High Priority probability
                  {high_dir} by {abs(high_diff):.1f} percentage points due to {change_str}.
                </div>""", unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="lbl" style="margin-top:0;">Key Market Signals</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#94a3b8;margin-bottom:8px;line-height:1.5;">Observable market signals used as ML inputs. Not causal attribution.</div>', unsafe_allow_html=True)

            def scls(v,t=0.05):
                if v>t: return "up","▲"
                if v<-t: return "down","▼"
                return "neu","━"

            sigs = [
                ("Visitor MoM Growth",    inp.get('visitor_mom_growth',0),   f"{inp.get('visitor_mom_growth',0)*100:+.1f}%",  "Month-over-month visitor change"),
                ("Buzz Volume Change",    inp.get('buzz_mom_growth',0),       f"{inp.get('buzz_mom_growth',0)*100:+.1f}%",    "SNS mention volume vs last month"),
                ("Engagement Change",     inp.get('engagement_mom_growth',0), f"{inp.get('engagement_mom_growth',0)*100:+.1f}%","SNS reactions vs last month"),
                ("vs 3M Average",         inp.get('visitor_vs_3m_avg',1)-1,   f"{(inp.get('visitor_vs_3m_avg',1)-1)*100:+.1f}%","Current vs 3-month average"),
                ("Positive Sentiment",    (inp.get('positive_pct',50)-55)/100,f"{inp.get('positive_pct',50):.1f}%",           "ML input signal"),
                ("Market Share",          (inp.get('country_share',0.2)-0.2)/0.2,f"{inp.get('country_share',0.2)*100:.1f}%", "Share of 5-market total"),
            ]
            html=""
            for name,val,disp,desc in sigs:
                cls,arrow = scls(val)
                html+=f"""<div class="sig-row">
                  <div><div style="color:#475569;font-weight:500;">{name}</div><div style="font-size:11px;color:#94a3b8;">{desc}</div></div>
                  <div class="{cls}">{arrow} {disp}</div></div>"""
            st.markdown(html, unsafe_allow_html=True)
            st.markdown("<br/>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:11px;color:#94a3b8;margin-bottom:8px;">Classification Probability</div>', unsafe_allow_html=True)
            for cn_l,p in [('High',prob_dict['High']),('Medium',prob_dict['Medium']),('Low',prob_dict['Low'])]:
                c2c = PCOLOR[cn_l]
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
                  <div style="width:56px;font-size:12px;color:#64748b;">{cn_l}</div>
                  <div style="flex:1;background:#f1f5f9;border-radius:4px;height:8px;overflow:hidden;">
                    <div style="width:{int(p*100)}%;height:100%;background:{c2c};border-radius:4px;"></div></div>
                  <div style="width:36px;text-align:right;font-family:'Outfit',sans-serif;font-size:12px;font-weight:700;color:{c2c};">{int(p*100)}%</div>
                </div>""", unsafe_allow_html=True)

        with r3:
            clr2=PCOLOR[lbl]; bc=PBDR[lbl]; cn3=CNAME[country_sel]
            sat_row = sat_df[sat_df['country']==country_sel]
            spend   = float(sat_row['spend_per_person_usd'].iloc[-1]) if not sat_row.empty else 0
            stay    = float(sat_row['stay_days'].iloc[-1]) if not sat_row.empty else 0
            revisit = float(sat_row['revisit_rate'].iloc[-1]) if not sat_row.empty else 0

            RECS = {
                'High':   ("Aggressive Offensive Strategy","Visitor volume, SNS, and sentiment signals are all strong.","Increase Budget","#eef2ff"),
                'Medium': ("Monitor & Optimize","Mid-tier signals. Watch for momentum before scaling.","Maintain Budget","#fffbeb"),
                'Low':    ("Reallocate & Monitor","Low signals. Redirect resources to higher-priority markets.","Minimize Budget","#f8fafc"),
            }
            title,desc,blbl,bg = RECS[lbl]
            actions = []
            if lbl=='High':
                actions += [("Budget Expansion",f"Increase {cn3}-specific ad spend 20–30% vs. last month"),
                            ("Local Language Content",f"Scale up {cn3}-language SNS content and influencer collaborations")]
                if spend>1500: actions.append(("Premium Targeting",f"High spend/person (${spend:,.0f}) — focus on premium travel packages"))
                if revisit>70: actions.append(("Loyalty Program",f"Revisit rate {revisit:.0f}% — strengthen repeat visitor rewards"))
                actions.append(("Korean Wave Push","Rising Korean Wave spending — link K-beauty and K-pop to campaigns"))
            elif lbl=='Medium':
                actions += [("Hold Steady","Maintain current campaign — monitor weekly KPIs"),
                            ("A/B Testing","Test new creative formats at moderate budget")]
                if stay>5: actions.append(("Long-Stay Bundle",f"Average stay {stay:.0f} days — offer multi-destination packages"))
                actions.append(("Trigger Plan","Upgrade strategy if MoM visitor growth exceeds +15%"))
            else:
                actions += [("Reallocate",f"Shift {cn3} budget to High-priority markets"),
                            ("Root Cause Analysis","Diagnose: geopolitical tensions, flight capacity, or seasonal factors?")]
                if revisit>60: actions.append(("Retention Focus",f"Revisit rate {revisit:.0f}% — target returning visitors rather than new acquisition"))
                actions.append(("Recovery Watch","Re-engage when MoM rebounds above +10%"))

            st.markdown('<div class="lbl" style="margin-top:0;">Strategic Recommendations</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="background:{bg};border:1px solid {clr2}33;border-radius:12px;padding:16px 18px;margin-bottom:14px;">
              <div style="font-family:'Outfit',sans-serif;font-size:16px;font-weight:700;color:{clr2};margin-bottom:6px;">{title}</div>
              <div style="font-size:12px;color:#64748b;line-height:1.5;margin-bottom:10px;">{desc}</div>
              <span style="background:{clr2};color:#fff;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:600;">{blbl}</span>
            </div>""", unsafe_allow_html=True)
            for at,ad in actions:
                st.markdown(f"""<div class="act {bc}-b"><div class="act-title">{at}</div><div class="act-desc">{ad}</div></div>""", unsafe_allow_html=True)
            if inp.get('positive_pct',50)<40:
                st.markdown("""<div class="act" style="border-left-color:#dc2626;background:#fef2f2;"><div class="act-title">🚨 Crisis Communication</div><div class="act-desc">Identify root cause of negative sentiment. Activate PR response immediately.</div></div>""", unsafe_allow_html=True)
            if inp.get('visitor_mom_growth',0)<-0.30:
                st.markdown("""<div class="act" style="border-left-color:#dc2626;background:#fef2f2;"><div class="act-title">🚨 Visitor Crash Response</div><div class="act-desc">Investigate cause — diplomatic tensions, flight suspensions, or external shocks.</div></div>""", unsafe_allow_html=True)
            if inp.get('is_peak_season'):
                st.markdown(f"""<div class="act" style="border-left-color:#10b981;background:#f0fdf4;"><div class="act-title">✨ Peak Season Opportunity</div><div class="act-desc">Month {int(inp.get('month',4))} is peak season — optimal timing for campaign launch.</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# BUDGET PLANNER
# ══════════════════════════════════════════════════════════════════
elif page == "💰  Budget Planner":
    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">Budget Planner</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:16px;">
      ML-predicted priority scores drive recommended budget allocation across markets.</p>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="insight-box">
      Markets classified as High Priority receive a minimum floor allocation, while the remaining budget is distributed
      proportionally to ML Priority Scores. This keeps strategic presence in promising markets while concentrating
      budget toward stronger signals.
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([1,1,1])
    with c1:
        total_budget = st.number_input("Total Marketing Budget (KRW)", value=100000000, step=10000000, format="%d")
    with c2:
        currency = st.selectbox("Display Currency", ["KRW (₩)","USD ($)","JPY (¥)"])
        fx  = {'KRW (₩)':1,'USD ($)':1380,'JPY (¥)':0.0092}[currency]
        sym = {'KRW (₩)':'₩','USD ($)':'$','JPY (¥)':'¥'}[currency]
    with c3:
        alloc_mode = st.selectbox("Allocation Mode", ["Balanced","Aggressive","Conservative"],
                                   help="Balanced: standard floors. Aggressive: concentrate on top markets. Conservative: ensure broader market presence.")

    floors_map = {
        'Balanced':     {'High':0.15,'Medium':0.08,'Low':0.04},
        'Aggressive':   {'High':0.10,'Medium':0.05,'Low':0.02},
        'Conservative': {'High':0.18,'Medium':0.10,'Low':0.06},
    }
    floors = floors_map[alloc_mode]

    latest_raw = df[df['year_month']==latest_month].copy()
    if 'ml_priority_score' not in latest_raw.columns or latest_raw['ml_priority_score'].isna().all():
        scores, preds = [], []
        for _, row in latest_raw.iterrows():
            pred, prob_dict, ml_score = get_ml_prediction(row_to_full_features(row))
            scores.append(ml_score); preds.append(pred)
        latest_raw['ml_priority_score'] = scores
        latest_raw['ml_pred_label'] = preds

    alloc_data = []
    for _, row in latest_raw.iterrows():
        lbl = row.get('ml_pred_label', row.get('priority_label','Low'))
        ms  = float(row.get('ml_priority_score', 0) or 0)
        hp  = ms / 100.0
        conf_l, _ = confidence_label(hp)
        alloc_data.append({'country':row['country'],'country_en':CNAME.get(row['country'],''),
                           'pred':lbl,'ml_score':ms,'high_prob':hp,'confidence':conf_l,
                           'visitor_count':row.get('visitor_count',0),'visitor_mom_growth':row.get('visitor_mom_growth',0)})

    alloc_df = pd.DataFrame(alloc_data).sort_values('ml_score',ascending=False)
    alloc_df['floor'] = alloc_df['pred'].map(floors)
    score_sum = alloc_df['ml_score'].sum()
    remaining = 1 - alloc_df['floor'].sum()
    alloc_df['extra']  = alloc_df['ml_score']/score_sum * remaining
    alloc_df['share']  = (alloc_df['floor'] + alloc_df['extra'])
    alloc_df['share']  = alloc_df['share']/alloc_df['share'].sum()
    alloc_df['budget'] = alloc_df['share']*total_budget

    st.markdown('<div class="lbl">Recommended Budget Allocation</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (_, r) in enumerate(alloc_df.iterrows()):
        clr = PCOLOR[r['pred']]
        _, conf_cls = confidence_label(r['high_prob'])
        budget_disp = r['budget']/fx
        fmt = f"{sym}{budget_disp:,.0f}"
        with cols[i]:
            st.markdown(f"""
            <div class="country-card {PBDR[r['pred']]}">
              <div style="margin-bottom:8px;">{flag(r['country'],32)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:14px;font-weight:700;color:#0f172a;margin-bottom:6px;">{r['country_en']}</div>
              <span class="badge {PBDR[r['pred']]}">{r['pred']}</span>
              <div style="margin-top:12px;">
                <div style="font-size:10px;color:#94a3b8;">Recommended Share</div>
                <div style="font-family:'Outfit',sans-serif;font-size:24px;font-weight:800;color:{clr};">{r['share']*100:.1f}%</div>
                <div style="font-size:13px;font-weight:600;color:#334155;">{fmt}</div>
                <div style="font-size:11px;color:#94a3b8;margin-top:4px;">ML Score: {r['ml_score']:.1f} · High: {r['high_prob']*100:.0f}%</div>
                <div style="margin-top:4px;"><span class="{conf_cls}">{r['confidence']} Confidence</span></div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Budget Share by Market</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(labels=alloc_df['country_en'],values=alloc_df['share']*100,marker_colors=COLORS,hole=0.4,textinfo='label+percent'))
        fig.update_layout(height=300,**CHART,showlegend=False); st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">Recommended Budget Amount</div>', unsafe_allow_html=True)
        alloc_df['Budget'] = alloc_df['budget']/fx
        fig2 = px.bar(alloc_df,x='country_en',y='Budget',color='pred',
                      color_discrete_map={'High':'#4f46e5','Medium':'#f59e0b','Low':'#94a3b8'},
                      labels={'Budget':f'Budget ({sym})','country_en':'','pred':'Priority'})
        fig2.update_layout(height=300,**CHART); st.plotly_chart(fig2,use_container_width=True)

    st.markdown('<div class="lbl">Detailed Allocation Table</div>', unsafe_allow_html=True)
    disp_df = alloc_df[['country_en','pred','ml_score','high_prob','confidence','share','budget']].copy()
    disp_df.columns = ['Market','Predicted Priority','ML Priority Score','High Probability','Confidence','Share (%)','Budget (KRW)']
    disp_df['Share (%)']       = (disp_df['Share (%)']*100).round(1)
    disp_df['High Probability']= (disp_df['High Probability']*100).round(1).astype(str)+'%'
    disp_df['Budget (KRW)']    = disp_df['Budget (KRW)'].apply(lambda x:f"₩{x:,.0f}")
    disp_df['ML Priority Score']= disp_df['ML Priority Score'].round(1)
    st.dataframe(disp_df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# MARKET PROFILES
# ══════════════════════════════════════════════════════════════════
elif page == "👤  Market Profiles":
    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">Market Profiles</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">Traveler behavior, satisfaction, and Korean Wave consumption by market (2015–2024)</p>
    """, unsafe_allow_html=True)

    IMPLICATIONS = {
        '중국': ("Package + Korean Wave Campaign","High visitor volume and strong Korean Wave spending — bundle K-beauty and K-pop"),
        '일본': ("Repeat Visitor Promotion","High revisit rate — focus on loyalty programs and short-trip packages"),
        '대만': ("SNS-Driven Influencer Campaign","Strong SNS engagement — influencer and UGC-led campaigns work well"),
        '미국': ("Premium Long-Haul Package","Highest spend/person — target high-value travelers with premium experiences"),
        '홍콩': ("City-Break Bundle","Short average stay — position Korea as a convenient weekend destination"),
    }
    ly = sat_df['year'].max(); lsat = sat_df[sat_df['year']==ly]
    st.markdown(f'<div class="lbl">Traveler Profile Summary — {ly}</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i,ctry in enumerate(['중국','일본','대만','미국','홍콩']):
        row = lsat[lsat['country']==ctry]
        if row.empty: continue
        r = row.iloc[0]
        impl_title, impl_desc = IMPLICATIONS[ctry]
        rows_html = "".join([f'<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f8fafc;font-size:12px;"><span style="color:#94a3b8;">{k}</span><span style="font-weight:600;color:#0f172a;">{v}</span></div>'
            for k,v in [("Spend/Person",f"${r['spend_per_person_usd']:,.0f}"),("Stay",f"{r['stay_days']} days"),("Revisit Rate",f"{r['revisit_rate']}%"),("Satisfaction",f"{r['overall_satisfaction']}%"),("Recommend",f"{r['recommend_intention']}%")]])
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="padding:20px 16px;border-top:4px solid {COLORS[i]};text-align:center;">
              <div style="margin-bottom:8px;">{flag(ctry,36)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:14px;font-weight:700;color:#0f172a;margin-bottom:14px;">{CNAME[ctry]}</div>
              {rows_html}
              <div style="margin-top:12px;padding:10px;background:#f8fafc;border-radius:8px;text-align:left;">
                <div style="font-size:10px;color:#94a3b8;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px;">Marketing Implication</div>
                <div style="font-size:11px;font-weight:600;color:#4f46e5;margin-bottom:3px;">{impl_title}</div>
                <div style="font-size:11px;color:#64748b;line-height:1.4;">{impl_desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    sat_df['Year'] = sat_df['year'].astype(str)
    sat_df['Market'] = sat_df['country'].map(CNAME)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Spend per Person (USD)</div>', unsafe_allow_html=True)
        fig = px.line(sat_df,x='Year',y='spend_per_person_usd',color='Market',color_discrete_sequence=COLORS,markers=True,labels={'spend_per_person_usd':'USD','Year':'','Market':'Market'})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">Revisit Rate (%)</div>', unsafe_allow_html=True)
        fig = px.line(sat_df,x='Year',y='revisit_rate',color='Market',color_discrete_sequence=COLORS,markers=True,labels={'revisit_rate':'%','Year':'','Market':'Market'})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)

    st.markdown('<div class="lbl">Korean Wave Spending Index</div>', unsafe_allow_html=True)
    hplot = hallyu_df.copy()
    hplot['Date']   = hplot['year_month'].apply(lambda x:f"{x[:4]}-{x[4:]}")
    hplot['Market'] = hplot['country'].map(CNAME)
    c3,c4 = st.columns(2)
    with c3:
        st.markdown('<div class="lbl">Total Korean Wave Transactions</div>', unsafe_allow_html=True)
        fig = px.line(hplot,x='Date',y='total_count',color='Market',color_discrete_sequence=COLORS,labels={'total_count':'Transactions','Date':'','Market':'Market'})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)
    with c4:
        st.markdown('<div class="lbl">Korean Wave Category Breakdown (Latest Period)</div>', unsafe_allow_html=True)
        liym = hallyu_ind['year_month'].max()
        lind = hallyu_ind[hallyu_ind['year_month']==liym].copy()
        lind['Market'] = lind['country'].map(CNAME)
        fig = px.bar(lind,x='Market',y='ratio',color='industry_en',barmode='stack',
                     color_discrete_sequence=['#4f46e5','#f59e0b','#10b981','#ef4444','#8b5cf6','#ec4899','#06b6d4','#84cc16','#f97316'],
                     labels={'ratio':'Share (%)','Market':'','industry_en':'Category'})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════════
elif page == "📈  Analytics":
    import plotly.express as px

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">Analytics</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">Explore trends by market and metric</p>
    """, unsafe_allow_html=True)

    df['Market'] = df['country'].map(CNAME)
    c1,c2 = st.columns([2,1])
    with c1:
        ctry_f = st.multiselect("Markets",['중국','일본','대만','미국','홍콩'],
                                 default=['중국','일본','대만','미국','홍콩'],
                                 format_func=lambda x:CNAME[x])
    with c2:
        MMAP = {'Visitor Count':'visitor_count','MoM Growth (%)':'visitor_mom_growth',
                'SNS Buzz':'buzz_volume','SNS Engagement':'engagement',
                'Potential Exposure':'potential_exposure','Positive Sentiment (%)':'positive_pct',
                'Korean Wave Transactions':'hallyu_spend_count',
                'ML Priority Score':'ml_priority_score'}
        ml2 = st.selectbox("Metric",list(MMAP.keys()))
        met = MMAP[ml2]

    dff = df[df['country'].isin(ctry_f)].copy()
    dff['Date'] = dff['year_month'].apply(lambda x:f"{x[:4]}-{x[4:]}")

    fig = px.line(dff,x='Date',y=met,color='Market',color_discrete_sequence=COLORS,labels={met:ml2,'Date':'','Market':'Market'})
    fig.update_traces(line=dict(width=2.5)); fig.update_layout(height=340,**CHART)
    if met == 'ml_priority_score':
        fig.add_hline(y=50,line_dash='dash',line_color='#94a3b8',annotation_text='50pt threshold')
    st.plotly_chart(fig,use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lbl">ML Priority Label History</div>', unsafe_allow_html=True)
        lc_col = 'ml_pred_label' if 'ml_pred_label' in dff.columns else 'priority_label'
        if lc_col in dff.columns:
            lc = dff.groupby(['Market',lc_col]).size().reset_index(name='Months')
            lc.columns = ['Market','Priority','Months']
            fig2 = px.bar(lc,x='Market',y='Months',color='Priority',barmode='group',
                          color_discrete_map={'High':'#4f46e5','Medium':'#f59e0b','Low':'#94a3b8'},
                          labels={'Months':'Months','Market':'','Priority':'Priority'})
            fig2.update_layout(height=270,**CHART); st.plotly_chart(fig2,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">Market Share Trend</div>', unsafe_allow_html=True)
        sd = dff[['Date','Market','country_share']].dropna()
        fig3 = px.area(sd,x='Date',y='country_share',color='Market',color_discrete_sequence=COLORS,
                       labels={'country_share':'Share','Date':'','Market':'Market'})
        fig3.update_layout(height=270,**CHART); st.plotly_chart(fig3,use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# METHODOLOGY
# ══════════════════════════════════════════════════════════════════
elif page == "🔬  Methodology":
    import plotly.graph_objects as go

    st.markdown("""
    <h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;margin-bottom:4px;">Data & Methodology</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">Technical documentation of the AI system design and evaluation</p>
    """, unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Dataset Overview</div>', unsafe_allow_html=True)
        rows_meta = [
            ("Data Period",         "2018.11 – 2026.04"),
            ("Unit of Analysis",    "Country × Month panel data"),
            ("Markets",             "China, Japan, Taiwan, USA, Hong Kong"),
            ("Total Observations",  f"{len(df):,} rows (post feature engineering)"),
            ("Training Samples",    f"{metrics['train_n']} (2018.11 – 2024.12)"),
            ("Test Samples",        f"{metrics['test_n']} (2025.01 – 2025.08)"),
            ("Inference Period",    "2025.09 – 2026.04 (recent dashboard display)"),
            ("Data Sources",        "Korea Tourism Organization (KTO), Korea Tourism Data Lab"),
            ("Input Features",      "29 engineered variables (5 categories)"),
            ("Target Variable",     "High / Medium / Low marketing priority"),
        ]
        for k,v in rows_meta:
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:13px;">
              <span style="color:#64748b;font-weight:500;">{k}</span>
              <span style="color:#0f172a;font-weight:600;text-align:right;">{v}</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="insight-box" style="margin-top:12px;">
          <b>Note on split:</b> The test set covers 2025.01–2025.08. Data from 2025.09 onward is used as recent
          inference data for real-time dashboard display and is not part of model evaluation.
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="lbl">Feature Categories (29 Total)</div>', unsafe_allow_html=True)
        feat_cats = [
            ("🧳 Visitor Metrics (10)","visitor_count, lag 1–3, MoM growth, 3M/6M moving avg, vs 3M avg, rolling std, country share"),
            ("📱 SNS Metrics (9)",      "buzz_volume, engagement, potential_exposure, MoM changes, per-visitor ratios, buzz vs 3M avg"),
            ("🇰🇷 Korean Wave (3)",    "hallyu_spend_count, MoM growth, per-visitor ratio"),
            ("⚙️ Macro Variables (4)", "exchange_rate, oil_price, month, quarter"),
            ("📅 Seasonality (3)",      "is_peak_season, month (1–12), quarter (1–4)"),
        ]
        for cat,feats in feat_cats:
            st.markdown(f"""<div style="background:#f8fafc;border-radius:10px;padding:12px 14px;margin-bottom:8px;">
              <div style="font-size:13px;font-weight:600;color:#0f172a;margin-bottom:4px;">{cat}</div>
              <div style="font-size:11px;color:#64748b;">{feats}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="lbl">System Design Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""<div style="background:#ffffff;border-radius:16px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
      <div style="font-size:13px;color:#475569;line-height:2.2;">
        <b style="color:#4f46e5;">Step 1 — Data Collection:</b>
        Monthly visitor statistics (KTO), SNS buzz &amp; engagement, Korean Wave spending, and macro indicators collected per country-month.<br/>
        <b style="color:#4f46e5;">Step 2 — Feature Engineering:</b>
        29 variables generated including lag features, moving averages, growth rates, per-visitor ratios, and macro indicators.<br/>
        <b style="color:#4f46e5;">Step 3 — Proxy Label Construction:</b>
        Because direct ground-truth labels for marketing priority are not available, domain-informed proxy labels were
        constructed from historical visitor, SNS, sentiment, Korean Wave, and macro indicators.
        This weak-supervision approach allows the model to learn structured decision patterns from historical market conditions.<br/>
        <b style="color:#4f46e5;">Step 4 — Model Training:</b>
        Random Forest classifier trained on 29 input features using a time-based split (train: ~2024, test: 2025.01–2025.08)
        to prevent data leakage.<br/>
        <b style="color:#4f46e5;">Step 5 — Prediction &amp; Display:</b>
        At inference time, only the ML model output is used. The ML Priority Score is defined as the predicted probability
        of High Priority × 100. Proxy label construction is not applied at inference time.
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="lbl">User Interaction</div>', unsafe_allow_html=True)
    st.markdown("""<div style="background:#ffffff;border-radius:16px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
      <div style="font-size:13px;color:#475569;line-height:2;">
        Users can inspect ML-based market priority rankings on the <b>Overview</b> page,
        adjust individual market indicators and run ML predictions in the <b>Priority Engine</b>,
        simulate what-if scenarios by modifying market conditions via sliders,
        allocate budgets proportionally to ML Priority Scores using the <b>Budget Planner</b>,
        explore traveler profiles and Korean Wave data in <b>Market Profiles</b>,
        and investigate historical trends across all metrics in <b>Analytics</b>.
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="lbl">Model Comparison — Why Random Forest?</div>', unsafe_allow_html=True)
    c1,c2 = st.columns([1,1.4])
    with c1:
        comp_data = {
            'Model':    ['Rule-Based Baseline','Logistic Regression','Random Forest ✓'],
            'Accuracy': [f"{metrics['rule_acc']*100:.1f}%",f"{metrics['lr_acc']*100:.1f}%",f"{metrics['rf_acc']*100:.1f}%"],
            'High F1':  ['N/A','~0.72',f"{metrics['cr']['High']['f1-score']:.2f}"],
            'Notes':    ['No training required','Linear boundaries only','Selected — best High F1'],
        }
        st.dataframe(pd.DataFrame(comp_data),use_container_width=True,hide_index=True)
        st.markdown(f"""<div class="insight-box">
          Random Forest achieved the highest High Priority F1 ({metrics['cr']['High']['f1-score']:.2f}),
          which is the most critical metric for budget allocation — missing a high-potential market is costly.
          It also captures non-linear interactions that logistic regression cannot.
          <br/><br/>
          <b>Note:</b> The rule-based baseline above is a simple visitor-count threshold model used only for performance comparison,
          distinct from the proxy label construction rules used to generate training labels.
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="lbl">Confusion Matrix (Test Set: 2025.01 – 2025.08)</div>', unsafe_allow_html=True)
        cm = metrics['cm']; cls = metrics['classes']
        fig_cm = go.Figure(go.Heatmap(z=cm,x=[f"Pred: {c}" for c in cls],y=[f"Act: {c}" for c in cls],
                                       text=cm,texttemplate="%{text}",colorscale='Blues',showscale=False))
        fig_cm.update_layout(height=280,**CHART); st.plotly_chart(fig_cm,use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="lbl">Classification Report</div>', unsafe_allow_html=True)
    cr = metrics['cr']
    cr_data = [{'Class':c,'Precision':f"{cr[c]['precision']:.2f}",'Recall':f"{cr[c]['recall']:.2f}",
                'F1 Score':f"{cr[c]['f1-score']:.2f}",'Support':int(cr[c]['support'])} for c in cls]
    st.dataframe(pd.DataFrame(cr_data),use_container_width=True,hide_index=True)
