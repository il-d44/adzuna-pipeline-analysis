import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import requests
from dotenv import load_dotenv
import os



# Load environment variables from .env file
load_dotenv()

# Database connection parameters from .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}
DB_NAME = os.getenv("DB_NAME")  # Retrieve the database name

# Adzuna API keys from .env
app_id = os.getenv("ADZUNA_APP_ID")
api_key = os.getenv("ADZUNA_API_KEY")


TABLE_NAME = 'student.data_engineer_jobs'


# Sends request to the API using specified search terms and returns extracted data as a dictionary, page_number is used to extract older pages from the API
def extract_adzuna_data(page_number, max_days_old = None):
    # Define the base URL for the Adzuna API
    url = f'https://api.adzuna.com/v1/api/jobs/gb/search/{page_number}'
    # Define the parameters 
    params = {
        'app_id': app_id,  
        'app_key': api_key,  
        'results_per_page': '50',  # Number of results to be displayed
        'what': 'Data Engineer',  # Search term
    }
    if max_days_old:
            params['max_days_old'] = max_days_old
    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response

        # Extract and structure the data
        extracted_data = []
        for job in data.get('results', []):  # 'results' is where the job listings are stored
            
            # Cleaning up messy fields so they can be inputted into database
            company_name = job.get('company_name', '').strip()  
            location_name = job.get('location', {}).get('display_name', '').strip() # Location data is nested in dictionary under display name
            description = job.get('description', '').strip()  
            redirect_url = job.get('redirect_url', '').strip()  

            # Ensure the job details are correctly formatted
            job_details = {
                'id': job.get('id'),
                'title': job.get('title'),
                'description': description,
                'company': company_name,
                'location': location_name,
                'salary_min': job.get('salary_min', None),
                'salary_max': job.get('salary_max', None),
                'redirect_url': redirect_url,
            }
            extracted_data.append(job_details)

        return extracted_data  # List of dictionaries containing job details
    else:
        # Handle errors
        print(f"Request failed with status code {response.status_code}")
        return None

    

# Connects to pagila database using credentials and creates table
def create_table():
    """Create the jobs table if it does not exist."""
    try:
        conn = psycopg2.connect(dbname= DB_NAME, **DB_CONFIG)
        cursor = conn.cursor()
        
        # SQL to create the table
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id BIGINT PRIMARY KEY,
            title TEXT,
            description TEXT,
            company TEXT,
            location TEXT,
            salary_min NUMERIC,
            salary_max NUMERIC,
            redirect_url TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Table '{TABLE_NAME}' created (or already exists).")
    
    except Exception as e:
        print("An error occurred while creating the table:", e)
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_jobs_to_db(data):
    """Insert job data into the jobs table."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, **DB_CONFIG)
        cursor = conn.cursor()
        
        # SQL query to insert job data
        insert_query = f"""
        INSERT INTO {TABLE_NAME} (id, title, description, company, location, 
                                salary_min, salary_max, redirect_url, created)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW()) 
        ON CONFLICT (id) DO NOTHING;
        """
        
        # Insert each job into the database
        for job in data:
            cursor.execute(insert_query, (
                job["id"],
                job["title"],
                job["description"],
                job["company"],
                job["location"],  
                job.get("salary_min", None),
                job.get("salary_max", None),
                job["redirect_url"]  
            ))
        
        conn.commit()
        print("Job data inserted successfully.")
    
    except Exception as e:
        print("An error occurred while inserting data:", e)
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


print(extract_adzuna_data(1))
