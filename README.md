# backend

# install python 

# install poetry
pip install poetry 

# install dependecies
poetry install
poetry self update

# activate poetry
poetry shell

# run the app
before running the backend add the frontend url in the main.py file

uvicorn main:app --reload

# running the docker

docker build -t "app_name" .

docker run -p 8000:80 "app_name"

