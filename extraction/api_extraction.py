import psycopg2
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

# Defining name for database table where job listings will be stored
TABLE_NAME = 'student.data_engineer_jobs'


def fetch_adzuna_jobs(page_number, max_days_old=None):
    """
    Makes API request to Adzuna with chosen parameters and returns response, handling errors that may occur

    Parameters:
    -----------
    page_number : int
        Integer number specifying the Azduna listing page to return
    
    max_days_old=None : int
        Optional parameter to return the most recent jobs by age in days

    Returns:
    --------
    list
        A list of dictionaries with each item representing a job listing

    """
    
    url = f'https://api.adzuna.com/v1/api/jobs/gb/search/{page_number}'
    params = {
        'app_id': app_id,
        'app_key': api_key,
        'results_per_page': '50',
        'what': 'Data Engineer',
    }
    if max_days_old:
        params['max_days_old'] = max_days_old

        # Try block to error handle API request
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for non-200 response

        # If status code is 200, return the results
        return response.json().get('results', [])
    
    except requests.exceptions.RequestException as e:
        # Exception class from results library to catch network-related errors 
        print(f"Network error: {e}")
    
    except ValueError:
        # Catches errors with incorrect response, e.g. HTML instead of JSON
        print("Error: Unable to parse response from API.")
    
    except Exception as e:
        # Catches any other unexpected errors
        print(f"An unexpected error occurred: {e}")

    return None  # Return None in case of failure

def clean_job_data(job):
    """
    Cleaning function, takes a single job dictionary and extracts relevant fields to create clean dictionary

    Parameters:
    -----------
    job : dict
        A dictionary containing job listing data.

    Returns:
    --------
    dict
        A cleaned dictionary with keys: 'id', 'title', 'description', 'company', 
        'location', 'salary_min', 'salary_max', 'redirect_url'.
    """
    return {
        'id': job.get('id'),
        'title': job.get('title'),
        'description': job.get('description', '').strip(),
        'company': job.get('company_name', '').strip(),
        'location': job.get('location', {}).get('display_name', '').strip(), # Location data is nested in dictionary under display name
        'salary_min': job.get('salary_min'),
        'salary_max': job.get('salary_max'),
        'redirect_url': job.get('redirect_url', '').strip(),
    }

def extract_adzuna_data(page_number, max_days_old=None):
    """
    Returns cleaned list of dictionaries for each job listing.

    Parameters:
    -----------
    page_number : int
        Integer number specifying the Azduna listing page to return
    
    max_days_old=None : int
        Optional parameter to return the most recent jobs by age in days

    Returns:
    --------
    list
        A list of dictionaries with each item a clean dictionary for each job listing. 
        Within the clean dictionary, each key represents a data field: 'id', 'location,' description' etc...

    """
    job_results = fetch_adzuna_jobs(page_number, max_days_old)
    return [clean_job_data(job) for job in job_results] if job_results else []


    

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

def insert_jobs_to_db(clean_data):
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
        for job in clean_data:
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
