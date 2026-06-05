import streamlit as st
import os
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Inbound Marketing Priority Recommender",
    page_icon="🎯",
    layout="wide"
)

@st.cache_resource
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'rf_model.pkl'), 'rb') as f:
        model = pickle.load(f)
    with open(os.path.join(base, 'label_encoder.pkl'), 'rb') as f:
        le = pickle.load(f)
    with open(os.path.join(base, 'feature_cols.pkl'), 'rb') as f:
        feature_cols = pickle.load(f)
    feat_imp = pd.read_csv(os.path.join(base, 'feature_importance.csv'), encoding='utf-8')
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

st.sidebar.title("🎯 Marketing Priority")
st.sidebar.markdown("**AI Inbound Marketing\nPriority Recommender**")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "📊 Dashboard",
    "🔮 Prediction",
    "👤 Visitor Profile",
    "📈 Data Explorer"
])

COUNTRY_EN = {'중국': 'China', '일본': 'Japan', '대만': 'Taiwan', '미국': 'USA', '홍콩': 'Hong Kong'}
PRIORITY_COLOR = {'High': '#FF4B4B', 'Medium': '#FFA500', 'Low': '#2196F3'}
PRIORITY_EMOJI = {'High': '🔴', 'Medium': '🟡', 'Low': '🔵'}

# ══════════════════════════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ══════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.title("🎯 AI Inbound Marketing Priority Recommender")
    st.markdown("**국가별 방한 외국인 데이터 + SNS 관심도 기반 마케팅 우선순위 추천 시스템**")
    st.markdown("> 면세점, 호텔, K-Beauty, OTA 등 관광 관련 기업의 마케팅 예산 배분 의사결정 지원")
    st.markdown("---")

    df['year_month'] = df['year_month'].astype(str).str.strip()
    latest_month = df['year_month'].max()
    latest = df[df['year_month'] == latest_month].copy()
    ym_display = f"{str(latest_month)[:4]}.{str(latest_month)[4:]}" if len(str(latest_month)) >= 6 else latest_month

    st.subheader(f"📅 Latest Priority Ranking — {ym_display}")
    cols = st.columns(5)
    for i, (_, row) in enumerate(latest.sort_values('priority_score', ascending=False).iterrows()):
        label = row.get('priority_label', 'N/A')
        color = PRIORITY_COLOR.get(label, '#888')
        emoji = PRIORITY_EMOJI.get(label, '⚪')
        with cols[i]:
            st.markdown(f"""
            <div style="background:{color}22; border-left:4px solid {color};
                        padding:12px; border-radius:8px; text-align:center;">
                <h4 style="margin:0;">{COUNTRY_EN.get(row['country'], row['country'])}</h4>
                <p style="font-size:28px; margin:4px 0;">{emoji}</p>
                <p style="font-size:18px; font-weight:bold; color:{color}; margin:0;">{label}</p>
                <p style="font-size:11px; color:#666; margin:0;">Score: {row['priority_score']:.3f}</p>
                <p style="font-size:11px; color:#666; margin:0;">{int(row['visitor_count']):,} visitors</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    df_plot = df.copy()
    df_plot['date_str'] = df_plot['year_month'].astype(str).apply(lambda x: f"{x[:4]}-{x[4:]}")

    with col1:
        st.subheader("📈 Monthly Visitor Trends")
        fig = px.line(df_plot, x='date_str', y='visitor_count', color='country',
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      labels={'visitor_count': 'Visitors', 'date_str': 'Month', 'country': 'Country'})
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💬 SNS Engagement Trends")
        fig2 = px.line(df_plot, x='date_str', y='engagement', color='country',
                       color_discrete_sequence=px.colors.qualitative.Set2,
                       labels={'engagement': 'Engagement', 'date_str': 'Month', 'country': 'Country'})
        fig2.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🔍 Top 10 Feature Importance")
        fig3 = px.bar(feat_imp.head(10), x='importance', y='feature', orientation='h',
                      color='importance', color_continuous_scale='Reds')
        fig3.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0),
                           yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("📊 Priority Distribution by Country")
        if 'priority_label' in df.columns:
            label_count = df.groupby(['country', 'priority_label']).size().reset_index(name='count')
            fig4 = px.bar(label_count, x='country', y='count', color='priority_label',
                          color_discrete_map=PRIORITY_COLOR, barmode='group',
                          labels={'country': 'Country', 'count': 'Months', 'priority_label': 'Priority'})
            fig4.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig4, use_container_width=True)

    # 모델 성능 요약
    st.markdown("---")
    st.subheader("🤖 Model Performance Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Model", "Random Forest")
    m2.metric("Accuracy", "77.4%")
    m3.metric("Training Samples", "336")
    m4.metric("Features Used", "26")

# ══════════════════════════════════════════════════════════════════
# PAGE 2: PREDICTION
# ══════════════════════════════════════════════════════════════════
elif page == "🔮 Prediction":
    st.title("🔮 Marketing Priority Prediction")
    st.markdown("국가와 최근 데이터를 선택하면 다음 달 마케팅 우선순위를 예측합니다.")
    st.markdown("---")

    country_sel = st.selectbox("🌏 국가 선택", ['중국', '일본', '대만', '미국', '홍콩'],
                                format_func=lambda x: f"{COUNTRY_EN[x]} ({x})")

    country_data = df[df['country'] == country_sel].sort_values('year_month').iloc[-1]

    st.markdown("#### 📥 Input Data")
    st.caption("최근 데이터로 자동 입력되었습니다. 값을 조정하여 시나리오를 테스트할 수 있습니다.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**🧳 방문객 데이터**")
        visitor_count = st.number_input("Current Month Visitors", value=int(country_data['visitor_count']), step=1000)
        visitor_lag1 = st.number_input("Last Month Visitors", value=int(country_data['visitor_lag1']), step=1000)
        visitor_lag2 = st.number_input("2 Months Ago", value=int(country_data['visitor_lag2']), step=1000)
        visitor_lag3 = st.number_input("3 Months Ago", value=int(country_data['visitor_lag3']), step=1000)
        visitor_3m_avg = st.number_input("3M Moving Average", value=float(country_data['visitor_3m_avg']), step=1000.0)
        visitor_6m_avg = st.number_input("6M Moving Average", value=float(country_data['visitor_6m_avg']), step=1000.0)
        country_share = st.number_input("Country Share (0~1)", value=float(country_data['country_share']),
                                         step=0.001, format="%.4f")

    with col2:
        st.markdown("**📱 SNS 데이터**")
        buzz_volume = st.number_input("Buzz Volume (언급량)", value=int(country_data['buzz_volume']), step=100)
        engagement = st.number_input("Engagement (인게이지먼트)", value=int(country_data['engagement']), step=1000)
        potential_exposure = st.number_input("Potential Exposure (잠재 노출량)",
                                              value=int(country_data['potential_exposure']), step=10000)
        positive_pct = st.slider("Positive Sentiment (%)", 0.0, 100.0,
                                  float(country_data['positive_pct']), 0.1)
        negative_pct = 100.0 - positive_pct
        st.caption(f"Negative Sentiment: {negative_pct:.1f}%")

    with col3:
        st.markdown("**📅 기타 정보**")
        month = st.selectbox("Month", list(range(1, 13)), index=int(country_data['month']) - 1)
        exchange_rate = st.number_input("Exchange Rate (원)", value=float(country_data['exchange_rate']), step=1.0)
        oil_price = st.number_input("Oil Price (USD/barrel)", value=float(country_data['oil_price']), step=1.0)

    # 파생변수 자동 계산
    visitor_mom_growth = (visitor_count - visitor_lag1) / visitor_lag1 if visitor_lag1 != 0 else 0
    visitor_vs_3m_avg = visitor_count / visitor_3m_avg if visitor_3m_avg != 0 else 1
    visitor_rolling_std = float(country_data.get('visitor_rolling_std', 0))
    buzz_lag1 = float(country_data.get('buzz_lag1', buzz_volume))
    engagement_lag1 = float(country_data.get('engagement_lag1', engagement))
    exposure_lag1 = float(country_data.get('exposure_lag1', potential_exposure))
    buzz_mom_growth = (buzz_volume - buzz_lag1) / buzz_lag1 if buzz_lag1 != 0 else 0
    engagement_mom_growth = (engagement - engagement_lag1) / engagement_lag1 if engagement_lag1 != 0 else 0
    exposure_mom_growth = (potential_exposure - exposure_lag1) / exposure_lag1 if exposure_lag1 != 0 else 0
    engagement_per_visitor = engagement / visitor_count if visitor_count != 0 else 0
    buzz_per_visitor = buzz_volume / visitor_count if visitor_count != 0 else 0
    buzz_3m_avg = float(country_data.get('buzz_3m_avg', buzz_volume))
    buzz_vs_3m_avg = buzz_volume / buzz_3m_avg if buzz_3m_avg != 0 else 1
    quarter = (month - 1) // 3 + 1
    is_peak_season = 1 if month in [3, 4, 5, 9, 10] else 0

    # 한류 소비 데이터 (최근값 사용)
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

    st.markdown("---")
    if st.button("🚀 Predict Marketing Priority", type="primary", use_container_width=True):
        # input_data에 없는 feature는 0으로 채움
        input_df = pd.DataFrame([input_data])
        for col in feature_cols:
            if col not in input_df.columns:
                input_df[col] = 0
        X_input = input_df[feature_cols]
        pred = model.predict(X_input)[0]
        proba = model.predict_proba(X_input)[0]
        label = le.inverse_transform([pred])[0]
        color = PRIORITY_COLOR[label]
        emoji = PRIORITY_EMOJI[label]

        col_r1, col_r2, col_r3 = st.columns([1.2, 1, 1])

        with col_r1:
            st.markdown(f"""
            <div style="background:{color}22; border:3px solid {color};
                        padding:28px; border-radius:16px; text-align:center;">
                <h2 style="margin:0; color:#333;">{COUNTRY_EN[country_sel]}</h2>
                <p style="font-size:56px; margin:8px 0;">{emoji}</p>
                <h1 style="color:{color}; margin:0; font-size:32px;">Priority: {label}</h1>
                <p style="color:#666; margin-top:8px; font-size:13px;">
                    Confidence: {max(proba)*100:.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_r2:
            st.markdown("**📊 Prediction Confidence**")
            for cls, prob in zip(le.classes_, proba):
                c = PRIORITY_COLOR[cls]
                st.markdown(f"{PRIORITY_EMOJI[cls]} **{cls}**: {prob*100:.1f}%")
                st.progress(float(prob))

            st.markdown("---")
            st.markdown("**📌 Key Metrics**")
            st.markdown(f"- Visitors: **{visitor_count:,}**")
            st.markdown(f"- MoM Growth: **{visitor_mom_growth*100:+.1f}%**")
            st.markdown(f"- vs 3M Avg: **{visitor_vs_3m_avg:.2f}x**")
            st.markdown(f"- Country Share: **{country_share*100:.1f}%**")

        with col_r3:
            st.markdown("**💡 Signal Summary**")
            def signal(val, positive_direction=True):
                if positive_direction:
                    return "🟢" if val > 0.05 else ("🔴" if val < -0.05 else "🟡")
                else:
                    return "🔴" if val > 0.05 else ("🟢" if val < -0.05 else "🟡")

            st.markdown(f"{signal(visitor_mom_growth)} Visitor Growth: **{visitor_mom_growth*100:+.1f}%**")
            st.markdown(f"{signal(buzz_mom_growth)} Buzz Growth: **{buzz_mom_growth*100:+.1f}%**")
            st.markdown(f"{signal(engagement_mom_growth)} Engagement Growth: **{engagement_mom_growth*100:+.1f}%**")
            st.markdown(f"{signal(exposure_mom_growth)} Exposure Growth: **{exposure_mom_growth*100:+.1f}%**")
            st.markdown(f"{'🟢' if positive_pct >= 70 else '🟡' if positive_pct >= 50 else '🔴'} Positive Sentiment: **{positive_pct:.1f}%**")

            st.markdown("---")
            st.markdown("**🎯 Recommended Actions**")
            actions = {
                'High': [
                    "✅ Increase ad budget",
                    "✅ Run country-specific promotions",
                    "✅ Strengthen local-language content",
                    "✅ Prioritize influencer partnerships",
                ],
                'Medium': [
                    "🔄 Maintain current campaign",
                    "🔄 Monitor for upsurge signals",
                    "🔄 Test new formats moderately",
                ],
                'Low': [
                    "⏸️ Minimize budget allocation",
                    "⏸️ Focus on higher-priority markets",
                    "⏸️ Set recovery signal alerts",
                ]
            }
            for action in actions[label]:
                st.markdown(action)

# ══════════════════════════════════════════════════════════════════
# PAGE 3: VISITOR PROFILE
# ══════════════════════════════════════════════════════════════════
elif page == "👤 Visitor Profile":
    st.title("👤 Visitor Profile by Country")
    st.markdown("국가별 방한 관광객의 행태 및 만족도 분석 (2015~2024)")
    st.markdown("---")

    sat_df['date_str'] = sat_df['year'].astype(str)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 1인 평균 지출 경비 (USD)")
        fig = px.line(sat_df, x='date_str', y='spend_per_person_usd', color='country',
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      markers=True,
                      labels={'spend_per_person_usd': 'Spend per Person (USD)', 'date_str': 'Year'})
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📅 평균 체재 기간 (일)")
        fig = px.line(sat_df, x='date_str', y='stay_days', color='country',
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      markers=True,
                      labels={'stay_days': 'Stay Duration (days)', 'date_str': 'Year'})
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🔁 재방문율 (%)")
        fig = px.line(sat_df, x='date_str', y='revisit_rate', color='country',
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      markers=True,
                      labels={'revisit_rate': 'Revisit Rate (%)', 'date_str': 'Year'})
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("😊 전반적 만족도 & 추천 의향 (%)")
        latest_sat = sat_df[sat_df['year'] == sat_df['year'].max()].copy()
        latest_sat['country_en'] = latest_sat['country'].map(COUNTRY_EN)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Overall Satisfaction', x=latest_sat['country_en'],
                             y=latest_sat['overall_satisfaction'],
                             marker_color='#4CAF50'))
        fig.add_trace(go.Bar(name='Recommend Intention', x=latest_sat['country_en'],
                             y=latest_sat['recommend_intention'],
                             marker_color='#2196F3'))
        fig.add_trace(go.Bar(name='Revisit Intention', x=latest_sat['country_en'],
                             y=latest_sat['revisit_intention'],
                             marker_color='#FF9800'))
        fig.update_layout(barmode='group', height=300, margin=dict(l=0, r=0, t=10, b=0),
                          yaxis_range=[0, 105])
        st.plotly_chart(fig, use_container_width=True)

    # 최신연도 국가별 프로파일 카드
    st.markdown("---")
    st.subheader(f"📋 Country Profile Summary — {sat_df['year'].max()}년 기준")
    latest_sat = sat_df[sat_df['year'] == sat_df['year'].max()].copy()

    cols = st.columns(5)
    for i, (_, row) in enumerate(latest_sat.iterrows()):
        with cols[i]:
            country_en = COUNTRY_EN.get(row['country'], row['country'])
            st.markdown(f"""
            <div style="background:#f8f9fa; border:1px solid #dee2e6;
                        padding:14px; border-radius:10px; text-align:center;">
                <h4 style="margin:0 0 8px 0;">{country_en}</h4>
                <p style="margin:3px 0; font-size:13px;">💰 <b>${row['spend_per_person_usd']:,.0f}</b>/person</p>
                <p style="margin:3px 0; font-size:13px;">📅 <b>{row['stay_days']}</b> days</p>
                <p style="margin:3px 0; font-size:13px;">🔁 Revisit: <b>{row['revisit_rate']}%</b></p>
                <p style="margin:3px 0; font-size:13px;">😊 Satisfaction: <b>{row['overall_satisfaction']}%</b></p>
                <p style="margin:3px 0; font-size:13px;">📣 Recommend: <b>{row['recommend_intention']}%</b></p>
            </div>
            """, unsafe_allow_html=True)

    # 한류 소비 추이
    st.markdown("---")
    st.subheader("🇰🇷 한류 소비건수 추이 (2018~2026)")
    hallyu_plot = hallyu_df.copy()
    hallyu_plot['date_str'] = hallyu_plot['year_month'].astype(str).apply(lambda x: f"{x[:4]}-{x[4:]}")
    fig_h = px.line(hallyu_plot, x='date_str', y='total_count', color='country',
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    markers=False,
                    labels={'total_count': 'Hallyu Spending Count', 'date_str': 'Month'})
    fig_h.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_h, use_container_width=True)

    # 업종별 비율 (최신 연도)
    st.subheader("🛍️ 한류 업종별 소비 비율 — 최신 기준")
    latest_ym = hallyu_ind_df['year_month'].max()
    latest_ind = hallyu_ind_df[hallyu_ind_df['year_month'] == latest_ym].copy()
    fig_ind = px.bar(latest_ind, x='country', y='ratio', color='industry',
                     barmode='stack',
                     color_discrete_sequence=px.colors.qualitative.Pastel,
                     labels={'ratio': 'Ratio (%)', 'country': 'Country', 'industry': 'Industry'})
    fig_ind.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_ind, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 4: DATA EXPLORER
# ══════════════════════════════════════════════════════════════════
elif page == "📈 Data Explorer":
    st.title("📈 Data Explorer")
    st.markdown("---")

    country_filter = st.multiselect("국가 선택", ['중국', '일본', '대만', '미국', '홍콩'],
                                     default=['중국', '일본', '대만', '미국', '홍콩'])
    df_filtered = df[df['country'].isin(country_filter)].copy()
    df_filtered['date_str'] = df_filtered['year_month'].astype(str).apply(lambda x: f"{x[:4]}-{x[4:]}")

    metric = st.selectbox("지표 선택", ['visitor_count', 'buzz_volume', 'engagement',
                                        'potential_exposure', 'positive_pct', 'visitor_mom_growth'])

    fig = px.line(df_filtered, x='date_str', y=metric, color='country',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Buzz Volume 추이")
        fig2 = px.area(df_filtered, x='date_str', y='buzz_volume', color='country',
                       color_discrete_sequence=px.colors.qualitative.Set2)
        fig2.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("Priority Label 분포")
        if 'priority_label' in df_filtered.columns:
            label_count = df_filtered.groupby(['country', 'priority_label']).size().reset_index(name='count')
            fig3 = px.bar(label_count, x='country', y='count', color='priority_label',
                          color_discrete_map=PRIORITY_COLOR, barmode='group')
            fig3.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📋 Raw Data")
    display_cols = ['year_month', 'country', 'visitor_count', 'visitor_mom_growth',
                    'buzz_volume', 'engagement', 'positive_pct', 'priority_label']
    st.dataframe(
        df_filtered[display_cols].sort_values(['year_month', 'country'], ascending=[False, True]),
        use_container_width=True
    )
