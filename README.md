# Aerospace & Mechanical Intelligence Suite (Power BI PBIP + AI Forecasting)

End-to-end **Power BI Project (PBIP / TMDL)** business intelligence and quantitative forecasting pipeline benchmarking **18 global and Indian aerospace, defense, and industrial engineering leaders** across a 10-year historical horizon (2016–2026) and a 3-year AI-projected trajectory (2026–2029).

---

## Repository Architecture

\\\	ext
PBI_Dashboards/
├── 01_fetch_and_forecast.py         # Market data ingestion, normalization (Base 100) & 3Y AI confidence cone generation
├── 02_generate_pbip.py              # Programmatic PBIP, TMDL semantic model, DAX measure & PBIR visual generator
├── data/
│   ├── aerospace_data.csv           # 9 Aerospace & Defense peers (1,371 monthly records)
│   └── mechanical_data.csv          # 9 Mechanical & Industrial peers (1,404 monthly records)
└── output/
    ├── Aerospace_Intelligence/      # 4-page Power BI Project (.pbip + .Report + .SemanticModel)
    └── Mechanical_Intelligence/     # 4-page Power BI Project (.pbip + .Report + .SemanticModel)
\\\

---

## Dashboard Pages & Analytical Scope

1. **Command Center (Aerospace / Mechanical)**
   * Executive KPI cards: Average Market Cap, 3-Year AI Projected Growth, Operating Margin, and NLP News Sentiment.
   * 10-year historical + 3-year AI growth trajectory (Base 100) and Operating Margin vs. 3Y AI Growth bubble quadrant.
   * 3Y AI Growth Leaderboard, Annualized Revenue Run-Rate share, and Peer Fundamentals matrix.
2. **Company AI Forecast Cone**
   * Single-company deep dive featuring 10-year actuals alongside Median, Upper 85%, and Lower 15% AI confidence bounds and annualized revenue projections.
3. **Peer Financial Matrix**
   * Side-by-side 10-year historical return vs. 3-year AI forward growth, ROE vs. Operating Margin comparison, market cap treemap, and full financial scorecard.
4. **Cross-Sector Comparison (All 18 Peers)**
   * Head-to-head sector benchmarking comparing **Aerospace** (+435.0% 10Y historical return, +3.5% 3Y AI growth, 30.8% ROE) against **Mechanical** (+405.1% 10Y historical return, +11.0% 3Y AI growth, 14.5% operating margin).

---

## Covered Peer Universe

* **Aerospace & Defense:** Airbus SE (AIR.PA), Bharat Dynamics (BDL.NS), Bharat Electronics (BEL.NS), Boeing (BA), GE Aerospace (GE), Hindustan Aeronautics (HAL.NS), Lockheed Martin (LMT), RTX Corporation (RTX), Safran SA (SAF.PA).
* **Mechanical & Industrial:** Bharat Forge (BHARATFORG.NS), Caterpillar (CAT), Cummins Inc. (CMI), Cummins India (CUMMINSIND.NS), Larsen & Toubro (LT.NS), Parker-Hannifin (PH), Schneider Electric (SU.PA), Siemens AG (SIE.DE), Thermax (THERMAX.NS).

---

## How to Run & Open

1. **Regenerate Datasets & PBIP Projects:**
   \\\ash
   python 01_fetch_and_forecast.py
   python 02_generate_pbip.py
   \\\
2. **Open in Power BI Desktop:**
   * Double-click \output/Aerospace_Intelligence/Aerospace_Intelligence.pbip\ or \output/Mechanical_Intelligence/Mechanical_Intelligence.pbip\ and click **Refresh** in the **Home** ribbon.