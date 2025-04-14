import re
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter
from nltk.tokenize import word_tokenize
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import nltk
from nltk.data import find
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os


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





def process_data_frame(data_frame, column_name='description'):
    """
    Preprocesses text data in a DataFrame column:
    - Converts text to lowercase
    - Removes punctuation & numbers
    - Tokenizes text
    - Removes stopwords

    Args:
        data_frame (pd.DataFrame): The DataFrame containing text data.
        column_name (str): The column to process (default: 'description').

    Returns:
        list: A list of cleaned words.
    """
    # Error Handling - ensure column exists in the dataframe
    if column_name not in data_frame.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")

    text = ' '.join(data_frame[column_name].dropna().astype(str))  # Convert to string & join

    text = text.lower()  # Lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers

    words = word_tokenize(text)  # Tokenize
    stop_words = set(stopwords.words('english'))  # Load stopwords
    words = [word for word in words if word not in stop_words]  # Remove stopwords

    return words


# Function for counting most common words from list of processed words
def top_words_counter(processed_words, number_of_words = 10): 
    word_counts = Counter(processed_words)
    most_common_words = word_counts.most_common(number_of_words)
    return dict(most_common_words)


def multi_count_word_category(processed_words, word_list):
    """
    Counts occurrences of words or multi-word phrases from a predefined category list 
    within a list of processed words.

    Parameters:
    -----------
    processed_words : list of str
        A list of words that have been preprocessed (tokenized, cleaned, and lowercased).
    
    word_list : list of str
        A list of keywords or multi-word phrases to check for in the processed text.

    Returns:
    --------
    dict
        A dictionary where the keys are the original words/phrases from `word_list` 
        (preserving case), and the values are the number of times they appear in `processed_words`.

    Explanation:
    ------------
    1. Converts all words/phrases in `word_list` to lowercase for case-insensitive matching.
    2. Sorts phrases by length (longest first) to ensure multi-word phrases are matched before 
       individual words (avoids partial matching issues).
    3. Joins the processed words into a single string for efficient phrase matching.
    4. Iterates through the sorted list and counts occurrences of each word/phrase in the text.
    5. Maps the counted words/phrases back to their original form from `word_list` (preserving case).
    6. Returns a dictionary with the counts of matched words and phrases.
    """
    # Normalize the word list and create a mapping from lowercase to original word/phrase
    word_mapping = {word.lower(): word for word in word_list}
    
    # Sort words/phrases by length (longest first) to prioritize multi-word phrases
    sorted_words = sorted(word_mapping.keys(), key=len, reverse=True)
    
    # Initialize a Counter for word occurrences
    word_count = Counter()

    # Convert tokenized text into a single string with spaces (for phrase matching)
    text_string = " ".join(processed_words)

    # Match words/phrases in the text
    for word in sorted_words:
        count = text_string.count(word)  # Count occurrences of the word/phrase
        if count > 0:
            word_count[word] += count

    # Map counts back to the original words/phrases (preserving case)
    mapped_word_count = {word_mapping[word]: count for word, count in word_count.items()}
    
    return mapped_word_count


# Function to create word cloud using word count frequencies
# Accepts multi_count_word_category and top_words_counter functions in argument to produce cloud

from wordcloud import WordCloud
from matplotlib.colors import LinearSegmentedColormap
import os

def generate_wordcloud_image(processed_words, word_list=None, count_function=multi_count_word_category):
    colors = ["#339783", "#339733", "#339723"]
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

    font_path = "app/fonts/JetBrainsMono-Bold.ttf"

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found at {font_path}. Please check the path or add the font.")

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='black',
        colormap=custom_cmap,
        prefer_horizontal=1.0,
        font_path=font_path
    )

    wordcloud.generate_from_frequencies(count_function(processed_words, word_list))
    return wordcloud