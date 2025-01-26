from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
import re
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
from nltk.data import find
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import numpy as np

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


# Function for counting most common words from list of processed words
def top_words_counter(processed_words, number_of_words = 10): 
    word_counts = Counter(processed_words)
    most_common_words = word_counts.most_common(number_of_words)
    return dict(most_common_words)


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


# Function to create word cloud using word count frequencies
# Accepts multi_count_word_category, single_count_word_category and top_words_counter functions in argument to produce cloud

def word_cloud_creator(image_path, processed_words, word_list = None, count_function = multi_count_word_category):
    # Check if the image file already exists
    if not os.path.exists(image_path):

        # Custom colors for the colormap
        colors = ["#339783","#339733","#339723"]  # Replace with your preferred colors
        custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

        # Create WordCloud object
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color=None,  # Transparent background for word cloud
            mode="RGBA",  # Supports transparency
            colormap=custom_cmap,  # Use your custom colormap
            prefer_horizontal=1.0,
            font_path="C:/Users/isaac/AppData/Local/Microsoft/Windows/Fonts/JetBrainsMono-Bold.ttf"
        )

        # Generate WordCloud from word frequencies
        wordcloud.generate_from_frequencies(count_function(processed_words, word_list))

        # Convert word cloud to RGBA image (this will be a transparent word cloud image)
        wordcloud_image = Image.fromarray(wordcloud.to_array())

        # Create an RGBA background (semi-transparent)
        background = Image.new("RGBA", (800, 400), (30, 30, 30, 200))  # Dark gray with alpha transparency

        # Ensure that the background is the correct size and mode
        wordcloud_image = wordcloud_image.convert("RGBA")
        
        # Composite the word cloud image over the RGBA background
        combined_image = Image.alpha_composite(background, wordcloud_image)

        # Save the final image
        combined_image.save(image_path)

        print(f"Word cloud saved at {image_path}")



##################################################################################################


# Execute function to load descriptions from database into dataframe
data_frame = load_descriptions(db_url)
# Execute function to process descriptions
processed_words = process_data_frame(data_frame)

word_cloud_creator("test2.png", processed_words, count_function= top_words_counter)

# print(top_words_counter(processed_words))
