import duckdb

# specify duckdb database
conn = duckdb.connect('../database/banking_data.duckdb')

# Sample query to verify date fields
query = """
SELECT 
    "Date_of_Account_Opening",
    "Last_Transaction_Date",
    "Last_Transaction_Amount" 
FROM banking_data 
LIMIT 5;
"""
results = conn.execute(query).fetchall()
print("Sample Data:", results)

conn.close()
print("Database saved and connection closed.")

