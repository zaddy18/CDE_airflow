# CDE Airflow Data Pipeline Assingment

This project uses [Apache Airflow](https://airflow.apache.org/) to manage and automate tasks for processing data. The pipeline is set up to:
- Dowload dump file from wikimedia, storing it in a compressed `.gz` format.
- Extract pageview data from wikimedia, storing it in a text `.txt` format.
- Check if the extracted file was downloaded.
- Transform it into a structured format by filtering selected companies `"Amazon", "Apple", "Facebook", "Google", "Microsoft"` and their page views to a.`.sql` file.
- Load it into a SQLite database.
- And, analyze data from SQLite database.

  ![image](https://github.com/user-attachments/assets/0c29c98e-cfd2-4bc4-ae33-66ff8be644b1)


## Project files
- [funk.py](https://github.com/zaddy18/CDE_airflow/blob/main/airbox/dags/wiki/funk.py) (Python functions for the DAG).
- [wiki.py](https://github.com/zaddy18/CDE_airflow/blob/main/airbox/dags/wiki/wiki.py) (DAG file).
- [Insert.sql](https://github.com/zaddy18/CDE_airflow/blob/main/airbox/dags/wiki/Insert.sql) (Sql commands for inserting data into the DB).


# Dependencies
- Python 3.8+ (Virtual Enviroment).
- Apache Airflow 2.x
- SQLite.
- Linux terminal or WSL on Windows.
