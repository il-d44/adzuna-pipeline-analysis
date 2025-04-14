from extraction.api_extraction import create_table, extract_adzuna_data, insert_jobs_to_db


def main():
    """
    Main function to execute the full pipeline of fetching, processing, and inserting job data into the database.
    
    Steps:
    1. Creates a database table if it doesn't already exist.
    2. Fetches job data from the Adzuna API across multiple pages.
    3. Inserts the fetched data into database if data is available; otherwise, prints a message indicating no data.
    """

    # Create the table in the database if it doesn't exist  
    create_table()

    # Initialize an empty list to hold the job data
    data = []

    # Fetch data from first 10 pages
    for i in range(1, 11):
        # Fetch data for the current page and extend the list with new job data for each iteration
        data.extend(extract_adzuna_data(i))  

    # If there is any data fetched, insert it into the database
    if data:
        insert_jobs_to_db(data)
    else:
        # If no data is fetched, print a message
        print("No data to insert.")

# This block ensures the main function is only executed when this script is run directly, not when imported.
if __name__ == '__main__':
    main()
