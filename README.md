📈 Stock Analysis Platform

An AI-powered stock analysis and forecasting dashboard focused on Indian markets (NSE).
Built with Python, Streamlit, and Gemini AI.

⚠️Disclaimer : This platform is for educational purposes only. 
* Not financial advice. Stock markets are highly unpredictable. 
* Always do your own research.

---

Live Demo
[Streamlit Cloud link after deployment]

---

Features :

Live Indian Stock Data — Real-time data via Yfinance API (NSE)
- 📊 Interactive Charts — Candlestick with SMA overlays, RSI, MACD
- 📉 Technical Indicators — SMA, EMA, RSI, MACD
- 🤖 ML Forecasting — Random Forest model trained on 5 years of data
- AI Insights — Gemini AI generated market summaries and trend analysis
- Explainability — Feature importance shows why the model made its prediction
- 🇮🇳 Indian Market Focus — RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS and more

---

Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Data | Yfinance, pandas, numpy |
| ML | Scikit-learn (Random Forest) |
| Visualization | Plotly |
| AI Insights | Google Gemini 2.5 Flash API |
| Language | Python 3.9+ |

---

Project Structure

```
stock-analysis-platform/
│
├── app/
│   ├── main.py              --> Streamlit entry point
│   ├── data/
│   │   └── fetcher.py       --> Live stock data via yfinance
│   ├── indicators/
│   │   └── technical.py     --> SMA, EMA, RSI, MACD
│   ├── models/
│   │   └── forecaster.py    --> Random Forest forecasting
│   ├── ai/
│   │   └── insights.py      --> Gemini AI market insights
│   └── ui/
│       └── charts.py        --> Plotly chart builders
│
├── .env                     --> API keys (never committed)
├── requirements.txt
└── README.md
```
---

⚙️ Setup & Installation

1. Clone the repository
```bash
git clone https://github.com/Ayushkmt/Stock-Analysis-Platform.git
cd Stock-Analysis-Platform
```
2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up environment variables
Create a `.env` file in the root directory:

5. Run the app
```bash
streamlit run app/main.py
```
---
📊 Model Performance

| Stock | R² Score | MAE |
|---|---|---|
| WIPRO.NS | 0.93 | ₹4.37 |
| RELIANCE.NS | 0.68 | ₹28.71 |
| HDFCBANK.NS | 0.59 | ₹44.59 |

* Model performance varies by stock volatility and sector sensitivity.
* Banking stocks are more sensitive to macro factors like RBI policy.

Working Flow-Chart

🔍 User inputs a stock ticker (e.g. RELIANCE.NS)

⬇️

Yfinance fetches 5 years of live NSE data

⬇️

📊 Technical indicators calculated (SMA, EMA, RSI, MACD)

⬇️

🤖 Random Forest model trained and forecasts next day price

⬇️

Gemini AI generates market summary and trend explanation

⬇️

Interactive dashboard displays everything visually
---
⚠️ Limitations

- ML model provides trend direction, not guaranteed price prediction
- AI insights are based on technical indicators only, not fundamentals or news
- Free tier Gemini API has rate limits (20 requests/day)
- Stock splits may affect historical data consistency

---

Author:
**Ayush Kamat**  
[GitHub](https://github.com/Ayushkmt) | [LinkedIn](your-linkedin-url)
