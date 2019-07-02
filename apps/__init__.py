from flask import Flask
from flask_cors import CORS
from celery import Celery

app = Flask(__name__,
            static_folder='../uploads',
            static_url_path='/uploads'
            )
CORS(app,supports_credentials=True)

# 配置celery的消息中间件
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6373/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6373/0'

# 创建Celery的客户端
capp = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
capp.conf.update(app.config)
capp.autodiscover_tasks(('apps',))  # 配置从哪些包下查找tasks.py文件中的异步任务