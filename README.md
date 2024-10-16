# CDE Airflow Data Pipeline Assingment

This project uses [Apache Airflow](https://airflow.apache.org/) to manage and automate tasks for processing data. The pipeline is set up to:
- Dowload dump file from wikimedia, storing it in a compressed `.gz` format.
- Check if the compressed file was downloaded.
- Extract pageview data from wikimedia, storing it in a text `.txt` format.
- Transform it into a structured format by filtering selected companies `["Amazon", "Apple", "Facebook", "Google", "Microsoft"]` and their page views to a.`.sql` file.
- And, Load it into a SQLite database for analysis.

## Project Structure
Main folder:
```plaintext
├── dags/
│   └── wiki/
│       ├── funk.py    # Python functions for the DAG
└──        ├── wiki.py     #DAG file
             
```

# Dependencies
- Python 3.8+ (Virtual Enviroment).
- Apache Airflow 2.x
- SQLite.
- Linux terminal or WSL on Windows.
