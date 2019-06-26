# from flask import current_app, render_template
# from flask_mail import Message
# from threading import Thread
# from apps import mail


# def async_send_email(app,msg): # 异步发送邮件
#     with app.app_context():
#         mail.send(msg)
#
# def email_code(to,subject,template,**kwargs):
#
#     app = current_app._get_current_object()
#     # 实例化Message对象
#     msg = Message(subject,sender='1223241490@qq.com',recipients=[to])
#     msg.body = render_template(template + '.txt',**kwargs)
#     msg.html = render_template(template + '.html',**kwargs)
#     thr = Thread(target=async_send_email,args=[app,msg])
#     thr.start()
#     return thr

# app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
# app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
# app.config['MAIL_SERVER'] = 'smtp.qq.com'   # 邮箱服务器
# app.config['MAIL_PORT'] = 465               # 端口
# app.config['MAIL_USE_SSL'] = True           # 重要，qq邮箱需要使用SSL
# app.config['MAIL_USE_TLS'] = False          # 不需要使用TLS
# app.config['MAIL_USERNAME'] = '1223241490@qq.com'  # 填邮箱
# app.config['MAIL_PASSWORD'] = 'ueqrenahhelyhdbc'      # 填授权码
# app.config['MAIL_DEFAULT_SENDER'] = '1223241490@qq.com'  # 填邮箱，默认发送者
# mail = Mail(app)