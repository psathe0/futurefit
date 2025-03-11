@ -0,0 +1,121 @@
# futurefit case study
# Part 1

## Overview

This project demonstrates an **ELT (Extract, Load, Transform)** process designed to transform nested JSON data into a structured data model. The data is then used to calculate industry metrics and track career growth for professionals.

The key steps include:
1. **Extracting** the data from nested JSON.
2. **Loading** the data into pandas DataFrames for transformation.
3. **Transforming** the data into a structured format suitable for analysis.
4. **Data Validation** to ensure data quality and consistency.
5. **Creating Fact and Dimension Tables** for use in business intelligence and analytics.
6. **Calculating Industry Metrics** such as job duration, salary bands, and career growth.

## Tools and Technologies

- **pandas**: Used for data manipulation and transformation.
- **JSON**: The source data is in a nested JSON format.
- **Python**: The programming language used to implement the data transformations.
- **Airflow (Optional)**: Could be used for orchestration (not implemented in this case due to tool limitations).
- **Snowflake (Optional)**: Used as the data warehouse for storing the processed data (not implemented in this case).
- **dbt (Optional)**: Could be used for transformation logic and model building in SQL (not implemented in this case).

## Data Model

### Fact Tables
- **fact_professional_job**: This table contains information about the professionals' jobs, including:
  - **job_duration**: Duration of time spent in each job (in months).
  - **is_career_growth**: Flag indicating whether there was a salary increase between jobs for a professional (1 if increased, 0 if not).

### Dimension Tables
- **dim_jobs**: Contains job-related information.
- **dim_professionals**: Contains professional-specific data (e.g., name, skills, education).
- **dim_skills**: Contains data on the skills of professionals.
- **dim_education**: Contains educational background data for professionals.
- **dim_certifications**: Contains certification information for professionals.

### Aggregated Metrics
- **agg_industry_role_metrics**: Contains aggregated metrics for each industry, such as:
  - **avg_job_duration**: Average duration of time spent in each job (in months).
  - **avg_salary_band**: Average salary band for the role and industry
  - **successful_growth_pct**: Percentage of professionals who experienced career growth (i.e., `is_career_growth = 1`) in a role and industry.

## Calculations
- **Job Duration**: The number of months spent in each job is calculated by comparing `start_date` and `end_date`.
- **Career Growth**: A flag indicating whether there has been a salary increase between jobs (`is_career_growth = 1` if there is an increase).
- **Industry Metrics**: We calculate industry-specific metrics such as average job duration, average job experience, average salary band, and career growth percentage.

## Data Validation
We apply the following checks to ensure data quality:
- **Date Validation**: Ensure that `start_date` is not later than `end_date`.
- **Null Checks**: Ensure `end_date` is not null and handle missing values where applicable.
- **Consistency Checks**: Exclude records where a professional has switched industries (i.e., ensure all job records for a professional are within the same industry).

## Data Pipeline Assumptions

- The data source is assumed to be a nested JSON format, which we flatten using pandas.
- For simplicity, we are focusing on two main data categories: **Jobs** and **Professionals**.
- Other attributes like skills, education, and certifications will be handled similarly in separate dimension tables.
- We are assuming no major industry switches for professionals in this case study, and that all records pertain to professionals within a specific industry.

## Note:
- The transformed data will be output as a CSV file for each table (fact and dimension).





# Part 2:

## 1. Key Questions to Clarify Requirements

To better understand the scope and requirements of the project, I would ask the team the following questions:
- How is "successful career growth" defined, and is it consistent across industries?
- How should skills be normalized, especially if we have varying skill descriptions and levels across different professionals?
- Are salary bands standardized across industries, or do they vary based on the industry or role?

## 2. Key Metrics

Based on the current assumptions, the following metrics would be valuable:
- **Avg_Tenure_Role_Industry**: This metric calculates the average tenure for professionals in a specific role within an industry. It helps professionals understand a typical career path in a given industry.
- **Avg_Salary_Band_Role_Industry**: This metric calculates the average salary band for a given role within an industry. It helps determine salary expectations and growth prospects within specific industries.

### Assumptions:
- Career growth is defined as an increase in salary band between jobs in the same industry.
- Salary bands are assumed to be consistent across all industries.
- For this case study, skills and certifications are not included in the career growth calculation.

## 3. Data Model Supporting Career Development Insights

The data model supports answering key career development questions by:
- **Aggregating Career Data**: An aggregate table, such as `Agg_Industry`, is created on top of the fact table. This provides a high-level view of career progression within specific industries.
- **Snapshot for Industry Trends**: By capturing snapshots of the `Agg_Industry` table, we can track changes in career growth patterns across industries over time.

## 4. Additional Data Sources

To enrich the analysis and provide more insights, the following data sources are recommended:
- **Salary Band by Role**: A detailed breakdown of salary bands for each role across different industries.
- **Standardized Job Titles**: A mapping table that maps job titles across different companies to ensure consistency in role definitions.


# Part 3: 

Below are the steps and considerations for productionizing the workflow:

1. Use DAG Factory for Dynamic DAG Creation
- **DAG Factory**: This ensures that the code is scalable and easy to maintain as new tasks or workflows are added.

2. Implement CI/CD Pipeline to automate testing, building, and deployment of DAGs. This will streamline updates and ensure that the DAGs are always tested before deployment. I will add the following as part of the CI/CD pipeline.
  - **Pydantic Validation**: To validate the DAG configuration file to ensure correct input types and values.
  - **Unit Tests**: To help verify the functionality and ensure they work as expected before production deployment.

3. Modularize the Code: Organize the code into reusable modules. Split functions and classes into separate Python files to make the code more manageable and maintainable.

4. Add Alerts for DAG Failures: Set up alerting mechanisms to notify relevant stakeholders in case of DAG failures. This can include email notifications, Slack messages, or other integrations to ensure timely intervention.

5. Version Control with Git

6. Secure Sensitive Information: Avoid hardcoding any critical values (e.g., passwords, API keys, etc.) directly into the code. Store sensitive information securely in **AWS Secrets Manager** or similar tools to ensure better security practices.
