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