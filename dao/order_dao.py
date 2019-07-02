from dao import BaseDao
from logger import api_logger


class OrderDao(BaseDao):
    def save(self, table_name, **values):     #创建订单记录
        api_logger.info("orders of %s is ok~" % values['user_id'])
        return super(OrderDao, self).save('orders', **values)


    def get_order_info(self,uid):   #查看当前用户的订单中的课程信息
        sql = "select orders.status,orders.order_num,courses.name,courses.img_url,courses.price " \
              "from orders join courses on courses.id = orders.course_id where user_id=%s"
        order = self.query(sql,uid)
        return order

    def get_order_pay_state(self,uid):   #获取 订单中支付和未支付的课程信息
        order_info = self.get_order_info(uid)
        order_pay_list = []
        order_no_pay_list = []
        for order_pay in order_info:
            if order_pay.get("status")== 1:
                order_pay_list.append(order_pay)

            elif order_pay.get("status")==0:
                order_no_pay_list.append(order_pay)
        return {
            "pay":order_pay_list,      #已支付的课程信息
            'no_pay':order_no_pay_list    #未支付的课程信息
        }

    def get_order_course(self,cid,uid):
        sql = "select videos.name from videos join orders on videos.course_id = orders.course_id" \
              " join users on users.id = orders.user_id"
        course = self.query(sql,(cid,uid))
        return course


    def get_order_detail(self,uid,o_num):    #通过订单编号获取当前用户的订单详情信息
        sql = "select * from orders where user_id=%s and order_num=%s"
        order_detail = self.query(sql,*(uid,o_num))
        return order_detail

    def delete_order(self,uid,o_num):     #取消订单
        sql = "delete from orders where user_id= %s and order_num=%s"
        success = False
        with self.db as c:
            c.execute(sql,(uid,o_num))
            success = True
        return success
