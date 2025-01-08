import os
import duckdb

# Define paths
database_path = '../database/banking_data.duckdb'  # Path to the existing DuckDB database
output_directory = '../output'                    # Dedicated output directory
output_file = os.path.join(output_directory, 'banking_data_style2.parquet')  # Output Parquet file path

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Connect to the DuckDB database
conn = duckdb.connect(database_path)

# Step 1: Export query results directly to Parquet file using the COPY command
export_query = f"""
COPY (SELECT * FROM banking_data) TO '{output_file}' (FORMAT 'parquet');
"""
conn.execute(export_query)
print(f"Data exported to Parquet file at: {output_file}")

# Close the connection
conn.close()
print("Connection to database closed.")
