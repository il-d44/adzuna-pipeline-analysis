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


# word_counts = Counter(processed_words)
# most_common_words = word_counts.most_common(10)  # Top 10 keywords
# print("Most Common Words:", most_common_words)

# # Create a word cloud
# wordcloud = WordCloud(
#     width=800, 
#     height=400, 
#     background_color='white', 
#     colormap='viridis'
# ).generate(' '.join(processed_words))

# # Display the word cloud
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.title('Word Cloud of Job Descriptions', fontsize=16)
# plt.show()

# AI generated list of top Data Engineering technologies
technologies = [
    "Excel", "Python", "Java", "Scala", "SQL", "R", "Hadoop", "Spark", "Kafka", "Flink", "Hive",
    "AWS", "Azure", "Google Cloud", "Snowflake", "Databricks", "PostgreSQL", "MySQL",
    "MongoDB", "Cassandra", "Redshift", "BigQuery", "Presto", "Athena", "Vertica", "Airflow",
    "NiFi", "DBT", "Informatica", "Talend", "Luigi", "Stitch", "Fivetran", "Git", "Docker",
    "Kubernetes", "Prefect", "Redis", "Elasticsearch", "Terraform", "Apache"
]

non_technical_skills = [
    "Clear Communication", "Collaboration", "Listening Skills", "Writing", "Presentation", "Negotiation",
    "Feedback", "Critical Thinking", "Troubleshooting", "Root Cause", "Creativity", "Attention to Detail",
    "Quality Focus", "Time Management", "Delegation", "Project Management", "Resource Management", "Risk Management",
    "Agility", "Multitasking", "Change Management", "Business Acumen", "Customer Focus", "Stakeholder Engagement",
    "Prioritization", "Cost-Benefit", "Learning", "Open-mindedness", "Self-motivation", "Resilience", "Flexibility",
    "Growth Mindset", "Teamwork", "Conflict Resolution", "Mentorship", "Empathy", "Cultural Sensitivity", "Tools Proficiency",
    "Leadership", "Decision Making", "Influence", "Visionary Thinking", "Empowerment", "Privacy Awareness", "Integrity",
    "Accountability", "Ethics", "Confidentiality", "Conflict Management", "Negotiation"
]


# !Single Word Finder! Function to count occurrence of description key-words matched to a pre-built list of word categories        
def single_count_word_category(processed_words, word_category_list):
    # Create a mapping of normalized (lowercase) to original word names
    word_category_mapping = {word.lower(): word for word in word_category_list}
    
    # Normalize category names into a set for efficient matching
    word_category_set = set(word_category_mapping.keys())
    
    # Initialize a Counter for technology occurrences
    word_count = Counter()

    # Iterate through processed words
    for word in processed_words:
        if word in word_category_set:
            word_count[word] += 1

    # Map the results back to the original technology names
    mapped_word_count = {word_category_mapping[word]: count for word, count in word_count.items()}
    return mapped_word_count




# !Multi Word Finder! Function counts word occurrence and can recognise multi word terms such as 'Google Cloud'
def multi_count_word_category(processed_words, word_list):

    # Normalize the word list and create a mapping from lowercase to original word/phrase
    word_mapping = {word.lower(): word for word in word_list}
    
    # Sort words/phrases by length to prioritize matching multi-word phrases first
    sorted_words = sorted(word_mapping.keys(), key=len, reverse=True)
    
    # Initialize a Counter for word occurrences
    word_count = Counter()

    # Convert tokenized text into a single string with spaces (for phrase matching)
    text_string = " ".join(processed_words)

    # Match words/phrases in the text
    for word in sorted_words:
        # Count occurrences of the normalized word/phrase in the text
        count = text_string.count(word)
        if count > 0:
            word_count[word] += count

    # Map counts back to the original words/phrases
    mapped_word_count = {word_mapping[word]: count for word, count in word_count.items()}
    
    return mapped_word_count




# # Step 1: Generate the WordCloud
# wordcloud = WordCloud(
#     width=800,  # Width of the canvas
#     height=400,  # Height of the canvas
#     background_color="white",  # Background color of the word cloud
#     colormap="viridis",  # Color map for the words
#     prefer_horizontal=1.0,  # Prefer horizontal orientation of words
# ).generate_from_frequencies(count_technologies(processed_words, technologies))

# # Step 2: Display the WordCloud
# plt.figure(figsize=(10, 5))  # Set the size of the figure
# plt.imshow(wordcloud, interpolation="bilinear")  # Render the word cloud
# plt.axis("off")  # Remove the axes
# plt.title("Technology Word Cloud", fontsize=16)  # Add a title
# plt.show()


    
# # Step 1: Generate the WordCloud
# wordcloud = WordCloud(
#     width=800,  # Width of the canvas
#     height=400,  # Height of the canvas
#     background_color="white",  # Background color of the word cloud
#     colormap="viridis",  # Color map for the words
#     prefer_horizontal=1.0,  # Prefer horizontal orientation of words
# ).generate_from_frequencies(multi_count_word_category(processed_words, technologies))

# # Step 2: Display the WordCloud
# plt.figure(figsize=(10, 5))  # Set the size of the figure
# plt.imshow(wordcloud, interpolation="bilinear")  # Render the word cloud
# plt.axis("off")  # Remove the axes
# plt.title("Technology Word Cloud", fontsize=16)  # Add a title
# plt.show()


# Step 1: Generate the WordCloud
wordcloud = WordCloud(
    width=800,  # Width of the canvas
    height=400,  # Height of the canvas
    background_color="white",  # Background color of the word cloud
    colormap="viridis",  # Color map for the words
    prefer_horizontal=1.0,  # Prefer horizontal orientation of words
).generate_from_frequencies(multi_count_word_category(processed_words, non_technical_skills))

# Step 2: Display the WordCloud
plt.figure(figsize=(10, 5))  # Set the size of the figure
plt.imshow(wordcloud, interpolation="bilinear")  # Render the word cloud
plt.axis("off")  # Remove the axes
plt.title("Technology Word Cloud", fontsize=16)  # Add a title
plt.show()

