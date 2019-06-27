import uuid

from flask import Blueprint, request,jsonify
from libs.cache_ import *
from dao.cart_dao import CartDao
from logger import api_logger

cart_blue = Blueprint("cart_blue",__name__)

@cart_blue.route("/add_cart/",methods=["POST",])   #还需传递参数token
def add_cart_view():
    token = request.args.get("token")
    c_id = request.args.get("cid")
    # 验证是否登录
    u_id = get_token_user_id(token)
    print(u_id)
    if u_id:
        add_cart = CartDao()
        cart = add_cart.check_cart(uid=u_id,cid=c_id) #如果已登录，通过当前用户和课程id,查询购物车是否有该条记录
        if not cart:
            #如果没有则创建一条购物车记录
            add_cart.save('cart',**{"u_id":u_id,"c_id":c_id,"is_select":1})
            result = {"code":200,'msg':"商品已添加至购物车！"}
            return jsonify(result)
        result = {'code': 201, 'msg': '该商品在购物车中已存在~'}
        return jsonify(result)

    api_logger.warn("%s 未登录 " % u_id)
    result = {'code':202,'msg':'用户还未登录或注册'}
    return jsonify(result)

@cart_blue.route("/ucenter/cart/",methods=["GET",])
def cart_view():
    #验证当前用户是否登录
    token = request.args.get("token")
    u_id = get_token_user_id(token)
    #通过用户id查询当前用户的购物车记录,及课程信息
    if u_id:
        print(u_id)
        cart_obj = CartDao()
        try:
            course_info = cart_obj.get_cart_course(u_id)
            total_price = cart_obj.total(u_id)
            result = {'code':200,'msg':'ok!','course':course_info,'total_price':total_price}
        except Exception as e:
            api_logger.error("checkout course_info failed!,cause:%s" % e)
            result = {'code':201,'msg':e}
        return jsonify(result)

    api_logger.warn("%s 未登录 " % u_id)
    result = {'code': 202, 'msg': '用户还未登录或注册'}
    return jsonify(result)


if __name__ == '__main__':
    token = uuid.uuid4().hex
    print(token)
    r.set(token,2)
