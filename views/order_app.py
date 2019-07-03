from flask import Blueprint, request, jsonify
from libs import cache_, crypt
from dao.cart_dao import CartDao
from dao.order_dao import OrderDao
from dao.pay_dao import PayDao
from dao.user_course_dao import UserCourseDao
from logger import api_logger
import uuid

order_blue = Blueprint("order_blue", __name__)


@order_blue.route("/confirmorder/", methods=["GET"])
def confirm_order():
    token = request.get_json().get("token",None)
    if token is None:  # 传递参数中未传递token
        return jsonify({"code": 201, "msg": "token查询参数必须提供！"})
    c_id = request.args.get("cid")  # 获取查询字符串中的课程id
    types = request.args.get("type")  # 获取查询字符串中的购买类型的
    u_id = cache_.get_token_user_id(token)
    if u_id:
        if types == "fromcart":  # 如果是从购物车去结算
            cart_obj = CartDao()
            course_info = cart_obj.will_pay_course(c_id, u_id).get("course_list")
            total_price = cart_obj.will_pay_course(c_id, u_id).get("total_price")
            return jsonify({"code": 200, "products": course_info, "total_price": total_price})
        elif types == "fromcombat":  # 如果是立即购买结算
            pay_obj = PayDao()
            cid = pay_obj.get_course_id(c_id)
            course_info = pay_obj.get_pay_course(cid).get("pay_course")
            total_price = pay_obj.get_pay_course(cid).get("total_price")
            return jsonify({"code": 200, "products": course_info, "total_price": total_price})

    return jsonify({"code": 201, "msg": "用户还未登录或注册！"})


@order_blue.route("/addorder/", methods=["POST"])  # 提交订单
def add_order():
    token = request.get_json().get("token")
    if token is None:
        return jsonify({"code": 201, "msg": "token查询参数必须提供"})
    resp = request.get_json()
    total = resp.get("total")
    type1 = resp.get("type")
    c_id = resp.get("course")  # 获取的c_id是字符串 <class 'str'>
    u_id = cache_.get_token_user_id(token)
    print(c_id)
    if u_id:
        if type1 == "fromcart":  # 如果是从购物车提交订单
            cart_dao = CartDao()
            course_info = cart_dao.will_pay_course(c_id, u_id).get("course_list")
            total_price = cart_dao.will_pay_course(c_id, u_id).get("total_price")
            # print("aaaaaaaaaa", course_info,type(course_info))
            if len(c_id) > 1:
                if total_price == total:  # 提交订单传递的总价是否和后台计算的总价相等
                    order_obj = OrderDao()
                    # user_course = UserCourseDao()
                    order_num = order_obj.next_order_num()  # 生成订单编号
                    for course in course_info:  # 创建订单记录
                        order_success = order_obj.save("orders", **{"order_num": order_num, "user_id": u_id,
                                                                    "course_id": course.get("id"),
                                                                    "price": course.get("price")})

                        if order_success:
                            # 如果创建订单，购买的课程存入用户课程表中成功，则删除购物车记录
                            cart_delete = cart_dao.delete_user_cart_course(course.get("id"), u_id)
                            if cart_delete:
                                continue
                    # 返回订单信息
                    return jsonify({"code": 200, "order_num": order_num, "data": course_info})
                return jsonify({"code": 201, "msg": "价格不正确"})
            elif len(c_id) == 1:
                if total_price == total:
                    order_obj = OrderDao()
                    order_num = order_obj.next_order_num()
                    order_success = order_obj.save("orders", **{"order_num": order_num, "user_id": u_id,
                                                                "course_id": course_info.get("id"),
                                                                "price": course_info.get("price")})
                    if order_success:  # 如果创建订单记录成功，返回订单信息
                        cart_delete = cart_dao.delete_user_cart_course(course_info.get("id"), u_id)
                        if cart_delete:
                            return jsonify({"code": 200, "order_num": order_num, "data": course_info})
                return jsonify({"code": 201, "msg": "价格不正确"})

        elif type1 == "fromcombat":  # 如果是立即购买提交订单
            pay_dao = PayDao()
            cid = pay_dao.get_course_id(c_id)
            course_info = pay_dao.get_pay_course(cid).get("pay_course")
            total_price = pay_dao.get_pay_course(cid).get("total_price")
            if total_price == total:  # 总价相等，创建一条订单记录
                order_obj = OrderDao()
                order_num = order_obj.next_order_num()
                order_success = order_obj.save("orders", **{"order_num": order_num, "user_id": u_id,
                                                            "course_id": course_info[0].get("id"),
                                                            "price": course_info[0].get("price")})
                if order_success:  # 如果创建订单记录成功，返回订单信息
                    return jsonify({"code": 200, "order_num": order_num, "data": course_info})
            return jsonify({"code": 201, "msg": "价格不正确"})
    return jsonify({"code": 201, "msg": "用户未登录或注册"})


@order_blue.route("/perorder/", methods=["GET"])
def my_order():
    token = request.headers.get("token")
    if token is None:
        return jsonify({{"code": 201, "msg": "token查询参数必须提供"}})
    u_id = cache_.get_token_user_id(token)
    if u_id:  # 如果用户登录，返回订单的信息
        order = OrderDao()
        order_all_info = order.get_order_info(u_id)  # 订单的全部信息
        order_pay = order.get_order_pay_state(u_id).get("pay")  # 已支付的订单信息
        order_no_pay = order.get_order_pay_state(u_id).get("no_pay")  # 未支付的订单信息
        if any((order_all_info,order_pay,order_no_pay)):
            return jsonify({
                "code": 200,
                'msg': "ok",
                'data': {
                    "order_all_info": order_all_info,
                    "order_pay": order_pay,
                    "order_no_pay": order_no_pay
                }
            })
        else:
            return jsonify({"code":200,"msg":"用户暂未相关订单"})
    return jsonify({"code": 201, "msg": "用户还未登录或注册"})


@order_blue.route("/orderdetail/", methods=["GET", ])
def order_detail():
    token = request.args.get("token", None)
    order_num = request.args.get("trade_number")
    if token is None:
        return jsonify({"code": 201, "msg": "token查询参数必须提供"})

    u_id = cache_.get_token_user_id(token)
    if u_id:
        order_detail_obj = OrderDao()
        order_detail = order_detail_obj.get_order_detail(u_id, order_num)
        return jsonify({"code": 200, 'msg': "ok", "order_detail": order_detail})

    return jsonify({"code": 201, "msg": "用户还未登录或注册"})


@order_blue.route("/cancelorder/", methods=["GET"])
def cancel_order():
    token = request.args.get("token", None)
    order_num = request.args.get("trade_number")
    if token is None:
        return jsonify({"code": 201, "msg": "token查询参数必须提供"})
    u_id = cache_.get_token_user_id(token)
    if u_id:
        order_cancel = OrderDao()
        delete_order = order_cancel.delete_order(u_id, order_num)
        if delete_order:
            return jsonify({"code": 200, "msg": "已关闭！"})
        else:
            return jsonify({"code": 200, "msg": "取消订单失败！"})

    return jsonify({"code": 201, "msg": "用户还未登录或注册"})

# user_course_success = user_course.save("user_courses", **{"user_id": u_id, "course_id": course.get("id"),
# "is_free":False})
