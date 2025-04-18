import sys
import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import psycopg2
from opencage.geocoder import OpenCageGeocode
import time

# Import dictionary of cities from another file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from analysis.resources.city_mapping import city_map
from analysis.resources.config import DB_CONFIG

# Retrieved variables from .env file
RETRIEVED_DB_NAME = os.getenv("DB_NAME")  # Retrieve the database name
RETRIEVED_API_KEY = os.getenv("GEOCODING_API_KEY")


# Defined sql query paths
GET_ID_LOCATION_QUERY_PATH = 'analysis/sql_queries/get_id_location.sql'
GET_CLEANED_LOCATION_QUERY_PATH= 'analysis/sql_queries/get_cleaned_location_query.sql'

def get_db_url():
    """
    Load database credentials from environment variables and return the database URL.
    """
    load_dotenv()  # Load environment variables

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    if not all([user, password, host, port, database]):
        raise ValueError("Error: One or more database environment variables are missing.")

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def load_query(db_url, query_path):
    """
    Load table from the database using a SQL query.
    """
    # Load SQL query from file
    try:
        with open(query_path, "r") as file:
            query = file.read().strip()

    # Handle file path error        
    except FileNotFoundError:
        raise FileNotFoundError("Error: SQL file not found. Please check the file path.")
    
    # Handle empty SQL file error
    if not query:
        raise ValueError("Error: The SQL query is empty. Please check the file contents.")

    # Establish database connection using SQLAlchemy
    engine = create_engine(db_url)

    # Execute the query and return results
    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            return df
    except Exception as e:
        raise Exception(f"An error occurred while executing the query: {e}")


# Function to map city names
def map_city(location):
    for city in city_map:
        if city in location:
            return city_map[city]  # Return mapped city 
    return None  # Return null 

def clean_location_data(df):
    # Remove rows where 'location' is 'UK' too generic to be useful
    df = df[df['location'].str.strip() != 'UK'].copy()
    # Convert 'location' to lowercase
    df.loc[:, 'location'] = df['location'].str.lower()
    # Apply the map_city function to 'location'
    df['cleaned_location'] = df['location'].apply(map_city)

    return df

def update_cleaned_location(cleaned_location_df):

    try: 
        conn = psycopg2.connect(dbname = RETRIEVED_DB_NAME, **DB_CONFIG)
        cursor = conn.cursor()
        
        # Raw SQL for updating cleaned_location given id
        update_query = f"""
        UPDATE student.data_engineer_jobs
        SET cleaned_location = %s
        WHERE id = %s;
        """

        for _, row in cleaned_location_df.iterrows():
            cursor.execute(update_query, (row['cleaned_location'], row['id']))

        conn.commit()
        print('cleaned_location updated.')

    except Exception as e:
        print("An error occurred while updating data:", e)
    
    finally:
        if cursor:
            cursor.close()
        if conn: 
            conn.close()

def run_clean_location_pipeline():
    location_df = load_query(get_db_url(), GET_ID_LOCATION_QUERY_PATH)
    cleaned_location_df = clean_location_data(location_df)
    update_cleaned_location(cleaned_location_df)


cleaned_location_df = load_query(get_db_url(), GET_CLEANED_LOCATION_QUERY_PATH)


def add_geocoordinates_opencage(cleaned_location_df, api_key):
    """
    Adds latitude and longitude columns to a dataframe using OpenCage geocoding API.

    Parameters:
        cleaned_location_df (pd.DataFrame): DataFrame with a 'cleaned_location' column.
        api_key (str): OpenCage API key.

    Returns:
        pd.DataFrame: The same DataFrame with 'latitude' and 'longitude' columns added.
    """
    geocoder = OpenCageGeocode(api_key)
    geocoded_df = cleaned_location_df.copy()
    geocoded_df["latitude"] = None
    geocoded_df["longitude"] = None

    for index, row in geocoded_df.iterrows():
        location = row["cleaned_location"]
        # Added print statement in loop for reassurance, api calling takes time
        print(f"Geocoding {index + 1}/{len(geocoded_df)}: '{location}'...")

        start_time = time.time()

        try:
            result = geocoder.geocode(location)
            if result and len(result):
                # Find country code returned by api check if in UK
                components = result[0].get("components", {})
                country_code = components.get("country_code", "")

                # Only accept UK-based results
                if country_code == "gb":  
                    lat = result[0]["geometry"]["lat"]
                    lng = result[0]["geometry"]["lng"]
                    geocoded_df.at[index, "latitude"] = lat
                    geocoded_df.at[index, "longitude"] = lng
                    print(f" UK location | Lat: {lat}, Lon: {lng}")
                else:
                    print(f" Location not in UK (country_code: {country_code})")
            else:
                print(f" No result found.")
        except Exception as e:
            print(f" Error geocoding '{location}': {e}")

        # measures time taken to call api and process
        elapsed_time = time.time() - start_time
        print(f" Time taken: {elapsed_time:.2f} seconds\n")

        time.sleep(0.5)  # Respect OpenCage's rate limit

    return geocoded_df

def update_coordinates(geocoded_df):

    try: 
        conn = psycopg2.connect(dbname = RETRIEVED_DB_NAME, **DB_CONFIG)
        cursor = conn.cursor()
        
        # Raw SQL for updating cleaned_location given id
        update_query = f"""
        UPDATE student.data_engineer_jobs 
        SET lat = %s, lon = %s
        WHERE id = %s;
        """

        for _, row in geocoded_df.iterrows():
            if row['latitude'] is not None and row['longitude'] is not None:
                cursor.execute(update_query, (row['latitude'], row['longitude'], row['id']))


        conn.commit()
        print('latitude and longitude updated.')

    except Exception as e:
        print("An error occurred while updating data:", e)
    
    finally:
        if cursor:
            cursor.close()
        if conn: 
            conn.close()


def run_coordinates_pipeline():
    cleaned_location_df = load_query(get_db_url(), GET_CLEANED_LOCATION_QUERY_PATH)
    geocoded_df = add_geocoordinates_opencage(cleaned_location_df, RETRIEVED_API_KEY)
    update_coordinates(geocoded_df)

run_coordinates_pipeline()
