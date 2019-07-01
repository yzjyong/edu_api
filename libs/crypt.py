import hashlib
import time


def make_password(passwd_str): # 对密码加密
    return hashlib.md5(("9@^"+passwd_str+"$&").encode()).hexdigest()


def check_password(passwd_str,encrypted_str): # 检查密码
    return make_password(passwd_str) == encrypted_str


def get_order_code():   #生成订单编号
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) \
               + str(time.time()).replace('.', '')[-7:]
    return order_no

if __name__ == '__main__':
    print(time.time())
    print(get_order_code())

