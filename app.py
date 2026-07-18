import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import joblib

# -----------------------------
# Load Machine Learning Model
# -----------------------------
model = joblib.load("models/random_forest_model.pkl")
model_columns = joblib.load("models/model_columns.pkl")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📦",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📋 Navigation")

page = st.sidebar.radio(
    "Select a Page",
    [
        "🏠 Home",
        "📈 Demand Forecasting",
        "📦 Inventory Optimization",
        "🔮 Predict Demand",
        "🤖 Model Comparison"
    ]
)

# -----------------------------
# HOME
# -----------------------------
if page == "🏠 Home":

    inventory = pd.read_csv("data/inventory_results.csv")

    total_products = inventory["Product_ID"].nunique()
    avg_inventory = round(inventory["Inventory_Level"].mean(), 2)
    avg_demand = round(inventory["Average_Daily_Demand"].mean(), 2)
    reorder_products = len(
        inventory[
            inventory["Inventory_Status"] == "Reorder Required"
        ]
    )

    st.title("📦 Retail Demand Forecasting Dashboard")

    st.caption(
        "End-to-End Machine Learning | Inventory Optimization | Business Analytics"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Products", total_products)
    c2.metric("Average Demand", avg_demand)
    c3.metric("Average Inventory", avg_inventory)
    c4.metric("Need Reorder", reorder_products)

    st.divider()

    st.subheader("📌 Project Overview")

    st.markdown("""
This dashboard predicts retail demand and helps optimize inventory using machine learning.

### Technologies Used

- Python
- MySQL
- Pandas
- Scikit-Learn
- ARIMA
- XGBoost
- Streamlit
""")
# -----------------------------
# FORECASTING
# -----------------------------
elif page == "📈 Demand Forecasting":

    st.title("📈 Demand Forecasting")

    st.subheader("Model Performance")

    metrics = pd.DataFrame({
        "Metric": ["MAE", "RMSE", "R²"],
        "Value": [12.82, 17.07, 0.868]
    })

    st.table(metrics)

    st.divider()

    try:

        forecast = pd.read_csv("data/forecast_results.csv")

        fig, ax = plt.subplots(figsize=(10,5))

        ax.plot(forecast["Actual"], label="Actual")
        ax.plot(forecast["Predicted"], label="Predicted")

        ax.set_title("Actual vs Predicted Demand")
        ax.set_xlabel("Observations")
        ax.set_ylabel("Demand")
        ax.legend()

        st.pyplot(fig)

    except Exception as e:

        st.error("forecast_results.csv not found.")
        st.write(e)

# -----------------------------
# INVENTORY
# -----------------------------
elif page == "📦 Inventory Optimization":

    st.title("📦 Inventory Optimization")

    try:

        inventory = pd.read_csv("data/inventory_results.csv")

        selected_product = st.selectbox(
            "Select Product",
            ["All"] + sorted(inventory["Product_ID"].unique())
        )

        if selected_product != "All":
            inventory = inventory[
                inventory["Product_ID"] == selected_product
                ]

        st.subheader("Inventory Table")

        st.dataframe(inventory)

        csv = inventory.to_csv(index=False)

        st.download_button(
            label="📥 Download Inventory Report",
            data=csv,
            file_name="inventory_report.csv",
            mime="text/csv"
        )

        st.divider()

        low_stock = inventory[
            inventory["Inventory_Status"] == "Reorder Required"
        ]

        st.subheader("Products Requiring Reorder")

        st.dataframe(low_stock)

    except Exception as e:

        st.error("inventory_results.csv not found.")
        st.write(e)
# -----------------------------
# PREDICT DEMAND
# -----------------------------
# -----------------------------
# PREDICT DEMAND
# -----------------------------
elif page == "🔮 Predict Demand":

    st.title("🔮 Predict Demand")

    st.write("Enter product information to predict demand.")

    # Numerical Inputs
    price = st.number_input("Price", value=100.0)
    discount = st.slider("Discount (%)", 0, 50, 10)
    inventory = st.number_input("Inventory Level", value=200)
    units_sold = st.number_input("Units Sold", value=100)
    units_ordered = st.number_input("Units Ordered", value=120)
    competitor_price = st.number_input("Competitor Price", value=95.0)

    epidemic = st.selectbox("Epidemic", [0, 1])
    promotion = st.selectbox("Promotion", [0, 1])

    category = st.selectbox(
        "Category",
        ["Electronics", "Furniture", "Clothing", "Groceries"]
    )

    region = st.selectbox(
        "Region",
        ["North", "South", "East", "West"]
    )

    weather = st.selectbox(
        "Weather",
        ["Sunny", "Rainy", "Cloudy", "Snowy"]
    )

    season = st.selectbox(
        "Season",
        ["Spring", "Summer", "Autumn", "Winter"]
    )

    month = st.slider("Month", 1, 12, 6)

    day = st.slider("Day", 1, 31, 15)

    dayofweek = st.slider("Day Of Week", 0, 6, 2)

    quarter = (month - 1) // 3 + 1

    weekofyear = 25

    inventory_turnover = units_sold / max(inventory, 1)

    discounted_price = price * (1 - discount / 100)

    if st.button("Predict Demand"):

        input_df = pd.DataFrame(
            columns=model_columns
        )

        input_df.loc[0] = 0

        # Numerical features
        input_df["Inventory_Level"] = inventory
        input_df["Units_Sold"] = units_sold
        input_df["Units_Ordered"] = units_ordered
        input_df["Price"] = price
        input_df["Discount"] = discount
        input_df["Promotion"] = promotion
        input_df["Competitor_Pricing"] = competitor_price
        input_df["Epidemic"] = epidemic

        input_df["Month"] = month
        input_df["Day"] = day
        input_df["DayOfWeek"] = dayofweek
        input_df["Quarter"] = quarter
        input_df["WeekOfYear"] = weekofyear

        input_df["Inventory_Turnover"] = inventory_turnover
        input_df["Discounted_Price"] = discounted_price

        # One-hot encoded columns
        category_col = f"Category_{category}"
        if category_col in input_df.columns:
            input_df.loc[0, category_col] = 1

        region_col = f"Region_{region}"
        if region_col in input_df.columns:
            input_df.loc[0, region_col] = 1

        weather_col = f"Weather_Condition_{weather}"
        if weather_col in input_df.columns:
            input_df.loc[0, weather_col] = 1

        season_col = f"Seasonality_{season}"
        if season_col in input_df.columns:
            input_df.loc[0, season_col] = 1

        prediction = model.predict(input_df)[0]

        if prediction >= 120:
            st.success(f"📈 Predicted Demand: {prediction:.2f} units")
            st.markdown("### 🟢 High Demand")
            st.info("Recommendation: Increase inventory to avoid stock-outs.")

        elif prediction >= 70:
            st.warning(f"📈 Predicted Demand: {prediction:.2f} units")
            st.markdown("### 🟡 Medium Demand")
            st.info("Recommendation: Current inventory appears sufficient.")

        else:
            st.error(f"📈 Predicted Demand: {prediction:.2f} units")
            st.markdown("### 🔴 Low Demand")
            st.info("Recommendation: Avoid overstocking. Consider promotions if needed.")

# -----------------------------
# MODEL COMPARISON
# -----------------------------
elif page == "🤖 Model Comparison":

    st.title("🤖 Model Comparison")

    comparison = pd.DataFrame({

        "Model":[
            "Random Forest",
            "ARIMA",
            "XGBoost"
        ],

        "MAE":[
            12.82,
            3169.64,
            1020.99
        ],

        "RMSE":[
            17.07,
            3644.91,
            1431.94
        ],

        "R²":[
            0.868,
            -3.006,
            0.334
        ]

    })

    fig = px.bar(
        comparison,
        x="Model",
        y="R²",
        color="Model",
        title="Model Comparison (R² Score)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success("Random Forest is selected as the final deployment model.")
