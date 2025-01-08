import os
import duckdb
# import pyarrow

# Define paths
database_path = '../database/banking_data.duckdb'  # Path to the existing DuckDB database
output_directory = '../output'                    # Dedicated output directory
output_file = os.path.join(output_directory, 'banking_data.parquet')  # Output Parquet file path

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Connect to the DuckDB database
conn = duckdb.connect(database_path)

# Step 1: Query the `banking_data` table
query = "SELECT * FROM banking_data limit 10;"
result = conn.execute(query).fetchdf()  # Fetch the data as a Pandas DataFrame
print("Queried data from `banking_data` table successfully!")

# Step 2: Export the queried data to a Parquet file
result.to_parquet(output_file)
print(f"Data exported to Parquet file at: {output_file}")

# Close the connection
conn.close()
print("Connection to database closed.")
