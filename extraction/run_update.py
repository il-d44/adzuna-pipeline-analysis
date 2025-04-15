from extraction.api_extraction import extract_adzuna_data, insert_jobs_to_db

# Program checks for new listing every hour from first page and inserts them to database if new
def main():
    data = extract_adzuna_data(1, max_days_old=1)

    # Insert the extracted data into the database
    if data:
        insert_jobs_to_db(data)
    else:
        print("No data to insert.")

if __name__ == '__main__':
    main()
