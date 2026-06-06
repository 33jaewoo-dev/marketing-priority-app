# Inbound Marketing Intelligence
### AI-Powered Inbound Tourism Marketing Priority System

**Deployed App:** [https://marketing-priority-app-xtxpnj5xrhkmcxkowpkl27.streamlit.app](https://marketing-priority-app-xtxpnj5xrhkmcxkowpkl27.streamlit.app)

---

## Project Overview

Tourism marketers must decide which inbound markets deserve more campaign budget under limited resources. This system supports data-driven market prioritization by combining visitor demand, SNS attention, Korean Wave consumption, and macro indicators.

The system classifies five major inbound markets (China, Japan, Taiwan, USA, Hong Kong) into **High**, **Medium**, or **Low** marketing priority using a Random Forest classifier trained on 29 engineered features from country-month panel data.

---

## Key Features

- **ML Priority Ranking** — Dashboard showing ML-predicted priority scores for all five markets
- **Priority Engine** — Input market indicators and receive real-time ML predictions
- **What-If Scenario Simulator** — Adjust market conditions via sliders to simulate priority changes
- **Budget Planner** — Allocate marketing budgets proportionally to ML Priority Scores (Balanced / Aggressive / Conservative modes)
- **Market Profiles** — Traveler behavior, satisfaction, and Korean Wave spending analysis
- **Analytics** — Interactive trend exploration across all metrics
- **Data & Methodology** — Full technical documentation including model comparison, confusion matrix, and classification report

---

## Methodology

This project uses country-month panel data to classify inbound tourism markets into High, Medium, and Low marketing priority. Since direct ground-truth labels for marketing priority are not available, domain-informed proxy labels were constructed from historical visitor, SNS, sentiment, Korean Wave, and macro indicators. A Random Forest classifier was trained on 29 engineered features using a time-based split. The final ML Priority Score is defined as the predicted probability of High Priority multiplied by 100.

**Data period:** 2018.11 – 2026.04  
**Training period:** 2018.11 – 2024.12  
**Test period:** 2025.01 – 2025.08  
**Inference period:** 2025.09 – 2026.04 (recent dashboard display)  
**Test accuracy:** 73.8% | **High Priority F1:** 0.83

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
├── full_dataset.csv            # Country-month panel dataset with 29 engineered features and ML priority scores
├── satisfaction_data.csv       # Traveler profile and satisfaction data (2015–2024)
├── korean_wave_spending.csv    # Korean Wave spending transaction data
├── korean_wave_industry.csv    # Korean Wave category breakdown by industry
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview and setup instructions
```

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/33jaewoo-dev/marketing-priority-app.git
cd marketing-priority-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## Limitations

- Uses proxy labels because true marketing-priority labels are unavailable
- Limited to five major inbound markets
- SNS indicators may be sensitive to short-term viral events
- Does not yet include actual campaign ROI or conversion data
- Monthly data granularity may miss rapid short-term shifts

---

## Future Improvements

- Add actual ad spend and conversion data for supervised label generation
- Expand to more inbound markets beyond the current five
- Add SHAP-based local feature attribution for individual predictions
- Automate weekly or monthly data updates via Korea Tourism Data Lab API
- Build ROI prediction module connecting priority scores to campaign outcomes

---

## Course Information

**Course:** BUSS305 — Artificial Intelligence & Business  
**Institution:** Korea University Business School, Spring 2026  
**Project Type:** Individual Final Project
