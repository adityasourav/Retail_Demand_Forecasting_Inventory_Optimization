import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Database Connection
connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="Aditya@123",      # Your actual password
    host="localhost",
    port=3306,
    database="retail_forecasting",
)

engine = create_engine(connection_url)

# Load Data
df = pd.read_sql("SELECT * FROM retail_sales", engine)

# Basic Information
print("=" * 50)
print("Dataset Shape")
print(df.shape)

print("\n" + "=" * 50)
print("Columns")
print(df.columns)

print("\n" + "=" * 50)
print("Data Types")
print(df.dtypes)

print("\n" + "=" * 50)
print("Missing Values")
print(df.isnull().sum())

print("\n" + "=" * 50)
print("Duplicate Rows")
print(df.duplicated().sum())

print("\n" + "=" * 50)
print("Summary Statistics")
print(df.describe())