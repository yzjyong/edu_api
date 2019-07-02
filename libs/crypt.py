import hashlib
import time


def make_password(passwd_str): # 对密码加密
    return hashlib.md5(("9@^"+passwd_str+"$&").encode()).hexdigest()


def check_password(passwd_str,encrypted_str): # 检查密码
    return make_password(passwd_str) == encrypted_str


