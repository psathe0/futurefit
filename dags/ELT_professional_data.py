
import pandas as pd
import json
import os
from datetime import datetime

# Function to extract the nested JSON from a local file
def _extract_data_from_local(local_file_path):
    try:
        with open(local_file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {local_file_path} was not found.")
        return None

def _get_file_name(directory, level, is_source=None):
    if is_source:
        # Add datetime to allow incremental load
        date_str = datetime.now().strftime("%Y-%m-%d")
    
        file_name = f"{directory}_{level}_{date_str}.csv"
    else:
        file_name = f"{directory}_{level}.csv"
    file_path = os.path.join(directory, file_name)

    # Check if the directory exists, and if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    return file_path

def _flatten_and_load_nested_data(professional_data, level=None, sep=None):
    # Initialize default separator if sep is None
    if sep is None:
        sep = '.'  # Default separator if no separator is provided
    
    # If level is provided, flatten the data using record_path
    if level:
        flat_df = pd.json_normalize(
            professional_data['professionals'],
            record_path=[level],
            meta_prefix=f'{level}_',
            meta=['professional_id','years_experience','current_industry','current_role','education_level'],
            sep=sep
        )
    else:
        # If level is None, flatten the 'professionals' data directly without record_path
        flat_df = pd.json_normalize(
            professional_data['professionals'],
            meta=['professional_id','years_experience','current_industry','current_role','education_level'],
            sep=sep
        )
        level = 'professional'
    file_name = _get_file_name('stg',level,'yes')
    flat_df.to_csv(file_name, index=False)
    print(f"Flatten data loaded to {file_name}")
    print(flat_df.head())


def _create_dim_tables(table_name, primary_key_columns, columns ):
    stg_file_name = _get_file_name('stg',table_name, 'yes')
    df = pd.read_csv(stg_file_name)

    # Get unique values
    unique_df = df[columns].drop_duplicates()

    # Create a primary key
    unique_df['primary_key'] = unique_df[primary_key_columns].astype(str).agg('_'.join, axis=1)

    # Reset the index for the final DataFrame (optional)
    unique_df.reset_index(drop=True, inplace=True)
    # Load the data in dim directory
    file_name = _get_file_name('dim',table_name)
    unique_df.to_csv(file_name, index=False)
    print("Dim table created")
    print(unique_df.head())

def _create_fact_table(table_name):
    # Step 1: Load file from local folder and load it in DataFrame
    stg_file_name = _get_file_name('stg', table_name, 'yes')
    df = pd.read_csv(stg_file_name)
    
    # Step 3: Fill missing values (NaN) in the 'end_date' column with the current date
    # This ensures that if there is no end date for a record, we set it as today's date.
    df.fillna({'end_date': pd.to_datetime('today')}, inplace=True)
    
    # Step 4: Calculte is_career_growth
    # If the value of salary_band is increasing with each next job then there is a carrer growth
    # for that individual
    df_sorted = df.sort_values(by=['start_date'])
    df_sorted['prev_salary_band'] = df_sorted.groupby('jobs_professional_id')['salary_band'].shift(1)

    df_sorted.fillna({'prev_salary_band': 0}, inplace=True)

    df_sorted['is_career_growth'] = (df_sorted['salary_band'] > df_sorted['prev_salary_band']).astype(int)
    df_sorted.drop('prev_salary_band', axis=1, inplace=False)

    # Step 5: Calculate job duration
    # Convert 'start_date' and 'end_date' to datetime
    df_sorted['start_date'] = pd.to_datetime(df['start_date'])
    df_sorted['end_date'] = pd.to_datetime(df['end_date'])

    # Calculate the difference in months
    df_sorted['job_duration'] = ((df_sorted['end_date'] - df_sorted['start_date']).dt.days) / 30.4375

    # Round the result if necessary, e.g., to nearest integer
    df_sorted['job_duration'] = df_sorted['job_duration'].round()
    
    # Step 9: Load the fact table in fct folder
    file_name = _get_file_name('fct', 'professional_job')
    df_sorted.to_csv(file_name, index=False)
    print("Fact table created")
    print(df_sorted.head())



def transform():

    # create dim tables
    _create_dim_tables('jobs', ['company', 'role'],['company', 'role','industry'] )
    # Same can be repeated to create dim tables for skills, certifications and education

    _create_fact_table('jobs')




def extract_load():
    local_file_path = 'data/full-professionals-json.json'
    professional_data = _extract_data_from_local(local_file_path)
    level = ['jobs','skills', 'certifications', 'education']
    _flatten_and_load_nested_data(professional_data)
    for i in level:
        _flatten_and_load_nested_data(professional_data, level=i , sep='_')
    print("Data extracted and loaded")



if __name__ == "__main__":
    extract_load()
    transform()
