echo 'Execution started...!'
echo 'Execution started...!'
docker ps
docker exec imdb-task_app_1  bash -c "echo 'Downloading requirements';pip install  pytest;pytest -s;"
