## init

# install fastApi and Uvicorn
# Uvicorn is an ASGI(Asynchronous Server Gateway Interface)
pip install fastapi uvicorn 

# create a new Python virtural environment  
python -m venv venv 

# activate the virtual environment (on Windows systems)
venv\Scripts\activate 

# run service
# 'reload' is used for hot reloading.
uvicorn main:app --reload


# dependencies management
poetry init 
poetry install      # dependencies install or update
poetry show         # show all of the dependencies
poetry env info     # show Virtualenv

poetry run uvicorn app.main:app --reload --port 8000