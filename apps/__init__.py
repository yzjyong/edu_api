from flask import Flask

app = Flask(__name__,
            static_folder='../uploads',
            static_url_path='/uploads'
            )