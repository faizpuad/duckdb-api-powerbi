from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import duckdb
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key configuration (hardcoded for demo)
API_KEY = "demo-api-key-12345"  # You can change this to any value you want
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# API key validation
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=403,
        detail="Invalid API Key"
    )

@app.get("/banking-data")
async def get_banking_data(api_key: APIKey = Depends(get_api_key)):
    try:
        # Connect to DuckDB
        logger.debug("Connecting to database...")
        conn = duckdb.connect('./database/banking_data.duckdb', read_only=True)
        
        # Execute query
        logger.debug("Executing query...")
        query = """
        SELECT 
            Customer_Name,
            Customer_ID,
            Product_of_Loan,
            Account_Number,
            Date_of_Account_Opening::STRING as Date_of_Account_Opening,
            Last_Transaction_Date::STRING as Last_Transaction_Date,
            Last_Transaction_Amount
        FROM banking_data
        LIMIT 1000
        """
        
        # Fetch data and convert to JSON-compatible format
        df = conn.execute(query).fetchdf()
        
        # Convert timestamps to strings in ISO format
        if 'Date_of_Account_Opening' in df.columns:
            df['Date_of_Account_Opening'] = pd.to_datetime(df['Date_of_Account_Opening']).dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'Last_Transaction_Date' in df.columns:
            df['Last_Transaction_Date'] = pd.to_datetime(df['Last_Transaction_Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        data = df.to_dict(orient="records")
        
        logger.debug(f"Retrieved {len(data)} records successfully")
        return JSONResponse(content=data)
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
