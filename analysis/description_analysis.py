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

# Helper function to check if NLTK resource is already downloaded in either 'tokenizers' or 'corpora'
def ensure_resource(resource_name):
    try:
        # Check in both 'tokenizers' and 'corpora' directories
        find(f'tokenizers/{resource_name}')
    except LookupError:
        try:
            find(f'corpora/{resource_name}')
        except LookupError:
            # If not found in either, download the resource
            nltk.download(resource_name)

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
    
print(load_descriptions(db_url))


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


# Execute function to load descriptions from database into dataframe
data_frame = load_descriptions(db_url)
# Execute function to process descriptions
processed_words = process_data_frame(data_frame)

# Count top 10 words from description
word_counts = Counter(processed_words)
most_common_words = word_counts.most_common(10)  # Top 10 keywords
print("Most Common Words:", most_common_words)

# Create a word cloud
wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color='grey', 
    colormap='viridis',
    prefer_horizontal=1.0,
    font_path="C:/Users/isaac/AppData/Local/Microsoft/Windows/Fonts/JetBrainsMono-Bold.ttf"
).generate(' '.join(processed_words))
wordcloud.to_file("top_10_words_grey.png")

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







#  Define the file path for the saved WordCloud image
wordcloud_image_path = "non_tech_skills_word_cloud_grey_all.png"


# Function to create word cloud using word count frequencies from single_count_word_category
def single_word_cloud_creator(wordcloud_image_path, processed_words, word_list):
    # Check if the image file already exists
    if not os.path.exists(wordcloud_image_path):

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color=(169, 169, 169),  # Set background color in RGB
            colormap="inferno",
            prefer_horizontal=1.0,
            font_path="C:/Users/isaac/AppData/Local/Microsoft/Windows/Fonts/JetBrainsMono-Bold.ttf"
        )

        # Generate WordCloud from your data using single_count_word_category function
        wordcloud.generate_from_frequencies(single_count_word_category(processed_words, word_list))

        # Save the generated WordCloud image
        wordcloud.to_file(wordcloud_image_path)


# Function to create word cloud using word count frequencies from multi_count_word_category
def multi_word_cloud_creator(wordcloud_image_path, processed_words, word_list):
    # Check if the image file already exists
    if not os.path.exists(wordcloud_image_path):

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color=(169, 169, 169),  # Set background color in RGB
            colormap="inferno",
            prefer_horizontal=1.0,
            font_path="C:/Users/isaac/AppData/Local/Microsoft/Windows/Fonts/JetBrainsMono-Bold.ttf"
        )

        # Generate WordCloud from your data using multi_count_word_category function
        wordcloud.generate_from_frequencies(multi_count_word_category(processed_words, word_list))

        # Save the generated WordCloud image
        wordcloud.to_file(wordcloud_image_path)

single_word_cloud_creator("single_count_tech_skills_word_cloud_grey_all.png", processed_words, technologies)

df = load_descriptions(db_url)
print(df)