from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
import re
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
from nltk.data import find
import ast

# Helper function to check if NLTK is already downloaded to prevent redownload
def ensure_resource(resource_name):
    try:
        find(f'tokenizers/{resource_name}')  # Check if resource exists
    except LookupError:
        nltk.download(resource_name)  # Download only if missing

# Ensure 'punkt', 'punkt_tab' and 'stopwords' and are downloaded
ensure_resource('punkt')
ensure_resource('stopwords')
ensure_resource('punkt_tab')




# Load environment variables from .env file
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"



def load_descriptions(db_url):
    """
    Load descriptions from the database using a SQL query.
    """
    # Load SQL query from file
    try:
        with open('analysis/get_description_query.sql', "r") as file:
            description_query = file.read().strip()

    # Handle file path error        
    except FileNotFoundError:
        raise FileNotFoundError("Error: SQL file not found. Please check the file path.")
    
    # Handle empty sql file error
    if not description_query:
        raise ValueError("Error: The SQL query is empty. Please check the file contents.")

    # Establish database connection using SQLAlchemy
    engine = create_engine(db_url)

    # Execute the query and return results
    try:
        with engine.connect() as conn:
            description_df = pd.read_sql(description_query, conn)
            return description_df
    except Exception as e:
        raise Exception(f"An error occurred while executing the query: {e}")
    



# Preprocess the text
def process_data_frame(data_frame):
    # Comine all data frame rows into single string
    text = ' '.join(data_frame['description'])
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # Tokenize
    words = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return words

file_path = "analysis/offline_description_data.txt"

def load_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the file content and convert it to a Python list
            content = file.read()
            # Convert the string representation of the list into an actual list
            data_list = ast.literal_eval(content)  
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        data_list = []
    
    return data_list






data_frame = load_descriptions(db_url)
processed_words = process_data_frame(data_frame)


word_counts = Counter(processed_words)
most_common_words = word_counts.most_common(10)  # Top 10 keywords
print("Most Common Words:", most_common_words)



        
        

    
