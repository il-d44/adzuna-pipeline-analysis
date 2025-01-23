from extraction.api_extraction import create_table, extract_adzuna_data, insert_jobs_to_db

def main():
    # Create the table if it doesn't exist
    create_table()

    data = []

    # Fetch data from 10 pages 
    for i in range(1, 11):
        data.extend(extract_adzuna_data(i))  
    # Insert the extracted data into the database
    if data:
        insert_jobs_to_db(data)
    else:
        print("No data to insert.")

if __name__ == '__main__':
    main()
