# run.py

from dotenv import load_dotenv
# Asegúrate de que esta línea esté correcta
from app import create_app 

load_dotenv() 

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8002)