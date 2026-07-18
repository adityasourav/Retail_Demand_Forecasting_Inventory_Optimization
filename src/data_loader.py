import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mysql+pymysql",
    username="root",          # change if different
    password="Aditya@123",    # your password
    host="localhost",
    database="retail_forecasting"
)

engine = create_engine(connection_url)

def load_data():
    query = "SELECT * FROM retail_sales"
    return pd.read_sql(query, engine)