from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from pendulum import datetime
from airflow.operators.python import PythonOperator
from docker.types import Mount

@dag(start_date=datetime(2024, 11, 28), schedule=None, catchup=False)
def airflow_docker_operator():
    start_task = EmptyOperator(task_id='start')

    
    def extract(**kwargs):
        #this is task to show how breaking up different steps in the pipeline would work
        ti = kwargs["ti"]
        data_string = '{"s3_bucket": "helicalbucket", "s3_key": "dataset"}'
        ti.xcom_push("order_data", data_string)

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )
    
    
    # helical_notebook_task = DockerOperator(
    #     task_id='helical_notebook_runner',
        
    #     #docker_url="unix://var/run/docker.sock",  # Use the default Docker socket
    #     docker_url='tcp://docker-socket-proxy:2375', # for the docker inside docker issue
    #     api_version='auto',  # Use 'auto' to let Docker select the appropriate API version
    #     auto_remove=True,  # Remove the container when the task completes
    #     image='helical-notebook-runner:latest',  # Replace with Docker image and tag
    #     container_name="helical_notebook_runner_container",
    #     environment={
    #         'DATASET': '{{ dag_run.conf["dataset"] }}',
    #         'MODEL': '{{ dag_run.conf["model"] }}',
    #         'APPLICATION': '{{ dag_run.conf["application"] }}',
    #     },  # Set environment variables inside the container
    #     #command=['python', 'run_notebook.py'],  # Replace with the command you want to run inside the container
    #     #command= ["papermill", "Quick-Start-Tutorial.ipynb", "output_notebook.ipynb"],
    #     command="""
    #     bash -c "cd /app && \
    #     python run_notebook.py && \
    #     cd /app/notebooks && \
    #     papermill Quick-Start-Tutorial.ipynb output_notebook.ipynb && \
    #     echo 'success'"
    #     """,
    #     # network_mode='bridge',  # Specify the network mode if needed
    #     #volumes=['/Users/brian/developer/helical/pipeline/output:/app/notebooks'],  # Mount volumes if needed
    #     # mounts=[
    #     # Mount(
    #     #     source='/Users/brian/developer/helical/pipeline/notebooks',
    #     #     target='/app/notebooks',
    #     #     type='bind'
    #     # )
    #     # ],
    # )


    helical_quick_task = DockerOperator(
        task_id='helical_quick_runner',
        
        #docker_url="unix://var/run/docker.sock",  # Use the default Docker socket
        docker_url='tcp://docker-socket-proxy:2375', # for the docker inside docker issue
        api_version='auto',  # Use 'auto' to let Docker select the appropriate API version
        auto_remove=True,  # Remove the container when the task completes
        image='helical-quick-runner:latest',  # Replace with Docker image and tag
        container_name="helical_quick_runner_container",
        environment={
            'DATASET': '{{ dag_run.conf["dataset"] }}',
            'MODEL': '{{ dag_run.conf["model"] }}',
            'APPLICATION': '{{ dag_run.conf["application"] }}',
        },  # Set environment variables inside the container
        #command=['python', 'run_notebook.py'],  # Replace with the command you want to run inside the container
        #command= ["papermill", "Quick-Start-Tutorial.ipynb", "output_notebook.ipynb"],
        command="""
        bash -c "cd /app && \
        python run_notebook.py && \
        cd /app/notebooks && \
        papermill Quick-Start-Tutorial.ipynb output_notebook.ipynb && \
        echo 'success'"
        """,
        # network_mode='bridge',  # Specify the network mode if needed
        #volumes=['/Users/brian/developer/helical/pipeline/output:/app/notebooks'],  # Mount volumes if needed
        # mounts=[
        # Mount(
        #     source='/Users/brian/developer/helical/pipeline/notebooks',
        #     target='/app/notebooks',
        #     type='bind'
        # )
        # ],
    )

    start_task >> extract_task >> helical_quick_task # >> helical_notebook_task



airflow_docker_operator()