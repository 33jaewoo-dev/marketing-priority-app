import streamlit as st
import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Inbound Marketing Intelligence", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
* { font-family:'Inter',sans-serif; }
h1,h2,h3 { font-family:'Outfit',sans-serif !important; }
.stApp { background:#f1f5f9; }
section[data-testid="stSidebar"]>div { background:#fff; border-right:1px solid #e2e8f0; }
.card { background:#fff; border-radius:16px; padding:24px; box-shadow:0 1px 3px rgba(0,0,0,.08); margin-bottom:16px; }
.country-card { background:#fff; border-radius:16px; padding:20px 16px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,.08); border-top:4px solid #e2e8f0; }
.country-card.high{border-top-color:#4f46e5;} .country-card.medium{border-top-color:#f59e0b;} .country-card.low{border-top-color:#94a3b8;}
.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;font-family:'Outfit',sans-serif;letter-spacing:.04em;}
.badge.high{background:#eef2ff;color:#4338ca;border:1px solid #a5b4fc;}
.badge.medium{background:#fffbeb;color:#d97706;border:1px solid #fcd34d;}
.badge.low{background:#f8fafc;color:#64748b;border:1px solid #cbd5e1;}
.conf-strong{background:#dcfce7;color:#15803d;border:1px solid #86efac;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600;}
.conf-moderate{background:#fef9c3;color:#854d0e;border:1px solid #fde047;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600;}
.conf-weak{background:#fee2e2;color:#dc2626;border:1px solid #fca5a5;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600;}
.lbl{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#94a3b8;margin-bottom:12px;}
.sig-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f1f5f9;font-size:13px;}
.up{color:#16a34a;font-weight:700;font-family:'Outfit',sans-serif;}
.down{color:#dc2626;font-weight:700;font-family:'Outfit',sans-serif;}
.neu{color:#d97706;font-weight:700;font-family:'Outfit',sans-serif;}
.act{background:#f8fafc;border-radius:10px;padding:12px 16px;margin-bottom:8px;border-left:3px solid #e2e8f0;}
.act.high-b{border-left-color:#4f46e5;} .act.medium-b{border-left-color:#f59e0b;} .act.low-b{border-left-color:#94a3b8;}
.act-title{font-size:13px;font-weight:600;color:#1e293b;margin-bottom:4px;}
.act-desc{font-size:12px;color:#64748b;line-height:1.5;}
.result-box{border-radius:20px;padding:36px 24px;text-align:center;border:2px solid #e2e8f0;background:#fff;}
.driver-pill{display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;margin:2px;}
.driver-pos{background:#eef2ff;color:#4338ca;} .driver-neg{background:#fef2f2;color:#dc2626;}
.stButton>button{background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%) !important;color:#fff !important;border:none !important;border-radius:12px !important;font-family:'Outfit',sans-serif !important;font-weight:600 !important;font-size:15px !important;height:52px !important;}
.stButton>button:hover{opacity:.92 !important;transform:translateY(-1px) !important;}
.stTabs [data-baseweb="tab-list"]{background:#e2e8f0;border-radius:10px;padding:3px;gap:2px;}
.stTabs [data-baseweb="tab"]{border-radius:8px;color:#64748b !important;font-weight:500;}
.stTabs [aria-selected="true"]{background:#fff !important;color:#0f172a !important;box-shadow:0 1px 3px rgba(0,0,0,.1) !important;}
hr{border-color:#e2e8f0 !important;margin:16px 0 !important;}
.insight-box{background:#f0f9ff;border-left:3px solid #0ea5e9;border-radius:0 10px 10px 0;padding:12px 16px;margin:12px 0;font-size:13px;color:#0c4a6e;line-height:1.6;}
.proxy-note{background:#fefce8;border-left:3px solid #eab308;border-radius:0 10px 10px 0;padding:10px 14px;margin:8px 0;font-size:12px;color:#713f12;line-height:1.5;}
.rev-badge{display:inline-block;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:700;}
.rev-very-high{background:#eef2ff;color:#3730a3;} .rev-high{background:#f0fdf4;color:#166534;}
.rev-medium{background:#fffbeb;color:#92400e;} .rev-low{background:#f8fafc;color:#475569;}
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
CHART  = dict(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(248,250,252,.6)',
              font=dict(family='Inter',color='#64748b',size=12),margin=dict(l=0,r=0,t=8,b=0),
              legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(size=11)),
              xaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0'),
              yaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0'))

INDUSTRY_EN = {
    'K-라이프스타일푸드':'K-Lifestyle Food','라이프스타일푸드':'K-Lifestyle Food',
    'K-쇼핑':'K-Shopping','쇼핑':'K-Shopping',
    'K-한식':'K-Food','한식':'K-Food',
    '숙식':'Accommodation & Dining',
    'K-뷰티웰니스':'K-Beauty & Wellness','뷰티웰니스':'K-Beauty & Wellness',
    'K-패션':'K-Fashion','패션':'K-Fashion',
    'K-문화체험':'K-Cultural Experience','문화체험':'K-Cultural Experience',
    'K-나이트컬처':'K-Nightlife','K-나이트컬쳐':'K-Nightlife','나이트컬처':'K-Nightlife','나이트컬쳐':'K-Nightlife',
    'K-스포츠':'K-Sports','스포츠':'K-Sports',
    'K-공연':'K-Performances','공연':'K-Performances',
}
def map_industry(v):
    mapped = INDUSTRY_EN.get(str(v).strip())
    if mapped: return mapped
    import re
    if re.search(r'[가-힣]', str(v)): return 'Other Korean Wave Category'
    return str(v)

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

def confidence_label(pred_class_prob):
    """Always based on predicted class probability, not High probability."""
    if pred_class_prob >= 0.65: return "Strong", "conf-strong"
    elif pred_class_prob >= 0.50: return "Moderate", "conf-moderate"
    else: return "Weak", "conf-weak"

def row_to_full_features(row):
    d={}
    for f in FEATS:
        val=row.get(f,0)
        try: d[f]=float(val) if pd.notna(val) else 0.0
        except: d[f]=0.0
    return d

def inp_to_full_features(inp): return {f:float(inp.get(f,0) or 0) for f in FEATS}

# ── What-if directional adjustment ───────────────────────────────
def calc_whatif_adjustment(v_chg, s_chg, bz_chg, se_chg, oi_chg, ex_chg):
    """
    Bounded post-processing calibration for What-if Scenario ONLY.
    Not used for model training, evaluation, or main dashboard ranking.
    """
    def pw(chg, tiers):
        abs_c=abs(chg); sign=1 if chg>=0 else -1; total=0.0; prev=0.0
        for thr,rate in tiers:
            band=min(abs_c,thr)-prev
            if band>0: total+=band*rate
            prev=thr
            if abs_c<=thr: break
        return sign*total
    v_adj  = np.clip(pw(v_chg,  [(10,.10),(30,.16),(50,.22)]), -12, 12)
    s_adj  = np.clip(pw(se_chg, [(5,.20),(15,.35),(20,.50)]), -10, 10)
    e_adj  = np.clip(pw(s_chg,  [(10,.06),(30,.10),(50,.15)]),  -8,  8)
    bz_adj = np.clip(pw(bz_chg, [(10,.04),(30,.08),(50,.12)]),  -6,  6)
    oi_adj = np.clip(pw(-oi_chg,[(10,.06),(30,.10),(50,.15)]),  -7,  7)
    ex_adj = np.clip(pw(ex_chg, [(10,.08),(20,.13),(30,.18)]),  -7,  7)
    total  = np.clip(v_adj+s_adj+e_adj+bz_adj+oi_adj+ex_adj, -20, 20)
    return round(float(total),2), {'visitor':round(float(v_adj),2),'sentiment':round(float(s_adj),2),
        'engagement':round(float(e_adj),2),'buzz':round(float(bz_adj),2),
        'oil':round(float(oi_adj),2),'exchange':round(float(ex_adj),2)}

# ── Revenue Opportunity helpers ───────────────────────────────────
# Latest market values for relative normalization (computed once at startup)
_LATEST_MV_CACHE = {}

def _get_market_val_percentile(market_val, all_market_vals):
    """Percentile rank within the 5 markets (0-100)."""
    if not all_market_vals or max(all_market_vals) == min(all_market_vals):
        return 50.0
    sorted_vals = sorted(all_market_vals)
    rank = sum(1 for v in sorted_vals if v <= market_val)
    return round(rank / len(sorted_vals) * 100, 1)

def get_revenue_opportunity(ml_score, market_val, mom, engagement, kwave, sentiment,
                             all_market_vals=None, all_kwave_vals=None):
    """
    Revenue Opportunity Level — relative proxy across 5 markets.
    Not an absolute revenue forecast. Uses percentile normalization
    so market value differences are preserved across markets.
    """
    # Market value percentile (relative to all 5 markets)
    if all_market_vals and len(all_market_vals) > 1:
        mv_pct = _get_market_val_percentile(market_val, all_market_vals) / 100.0
    else:
        mv_pct = np.clip(market_val / 2e9, 0, 1)  # fallback: 2B USD scale

    # Korean Wave percentile (relative to all 5 markets)
    if all_kwave_vals and len(all_kwave_vals) > 1:
        kw_pct = _get_market_val_percentile(kwave, all_kwave_vals) / 100.0
    else:
        kw_pct = np.clip(kwave / 1e6, 0, 1)  # fallback

    mom_score   = float(np.clip((mom + 0.5) / 1.0, 0, 1))
    eng_pct     = float(np.clip(engagement / 4e6, 0, 1))
    sent_score  = float(np.clip(sentiment / 100.0, 0, 1))

    score = (ml_score * 0.30 +
             mv_pct   * 100 * 0.25 +
             kw_pct   * 100 * 0.15 +
             mom_score * 100 * 0.15 +
             eng_pct   * 100 * 0.10 +
             sent_score * 100 * 0.05)

    if score >= 72: return "Very High", "rev-very-high"
    elif score >= 52: return "High",     "rev-high"
    elif score >= 32: return "Medium",   "rev-medium"
    else:             return "Low",      "rev-low"

def get_growth_driver_campaign(row_data, spend_per_person=0, revisit_rate=0,
                               all_mv=None, all_vc=None, all_kw=None):
    """
    Assign growth driver and campaign type using relative market comparisons.
    Priority order: Recovery > Volume-Led > Korean Wave > SNS Momentum > Revisit > Premium > Mixed
    Premium Spend is only assigned when visitor base is relatively small AND spend is high.
    """
    vc  = float(row_data.get('visitor_count',0) or 0)
    mom = float(row_data.get('visitor_mom_growth',0) or 0)
    eng = float(row_data.get('engagement',0) or 0)
    bz  = float(row_data.get('buzz_volume',0) or 0)
    kw  = float(row_data.get('hallyu_spend_count',0) or 0)
    cs  = float(row_data.get('country_share',0.2) or 0.2)

    # Relative thresholds using latest 5-market medians
    median_vc = float(np.median(all_vc)) if all_vc else 150000
    median_kw = float(np.median(all_kw)) if all_kw else 400000
    high_vc   = cs > 0.28 or vc > median_vc * 1.3   # large volume market

    # Recovery: sharp decline but still meaningful base
    if mom < -0.15 and vc > 30000:
        return "Recovery Opportunity", "Recovery Campaign"

    # Volume-Driven: large visitor base / high market share — takes priority over premium
    if high_vc and mom >= -0.10:
        # Check if Korean Wave is also very strong for this large-volume market
        if kw > median_kw * 1.5:
            return "Korean Wave-Driven Growth", "K-content Campaign"
        return "Volume-Driven Growth", "Acquisition Focus"

    # Korean Wave-Driven: strong KW regardless of volume
    if kw > median_kw * 1.2:
        return "Korean Wave-Driven Growth", "K-content Campaign"

    # SNS Momentum-Driven: strong digital attention with positive momentum
    if (eng > 300000 or bz > 30000) and mom >= 0:
        return "SNS Momentum-Driven Growth", "Awareness-to-Conversion"

    # Revisit-Driven: high loyalty metric
    if revisit_rate > 68:
        return "Revisit-Driven Growth", "Retention & Loyalty Campaign"

    # Premium: high spend AND relatively small volume (not a mass-volume market)
    if spend_per_person > 1500 and not high_vc:
        return "Premium Spend-Driven Growth", "Premium Upsell"

    return "Mixed-Signal Market", "Balanced Campaign"

def get_market_signals(inp):
    pos=[(n,v) for n,v,t in [('Visitor volume',inp['visitor_count'],200000),
        ('Visitor momentum',inp['visitor_mom_growth'],0.05),('SNS engagement',inp['engagement'],200000),
        ('Buzz volume',inp['buzz_volume'],30000),('Positive sentiment',inp['positive_pct'],65),
        ('Korean Wave spend',inp['hallyu_spend_count'],200000)] if v>t]
    neg=[(n,v) for n,v,t in [('Visitor crash',inp['visitor_mom_growth'],-0.15),
        ('Negative sentiment',inp['positive_pct'],50)] if v<t]
    return pos[:2],neg[:1]

# ── Model ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Initializing AI model...")
def load_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
    base=os.path.dirname(os.path.abspath(__file__))
    df=pd.read_csv(os.path.join(base,'full_dataset.csv'),encoding='utf-8',dtype={'year_month':str})
    df['year_month']=df['year_month'].astype(str).str.strip()
    dc=df[FEATS+['priority_label','year_month']].dropna()
    le=LabelEncoder()
    train_mask=dc['year_month']<='202412'; test_mask=(dc['year_month']>='202501')&(dc['year_month']<='202508')
    X_train=dc[train_mask][FEATS]; X_test=dc[test_mask][FEATS]
    y_train=le.fit_transform(dc[train_mask]['priority_label'])
    y_test=le.transform(dc[test_mask]['priority_label'])
    rf=RandomForestClassifier(n_estimators=200,max_depth=10,random_state=42,class_weight='balanced')
    rf.fit(X_train,y_train)
    rf_pred=rf.predict(X_test); rf_acc=accuracy_score(y_test,rf_pred)
    cm=confusion_matrix(y_test,rf_pred)
    cr=classification_report(y_test,rf_pred,target_names=le.classes_,output_dict=True,labels=list(range(len(le.classes_))),zero_division=0)
    scaler=StandardScaler(); lr=LogisticRegression(max_iter=1000,class_weight='balanced',random_state=42)
    lr.fit(scaler.fit_transform(X_train),y_train)
    lr_acc=accuracy_score(y_test,lr.predict(scaler.transform(X_test)))
    def rule_fn(row):
        if row['visitor_count']>300000 and row['visitor_mom_growth']>0.05: return le.transform(['High'])[0]
        elif row['visitor_count']<100000 or row['visitor_mom_growth']<-0.15: return le.transform(['Low'])[0]
        else: return le.transform(['Medium'])[0]
    rule_acc=accuracy_score(y_test,dc[test_mask].apply(rule_fn,axis=1))
    fi=pd.DataFrame({'feature':FEATS,'importance':rf.feature_importances_}).sort_values('importance',ascending=False)
    met={'rf_acc':rf_acc,'lr_acc':lr_acc,'rule_acc':rule_acc,'cm':cm,'cr':cr,'classes':le.classes_,'train_n':len(X_train),'test_n':len(X_test)}
    return rf,le,fi,met

@st.cache_data
def load_data():
    base=os.path.dirname(os.path.abspath(__file__))
    df =pd.read_csv(os.path.join(base,'full_dataset.csv'),encoding='utf-8',dtype={'year_month':str})
    sat=pd.read_csv(os.path.join(base,'satisfaction_data.csv'),encoding='utf-8')
    hsp=pd.read_csv(os.path.join(base,'korean_wave_spending.csv'),encoding='utf-8',dtype={'year_month':str})
    hid=pd.read_csv(os.path.join(base,'korean_wave_industry.csv'),encoding='utf-8',dtype={'year_month':str})
    df['year_month']=df['year_month'].astype(str).str.strip()
    hid['industry_en']=hid['industry'].apply(map_industry)
    return df,sat,hsp,hid

model,le,feat_imp,metrics=load_model()
df,sat_df,hallyu_df,hallyu_ind=load_data()
latest_month=df['year_month'].max()
ym_disp=f"{latest_month[:4]}.{latest_month[4:]}"

def get_ml_prediction(inp_full):
    idf=pd.DataFrame([inp_full])[FEATS]
    proba=model.predict_proba(idf)[0]
    pred=le.inverse_transform(model.predict(idf))[0]
    pd_={cls:proba[i] for i,cls in enumerate(le.classes_)}
    ml_score=round(pd_['High']*100,1)
    pred_prob=pd_[pred]
    return pred,pd_,ml_score,pred_prob

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""<div style="padding:16px 0 24px;">
      <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:800;color:#0f172a;line-height:1.2;letter-spacing:-.02em;">
        Inbound Marketing<br/><span style="color:#4f46e5;">Intelligence</span></div>
      <div style="font-size:10px;color:#94a3b8;margin-top:6px;letter-spacing:.1em;text-transform:uppercase;">Korea Tourism AI Platform</div>
    </div>""",unsafe_allow_html=True)
    page=st.radio("",["📊  Overview","🔮  Priority Engine","💰  Budget Planner","🔀  Compare Markets","👤  Market Profiles","📈  Analytics","🔬  Methodology"],label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"""<div style="font-size:11px;color:#94a3b8;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px;">Latest Data</div>
    <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;color:#0f172a;">{ym_disp}</div>
    <div style="font-size:11px;color:#94a3b8;margin-top:2px;">Korea Tourism Data Lab</div>""",unsafe_allow_html=True)
    st.markdown("---")
    flag_row="".join([f'<img src="{FLAG_URL[c]}" width="18" style="border-radius:2px;margin-right:3px;">' for c in ['중국','일본','대만','미국','홍콩']])
    st.markdown(f"""<div style="font-size:12px;color:#64748b;line-height:2.2;">
      <b style="color:#334155;">Model</b><br/>Random Forest · {metrics['rf_acc']*100:.1f}% Accuracy<br/>
      <b style="color:#334155;">Split</b><br/>Time-based (~2024 train / 2025 test)<br/>
      <b style="color:#334155;">Data</b><br/>KTO · SNS · Korean Wave Index<br/>
      <b style="color:#334155;">Markets</b><br/>{flag_row}
    </div><div style="font-size:11px;color:#94a3b8;margin-top:16px;">Last updated: {ym_disp}</div>""",unsafe_allow_html=True)

# ── Precompute latest ML results ──────────────────────────────────
latest_raw=df[df['year_month']==latest_month].copy()
# Pre-collect market values for percentile normalization
_sat_latest = sat_df.sort_values('year').groupby('country').last().reset_index()
def _spend_for(ctry):
    r=_sat_latest[_sat_latest['country']==ctry]
    return float(r['spend_per_person_usd'].iloc[0]) if not r.empty else 0
_spend_map = {c: _spend_for(c) for c in ['중국','일본','대만','미국','홍콩']}
_mv_map  = {c: float(latest_raw[latest_raw['country']==c]['visitor_count'].values[0] if len(latest_raw[latest_raw['country']==c])>0 else 0)*_spend_map.get(c,0) for c in ['중국','일본','대만','미국','홍콩']}
_kw_map  = {c: float(latest_raw[latest_raw['country']==c]['hallyu_spend_count'].values[0] if len(latest_raw[latest_raw['country']==c])>0 else 0) for c in ['중국','일본','대만','미국','홍콩']}
_all_mv  = list(_mv_map.values())
_all_kw  = list(_kw_map.values())

latest_computed=[]
for _,row in latest_raw.iterrows():
    inp=row_to_full_features(row)
    pred,pd_,ml_score,pred_prob=get_ml_prediction(inp)
    conf_l,conf_cls=confidence_label(pred_prob)
    sat_r=sat_df[sat_df['country']==row['country']]
    spend=float(sat_r['spend_per_person_usd'].iloc[-1]) if not sat_r.empty else 0
    revisit=float(sat_r['revisit_rate'].iloc[-1]) if not sat_r.empty else 0
    stay=float(sat_r['stay_days'].iloc[-1]) if not sat_r.empty else 0
    mv=float(row.get('visitor_count',0) or 0)*(spend or 0)
    kwave=float(row.get('hallyu_spend_count',0) or 0)
    rev_opp,rev_cls=get_revenue_opportunity(ml_score,mv,float(row.get('visitor_mom_growth',0) or 0),
        float(row.get('engagement',0) or 0),kwave,float(row.get('positive_pct',50) or 50),
        all_market_vals=_all_mv, all_kwave_vals=_all_kw)
    _vc_vals=[float(latest_raw[latest_raw['country']==c]['visitor_count'].values[0]) if len(latest_raw[latest_raw['country']==c])>0 else 0 for c in ['중국','일본','대만','미국','홍콩']]
    driver,campaign=get_growth_driver_campaign(row,spend,revisit,all_mv=_all_mv,all_vc=_vc_vals,all_kw=_all_kw)
    pos_d,neg_d=get_market_signals(inp)
    latest_computed.append({'country':row['country'],'pred':pred,'prob_dict':pd_,'ml_score':ml_score,
        'pred_prob':pred_prob,'conf_label':conf_l,'conf_cls':conf_cls,
        'visitor_count':float(row.get('visitor_count',0) or 0),
        'visitor_mom_growth':float(row.get('visitor_mom_growth',0) or 0),
        'spend':spend,'revisit':revisit,'stay':stay,'market_value':mv,
        'rev_opp':rev_opp,'rev_cls':rev_cls,'driver':driver,'campaign':campaign,
        'pos_d':pos_d,'neg_d':neg_d,'row_data':row})
latest_computed.sort(key=lambda x:-x['ml_score'])

# ══════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page=="📊  Overview":
    import plotly.express as px
    st.markdown("""<h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-.02em;margin-bottom:4px;">Marketing Priority Dashboard</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:8px;">Tourism marketers must decide which inbound markets deserve more campaign budget under limited resources. This system supports data-driven market prioritization by combining visitor demand, SNS attention, Korean Wave consumption, and macro indicators. The core business question is which inbound market can serve as the strongest growth driver under limited marketing resources.</p>""",unsafe_allow_html=True)
    st.markdown("""<div class="insight-box"><b>How to use:</b> (1) Check ML priority ranking → (2) Review trends → (3) Open <b>Priority Engine</b> for scenario simulation → (4) Use <b>Budget Planner</b> for allocation → (5) Use <b>Compare Markets</b> for head-to-head analysis</div>""",unsafe_allow_html=True)

    st.markdown(f'<div class="lbl" style="margin-top:16px;">ML Priority Ranking — {ym_disp} · Random Forest · {metrics["rf_acc"]*100:.1f}% Test Accuracy</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for i,r in enumerate(latest_computed):
        lbl=r['pred']; clr=PCOLOR[lbl]; rank=['1st','2nd','3rd','4th','5th'][i]
        mom=r['visitor_mom_growth']; ms=r['ml_score']
        dh="".join([f'<span class="driver-pill driver-pos">↑ {n}</span>' for n,_ in r['pos_d']])
        dh+="".join([f'<span class="driver-pill driver-neg">↓ {n}</span>' for n,_ in r['neg_d']])
        mv_disp=f"${r['market_value']/1e6:.0f}M" if r['market_value']>0 else "N/A"
        with cols[i]:
            st.markdown(f"""<div class="country-card {PBDR[lbl]}">
              <div style="font-size:10px;color:#94a3b8;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px;">{rank}</div>
              <div style="margin-bottom:10px;">{flag(r['country'],36)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:15px;font-weight:700;color:#0f172a;margin-bottom:8px;">{CNAME[r['country']]}</div>
              <span class="badge {PBDR[lbl]}">{lbl}</span>
              <div style="margin-top:12px;padding-top:10px;border-top:1px solid #f1f5f9;">
                <div style="font-size:10px;color:#94a3b8;margin-bottom:2px;">ML Priority Score</div>
                <div style="font-family:'Outfit',sans-serif;font-size:26px;font-weight:800;color:{clr};">{ms:.1f}<span style="font-size:13px;color:#94a3b8;">/100</span></div>
                <div style="font-size:11px;color:#94a3b8;">High Prob: <b style="color:{clr};">{ms:.0f}%</b></div>
                <div style="margin:4px 0;"><span class="{r['conf_cls']}">{r['conf_label']} Confidence</span></div>
                <div style="font-size:11px;font-weight:600;color:{'#16a34a' if mom>0 else '#dc2626'};margin-top:4px;">{'▲' if mom>0 else '▼'} {abs(mom*100):.1f}% MoM</div>
                <div style="font-size:11px;color:#94a3b8;">{int(r['visitor_count']):,} visitors</div>
              </div>
              <div style="margin-top:8px;padding-top:8px;border-top:1px solid #f1f5f9;text-align:left;">
                <div style="font-size:10px;color:#94a3b8;margin-bottom:3px;">Revenue Opportunity</div>
                <span class="rev-badge {r['rev_cls']}">{r['rev_opp']}</span>
                <div style="font-size:10px;color:#94a3b8;margin-top:4px;">Market Value Proxy: {mv_disp}</div>
                <div style="font-size:10px;color:#94a3b8;margin-top:2px;">Growth Driver: {r['driver'][:22]}</div>
              </div>
              <div style="margin-top:8px;padding-top:8px;border-top:1px solid #f1f5f9;text-align:left;">
                <div style="font-size:10px;color:#94a3b8;margin-bottom:4px;">Observable Market Signals</div>
                {dh if dh else '<span style="font-size:11px;color:#94a3b8;">No dominant signal</span>'}
                <div style="font-size:9px;color:#cbd5e1;margin-top:4px;font-style:italic;">Not causal attribution</div>
              </div>
            </div>""",unsafe_allow_html=True)

    st.markdown("""<div class="proxy-note" style="margin-top:8px;">
      <b>Note:</b> Revenue Opportunity Level and Market Value Proxy are directional proxies based on visitor count, average spending per person, ML priority score, and SNS signals.
      They are not actual campaign revenue or guaranteed ROI forecasts.
    </div>""",unsafe_allow_html=True)

    st.markdown("<br/>",unsafe_allow_html=True)
    df_p=df.copy(); df_p['Date']=df_p['year_month'].apply(lambda x:f"{x[:4]}-{x[4:]}"); df_p['Market']=df_p['country'].map(CNAME)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Monthly Visitor Trends</div>',unsafe_allow_html=True)
        fig=px.line(df_p,x='Date',y='visitor_count',color='Market',color_discrete_sequence=COLORS,labels={'visitor_count':'Visitors','Date':'','Market':'Market'})
        fig.update_traces(line=dict(width=2.5)); fig.update_layout(height=300,**CHART); st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">SNS Engagement Trends</div>',unsafe_allow_html=True)
        fig2=px.line(df_p,x='Date',y='engagement',color='Market',color_discrete_sequence=COLORS,labels={'engagement':'Engagement','Date':'','Market':'Market'})
        fig2.update_traces(line=dict(width=2.5)); fig2.update_layout(height=300,**CHART); st.plotly_chart(fig2,use_container_width=True)
    c3,c4=st.columns(2)
    with c3:
        st.markdown('<div class="lbl">Positive Sentiment (%) — Thresholds Used in Proxy Label Construction</div>',unsafe_allow_html=True)
        fig3=px.line(df_p,x='Date',y='positive_pct',color='Market',color_discrete_sequence=COLORS,labels={'positive_pct':'%','Date':'','Market':'Market'})
        fig3.update_traces(line=dict(width=2.5))
        fig3.add_hline(y=55,line_dash='dash',line_color='#94a3b8',annotation_text='Neutral')
        fig3.add_hline(y=40,line_dash='dot',line_color='#ef4444',annotation_text='Critical')
        fig3.update_layout(height=280,**CHART); st.plotly_chart(fig3,use_container_width=True)
    with c4:
        st.markdown('<div class="lbl">Feature Importance — Top 10</div>',unsafe_allow_html=True)
        fi_d=feat_imp.head(10).copy(); fi_d['Feature']=fi_d['feature'].str.replace('_',' ').str.title()
        fig4=px.bar(fi_d,x='importance',y='Feature',orientation='h',color='importance',color_continuous_scale=['#e0e7ff','#4f46e5','#3730a3'])
        fig4.update_layout(height=280,showlegend=False,coloraxis_showscale=False,**CHART)
        fig4.update_yaxes(categoryorder='total ascending'); st.plotly_chart(fig4,use_container_width=True)
        top3=feat_imp.head(3)['feature'].str.replace('_',' ').tolist()
        st.markdown(f'<div class="insight-box">The model places the highest weight on <b>{top3[0]}</b>, <b>{top3[1]}</b>, and <b>{top3[2]}</b>, suggesting both actual tourism demand and digital attention are important for priority classification.</div>',unsafe_allow_html=True)

    st.markdown('<div class="lbl">Model Performance</div>',unsafe_allow_html=True)
    mc=st.columns(5); m=metrics
    for col,l,v,s in [(mc[0],"Algorithm","Random Forest","200 estimators · depth 10"),
        (mc[1],"Test Accuracy",f"{m['rf_acc']*100:.1f}%","Time-based split"),
        (mc[2],"High Priority F1",f"{m['cr']['High']['f1-score']:.2f}","Prec {:.0f}% · Rec {:.0f}%".format(m['cr']['High']['precision']*100,m['cr']['High']['recall']*100)),
        (mc[3],"Train Period","2018.11 – 2024.12",f"{m['train_n']} samples"),
        (mc[4],"Test Period","2025.01 – 2025.08",f"{m['test_n']} samples")]:
        with col:
            st.markdown(f"""<div class="card" style="padding:18px 20px;">
              <div style="font-size:10px;color:#94a3b8;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px;">{l}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:19px;font-weight:700;color:#0f172a;">{v}</div>
              <div style="font-size:11px;color:#94a3b8;margin-top:4px;">{s}</div>
            </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PRIORITY ENGINE
# ══════════════════════════════════════════════════════════════════
elif page=="🔮  Priority Engine":
    st.markdown("""<h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-.02em;margin-bottom:4px;">Priority Engine</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:16px;">Adjust market indicators — the Random Forest model predicts marketing priority using all 29 input features.</p>""",unsafe_allow_html=True)
    mode=st.radio("",["📋  Standard Input","⚡  What-If Scenario"],horizontal=True,label_visibility="collapsed")
    st.markdown("<br/>",unsafe_allow_html=True)
    country_sel=st.selectbox("Select Market",['중국','일본','대만','미국','홍콩'],format_func=lambda x:CNAME[x])
    cd=df[df['country']==country_sel].sort_values('year_month').iloc[-1]
    sat_r=sat_df[sat_df['country']==country_sel]
    spend=float(sat_r['spend_per_person_usd'].iloc[-1]) if not sat_r.empty else 0
    stay=float(sat_r['stay_days'].iloc[-1]) if not sat_r.empty else 0
    revisit=float(sat_r['revisit_rate'].iloc[-1]) if not sat_r.empty else 0

    v_chg=s_chg=bz_chg=se_chg=oi_chg=ex_chg=0

    if "Standard" in mode:
        t1,t2,t3=st.tabs(["🧳  Visitor Metrics","📱  SNS Metrics","⚙️  Macro Environment"])
        with t1:
            c1,c2,c3=st.columns(3)
            with c1: visitor_count=st.number_input("Current Month Visitors",value=int(cd['visitor_count']),step=1000); visitor_lag1=st.number_input("Previous Month",value=int(cd['visitor_lag1']),step=1000)
            with c2: visitor_lag2=st.number_input("2 Months Ago",value=int(cd['visitor_lag2']),step=1000); visitor_lag3=st.number_input("3 Months Ago",value=int(cd['visitor_lag3']),step=1000)
            with c3: visitor_3m_avg=st.number_input("3-Month Moving Average",value=float(cd['visitor_3m_avg']),step=1000.0); visitor_6m_avg=st.number_input("6-Month Moving Average",value=float(cd['visitor_6m_avg']),step=1000.0)
            country_share=st.number_input("Market Share (0–1)",value=float(cd['country_share']),step=0.001,format="%.4f")
        with t2:
            c1,c2=st.columns(2)
            with c1: buzz_volume=st.number_input("Buzz Volume (SNS Mentions)",value=int(cd['buzz_volume']),step=100); engagement=st.number_input("Engagement",value=int(cd['engagement']),step=1000)
            with c2:
                potential_exposure=st.number_input("Potential Exposure",value=int(cd['potential_exposure']),step=10000)
                positive_pct=st.slider("Positive Sentiment (%)",0.0,100.0,float(cd['positive_pct']),0.5,help="Sentiment ML input signal. Below 40% historically associated with Low Priority cases.")
            negative_pct=100.0-positive_pct
            if positive_pct<40: st.error("🚨 Below 40%: historically associated with Low Priority cases")
            elif positive_pct<50: st.warning("⚠️ Below 50%: may suppress predicted priority")
        with t3:
            c1,c2,c3=st.columns(3)
            with c1: month=st.selectbox("Reference Month",list(range(1,13)),index=int(cd['month'])-1)
            with c2: exchange_rate=st.number_input("Exchange Rate (KRW)",value=float(cd['exchange_rate']),step=1.0,help="Higher = weaker KRW = Korea more affordable for foreign tourists")
            with c3: oil_price=st.number_input("Oil Price (USD/barrel)",value=float(cd['oil_price']),step=1.0,help="Higher = higher airfare = historically associated with reduced travel demand")
        vmom=(visitor_count-visitor_lag1)/visitor_lag1 if visitor_lag1 else 0
        vvs3=visitor_count/visitor_3m_avg if visitor_3m_avg else 1
        vstd=float(cd.get('visitor_rolling_std',0) or 0)
        bl1=float(cd.get('buzz_lag1',buzz_volume) or buzz_volume); el1=float(cd.get('engagement_lag1',engagement) or engagement); exl1=float(cd.get('exposure_lag1',potential_exposure) or potential_exposure)
        bmom=(buzz_volume-bl1)/bl1 if bl1 else 0; emom=(engagement-el1)/el1 if el1 else 0; exmom=(potential_exposure-exl1)/exl1 if exl1 else 0
        epv=engagement/visitor_count if visitor_count else 0; bpv=buzz_volume/visitor_count if visitor_count else 0
        b3m=float(cd.get('buzz_3m_avg',buzz_volume) or buzz_volume); bvs3=buzz_volume/b3m if b3m else 1
        qtr=(month-1)//3+1; peak=1 if month in [3,4,5,9,10] else 0
        hc=float(cd.get('hallyu_spend_count',0) or 0); hl1=float(cd.get('hallyu_lag1',hc) or hc)
        hmom=(hc-hl1)/hl1 if hl1 else 0; hpv=hc/visitor_count if visitor_count else 0
        inp=inp_to_full_features({'visitor_count':visitor_count,'visitor_lag1':visitor_lag1,'visitor_lag2':visitor_lag2,'visitor_lag3':visitor_lag3,'visitor_mom_growth':vmom,'visitor_3m_avg':visitor_3m_avg,'visitor_6m_avg':visitor_6m_avg,'visitor_vs_3m_avg':vvs3,'visitor_rolling_std':vstd,'country_share':country_share,'buzz_volume':buzz_volume,'engagement':engagement,'potential_exposure':potential_exposure,'buzz_mom_growth':bmom,'engagement_mom_growth':emom,'exposure_mom_growth':exmom,'engagement_per_visitor':epv,'buzz_per_visitor':bpv,'buzz_vs_3m_avg':bvs3,'positive_pct':positive_pct,'negative_pct':negative_pct,'hallyu_spend_count':hc,'hallyu_mom_growth':hmom,'hallyu_per_visitor':hpv,'month':month,'quarter':qtr,'is_peak_season':peak,'exchange_rate':exchange_rate,'oil_price':oil_price})
        is_whatif=False
    else:
        st.markdown('<div class="lbl">What-If Scenario Simulator</div>',unsafe_allow_html=True)
        st.markdown("""<div class="proxy-note">Raw ML Priority Score is generated by the Random Forest model.
        Scenario-adjusted Score applies a bounded post-processing calibration for interactive what-if simulation only.
        This adjustment is not used for model training, evaluation, feature importance, or dashboard ranking.</div>""",unsafe_allow_html=True)
        cd_full=row_to_full_features(cd)
        c1,c2=st.columns(2)
        with c1:
            v_chg=st.slider("Visitor Count Change (%)",-50,50,0,5)
            s_chg=st.slider("SNS Engagement Change (%)",-50,50,0,5)
            bz_chg=st.slider("Buzz Volume Change (%)",-50,50,0,5)
        with c2:
            se_chg=st.slider("Positive Sentiment Change (pp)",-20,20,0,1)
            oi_chg=st.slider("Oil Price Change (%)",-30,50,0,5)
            ex_chg=st.slider("Exchange Rate Change (%)",-20,20,0,2)
        inp=cd_full.copy()
        bvc=inp['visitor_count']; b_eng=inp['engagement']; b_bz=inp['buzz_volume']

        # ── Primary inputs ──────────────────────────────────────────
        inp['visitor_count']   = bvc*(1+v_chg/100)
        inp['engagement']      = b_eng*(1+s_chg/100)
        inp['buzz_volume']     = b_bz*(1+bz_chg/100)
        inp['positive_pct']    = max(0,min(100,inp['positive_pct']+se_chg))
        inp['negative_pct']    = 100-inp['positive_pct']
        inp['oil_price']       = inp['oil_price']*(1+oi_chg/100)
        inp['exchange_rate']   = inp['exchange_rate']*(1+ex_chg/100)

        # ── Derived features: visitor ────────────────────────────────
        inp['visitor_mom_growth']   = (inp['visitor_count']-inp['visitor_lag1'])/inp['visitor_lag1'] if inp['visitor_lag1'] else 0
        inp['visitor_vs_3m_avg']    = inp['visitor_count']/inp['visitor_3m_avg'] if inp['visitor_3m_avg'] else 1

        # ── Derived features: engagement ─────────────────────────────
        el1_base = float(cd_full.get('engagement_lag1', b_eng) or b_eng)
        inp['engagement_mom_growth']  = (inp['engagement']-el1_base)/el1_base if el1_base else 0
        inp['engagement_per_visitor'] = inp['engagement']/inp['visitor_count'] if inp['visitor_count'] else 0

        # ── Derived features: buzz ────────────────────────────────────
        bl1_base = float(cd_full.get('buzz_lag1', b_bz) or b_bz)
        b3m_base = float(cd_full.get('buzz_3m_avg', b_bz) or b_bz)
        inp['buzz_mom_growth']   = (inp['buzz_volume']-bl1_base)/bl1_base if bl1_base else 0
        inp['buzz_vs_3m_avg']    = inp['buzz_volume']/b3m_base if b3m_base else 1
        inp['buzz_per_visitor']  = inp['buzz_volume']/inp['visitor_count'] if inp['visitor_count'] else 0

        # ── Derived features: hallyu ──────────────────────────────────
        hc_base = float(cd_full.get('hallyu_spend_count', 0) or 0)
        inp['hallyu_per_visitor'] = hc_base/inp['visitor_count'] if inp['visitor_count'] else 0
        is_whatif=True

    st.markdown("<br/>",unsafe_allow_html=True)
    if st.button("🤖  Run ML Priority Prediction",use_container_width=True):
        pred,pd_,ml_score,pred_prob=get_ml_prediction(inp)
        lbl=pred; clr=PCOLOR[lbl]; cn=CNAME[country_sel]
        conf_l,conf_cls=confidence_label(pred_prob)
        cd_full2=row_to_full_features(cd)
        _,_,base_score,_=get_ml_prediction(cd_full2)
        raw_diff=round(ml_score-base_score,1)
        adj_total=0; adj_breakdown={}
        if is_whatif:
            adj_total,adj_breakdown=calc_whatif_adjustment(v_chg,s_chg,bz_chg,se_chg,oi_chg,ex_chg)
        raw_scenario = float(np.clip(ml_score+adj_total,0,100))

        # ── Single-variable monotonic sanity correction ───────────────
        # When only one slider is active, guarantee directional consistency.
        # This is a UI post-processing correction — NOT used in model training/evaluation.
        if is_whatif:
            active = sum(1 for x in [v_chg,s_chg,bz_chg,se_chg,oi_chg,ex_chg] if x!=0)
            if active == 1:
                # Positive-direction variables: score must not fall below baseline
                if v_chg>0  and raw_scenario < base_score: raw_scenario = base_score
                if s_chg>0  and raw_scenario < base_score: raw_scenario = base_score
                if bz_chg>0 and raw_scenario < base_score: raw_scenario = base_score
                if se_chg>0 and raw_scenario < base_score: raw_scenario = base_score
                if ex_chg>0 and raw_scenario < base_score: raw_scenario = base_score
                # Negative-direction variables: score must not rise above baseline
                if v_chg<0  and raw_scenario > base_score: raw_scenario = base_score
                if s_chg<0  and raw_scenario > base_score: raw_scenario = base_score
                if bz_chg<0 and raw_scenario > base_score: raw_scenario = base_score
                if se_chg<0 and raw_scenario > base_score: raw_scenario = base_score
                if oi_chg>0 and raw_scenario > base_score: raw_scenario = base_score  # oil up = score down
                if oi_chg<0 and raw_scenario < base_score: raw_scenario = base_score  # oil down = score up
                if ex_chg<0 and raw_scenario > base_score: raw_scenario = base_score

        scenario_score=round(raw_scenario,1)
        pos_d,neg_d=get_market_signals(inp)
        mv=inp['visitor_count']*(spend or 0)
        rev_opp,rev_cls=get_revenue_opportunity(ml_score,mv,inp.get('visitor_mom_growth',0),inp.get('engagement',0),inp.get('hallyu_spend_count',0),inp.get('positive_pct',50))
        try:
            _pe_vc_vals=[float(latest_raw[latest_raw['country']==c]['visitor_count'].values[0]) if len(latest_raw[latest_raw['country']==c])>0 else 0 for c in ['중국','일본','대만','미국','홍콩']]
            driver,campaign=get_growth_driver_campaign(inp,spend,revisit,all_mv=_all_mv,all_vc=_pe_vc_vals,all_kw=_all_kw)
        except:
            driver,campaign=get_growth_driver_campaign(inp,spend,revisit)

        st.markdown('<div class="lbl">Prediction Results</div>',unsafe_allow_html=True)
        r1,r2,r3=st.columns([1.1,1,1.2])
        with r1:
            tags=[]
            if inp.get('is_peak_season'): tags.append("✨ Peak season")
            if inp.get('positive_pct',50)<50: tags.append("⚠️ Sentiment risk")
            if inp.get('visitor_mom_growth',0)<-0.15: tags.append("🔴 Visitor drop")
            tag_html="&nbsp;".join([f'<span style="background:#f1f5f9;border-radius:6px;padding:3px 8px;font-size:10px;color:#475569;">{t}</span>' for t in tags])
            pos_pills="".join([f'<span class="driver-pill driver-pos">↑ {n}</span>' for n,_ in pos_d])
            neg_pills="".join([f'<span class="driver-pill driver-neg">↓ {n}</span>' for n,_ in neg_d])
            raw_diff_html=f'<span style="color:{"#16a34a" if raw_diff>=0 else "#dc2626"};font-size:11px;font-weight:600;">{"▲" if raw_diff>=0 else "▼"} {abs(raw_diff):.1f} pts vs baseline</span>'
            score_display=scenario_score if is_whatif else ml_score
            score_label="Scenario-Adjusted Score" if is_whatif else "ML Priority Score"
            if is_whatif:
                scenario_tier = "High Scenario Signal" if scenario_score>=65 else ("Medium Scenario Signal" if scenario_score>=40 else "Low Scenario Signal")
                adj_html=f'''<div style="font-size:11px;color:#94a3b8;margin-top:4px;">
                  Raw ML Priority Score: {ml_score} &nbsp;|&nbsp; Adjustment: {adj_total:+.1f}
                </div>
                <div style="font-size:11px;margin-top:4px;">
                  <span style="background:#f1f5f9;border-radius:6px;padding:2px 8px;font-size:10px;color:#475569;">Scenario Score Tier: {scenario_tier}</span>
                </div>
                <div style="font-size:9px;color:#94a3b8;margin-top:3px;font-style:italic;">Scenario Tier ≠ ML class prediction</div>'''
            else:
                adj_html=''
            st.markdown(f"""<div class="result-box" style="border-top:4px solid {clr};">
              <div style="margin-bottom:12px;">{flag(country_sel,48)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;color:#0f172a;margin-bottom:12px;">{cn}</div>
              <span class="badge {PBDR[lbl]}" style="font-size:13px;padding:5px 16px;">{lbl} Priority</span>
              &nbsp;<span class="{conf_cls}">{conf_l} Confidence</span>
              <div style="margin:18px 0 6px;">
                <div style="font-size:10px;color:#94a3b8;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;">{score_label}</div>
                <div style="font-size:10px;color:#94a3b8;margin-bottom:4px;">High Priority Probability × 100</div>
                <div style="font-family:'Outfit',sans-serif;font-size:58px;font-weight:800;color:{clr};letter-spacing:-.04em;line-height:1;">{score_display}</div>
                <div style="font-size:14px;color:#94a3b8;margin-bottom:6px;">/ 100 · High prob: <b style="color:{clr};">{pd_['High']*100:.0f}%</b></div>
                {adj_html}
                <div style="margin-top:4px;">{raw_diff_html}</div>
              </div>
              <div style="background:#f1f5f9;border-radius:8px;height:10px;margin:12px 0 6px;overflow:hidden;">
                <div style="width:{score_display}%;height:100%;background:linear-gradient(90deg,{clr}88,{clr});border-radius:8px;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:#94a3b8;margin-bottom:12px;"><span>0</span><span>50</span><span>100</span></div>
              <div style="margin-bottom:6px;">
                <div style="font-size:10px;color:#94a3b8;margin-bottom:3px;">Revenue Opportunity</div>
                <span class="rev-badge {rev_cls}">{rev_opp}</span>
              </div>
              <div style="font-size:11px;color:#64748b;margin-bottom:8px;">Growth Driver: <b>{driver}</b><br/>Campaign: <b>{campaign}</b></div>
              <div style="margin-bottom:8px;">{pos_pills}{neg_pills}</div>
              <div>{tag_html}</div>
            </div>""",unsafe_allow_html=True)
            if is_whatif:
                changes=[]; interps=[]
                if v_chg!=0:
                    d="stronger" if v_chg>0 else "weaker"
                    changes.append(f"visitor count ({'+' if v_chg>0 else ''}{v_chg}%)")
                    interps.append("Higher visitor count strengthens observed demand signals." if v_chg>0 else "Lower visitor count weakens observed demand signals.")
                if se_chg!=0:
                    changes.append(f"sentiment ({'+' if se_chg>0 else ''}{se_chg}pp)")
                    interps.append("Improved sentiment strengthens market attractiveness." if se_chg>0 else "Lower sentiment weakens market attractiveness and may increase communication risk.")
                if s_chg!=0:
                    changes.append(f"SNS engagement ({'+' if s_chg>0 else ''}{s_chg}%)")
                    interps.append("Higher SNS engagement indicates stronger digital attention." if s_chg>0 else "Lower SNS engagement suggests weaker digital attention.")
                if oi_chg!=0:
                    changes.append(f"oil price ({'+' if oi_chg>0 else ''}{oi_chg}%)")
                    interps.append("Higher oil prices may increase travel costs and reduce inbound attractiveness." if oi_chg>0 else "Lower oil prices may ease travel costs and support inbound attractiveness.")
                if ex_chg!=0:
                    changes.append(f"exchange rate ({'+' if ex_chg>0 else ''}{ex_chg}%)")
                    interps.append("A weaker KRW can improve Korea's affordability for inbound tourists." if ex_chg>0 else "A stronger KRW can reduce Korea's affordability for inbound tourists.")
                if changes:
                    direction="remains" if pred==le.inverse_transform(model.predict(pd.DataFrame([cd_full2])[FEATS]))[0] else f"changes to {pred}"
                    adj_sign="increases" if adj_total>0 else "decreases"
                    interp_str=" ".join(interps[:2])
                    st.markdown(f"""<div class="insight-box" style="margin-top:12px;font-size:12px;">
                      <b>Scenario interpretation:</b> Under this scenario, {cn} priority {direction}. The scenario-adjusted score {adj_sign} by {abs(adj_total):.1f} points.
                      {interp_str}
                    </div>""",unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="lbl" style="margin-top:0;">Key Market Signals</div>',unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">Observable market signals used as ML inputs. Not causal attribution.</div>',unsafe_allow_html=True)
            def scls(v,t=0.05):
                if v>t: return "up","▲"
                if v<-t: return "down","▼"
                return "neu","━"
            sigs=[("Visitor MoM Growth",inp.get('visitor_mom_growth',0),f"{inp.get('visitor_mom_growth',0)*100:+.1f}%","MoM change"),
                  ("Buzz Volume Change",inp.get('buzz_mom_growth',0),f"{inp.get('buzz_mom_growth',0)*100:+.1f}%","vs last month"),
                  ("Engagement Change",inp.get('engagement_mom_growth',0),f"{inp.get('engagement_mom_growth',0)*100:+.1f}%","vs last month"),
                  ("vs 3M Average",inp.get('visitor_vs_3m_avg',1)-1,f"{(inp.get('visitor_vs_3m_avg',1)-1)*100:+.1f}%","vs 3-month avg"),
                  ("Positive Sentiment",(inp.get('positive_pct',50)-55)/100,f"{inp.get('positive_pct',50):.1f}%","ML input signal"),
                  ("Market Share",(inp.get('country_share',0.2)-0.2)/0.2,f"{inp.get('country_share',0.2)*100:.1f}%","Share of 5 markets")]
            html=""
            for name,val,disp,desc in sigs:
                cls,arrow=scls(val)
                html+=f"""<div class="sig-row"><div><div style="color:#475569;font-weight:500;">{name}</div><div style="font-size:11px;color:#94a3b8;">{desc}</div></div><div class="{cls}">{arrow} {disp}</div></div>"""
            st.markdown(html,unsafe_allow_html=True)
            st.markdown("<br/>",unsafe_allow_html=True)
            st.markdown('<div style="font-size:11px;color:#94a3b8;margin-bottom:8px;">Classification Probability</div>',unsafe_allow_html=True)
            for cn_l,p in [('High',pd_['High']),('Medium',pd_['Medium']),('Low',pd_['Low'])]:
                c2c=PCOLOR[cn_l]
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
                  <div style="width:56px;font-size:12px;color:#64748b;">{cn_l}</div>
                  <div style="flex:1;background:#f1f5f9;border-radius:4px;height:8px;overflow:hidden;">
                    <div style="width:{int(p*100)}%;height:100%;background:{c2c};border-radius:4px;"></div></div>
                  <div style="width:36px;text-align:right;font-family:'Outfit',sans-serif;font-size:12px;font-weight:700;color:{c2c};">{int(p*100)}%</div>
                </div>""",unsafe_allow_html=True)

        with r3:
            clr2=PCOLOR[lbl]; bc=PBDR[lbl]; cn3=CNAME[country_sel]
            RECS={'High':("Aggressive Offensive Strategy","Visitor volume, SNS, and sentiment signals are all strong.","Increase Budget","#eef2ff"),
                  'Medium':("Monitor & Optimize","Mid-tier signals. Watch for momentum before scaling.","Maintain Budget","#fffbeb"),
                  'Low':("Reallocate & Monitor","Low signals. Redirect resources to higher-priority markets.","Minimize Budget","#f8fafc")}
            title,desc,blbl,bg=RECS[lbl]
            actions=[]
            if lbl=='High':
                actions+=[("Budget Expansion",f"Increase {cn3}-specific ad spend 20–30% vs. last month"),("Campaign Type",f"Recommended: {campaign}")]
                if spend>1500: actions.append(("Premium Targeting",f"High spend/person (${spend:,.0f}) — focus on premium packages"))
                if revisit>70: actions.append(("Loyalty Program",f"Revisit rate {revisit:.0f}% — strengthen repeat visitor rewards"))
                actions.append(("Growth Driver",f"Primary driver: {driver}"))
            elif lbl=='Medium':
                actions+=[("Hold Steady","Maintain current campaign — monitor weekly KPIs"),("Campaign Type",f"Recommended: {campaign}")]
                if stay>5: actions.append(("Long-Stay Bundle",f"Average stay {stay:.0f} days — offer multi-destination packages"))
                actions.append(("Trigger Plan","Upgrade strategy if MoM visitor growth exceeds +15%"))
            else:
                actions+=[("Reallocate",f"Shift {cn3} budget to High-priority markets"),("Root Cause Analysis","Diagnose: geopolitical tensions, flight capacity, or seasonal?")]
                if revisit>60: actions.append(("Retention Focus",f"Revisit rate {revisit:.0f}% — target returning visitors"))
                actions.append(("Recovery Watch","Re-engage when MoM rebounds above +10%"))
            st.markdown('<div class="lbl" style="margin-top:0;">Strategic Recommendations</div>',unsafe_allow_html=True)
            st.markdown(f"""<div style="background:{bg};border:1px solid {clr2}33;border-radius:12px;padding:16px 18px;margin-bottom:14px;">
              <div style="font-family:'Outfit',sans-serif;font-size:16px;font-weight:700;color:{clr2};margin-bottom:6px;">{title}</div>
              <div style="font-size:12px;color:#64748b;line-height:1.5;margin-bottom:10px;">{desc}</div>
              <span style="background:{clr2};color:#fff;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:600;">{blbl}</span>
            </div>""",unsafe_allow_html=True)
            for at,ad in actions:
                st.markdown(f"""<div class="act {bc}-b"><div class="act-title">{at}</div><div class="act-desc">{ad}</div></div>""",unsafe_allow_html=True)
            if inp.get('positive_pct',50)<40:
                st.markdown("""<div class="act" style="border-left-color:#dc2626;background:#fef2f2;"><div class="act-title">🚨 Crisis Communication</div><div class="act-desc">Identify root cause of negative sentiment. Activate PR response immediately.</div></div>""",unsafe_allow_html=True)
            if inp.get('visitor_mom_growth',0)<-0.30:
                st.markdown("""<div class="act" style="border-left-color:#dc2626;background:#fef2f2;"><div class="act-title">🚨 Visitor Crash Response</div><div class="act-desc">Investigate cause — diplomatic tensions, flight suspensions, or external shocks.</div></div>""",unsafe_allow_html=True)
            if inp.get('is_peak_season'):
                st.markdown(f"""<div class="act" style="border-left-color:#10b981;background:#f0fdf4;"><div class="act-title">✨ Peak Season Opportunity</div><div class="act-desc">Month {int(inp.get('month',4))} is peak season — optimal timing for campaign launch.</div></div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# BUDGET PLANNER
# ══════════════════════════════════════════════════════════════════
elif page=="💰  Budget Planner":
    import plotly.express as px
    import plotly.graph_objects as go
    st.markdown("""<h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-.02em;margin-bottom:4px;">Budget Planner</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:16px;">ML-predicted priority scores drive recommended budget allocation across markets.</p>""",unsafe_allow_html=True)
    st.markdown("""<div class="insight-box">Markets classified as High Priority receive a minimum floor allocation, while the remaining budget is distributed proportionally to ML Priority Scores. This keeps strategic presence in promising markets while concentrating budget toward stronger signals.</div>""",unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,1,1])
    with c1: total_budget=st.number_input("Total Marketing Budget (KRW)",value=100000000,step=10000000,format="%d")
    with c2:
        currency=st.selectbox("Display Currency",["KRW (₩)","USD ($)","JPY (¥)"])
        krw_per_unit={'KRW (₩)':1,'USD ($)':1380,'JPY (¥)':9.2}[currency]
        sym={'KRW (₩)':'₩','USD ($)':'$','JPY (¥)':'¥'}[currency]
    with c3:
        alloc_mode=st.selectbox("Allocation Mode",["Balanced","Aggressive","Conservative"],
                                 help="Balanced: standard floors. Aggressive: concentrate on top markets. Conservative: broader market presence.")
    floors_map={'Balanced':{'High':0.15,'Medium':0.08,'Low':0.04},'Aggressive':{'High':0.10,'Medium':0.05,'Low':0.02},'Conservative':{'High':0.18,'Medium':0.10,'Low':0.06}}
    floors=floors_map[alloc_mode]
    alloc_data=[]
    for r in latest_computed:
        alloc_data.append({'country':r['country'],'country_en':CNAME[r['country']],'pred':r['pred'],
            'ml_score':r['ml_score'],'high_prob':r['prob_dict']['High'],
            'conf_label':r['conf_label'],'conf_cls':r['conf_cls'],
            'rev_opp':r['rev_opp'],'rev_cls':r['rev_cls'],'driver':r['driver'],'campaign':r['campaign'],
            'market_value':r['market_value']})
    alloc_df=pd.DataFrame(alloc_data).sort_values('ml_score',ascending=False)
    alloc_df['floor']=alloc_df['pred'].map(floors)
    score_sum=alloc_df['ml_score'].sum(); remaining=1-alloc_df['floor'].sum()
    alloc_df['extra']=alloc_df['ml_score']/score_sum*remaining
    alloc_df['share']=(alloc_df['floor']+alloc_df['extra']); alloc_df['share']=alloc_df['share']/alloc_df['share'].sum()
    alloc_df['budget']=alloc_df['share']*total_budget
    st.markdown('<div class="lbl">Recommended Budget Allocation</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for i,(_,r) in enumerate(alloc_df.iterrows()):
        clr=PCOLOR[r['pred']]; budget_disp=r['budget']/krw_per_unit; fmt=f"{sym}{budget_disp:,.0f}"
        mv_disp=f"${r['market_value']/1e6:.0f}M" if r['market_value']>0 else "N/A"
        with cols[i]:
            st.markdown(f"""<div class="country-card {PBDR[r['pred']]}">
              <div style="margin-bottom:8px;">{flag(r['country'],32)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:14px;font-weight:700;color:#0f172a;margin-bottom:6px;">{r['country_en']}</div>
              <span class="badge {PBDR[r['pred']]}">{r['pred']}</span>
              <div style="margin-top:10px;">
                <div style="font-size:10px;color:#94a3b8;">Recommended Share</div>
                <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;color:{clr};">{r['share']*100:.1f}%</div>
                <div style="font-size:13px;font-weight:600;color:#334155;">{fmt}</div>
                <div style="font-size:11px;color:#94a3b8;margin-top:3px;">ML Score: {r['ml_score']:.1f} · High: {r['high_prob']*100:.0f}%</div>
                <div style="margin:3px 0;"><span class="{r['conf_cls']}">{r['conf_label']} Confidence</span></div>
                <div style="margin-top:4px;"><span class="rev-badge {r['rev_cls']}">{r['rev_opp']}</span></div>
                <div style="font-size:10px;color:#94a3b8;margin-top:3px;">Mkt Value: {mv_disp}</div>
                <div style="font-size:10px;color:#64748b;margin-top:2px;">{r['driver'][:25]}</div>
              </div>
            </div>""",unsafe_allow_html=True)
    st.markdown("""<div class="proxy-note" style="margin-top:8px;">
      Revenue Opportunity Level and Market Value Proxy are directional proxies, not actual campaign revenue or guaranteed ROI forecasts.
    </div>""",unsafe_allow_html=True)
    st.markdown("<br/>",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Budget Share by Market</div>',unsafe_allow_html=True)
        fig=go.Figure(go.Pie(labels=alloc_df['country_en'],values=alloc_df['share']*100,marker_colors=COLORS,hole=0.4,textinfo='label+percent'))
        fig.update_layout(height=280,**CHART,showlegend=False); st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">Recommended Budget Amount</div>',unsafe_allow_html=True)
        alloc_df['Budget']=alloc_df['budget']/krw_per_unit
        fig2=px.bar(alloc_df,x='country_en',y='Budget',color='pred',color_discrete_map={'High':'#4f46e5','Medium':'#f59e0b','Low':'#94a3b8'},labels={'Budget':f'Budget ({sym})','country_en':'','pred':'Priority'})
        fig2.update_layout(height=280,**CHART); st.plotly_chart(fig2,use_container_width=True)
    st.markdown('<div class="lbl">Detailed Allocation Table</div>',unsafe_allow_html=True)
    disp_df=alloc_df[['country_en','pred','ml_score','high_prob','conf_label','rev_opp','driver','campaign','share','budget']].copy()
    disp_df.columns=['Market','Priority','ML Score','High Prob','Confidence','Rev Opportunity','Growth Driver','Campaign Type','Share (%)','Budget (KRW)']
    disp_df['Share (%)']=disp_df['Share (%)'].multiply(100).round(1)
    disp_df['High Prob']=disp_df['High Prob'].multiply(100).round(1).astype(str)+'%'
    disp_df['Budget (KRW)']=disp_df['Budget (KRW)'].apply(lambda x:f"₩{x:,.0f}")
    disp_df['ML Score']=disp_df['ML Score'].round(1)
    st.dataframe(disp_df,use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════════════════
# COMPARE MARKETS
# ══════════════════════════════════════════════════════════════════
elif page=="🔀  Compare Markets":
    import plotly.graph_objects as go
    st.markdown("""<h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-.02em;margin-bottom:4px;">Compare Markets</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">Head-to-head comparison of two inbound markets to identify relative growth opportunities.</p>""",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: mkt_a=st.selectbox("Market A",['중국','일본','대만','미국','홍콩'],index=0,format_func=lambda x:CNAME[x])
    with c2: mkt_b=st.selectbox("Market B",['중국','일본','대만','미국','홍콩'],index=1,format_func=lambda x:CNAME[x])

    def get_market_data(ctry):
        r=next((x for x in latest_computed if x['country']==ctry),None)
        if r is None: return None
        sat_r=sat_df[sat_df['country']==ctry]
        spend=float(sat_r['spend_per_person_usd'].iloc[-1]) if not sat_r.empty else 0
        stay=float(sat_r['stay_days'].iloc[-1]) if not sat_r.empty else 0
        revisit=float(sat_r['revisit_rate'].iloc[-1]) if not sat_r.empty else 0
        return {**r,'spend':spend,'stay':stay,'revisit':revisit}

    da=get_market_data(mkt_a); db=get_market_data(mkt_b)
    if da and db and mkt_a!=mkt_b:
        c1,c2=st.columns(2)
        for col,d,ctry in [(c1,da,mkt_a),(c2,db,mkt_b)]:
            clr=PCOLOR[d['pred']]
            with col:
                mv_disp=f"${d['market_value']/1e6:.0f}M" if d['market_value']>0 else "N/A"
                st.markdown(f"""<div class="card" style="border-top:4px solid {clr};">
                  <div style="text-align:center;margin-bottom:16px;">{flag(ctry,48)}</div>
                  <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:700;color:#0f172a;text-align:center;margin-bottom:12px;">{CNAME[ctry]}</div>
                  <div style="display:flex;justify-content:center;gap:8px;margin-bottom:16px;">
                    <span class="badge {PBDR[d['pred']]}">{d['pred']}</span>
                    <span class="{d['conf_cls']}">{d['conf_label']} Confidence</span>
                  </div>
                  {"".join([f'<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #f1f5f9;font-size:13px;"><span style="color:#64748b;">{k}</span><span style="font-weight:600;color:#0f172a;">{v}</span></div>' for k,v in [
                    ("ML Priority Score",f"{d['ml_score']:.1f}/100"),("High Probability",f"{d['prob_dict']['High']*100:.0f}%"),
                    ("Revenue Opportunity",d['rev_opp']),("Market Value Proxy",mv_disp),
                    ("Current Visitors",f"{int(d['visitor_count']):,}"),("MoM Growth",f"{d['visitor_mom_growth']*100:+.1f}%"),
                    ("Spend per Person",f"${d['spend']:,.0f}"),("Stay Days",f"{d['stay']:.0f} days"),
                    ("SNS Engagement",f"{int(d['row_data'].get('engagement',0) or 0):,}"),("Korean Wave Spend",f"{int(d['row_data'].get('hallyu_spend_count',0) or 0):,}"),
                    ("Revisit Rate",f"{d['revisit']:.0f}%"),("Growth Driver",d['driver'][:28]),("Campaign Type",d['campaign'][:28]),
                  ]])}
                </div>""",unsafe_allow_html=True)

        # Auto interpretation
        cn_a=CNAME[mkt_a]; cn_b=CNAME[mkt_b]
        interps=[]
        if da['ml_score']>db['ml_score']+5: interps.append(f"{cn_a} has a stronger ML Priority Score ({da['ml_score']:.1f} vs {db['ml_score']:.1f}), suggesting higher overall marketing priority.")
        elif db['ml_score']>da['ml_score']+5: interps.append(f"{cn_b} has a stronger ML Priority Score ({db['ml_score']:.1f} vs {da['ml_score']:.1f}), suggesting higher overall marketing priority.")
        else: interps.append(f"{cn_a} and {cn_b} have similar ML Priority Scores ({da['ml_score']:.1f} vs {db['ml_score']:.1f}), indicating comparable overall priority.")
        if da['spend']>db['spend']*1.3: interps.append(f"{cn_a} is more attractive for premium spend-driven campaigns (${da['spend']:,.0f} vs ${db['spend']:,.0f} per person).")
        elif db['spend']>da['spend']*1.3: interps.append(f"{cn_b} is more attractive for premium spend-driven campaigns (${db['spend']:,.0f} vs ${da['spend']:,.0f} per person).")
        if da['visitor_count']>db['visitor_count']*1.5: interps.append(f"{cn_a} offers stronger volume-driven growth potential with {int(da['visitor_count']):,} vs {int(db['visitor_count']):,} visitors.")
        elif db['visitor_count']>da['visitor_count']*1.5: interps.append(f"{cn_b} offers stronger volume-driven growth potential with {int(db['visitor_count']):,} vs {int(da['visitor_count']):,} visitors.")
        if da['driver']!=db['driver']: interps.append(f"{cn_a} is positioned as {da['driver'].lower()}, while {cn_b} is positioned as {db['driver'].lower()} — suggesting different campaign roles.")
        st.markdown(f"""<div class="insight-box" style="margin-top:16px;">
          <b>Comparative Interpretation:</b> {"  ".join(interps)}
          <br/><i style="font-size:11px;color:#0369a1;">These comparisons are based on observable market signals and directional proxies. Not causal attribution or guaranteed ROI forecast.</i>
        </div>""",unsafe_allow_html=True)
    elif mkt_a==mkt_b:
        st.info("Please select two different markets for comparison.")

# ══════════════════════════════════════════════════════════════════
# MARKET PROFILES
# ══════════════════════════════════════════════════════════════════
elif page=="👤  Market Profiles":
    import plotly.express as px, plotly.graph_objects as go
    st.markdown("""<h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-.02em;margin-bottom:4px;">Market Profiles</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">Traveler behavior, satisfaction, and Korean Wave consumption by market (2015–2024)</p>""",unsafe_allow_html=True)
    IMPL={'중국':("Package + Korean Wave Campaign","High visitor volume and Korean Wave spending — bundle K-beauty and K-pop"),'일본':("Repeat Visitor Promotion","High revisit rate — loyalty programs and short-trip packages"),'대만':("SNS-Driven Influencer Campaign","Strong SNS engagement — influencer and UGC campaigns"),'미국':("Premium Long-Haul Package","Highest spend/person — target high-value travelers"),'홍콩':("City-Break Bundle","Short average stay — position Korea as a convenient weekend destination")}
    ly=sat_df['year'].max(); lsat=sat_df[sat_df['year']==ly]
    st.markdown(f'<div class="lbl">Traveler Profile Summary — {ly}</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for i,ctry in enumerate(['중국','일본','대만','미국','홍콩']):
        row=lsat[lsat['country']==ctry]
        if row.empty: continue
        r=row.iloc[0]; it,id_=IMPL[ctry]
        rows_html="".join([f'<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f8fafc;font-size:12px;"><span style="color:#94a3b8;">{k}</span><span style="font-weight:600;color:#0f172a;">{v}</span></div>' for k,v in [("Spend/Person",f"${r['spend_per_person_usd']:,.0f}"),("Stay",f"{r['stay_days']} days"),("Revisit Rate",f"{r['revisit_rate']}%"),("Satisfaction",f"{r['overall_satisfaction']}%"),("Recommend",f"{r['recommend_intention']}%")]])
        with cols[i]:
            st.markdown(f"""<div class="card" style="padding:20px 16px;border-top:4px solid {COLORS[i]};text-align:center;">
              <div style="margin-bottom:8px;">{flag(ctry,36)}</div>
              <div style="font-family:'Outfit',sans-serif;font-size:14px;font-weight:700;color:#0f172a;margin-bottom:14px;">{CNAME[ctry]}</div>
              {rows_html}
              <div style="margin-top:12px;padding:10px;background:#f8fafc;border-radius:8px;text-align:left;">
                <div style="font-size:10px;color:#94a3b8;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px;">Marketing Implication</div>
                <div style="font-size:11px;font-weight:600;color:#4f46e5;margin-bottom:3px;">{it}</div>
                <div style="font-size:11px;color:#64748b;line-height:1.4;">{id_}</div>
              </div>
            </div>""",unsafe_allow_html=True)
    st.markdown("<br/>",unsafe_allow_html=True)
    sat_df['Year']=sat_df['year'].astype(str); sat_df['Market']=sat_df['country'].map(CNAME)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Spend per Person (USD)</div>',unsafe_allow_html=True)
        fig=px.line(sat_df,x='Year',y='spend_per_person_usd',color='Market',color_discrete_sequence=COLORS,markers=True,labels={'spend_per_person_usd':'USD','Year':'','Market':'Market'})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">Revisit Rate (%)</div>',unsafe_allow_html=True)
        fig=px.line(sat_df,x='Year',y='revisit_rate',color='Market',color_discrete_sequence=COLORS,markers=True,labels={'revisit_rate':'%','Year':'','Market':'Market'})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)
    st.markdown('<div class="lbl">Korean Wave Spending Index</div>',unsafe_allow_html=True)
    hplot=hallyu_df.copy(); hplot['Date']=hplot['year_month'].apply(lambda x:f"{x[:4]}-{x[4:]}"); hplot['Market']=hplot['country'].map(CNAME)
    c3,c4=st.columns(2)
    with c3:
        st.markdown('<div class="lbl">Total Korean Wave Transactions</div>',unsafe_allow_html=True)
        fig=px.line(hplot,x='Date',y='total_count',color='Market',color_discrete_sequence=COLORS,labels={'total_count':'Transactions','Date':'','Market':'Market'})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)
    with c4:
        st.markdown('<div class="lbl">Korean Wave Category Breakdown (Latest Period)</div>',unsafe_allow_html=True)
        liym=hallyu_ind['year_month'].max(); lind=hallyu_ind[hallyu_ind['year_month']==liym].copy(); lind['Market']=lind['country'].map(CNAME)
        fig=px.bar(lind,x='Market',y='ratio',color='industry_en',barmode='stack',
                   color_discrete_sequence=['#4f46e5','#f59e0b','#10b981','#ef4444','#8b5cf6','#ec4899','#06b6d4','#84cc16','#f97316'],
                   labels={'ratio':'Share (%)','Market':'','industry_en':'Category'})
        fig.update_layout(height=270,**CHART); st.plotly_chart(fig,use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════════
elif page=="📈  Analytics":
    import plotly.express as px
    st.markdown("""<h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-.02em;margin-bottom:4px;">Analytics</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">Explore trends by market and metric</p>""",unsafe_allow_html=True)
    df['Market']=df['country'].map(CNAME)
    df_a=df.copy()
    df_a['Visitor MoM Growth (%)']=df_a['visitor_mom_growth']*100
    df_a['Market Share (%)']=df_a['country_share']*100
    c1,c2=st.columns([2,1])
    with c1: ctry_f=st.multiselect("Markets",['중국','일본','대만','미국','홍콩'],default=['중국','일본','대만','미국','홍콩'],format_func=lambda x:CNAME[x])
    with c2:
        MMAP={'Visitor Count':'visitor_count','Visitor MoM Growth (%)':'Visitor MoM Growth (%)','SNS Buzz':'buzz_volume','SNS Engagement':'engagement','Potential Exposure':'potential_exposure','Positive Sentiment (%)':'positive_pct','Korean Wave Transactions':'hallyu_spend_count','ML Priority Score':'ml_priority_score','Market Share (%)':'Market Share (%)'}
        ml2=st.selectbox("Metric",list(MMAP.keys())); met=MMAP[ml2]
    dff=df_a[df_a['country'].isin(ctry_f)].copy(); dff['Date']=dff['year_month'].apply(lambda x:f"{x[:4]}-{x[4:]}")
    if met not in dff.columns and met in df.columns: dff[met]=df[df['country'].isin(ctry_f)][met].values
    fig=px.line(dff,x='Date',y=met,color='Market',color_discrete_sequence=COLORS,labels={met:ml2,'Date':'','Market':'Market'})
    fig.update_traces(line=dict(width=2.5)); fig.update_layout(height=340,**CHART)
    if met=='ml_priority_score': fig.add_hline(y=50,line_dash='dash',line_color='#94a3b8',annotation_text='50pt threshold')
    st.plotly_chart(fig,use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="lbl">ML Priority Label History</div>',unsafe_allow_html=True)
        lc_col='ml_pred_label' if 'ml_pred_label' in dff.columns else 'priority_label'
        if lc_col in dff.columns:
            lc=dff.groupby(['Market',lc_col]).size().reset_index(name='Months'); lc.columns=['Market','Priority','Months']
            fig2=px.bar(lc,x='Market',y='Months',color='Priority',barmode='group',color_discrete_map={'High':'#4f46e5','Medium':'#f59e0b','Low':'#94a3b8'},labels={'Months':'Months','Market':'','Priority':'Priority'})
            fig2.update_layout(height=270,**CHART); st.plotly_chart(fig2,use_container_width=True)
    with c2:
        st.markdown('<div class="lbl">Market Share Trend (%)</div>',unsafe_allow_html=True)
        sd=dff[['Date','Market','Market Share (%)']].dropna()
        fig3=px.area(sd,x='Date',y='Market Share (%)',color='Market',color_discrete_sequence=COLORS,labels={'Market Share (%)':'Share (%)','Date':'','Market':'Market'})
        fig3.update_layout(height=270,**CHART); st.plotly_chart(fig3,use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# METHODOLOGY
# ══════════════════════════════════════════════════════════════════
elif page=="🔬  Methodology":
    import plotly.graph_objects as go
    st.markdown("""<h1 style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-.02em;margin-bottom:4px;">Data & Methodology</h1>
    <p style="color:#64748b;font-size:14px;margin-bottom:28px;">Technical documentation of the AI system design and evaluation</p>""",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="lbl">Dataset Overview</div>',unsafe_allow_html=True)
        for k,v in [("Data Period","2018.11 – 2026.04"),("Unit of Analysis","Country × Month panel data"),("Markets","China, Japan, Taiwan, USA, Hong Kong"),(f"Total Observations",f"{len(df):,} rows (post feature engineering)"),("Training Samples",f"{metrics['train_n']} (2018.11 – 2024.12)"),("Test Samples",f"{metrics['test_n']} (2025.01 – 2025.08)"),("Inference Period","2025.09 – 2026.04 (recent dashboard display)"),("Data Sources","Korea Tourism Organization (KTO), Korea Tourism Data Lab"),("Input Features","29 engineered variables (5 categories)"),("Target Variable","High / Medium / Low marketing priority")]:
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f1f5f9;font-size:13px;"><span style="color:#64748b;font-weight:500;">{k}</span><span style="color:#0f172a;font-weight:600;text-align:right;">{v}</span></div>""",unsafe_allow_html=True)
        st.markdown("""<div class="insight-box" style="margin-top:12px;"><b>Note on split:</b> Test set covers 2025.01–2025.08. Data from 2025.09 onward is used as recent inference data for dashboard display and is not part of model evaluation.</div>""",unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="lbl">Feature Categories (29 Total)</div>',unsafe_allow_html=True)
        for cat,feats in [("🧳 Visitor Metrics (10)","visitor_count, lag 1–3, MoM growth, 3M/6M moving avg, vs 3M avg, rolling std, country share"),("📱 SNS Metrics (9)","buzz_volume, engagement, potential_exposure, MoM changes, per-visitor ratios, buzz vs 3M avg"),("🇰🇷 Korean Wave (3)","hallyu_spend_count, MoM growth, per-visitor ratio"),("⚙️ Macro Variables (4)","exchange_rate, oil_price, month, quarter"),("📅 Seasonality (3)","is_peak_season, month (1–12), quarter (1–4)")]:
            st.markdown(f"""<div style="background:#f8fafc;border-radius:10px;padding:12px 14px;margin-bottom:8px;"><div style="font-size:13px;font-weight:600;color:#0f172a;margin-bottom:4px;">{cat}</div><div style="font-size:11px;color:#64748b;">{feats}</div></div>""",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="lbl">System Design Pipeline</div>',unsafe_allow_html=True)
    st.markdown("""<div style="background:#fff;border-radius:16px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);">
      <div style="font-size:13px;color:#475569;line-height:2.2;">
        <b style="color:#4f46e5;">Step 1 — Data Collection:</b> Monthly visitor statistics, SNS buzz &amp; engagement, Korean Wave spending, and macro indicators collected per country-month.<br/>
        <b style="color:#4f46e5;">Step 2 — Feature Engineering:</b> 29 variables generated including lag features, moving averages, growth rates, per-visitor ratios, and macro indicators.<br/>
        <b style="color:#4f46e5;">Step 3 — Proxy Label Construction:</b> Because direct ground-truth labels for marketing priority are not available, domain-informed proxy labels were constructed from historical visitor, SNS, sentiment, Korean Wave, and macro indicators. This weak-supervision approach allows the model to learn structured decision patterns from historical market conditions.<br/>
        <b style="color:#4f46e5;">Step 4 — Model Training:</b> Random Forest classifier trained on 29 input features using a time-based split to prevent data leakage.<br/>
        <b style="color:#4f46e5;">Step 5 — Prediction &amp; Display:</b> At inference time, only the ML model output is used. ML Priority Score = High Priority probability × 100.<br/>
        <b style="color:#4f46e5;">Step 6 — Scenario Calibration (What-If only):</b> For the interactive What-If Scenario only, the app applies a bounded post-processing calibration layer so that user-controlled changes respond in economically intuitive directions. This calibration is not used for model training, test evaluation, feature importance, confusion matrix, or the main dashboard ranking.
      </div>
    </div>""",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="lbl">User Interaction</div>',unsafe_allow_html=True)
    st.markdown("""<div style="background:#fff;border-radius:16px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.08);">
      <div style="font-size:13px;color:#475569;line-height:2.2;">
        Users can inspect ML-based market priority rankings on the <b>Overview</b> page,
        adjust market indicators in the <b>Priority Engine</b> and receive real-time ML predictions,
        simulate what-if scenarios via sliders with economically interpretable feedback,
        compare two markets head-to-head using <b>Compare Markets</b>,
        allocate marketing budgets proportionally to ML Priority Scores using the <b>Budget Planner</b>,
        explore traveler profiles and Korean Wave data in <b>Market Profiles</b>,
        and investigate historical trends across all metrics in <b>Analytics</b>.
        All revenue-related outputs are directional proxies, not causal ROI forecasts.
      </div>
    </div>""",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="lbl">Model Comparison — Why Random Forest?</div>',unsafe_allow_html=True)
    c1,c2=st.columns([1,1.4])
    with c1:
        comp_data={'Model':['Rule-Based Baseline','Logistic Regression','Random Forest ✓'],'Accuracy':[f"{metrics['rule_acc']*100:.1f}%",f"{metrics['lr_acc']*100:.1f}%",f"{metrics['rf_acc']*100:.1f}%"],'High F1':['N/A','~0.72',f"{metrics['cr']['High']['f1-score']:.2f}"],'Notes':['No training required','Linear boundaries only','Selected — best High F1']}
        st.dataframe(pd.DataFrame(comp_data),use_container_width=True,hide_index=True)
        st.markdown(f"""<div class="insight-box">Random Forest achieved the highest High Priority F1 ({metrics['cr']['High']['f1-score']:.2f}), the most critical metric for budget allocation — missing a high-potential market is costly. It captures non-linear variable interactions that logistic regression cannot.<br/><br/><b>Note:</b> The rule-based baseline above is a simple visitor-count threshold model for performance comparison only, distinct from the proxy label construction rules used to generate training labels.</div>""",unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="lbl">Confusion Matrix (Test Set: 2025.01 – 2025.08)</div>',unsafe_allow_html=True)
        cm=metrics['cm']; cls=metrics['classes']
        fig_cm=go.Figure(go.Heatmap(z=cm,x=[f"Pred: {c}" for c in cls],y=[f"Act: {c}" for c in cls],text=cm,texttemplate="%{text}",colorscale='Blues',showscale=False))
        fig_cm.update_layout(height=280,**CHART); st.plotly_chart(fig_cm,use_container_width=True)
    st.markdown("---")
    st.markdown('<div class="lbl">Classification Report</div>',unsafe_allow_html=True)
    cr=metrics['cr']
    cr_data=[{'Class':c,'Precision':f"{cr[c]['precision']:.2f}",'Recall':f"{cr[c]['recall']:.2f}",'F1 Score':f"{cr[c]['f1-score']:.2f}",'Support':int(cr[c]['support'])} for c in cls]
    st.dataframe(pd.DataFrame(cr_data),use_container_width=True,hide_index=True)
    st.markdown("""<div class="proxy-note" style="margin-top:16px;">
      <b>Revenue Proxy Note:</b> Revenue Opportunity Level and Market Value Proxy are directional business proxies, not causal ROI forecasts.
      They combine ML priority, visitor scale, average spending, momentum, SNS attention, and Korean Wave signals to support relative market comparison.
    </div>""",unsafe_allow_html=True)
