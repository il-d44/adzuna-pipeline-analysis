
import streamlit as st 

main_section_css = """
<style>
/* Target the main content area */
div[data-testid="stAppViewContainer"] {
    background-image: url('https://i.imgur.com/GybfpVf.png');
    background-size: cover; /* Adjust to cover the entire area */
    background-position: center; /* Center the image */
    background-repeat: no-repeat; /* Prevent tiling */
    background-attachment: fixed; /* Make the background fixed while scrolling */
}

[data-testid="stHeader"] {
background-color: rgba(0, 0, 0, 0);
} 

</style>
"""

# Inject the CSS
st.markdown(main_section_css, unsafe_allow_html=True)







# Path to the font file
font_path="C:/Users/isaac/AppData/Local/Microsoft/Windows/Fonts/JetBrainsMono-Bold.ttf"

# Inject custom CSS
custom_css = f"""
<style>
@font-face {{
    font-family: 'MyCustomFont';
    src: url('{font_path}');
}}
h1 {{
    font-family: 'MyCustomFont', sans-serif;
    font-size: 36px;
    text-align: center;
    color: #4CAF50;
}}
</style>
"""


# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)


st.markdown("""
<h1 style='color: white; background-color: black; padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Deciphering Data Engineer Jobs with Adzuna's API
</h1>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True) 



image_path = "C:/Users/isaac/Documents/Ilyaas/Python/adzuna-analysis_online/streamlit/adzuna_logo.png"  # Replace with the actual path to your image
st.image(image_path)


st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True) 


st.markdown("""
<h1 style='color: white; background-color: rgba(25, 111, 87,0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Adzuna's Search Page
</h1>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True) 

image_path = "streamlit/adzuna_DE_ search.png"  # Replace with the actual path to your image
st.image(image_path)





st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("""
<h1 style='color: white; background-color: rgba(25, 111, 87,0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Whats in a job description?
</h1>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

image_path = "top_10_words_grey.png"  # Replace with the actual path to your image
st.image(image_path)

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True) 


st.markdown("""
<h1 style='color: white; background-color: rgba(25, 111, 87,0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    What does it take to be a data engineer?
</h1>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


# Display a locally saved image
image_path = "non_tech_skills_word_cloud_grey_all.png"  # Replace with the actual path to your image
st.image(image_path, caption="Most frequently mentioned skills")

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("""
<h1 style='color: white; background-color: rgba(25, 111, 87,0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    What technologies do you need?
</h1>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

image_path = "test.png"  # Replace with the actual path to your image
st.image(image_path, caption="Most frequently mentioned technologies")

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True) 


st.markdown("""
<h1 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    How Did We Get Here?
</h1>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Extracting the API Data
</h2>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

st.markdown("""
<p style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
          text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    This function extracts data from the Adzuna API call, cleans it and stores the categories as a list of dictionaries.
</p>
""", unsafe_allow_html=True)

st.code("""
# Sends request to the API using specified search terms and returns extracted data as a dictionary, page_number is used to extract older pages from the API
def extract_adzuna_data(page_number, max_days_old = None):
    # Define the base URL for the Adzuna API
    url = f'https://api.adzuna.com/v1/api/jobs/gb/search/{page_number}'
    # Define the parameters 
    params = {
        'app_id': app_id,  # Your app ID
        'app_key': api_key,  # Your API key
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

    
""", language="python")

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    A look at Adzuna's API
</h2>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

image_path = "streamlit/adzuna_api_menu.png"
st.image(image_path, caption="Adzuna's interactive API console")

st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 15px; 
          text-align: left; border-radius: 10px; font-size: 16px;'>
    Adzuna has an interactive console with fields for their API parameters
    <ul>
        <li>The code requests 50 pages for each call to maximise data</li>
        <li>'Data Engineer' is entered in the 'what' field to return only related jobs</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    A mess... to success
</h2>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


image_path = "streamlit/raw_api_response_body.png"
st.image(image_path, caption="Raw JSON response from API call")

st.markdown("""
<p style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
          text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    Here's the raw response from the API call, which is really a <em>bit</em> messy. Needs some cleaning up before we put it in our database!
</p>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    A little better...
</h2>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


image_path = "streamlit/extract_adzuna_console_ouput.png"
st.image(image_path, width=800, caption="Console output from calling extract_adzuna_data")

st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    Maybe doesn't look that pretty... But we now have a separate dictionary for each job listing, 
    with each category a key with its corresponding value.
</div>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Challenge: Nests can be a pest
</h2>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

image_path = "streamlit/extract_adzuna_nest_output.png"
st.image(image_path, width=800, caption="Console with nested dictionary in output, from earlier extract_adzuna_data version")

st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    Earlier attempts at extracting the data also produced a list of dictionaries. But on closer 
    inspection the 'location' category key had another dictionary as its value, which did not easily 
    insert into the database.
</div>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    .get to the rescue
</h2>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


st.code("""
        # Cleaning up messy fields so they can be inputted into the database
        company_name = job.get('company_name', '').strip()
        location_name = job.get('location', {}).get('display_name', '').strip()  # Location data is nested in dictionary under display name
        description = job.get('description', '').strip()
        redirect_url = job.get('redirect_url', '').strip()
        """, language="python")

st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    By adding .get('display name','') to job.get('location', {}), we are able to 
    retrieve the information we want from 'location' as a single string.
</div>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

st.markdown("""
<h1 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Analysing Job Descriptions
</h1>
""", unsafe_allow_html=True)

# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Warning!!! Data Incompleteness
</h2>
""", unsafe_allow_html=True)

image_path = "streamlit/data_incomplete_extract.png"
st.image(image_path, width=800, caption="Showing incomplete description data field in DBeaver")

st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    At one point it became apparent the job description field was not complete. Realising Adzuna 
    truncates the description when returning its API. Although the incompleteness of the data makes 
    the validity of the analysis somewhat questionable, the overall results are still of interest.
</div>
""", unsafe_allow_html=True)


# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Loading Description Data Back to Python
</h2>
""", unsafe_allow_html=True)


# Add some space between the header and the image
st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break


image_path = "streamlit/loaded_descriptions_data_frame.png"
st.image(image_path, width=800, caption="Loaded description data frame")


st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    First step to description analysis is loading the data into a data frame.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Processing Data
</h2>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.code(""" 
# Preprocess the text
def process_data_frame(data_frame):
    # Combine all data frame rows into single string
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
""", language="python")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Process_data_frame Output
</h2>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

image_path = "streamlit/processed_data_output.png"
st.image(image_path, width=800, caption="Processed description data")

st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    To analyse key words in the job descriptions, the data needs processing:
                
    1. First, every row of data is joined into one string.
    2. The words are all made lowercase to avoid case issues.
    3. RegEx is used to remove non-alphabetic characters.
    4. Words are tokenized - each word is entered as a separate string entry in a list.
    5. Finally, stopwords such as 'I, and, they' are removed as they are not relevant to analysis.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Counting Mentions of Technologies
</h2>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px; font-size: 16px;'>
    **Counting the frequency certain technologies appear in the descriptions is two-parted.**
    
    1. Pre-build a list of the most common technologies.
    2. Use the list to match words in the descriptions and count every match.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h3 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    AI-generated list of top technologies
</h3>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.code(""" 
technologies = [
    "Excel", "Python", "Java", "Scala", "SQL", "R", "Hadoop", "Spark", "Kafka", "Flink", "Hive",
    "AWS", "Azure", "Google Cloud", "Snowflake", "Databricks", "PostgreSQL", "MySQL",
    "MongoDB", "Cassandra", "Redshift", "BigQuery", "Presto", "Athena", "Vertica", "Airflow",
    "NiFi", "DBT", "Informatica", "Talend", "Luigi", "Stitch", "Fivetran", "Git", "Docker",
    "Kubernetes", "Prefect", "Redis", "Elasticsearch", "Terraform", "Apache"
]
""", language="python")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Function to Count Word Frequencies
</h2>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.code(""" 
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
""", language="python")

st.markdown("<br>", unsafe_allow_html=True)


st.markdown("""
<h3 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Function Output
</h3>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


image_path = "streamlit/word_frequency_counter_output.png"
st.image(image_path, width=1200, caption="single_count_word_category output")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: left; display: inline-block; border-radius: 10px; font-size: 16px;'>
    single_count_word_category takes in processed description words and a prebuilt list of category words e.g. 'technologies'. It outputs a dictionary mapping each word from the list to its count by:
            
    1. 'word_category_mapping' creates a dictionary that maps each word in `word_category_list` to its lowercase version.
    2. 'word_category_set' converts the normalized keys (lowercased words) into a set. Sets provide faster lookup times than lists.
    3. A 'Counter' object, 'word_count', is initialized to track how many times each word from `word_category_list` appears in `processed_words`.
    4. The lowercase keys in 'word_count' are mapped back to their original format using `word_category_mapping`.
    5. Returning the result.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h1 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Missing a trick?
</h1>
""", unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Spot the difference!
</h2>
""", unsafe_allow_html=True)

import streamlit as st

# Creating two columns
col1, col2 = st.columns(2)

# Display the first image in the first column
with col1:
    st.image("single_count_tech_skills_word_cloud_grey_all.png", width=350, caption="First attempt at word cloud using single_count method")

# Display the second image in the second column
with col2:
    st.image("tech_skills_word_cloud_grey_all.png", width=350, caption="Second attempt at word cloud using multi_count method")




st.markdown("<br>", unsafe_allow_html=True)



st.markdown("""
<h1 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Dynamic Database
</h1>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Database Changes Over Time
</h2>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

image_path = "streamlit/Group_by_created_query.png"
st.image(image_path, width=1200, caption="Group by query showing changes in database over time")


st.markdown("<br>", unsafe_allow_html=True)


st.markdown("""
<h1 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Concluding Thoughts...
</h1>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    What more analysis can be done?
</h2>
""", unsafe_allow_html=True)#

st.markdown("<br>", unsafe_allow_html=True)


st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    Improvements...
</h2>
""", unsafe_allow_html=True)            

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: white; background-color: rgba(30, 30, 30, 0.5); padding: 10px; 
           text-align: center; display: inline-block; border-radius: 10px;'>
    How could tools be used differently?
</h2>
""", unsafe_allow_html=True)