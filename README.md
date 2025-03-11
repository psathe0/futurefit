## Steps to Setup Project Locally:
This project uses **docker-airflow** to run the DAGs.

1. **Set Up Airflow with Docker**  
   Follow the official guide to set up Airflow with Docker:  
   [Airflow Docker Compose Setup Guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

   **Note**: During the setup, a file called `docker-compose.yaml` will be created. You will need to make some changes to this file.  
   Copy the contents of `docker-compose_main.yaml` to `docker-compose.yaml` for the code to work.

2. **Install Dependencies**  
   Run the following command to install required Python dependencies:
   ```bash
   pip install -r requirements.txt

3. It is recommended to use a Python virtual environment for isolated execution.
