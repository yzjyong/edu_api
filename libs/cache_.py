import uuid
from libs import r


def new_token():
    return uuid.uuid4().hex

def save_token(token,id):
    r.setex(token,id,12*3600) # 保存12小时

def check_token(token):
    # 验证token
    return r.exists(token)

def get_token_user_id(token):
    if check_token(token):
        return r.get(token).decode()


if __name__ == '__main__':
    r.delete()