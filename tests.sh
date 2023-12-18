echo 'Execution started...!'
echo 'Execution started...!'
docker ps
docker exec app  bash -c "echo 'Downloading requirements';pip install  pytest;pytest -s;"
