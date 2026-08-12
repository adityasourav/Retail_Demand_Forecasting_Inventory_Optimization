import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import joblib


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "images",
    "models",
    "random_forest_model.pkl"
)

COLUMNS_PATH = os.path.join(
    BASE_DIR,
    "images",
    "models",
    "model_columns.pkl"
)

INVENTORY_PATH = os.path.join(
    BASE_DIR,
    "data",
    "inventory_results.csv"
)

FORECAST_PATH = os.path.join(
    BASE_DIR,
    "data",
    "forecast_results.csv"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📦",
    layout="wide"
)


# ============================================================
# LOAD MODEL
# ============================================================

try:

    model = joblib.load(MODEL_PATH)
    model_columns = joblib.load(COLUMNS_PATH)

except Exception as e:

    st.error(f"Unable to load model files: {e}")
    st.stop()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("📋 Navigation")

page = st.sidebar.radio(
    "Select a Page",
    [
        "🏠 Home",
        "📈 Demand Forecasting",
        "📦 Inventory Optimization",
        "Predict Demand",
        "🤖 Model Comparison"
    ]
)


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    try:

        inventory = pd.read_csv(INVENTORY_PATH)

        total_products = inventory["Product_ID"].nunique()

        avg_inventory = round(
            inventory["Inventory_Level"].mean(),
            2
        )

        avg_demand = round(
            inventory["Average_Daily_Demand"].mean(),
            2
        )

        reorder_products = len(
            inventory[
                inventory["Inventory_Status"] == "Reorder Required"
            ]
        )

        st.title("📦 Retail Demand Forecasting Dashboard")

        st.caption(
            "End-to-End Machine Learning | "
            "Inventory Optimization | Business Analytics"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Products",
            total_products
        )

        c2.metric(
            "Average Demand",
            avg_demand
        )

        c3.metric(
            "Average Inventory",
            avg_inventory
        )

        c4.metric(
            "Need Reorder",
            reorder_products
        )

        st.divider()

        st.subheader("📌 Project Overview")

        st.markdown(
            """
            This dashboard predicts retail demand and helps optimize
            inventory using machine learning.

            ### Technologies Used

            - Python
            - MySQL
            - Pandas
            - Scikit-Learn
            - ARIMA
            - XGBoost
            - Random Forest
            - Streamlit
            """
        )

    except Exception as e:

        st.error("Unable to load inventory data.")
        st.write(e)


# ============================================================
# DEMAND FORECASTING
# ============================================================

elif page == "📈 Demand Forecasting":

    st.title("📈 Demand Forecasting")

    st.subheader("Model Performance")

    metrics = pd.DataFrame(
        {
            "Metric": [
                "MAE",
                "RMSE",
                "R²"
            ],
            "Value": [
                12.89,
                17.20,
                0.866
            ]
        }
    )

    st.table(metrics)

    st.divider()

    try:

        forecast = pd.read_csv(FORECAST_PATH)

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.plot(
            forecast["Actual"],
            label="Actual"
        )

        ax.plot(
            forecast["Predicted"],
            label="Predicted"
        )

        ax.set_title(
            "Actual vs Predicted Demand"
        )

        ax.set_xlabel(
            "Observations"
        )

        ax.set_ylabel(
            "Demand"
        )

        ax.legend()

        st.pyplot(fig)

    except Exception as e:

        st.error(
            "Unable to load forecast results."
        )

        st.write(e)


# ============================================================
# INVENTORY OPTIMIZATION
# ============================================================

elif page == "📦 Inventory Optimization":

    st.title("📦 Inventory Optimization")

    try:

        inventory = pd.read_csv(
            INVENTORY_PATH
        )

        selected_product = st.selectbox(
            "Select Product",
            ["All"]
            + sorted(
                inventory["Product_ID"].unique()
            )
        )

        if selected_product != "All":

            inventory = inventory[
                inventory["Product_ID"]
                == selected_product
            ]

        st.subheader(
            "Inventory Table"
        )

        st.dataframe(
            inventory,
            use_container_width=True
        )

        csv = inventory.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Inventory Report",
            data=csv,
            file_name="inventory_report.csv",
            mime="text/csv"
        )

        st.divider()

        low_stock = inventory[
            inventory["Inventory_Status"]
            == "Reorder Required"
        ]

        st.subheader(
            "Products Requiring Reorder"
        )

        st.dataframe(
            low_stock,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            "Unable to load inventory results."
        )

        st.write(e)


# ============================================================
# PREDICT DEMAND
# ============================================================

elif page == "Predict Demand":

    st.title("Predict Demand")

    st.write(
        "Enter product information to predict expected demand."
    )

    st.divider()

    # --------------------------------------------------------
    # PRODUCT / NUMERICAL INPUTS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        price = st.number_input(
            "Price",
            min_value=0.0,
            value=100.0,
            step=1.0
        )

        discount = st.slider(
            "Discount (%)",
            min_value=0,
            max_value=50,
            value=10
        )

        inventory = st.number_input(
            "Inventory Level",
            min_value=0,
            value=200,
            step=1
        )

        units_sold = st.number_input(
            "Units Sold",
            min_value=0,
            value=100,
            step=1
        )

    with col2:

        units_ordered = st.number_input(
            "Units Ordered",
            min_value=0,
            value=120,
            step=1
        )

        competitor_price = st.number_input(
            "Competitor Price",
            min_value=0.0,
            value=95.0,
            step=1.0
        )

        epidemic = st.selectbox(
            "Epidemic",
            [0, 1]
        )

        promotion = st.selectbox(
            "Promotion",
            [0, 1]
        )

    with col3:

        category = st.selectbox(
            "Category",
            [
                "Electronics",
                "Furniture",
                "Groceries",
                "Toys"
            ]
        )

        region = st.selectbox(
            "Region",
            [
                "North",
                "South",
                "West"
            ]
        )

        weather = st.selectbox(
            "Weather",
            [
                "Sunny",
                "Rainy",
                "Snowy"
            ]
        )

        season = st.selectbox(
            "Season",
            [
                "Spring",
                "Summer",
                "Winter"
            ]
        )

    # --------------------------------------------------------
    # DATE FEATURES
    # --------------------------------------------------------

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        year = st.number_input(
            "Year",
            min_value=2000,
            max_value=2100,
            value=2026,
            step=1
        )

    with col2:

        month = st.slider(
            "Month",
            1,
            12,
            6
        )

    with col3:

        day = st.slider(
            "Day",
            1,
            31,
            15
        )

    with col4:

        dayofweek = st.slider(
            "Day Of Week",
            0,
            6,
            2
        )

    # --------------------------------------------------------
    # DERIVED FEATURES
    # --------------------------------------------------------

    quarter = (
        (month - 1) // 3
    ) + 1

    weekofyear = 25

    inventory_turnover = (
        units_sold / max(inventory, 1)
    )

    discounted_price = (
        price * (1 - discount / 100)
    )

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    if st.button(
        "🔮 Predict Demand",
        use_container_width=True
    ):

        try:

            # Create dataframe using the exact
            # deployment feature schema
            input_df = pd.DataFrame(
                0,
                index=[0],
                columns=model_columns
            )

            # ------------------------------------------------
            # NUMERICAL FEATURES
            # ------------------------------------------------

            input_df["Inventory_Level"] = inventory

            input_df["Units_Sold"] = units_sold

            input_df["Units_Ordered"] = units_ordered

            input_df["Price"] = price

            input_df["Discount"] = discount

            input_df["Promotion"] = promotion

            input_df["Competitor_Pricing"] = (
                competitor_price
            )

            input_df["Epidemic"] = epidemic

            # ------------------------------------------------
            # DATE FEATURES
            # ------------------------------------------------

            input_df["Year"] = year

            input_df["Month"] = month

            input_df["Day"] = day

            input_df["DayOfWeek"] = dayofweek

            input_df["Quarter"] = quarter

            input_df["WeekOfYear"] = weekofyear

            # ------------------------------------------------
            # ENGINEERED FEATURES
            # ------------------------------------------------

            input_df["Inventory_Turnover"] = (
                inventory_turnover
            )

            input_df["Discounted_Price"] = (
                discounted_price
            )

            # ------------------------------------------------
            # ONE-HOT ENCODING
            # ------------------------------------------------

            category_col = (
                f"Category_{category}"
            )

            if category_col in input_df.columns:

                input_df.loc[
                    0,
                    category_col
                ] = 1

            region_col = (
                f"Region_{region}"
            )

            if region_col in input_df.columns:

                input_df.loc[
                    0,
                    region_col
                ] = 1

            weather_col = (
                f"Weather_Condition_{weather}"
            )

            if weather_col in input_df.columns:

                input_df.loc[
                    0,
                    weather_col
                ] = 1

            season_col = (
                f"Seasonality_{season}"
            )

            if season_col in input_df.columns:

                input_df.loc[
                    0,
                    season_col
                ] = 1

            # ------------------------------------------------
            # FINAL FEATURE VALIDATION
            # ------------------------------------------------

            if len(model_columns) != 29:

                st.error(
                    f"Expected 29 model features, "
                    f"but model_columns.pkl contains "
                    f"{len(model_columns)}."
                )

                st.stop()

            missing_features = [
                feature
                for feature in model_columns
                if feature not in input_df.columns
            ]

            if missing_features:

                st.error(
                    f"Missing features: "
                    f"{missing_features}"
                )

                st.stop()

            # Ensure exact feature order
            input_df = input_df[
                model_columns
            ]

            # ------------------------------------------------
            # MODEL PREDICTION
            # ------------------------------------------------

            prediction = model.predict(
                input_df
            )[0]

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            st.divider()

            st.subheader(
                "Prediction Result"
            )

            st.metric(
                "Predicted Demand",
                f"{prediction:.2f} units"
            )

            if prediction >= 120:

                st.success(
                    "🟢 High Demand"
                )

                st.info(
                    "Recommendation: Increase "
                    "inventory to reduce the risk "
                    "of stock-outs."
                )

            elif prediction >= 70:

                st.warning(
                    "🟡 Medium Demand"
                )

                st.info(
                    "Recommendation: Current "
                    "inventory appears sufficient."
                )

            else:

                st.error(
                    "🔴 Low Demand"
                )

                st.info(
                    "Recommendation: Avoid "
                    "overstocking. Consider "
                    "promotions if required."
                )

        except Exception as e:

            st.error(
                f"Prediction failed: {e}"
            )


# ============================================================
# MODEL COMPARISON
# ============================================================

elif page == "🤖 Model Comparison":

    st.title(
        "🤖 Model Comparison"
    )

    comparison = pd.DataFrame(
        {
            "Model": [
                "Random Forest",
                "ARIMA",
                "XGBoost"
            ],

            "MAE": [
                12.89,
                3169.64,
                1020.99
            ],

            "RMSE": [
                17.20,
                3644.91,
                1431.94
            ],

            "R²": [
                0.866,
                -3.006,
                0.334
            ]
        }
    )

    st.dataframe(
        comparison,
        use_container_width=True
    )

    fig = px.bar(
        comparison,
        x="Model",
        y="R²",
        color="Model",
        title="Model Comparison — R² Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        "Random Forest is selected as "
        "the final deployment model."
    )