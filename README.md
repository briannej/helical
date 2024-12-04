This repo is to create and execute Helical workflows for
applying biological foundation models in biological applications notebooks. This is done using a frontend Next.js 15 app. The backend uses server actions from Nextjs. The pipeline is executed using Airflow. In airflow, a docker container running Helical, and papermill is used to run notebooks.
All the application including the frontend, backend and Airflow, is containerized.

## Getting Started

First, initialize the database. You need to run database migrations and create the first user account. To do this, run

```bash
docker compose up airflow-init
```
After initilization, the account created has the login airflow and the password airflow.

Now you can start all services:
```bash
docker compose up
```
This will take some time (perhaps up to 30 mins). When done, open [http://localhost:3000/dashboard](http://localhost:3000/dashboard) to see the Helical dashboard to create a pipeline.

After, clicking on create pipeline on the previous page, go to [http://localhost:8080](http://localhost:8080). Login with username airflow, and password airflow to see the airflow dashboard. You can see the pipleline. You can check the logs to see that the helical notebook was run.

There is a service called helical-notebook-runner which runs example Helical notebooks. However, this takes a long time. In order to simulate running Helical notebooks there is another service, called Helical-quick-runner. This simulated service is what is seen in the airflow dashboard. In order to see the actual Helical notebook running, uncomment the code in the dags folder.