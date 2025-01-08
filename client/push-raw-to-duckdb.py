import os
import duckdb
import pandas as pd

# Directory containing CSV files
data_folder = '../raw-data/'
db_file = '../database/banking_data.duckdb'
table_name = 'banking_data'

# Get a list of all CSV files in the directory
csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.csv')]

# soecify duckdb database
conn = duckdb.connect('banking_data.duckdb')

# Load data into DuckDB
for csv_file in csv_files:
    # Load CSV into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Transform date columns into a consistent DATETIME format
    df['Date of Account Opening'] = pd.to_datetime(df['Date of Account Opening'], format='%Y-%m-%d')
    df['Last Transaction Date'] = pd.to_datetime(df['Last Transaction Date'], format='%Y-%m-%d')
    
    # Load transformed data into DuckDB
    conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")

print("All data loaded successfully.")

# Step 3: Verify the Loaded Data
result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
print(f"Total records in `{table_name}`: {result[0]}")

# Query sample data
sample_data = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()
print("Sample Data:", sample_data)

# Close the connection
conn.close()
print("Database connection closed.")

