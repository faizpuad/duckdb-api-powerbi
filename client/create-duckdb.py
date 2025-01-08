import duckdb

table_name = "banking_data"

# Create or connect to a DuckDB database file
conn = duckdb.connect('../database/banking_data.duckdb')

# Verify connection
print("Database connected successfully!")

# Step 1: Define the Schema for the Table
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    Customer_Name VARCHAR,
    Customer_ID BIGINT,
    Product_of_Loan VARCHAR,
    Account_Number BIGINT,
    Date_of_Account_Opening DATETIME,
    Last_Transaction_Date DATETIME,
    Last_Transaction_Amount DOUBLE
);
"""
conn.execute(create_table_query)
print(f"Table `{table_name}` created with schema.")

conn.close()
print("Database saved and connection closed.")

