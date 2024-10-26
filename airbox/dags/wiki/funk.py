import requests
import gzip
from sqlalchemy import create_engine
import os
from sqlalchemy import create_engine,text


#function to download compressed file
def download_pageviews(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)


#function to check if file was truly downloaded
def check_file_exists(file_path):
    if os.path.exists(file_path):
        print(f"{file_path} exists.")
    else:
        raise FileNotFoundError(f"{file_path} does not exist.")

#function to filter selected companies and their page views
def filter_company_pageviews(input_path, output_sql_path):
    selected_companies = ["Amazon", "Apple", "Facebook", "Google", "Microsoft"]
    insert_statements = []
    
    print(f"Input path: {input_path}")
    with open(input_path, 'r') as file:
        for line in file:
            columns = line.split()
            domain_code = columns[0]
            page_title = columns[1]
            view_count = columns[2]
            # Check if any of the selected companies are in the page title
            if any(company.title() == page_title.title() for company in selected_companies):
                insert_statements.append(
                    f"INSERT INTO pageviews (company, view_count) VALUES ('{page_title.title()}', {view_count});"
                )
    
    # Writing the insert statements to the SQL file
    with open(output_sql_path, 'w') as sql_file:
        sql_file.write("\n".join(insert_statements))


#function to create table and insert data in sqlite
def load_data(sql_path):
    db_url = 'sqlite:///airflow.db'  # sqlite database URL due to testing
    engine = create_engine(db_url)
    
    drop_table = """
    DROP TABLE IF EXISTS pageviews;
    """
    create_table = """
    CREATE TABLE IF NOT EXISTS pageviews (
        company TEXT,
        view_count INTEGER
    );
    """

    with engine.begin() as conn:  
        # Running first two SQL commands before insert
        conn.execute(text(drop_table))
        conn.execute(text(create_table))
    
    # Opening the SQL file to split by individual queries because SQLite does not allow executing multiple SQL statements in a single call when using execute
    with open(sql_path, 'r') as f:
        sql_commands = f.read().split(';')
        
    with engine.begin() as conn:  # starting a transaction
        for command in sql_commands:
            if command.strip():  # Running this non-null commands to increase execution rate
                conn.execute(text(command.strip()))


#query to get top company by sum of pageviews
def get_top_company():
    db_url = 'sqlite:///airflow.db'  
    engine = create_engine(db_url)
    
    query = text("""
    SELECT company, SUM(view_count) as total_views
    FROM pageviews
    GROUP BY company
    ORDER BY total_views DESC
    LIMIT 1;
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            print(row)
