 ## Outline
 This project contains a python script for extracting data on Data Engineer jobs from Adzuna's (website that lists jobs) Api. The data is then added to a Postgres database for analysis.

 ## Extraction Script Instructions
- Please create `.venv` file
- Please install the packages from `requirements.txt`
- Please insert supplied `.env` file into root of project
- Please execute `run_extraction` **once** to populate the database

## Chron Details
- Please execute `run_update` every 4 hours to update database

## Project Plan 
### Goals
1. Successfully extract and regularly update a database with new job listings via Adzuna API.
2. Once the database is populated, ensure data is clean and transformed.
3. Analyse the job description field and aggregate data on most desired technologies.
4. Analyse the impact of location on salary
5. Create streamlit app to display findings

### Methods
1. **Successfully extract and regularly update a database with new job listings via Adzuna API.**
- Create function to request from API and store data in dictionary
- Wite function to connect to pagila database and create table
- Write function to insert data from the dictionary into created table.

  
2. **Once the database is populated, ensure data is clean and transformed.**
- Remove duplicates, handle missing values, and standardise formats.
- Validate the cleaned data to ensure consistency and accuracy.
**
3. **Analyse the job description field and aggregate data on most desired technologies.**
- Extract key technology-related terms from job descriptions using natural language processing (NLP).
- Group and count the occurrence of technologies to identify trends.
- Visualize the results to highlight the most in-demand technologies.

4. **Analyse the impact of location on salary**
- Conduct statistical analysis to identify correlation patterns between location and salary.
- Present findings with visualizations to compare salary ranges across locations.

5. **Create streamlit app to display findings**
- Create markdown to tell story of the project
- Display visualisations on the page
- Create markdown to tell story of analysis





