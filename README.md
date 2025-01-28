 ## Outline

This project focuses on extracting, transforming, and analysing job listing data using the Adzuna API. The ETL pipeline is designed to extract raw data on job postings, structure it into a clean, organised format, and load it into a remote PostgreSQL database for efficient storage and querying. To ensure the data remains up to date, the pipeline is automated to update the database every 4 hours with new job listing data.

To gain insights from the job descriptions, I applied Natural Language Processing (NLP) techniques, identifying key patterns, popular skills, and technologies in job requirements. The findings are presented through a custom-built Streamlit application, which visually narrates the analysis and the end-to-end ETL process.

 ## Extraction Script Instructions
- Please create `.venv` file
- Please install the packages from `requirements.txt`
- Please insert supplied `.env` file into root of project
- Please execute `run_extraction` **once** to populate the database

## Chron Details
- Please execute `run_update` every 4 hours to update database

## Goals
1. **As a data engineer,** I want to extract and regularly update a database with new job listings via the Adzuna API so that I can maintain an up-to-date dataset for analysis.
2. **As a data engineer,** I want to clean and transform the data to ensure it is accurate, consistent, and ready for meaningful insights.
3. **As a data analyst,** I want to analyze job descriptions to identify the most in-demand technologies so that I can understand trends in the job market.
4. **As a data analyst,** I want to examine the relationship between location and salary so that I can uncover how location impacts earnings.
5. **As a presenter,** I want to create a Streamlit app to showcase the project findings in an engaging and user-friendly way so that stakeholders can easily explore the insights.


## Methods 

1. ### Extract and Update Database:

- **As a data engineer,** I want to create a function to request job data from the Adzuna API and store it in a dictionary so that I can retrieve structured data.
- **As a data engineer,** I want to connect to the Pagila database and set up the necessary tables to store job listings so that the data is properly organized.
- **As a data engineer,** I want to write a function to insert job data from the dictionary into the database so that the database is consistently updated.


2. ### Clean and Transform Data:

- **As a data engineer,** I want to remove duplicates, handle missing values, and standardize formats so that the data is clean and ready for analysis.
- **As a data engineer,** I want to validate the cleaned data to ensure it is accurate and consistent so that analysis results are trustworthy.

3. ### Analyse Job Descriptions:

- **As a data analyst,** I want to extract key technology-related terms from job descriptions using NLP so that I can identify relevant trends.
- **As a data analyst,** I want to group and count the occurrences of technologies to uncover which ones are most in demand.
- **As data analyst,** I want to visualize the results to clearly communicate the top technologies in the job market.

4. ### Impact of Location on Salary:

- **As a data analyst,** I want to perform statistical analysis to identify patterns between location and salary so that I can understand geographic differences in earnings.
- **As a data analyst,** I want to present the findings with clear visualizations to compare salary ranges across different locations.


5. ### Streamlit Presentation:

- **As a data analyst**, I want to write markdown content that tells the story of the project so that users understand its context and purpose.
- **As a data analyst,** I want to display the visualisations clearly.
- **As a data analyst**, I want to create clear explanations of the findings in markdown so that users can easily follow the analysis journey.





