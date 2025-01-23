
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

# Add a header to test the font
st.markdown("<h1>My Customized Title</h1>", unsafe_allow_html=True)

## Main title data engineer job descriptions from ADZUNA

st.title("Whats in a job description?")

image_path = "top_10_words_grey.png"  # Replace with the actual path to your image
st.image(image_path)

st.title("What does it take to be a data engineer?")

st.header("What skills do you need?")

# Display a locally saved image
image_path = "non_tech_skills_word_cloud_grey_all.png"  # Replace with the actual path to your image
st.image(image_path, caption="Most frequently mentioned skills")


st.header("What technologies do you need?")
image_path = "tech_skills_word_cloud_grey_all.png"  # Replace with the actual path to your image
st.image(image_path, caption="Most frequently mentioned technologies")

st.title("How Did We Get Here?")

st.header("Extracting the API Data")

st.markdown("This function extracts data from the Adzuna API call, cleans it and stores the categories as a list of dictionaries")

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


st.header("A look at Adzuna's API")

image_path = "streamlit/adzuna_api_menu.png"
st.image(image_path, caption="Adzuna's interactive API console")

st.markdown('''Adzuna has an interactive console with fields for their API parameters
            - The code requests 50 pages for each call to maximise data
            - 'Data Engineer' is entered in the 'what' field to return only related jobs
            ''')

st.header("A mess... to success")

image_path = "streamlit/raw_api_response_body.png"
st.image(image_path, caption="Raw JSON response from API call")

st.markdown("This the raw response from the API call, which is really a *bit* messy. Needs some cleaning up before we put it in our database!")

st.header("A little better")
image_path = "streamlit/extract_adzuna_console_ouput.png"
st.image(image_path, width=800, caption="Console output from calling extract_adzuna_data")

st.markdown("Maybe doesn't look that pretty... But we now have a separate dictionary for each job listing, with each category a key with its corresponding value.")

st.header("Challenge: Nests can be a pest")

image_path = "streamlit/extract_adzuna_nest_output.png"
st.image(image_path, width=800, caption="Console with nested dictionary in output, from earlier extract_adzuna_data version")

st.markdown("Earlier attempts at extracting the data also produced a list of dictionaries. But on closer inspection the 'location' category key had another dictionary as its value, which did not easily insert into the database.")

st.header(".get to the rescue")

st.code("""
        # Cleaning up messy fields so they can be inputted into the database
        company_name = job.get('company_name', '').strip()
        location_name = job.get('location', {}).get('display_name', '').strip()  # Location data is nested in dictionary under display name
        description = job.get('description', '').strip()
        redirect_url = job.get('redirect_url', '').strip()
        """, language="python")

st.markdown("By adding ```.get('display name','')``` to ```job.get('location', {})``` we are able to retrieve the information we want from 'location' as a single string.")


st.title("Analysing the description")