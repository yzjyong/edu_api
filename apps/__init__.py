from flask import Flask
from flask_cors import CORS

app = Flask(__name__,
            static_folder='../uploads',
            static_url_path='/uploads'
            )
CORS(app,supports_credentials=True)