import os
from faker import Faker
import pandas as pd
import random
from datetime import datetime

# Initialize Faker and constants
fake = Faker()
months = ["2023-10", "2023-11", "2023-12"]
product_types = ["Home Loan", "Car Loan", "Personal Loan", "Education Loan", "Business Loan"]

# Directory for saving files
output_dir = "../raw-data"
os.makedirs(output_dir, exist_ok=True)

# Function to generate random data for one month
def generate_and_save_data_for_month(month, folder_path, num_records=100):
    data = []
    start_date = datetime.strptime(f"{month}-01", "%Y-%m-%d")
    end_date = datetime.strptime(f"{month}-28", "%Y-%m-%d")
    for _ in range(num_records):
        customer_id = fake.random_int(min=10**11, max=10**12-1)  # 12-digit ID
        account_number = fake.random_int(min=10**16, max=10**17-1)  # 17-digit number
        date_of_account_opening = fake.date_between(start_date=start_date.replace(year=start_date.year - 10), end_date=start_date)
        last_transaction_date = fake.date_between(start_date=date_of_account_opening, end_date=end_date)
        data.append({
            "Customer Name": fake.name(),
            "Customer ID": customer_id,
            "Product of Loan": random.choice(product_types),
            "Account Number": account_number,
            "Date of Account Opening": date_of_account_opening,
            "Last Transaction Date": last_transaction_date,
            "Last Transaction Amount": round(random.uniform(100.0, 5000.0), 2)
        })
    # Save to CSV
    file_path = os.path.join(folder_path, f"banking_customer_data_{month}.csv")
    pd.DataFrame(data).to_csv(file_path, index=False)
    return file_path

# Generate and save data for each month
file_paths_combined = [generate_and_save_data_for_month(month, output_dir) for month in months]

file_paths_combined
