# 📊 Retail Demand Forecasting & Inventory Optimization

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![BI Tool](https://img.shields.io/badge/BI%20Tool-Power%20BI-F2C811.svg)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end Machine Learning-powered system that predicts future product demand, automates reorder recommendations, and provides businesses with interactive decision-support tools. This project bridges the gap between predictive modeling and actionable supply chain intelligence.

---

## 📌 Executive Summary

Maintaining the perfect balance of inventory is a classic retail challenge: overstocking ties up valuable capital, while stockouts lead to lost revenue and frustrated customers. 

This project follows the complete Data Science lifecycle—from raw data ingestion and feature engineering to model serialization and deployment—to solve this exact dilemma. By combining robust machine learning regressors (Random Forest, XGBoost) with classical time-series analysis (ARIMA), the system generates high-accuracy demand forecasts. These forecasts feed directly into an interactive **Streamlit Web Application** for real-time inference and an automated **Reorder Recommendation Engine** paired with an enterprise-ready **Power BI Dashboard**.

---

## ✨ Core Features

* **🔮 Demand Prediction Engine:** Instantly forecast product demand based on custom input parameters using our optimized production model.
* **📦 Inventory Optimization Module:** Calculates stock statuses dynamically, identifying items at risk of depletion.
* **🚨 Automated Reorder System:** Generates proactive replenishment recommendations based on forecasted demand thresholds.
* **📊 Dual-Front Interface:**
  * *Operational Tools:* Interactive Streamlit application for day-to-day warehouse and manager queries.
  * *Strategic Insights:* Enterprise Power BI dashboard for executive trend monitoring and high-level KPI tracking.
* **📈 Model Benchmarking:** Native comparative analysis dashboard displaying performance metrics ($R^2$, MAE, RMSE) across different algorithmic approaches.

---

## 🛠️ Tech Stack & Architecture

### **Data & Modeling Pipeline**
* **Data Processing:** Pandas, NumPy
* **Machine Learning:** Scikit-learn, XGBoost
* **Time Series Analysis:** Statsmodels (ARIMA)
* **Model Serialization:** Joblib

### **Visualization & Deployment**
* **Web Framework:** Streamlit
* **Business Intelligence:** Power BI
* **Plotting Libraries:** Matplotlib, Seaborn

---

## 📂 Project Structure

```text
Retail_Demand_Forecasting/
│
├── app.py                  # Main Streamlit web application
├── notebook.ipynb          # End-to-end EDA, Feature Engineering & Model Training
├── requirements.txt        # Python library dependencies
├── README.md               # Detailed project documentation
│
├── data/                   # Raw and processed datasets
│   └── (Data files intentionally omitted from git tracking)
│
├── models/                 # Serialized production models (.pkl)
│   └── random_forest_prod.pkl
│
└── images/                 # Dashboard previews and system visuals
    ├── workflow.png
    ├── home_page.png
    ├── predict_demand.png
    ├── inventory_optimization.png
    ├── products_requiring_reorder.png
    ├── model_comparison.png
    ├── correlation_heatmap.png
    ├── actual_vs_predicted.png
    ├── performance_metrics.png
    └── arima_forecast_vs_actual.png
