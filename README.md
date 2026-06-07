# Inbound Marketing Intelligence
### AI-Powered Inbound Tourism Marketing Priority System

**Deployed App:** [https://marketing-priority-app-xtxpnj5xrhkmcxkowpkl27.streamlit.app](https://marketing-priority-app-xtxpnj5xrhkmcxkowpkl27.streamlit.app)

---

## Project Overview

Tourism marketers must decide which inbound markets deserve more campaign budget under limited resources. **The core business question is which inbound market can serve as the strongest growth driver under limited marketing resources.** This system supports data-driven market prioritization by combining visitor demand, SNS attention, Korean Wave consumption, and macro indicators across five major markets: China, Japan, Taiwan, USA, and Hong Kong.

> **Important:** Revenue-related outputs (Revenue Opportunity Level, Market Value Proxy) are directional business proxies, not causal ROI forecasts. The scenario-adjusted score is designed for interactive simulation and should be interpreted as a directional what-if indicator, not as a causal ROI forecast.

---

## Key Features

- **Market Attractiveness Ranking** — Dashboard showing ML-informed Market Attractiveness Scores with confidence levels
- **Priority Engine** — Standard Input or What-If Scenario with real-time Random Forest predictions, score component breakdown, and Action Plan
- **What-If Scenario Simulator** — Sliders recalculate the Market Attractiveness Score as market conditions change, with a small bounded scenario calibration for usability
- **Budget Planner** — Market Attractiveness Score-based budget allocation (Balanced / Aggressive / Conservative)
- **Compare Markets** — Head-to-head market comparison with auto-generated interpretation
- **Market Profiles** — Traveler behavior, satisfaction, and Korean Wave spending analysis
- **Analytics** — Interactive trend exploration across all metrics
- **Data & Methodology** — Model comparison, confusion matrix, classification report, pipeline documentation

---

## Methodology

This project uses country-month panel data to classify inbound tourism markets into High, Medium, and Low marketing priority. Since direct ground-truth labels for marketing priority are not available, domain-informed proxy labels were constructed from historical visitor, SNS, sentiment, Korean Wave, and macro indicators. A Random Forest classifier was trained on 29 engineered features using a time-based split.

The Random Forest model predicts whether each market belongs to the High, Medium, or Low Priority class. Its High Priority probability is used as the ML component of the Market Attractiveness Score. The final Market Attractiveness Score combines ML probability with observable business signals:

- **45%** — ML High Priority Probability (Random Forest output)
- **20%** — Demand Score (visitor volume, momentum, vs 3-month average)
- **15%** — Digital Momentum Score (SNS engagement, buzz volume, growth rates)
- **10%** — Sentiment Score (positive sentiment %)
- **10%** — Revenue / Korean Wave Proxy Score (market value proxy, Korean Wave spending)

The What-If Scenario recalculates the Market Attractiveness Score as users adjust market indicators. A small bounded scenario calibration is applied only for interactive simulation usability and is not used for model training, evaluation, feature importance, or main dashboard ranking.

**Data period:** 2018.11 – 2026.04  
**Training period:** 2018.11 – 2024.12  
**Test period:** 2025.01 – 2025.08  
**Inference period:** 2025.09 – 2026.04 (recent dashboard display)

---

## Data Sources

| Source | Description |
|--------|-------------|
| Korea Tourism Organization (KTO) | Monthly inbound visitor statistics by country |
| Korea Tourism Data Lab | SNS buzz, engagement, potential exposure by country |
| Korea Tourism Data Lab | Korean Wave spending transaction data by category |
| Macro indicators | Exchange rate (KRW), international oil price (USD/barrel) |

---

## File Structure

```
marketing-priority-app/
├── app.py                      # Streamlit dashboard and ML prediction interface
├── full_dataset.csv            # Country-month panel dataset with 29 engineered features and ML scores
├── satisfaction_data.csv       # Traveler profile and satisfaction data (2015–2024)
├── korean_wave_spending.csv    # Korean Wave spending transaction data
├── korean_wave_industry.csv    # Korean Wave category breakdown by industry
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview and setup instructions
```

---

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Limitations

- Uses proxy labels because true marketing-priority labels are unavailable
- Limited to five major inbound markets
- SNS indicators may be sensitive to short-term viral events
- Does not include actual campaign ROI or conversion data
- Revenue-related outputs are directional business proxies, not causal ROI forecasts
- Scenario-adjusted scores are directional what-if indicators, not separate trained model outputs

---

## Future Improvements

- Add actual ad spend and conversion data for supervised label generation
- Expand to more inbound markets
- Add SHAP-based local feature attribution for individual predictions
- Automate monthly data updates via Korea Tourism Data Lab API
- Build campaign performance forecasting module using actual campaign data

---

**Course:** BUSS305 — Artificial Intelligence & Business · Korea University Business School · Spring 2026
