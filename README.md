# 🌍 Global Phosphate Market Analytics Platform

> End-to-end Data Engineering, Data Analytics and Machine Learning platform for analyzing the global phosphate market and forecasting benchmark prices through 2030.

---

# 🚀 Project Overview

The Global Phosphate Market Analytics Platform is a complete end-to-end analytics solution designed to collect, process, analyze, visualize and forecast worldwide phosphate market data.

The project combines modern Data Engineering, Business Intelligence and Machine Learning techniques into one unified platform.

Instead of focusing only on dashboards, this project reproduces a real enterprise analytics architecture used inside modern organizations.

The platform integrates multiple public datasets including:

- Global phosphate prices
- Worldwide production
- International exports
- International imports
- Inflation indicators

The processed data is transformed into analytical datasets inside Snowflake before being consumed by Power BI dashboards, Machine Learning models and an interactive Streamlit application.

---

# 🎯 Project Objectives

The main objectives are:

- Build a complete data pipeline
- Automate data ingestion
- Clean and standardize raw datasets
- Design a modern Data Warehouse
- Produce business-ready analytics
- Train multiple Machine Learning models
- Forecast phosphate prices until 2030
- Develop interactive dashboards
- Deliver an enterprise-grade analytics platform

---

# 🏗 Architecture

```
                  Public Data Sources
                           │
                           ▼
                 Python Data Ingestion
                           │
                           ▼
                     MinIO (Bronze)
                           │
                           ▼
                  Snowflake Bronze Layer
                           │
                           ▼
                    dbt Silver Models
                           │
                           ▼
                     dbt Gold Models
               (Galaxy Schema Warehouse)
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Power BI Dashboard   Machine Learning   Streamlit App
```

---

# ⚙ Technology Stack

## Data Engineering

- Python
- SQL
- Snowflake
- dbt
- Apache Airflow
- MinIO

## Analytics

- Pandas
- NumPy
- Plotly
- Power BI
- Streamlit

## Machine Learning

- Scikit-learn
- ARIMA
- Random Forest
- XGBoost
- Prophet
- Linear Regression

## Version Control

- Git
- GitHub

---

# 📂 Project Structure

```
project/

│
├── airflow/
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── ingestion/
├── profiling/
├── sql/
├── dbt/
├── notebooks/
├── powerbi/
├── machine_learning/
│   ├── app/
│   ├── models/
│   ├── reports/
│   └── scripts/
│
├── docs/
│
└── README.md
```

---

# 📊 Data Sources

The project integrates several international datasets:

- Phosphate benchmark prices
- Global phosphate production
- International exports
- International imports
- Inflation indicators

Historical coverage:

**2016 → 2026**

Forecast horizon:

**2026 → 2030**

---

# 🧹 Data Engineering Pipeline

The pipeline performs:

- Data ingestion
- Data validation
- Data profiling
- Duplicate removal
- Missing value handling
- Type standardization
- Data transformation
- Gold layer creation

---

# 🏛 Data Warehouse

A Galaxy Schema was implemented inside Snowflake.

Dimension tables include:

- DIM_DATE
- DIM_COUNTRY
- DIM_COMMODITY

Fact tables include:

- FACT_PRICE
- FACT_PRODUCTION
- FACT_EXPORT
- FACT_IMPORT
- FACT_INFLATION
- FACT_PRICE_FORECAST

---

# 📈 Power BI Dashboard

The dashboard provides business insights including:

- Executive Overview
- Price Analytics
- Production Analysis
- Trade Analysis
- Interactive filtering
- KPI Monitoring
- Geographic visualizations
- Trend analysis

---

# 🤖 Machine Learning

Several forecasting models were evaluated.

Models:

- ARIMA
- Random Forest
- XGBoost
- Prophet
- Linear Regression

Evaluation metrics:

- MAE
- RMSE
- MAPE
- R²

Walk-Forward Validation was used for time-series evaluation.

---

# 🔮 Forecasting

The final forecasting pipeline generates monthly phosphate benchmark prices through:

**2030**

The forecast includes:

- Point predictions
- 95% confidence intervals
- Historical comparison
- Forecast visualization

---

# 💻 Streamlit Application

The project includes an enterprise-style web application featuring:

- Home
- Data Overview
- Market Analytics
- Machine Learning
- Forecast
- Model Comparison
- About

The application provides interactive visual analytics directly from the analytical warehouse.

---

# 📊 Key Features

✔ End-to-End Data Pipeline

✔ Modern Data Warehouse

✔ Automated Data Cleaning

✔ Interactive Dashboards

✔ Machine Learning Forecasting

✔ Time-Series Analysis

✔ Business Intelligence

✔ Forecast until 2030

✔ Professional Streamlit Application

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/ouiam555/projet_phosphate.git
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run the Streamlit Application

```bash
cd machine_learning

streamlit run app/app.py
```

---

# 📈 Project Workflow

1. Data Collection
2. Data Profiling
3. Data Cleaning
4. Bronze Layer
5. Silver Layer
6. Gold Layer
7. Analytics
8. Dashboard Development
9. Machine Learning
10. Forecast Generation
11. Interactive Web Application

---

# 📌 Future Improvements

Potential future enhancements include:

- Real-time data ingestion
- API integration
- Automated retraining
- MLOps pipeline
- Docker deployment
- CI/CD workflows
- Cloud deployment
- Explainable AI dashboards

---

# 👩 Author

**Ouiam El Khalfi**

Data Analyst | Data Engineering Enthusiast

GitHub

https://github.com/ouiam555

---

