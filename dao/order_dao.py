from dao import BaseDao
from logger import api_logger


class OrderDao(BaseDao):
    def save(self, table_name, **values):
        api_logger.info("orders of %s is ok~" % values['user_id'])
        return super(OrderDao, self).save('orders', **values)


    def get_order_info(self,uid):
        sql = "select * from orders where user_id=%s"
        order = self.query(sql,uid)
        return order

    def get_order_pay_state(self,uid):
        order_info = self.get_order_info(uid)
        order_pay_list = []
        order_no_pay_list = []
        for order_pay in order_info:
            if order_pay.get("status")== 1:
                order_pay_list.append(order_pay)

            elif order_pay.get("status")==0:
                order_no_pay_list.append(order_pay)
        return {
            "pay":order_pay_list,
            'no_pay':order_no_pay_list
        }

    def get_order_detail(self,uid,o_num):
        sql = "select * from orders where user_id=%s and order_num=%s"
        order_detail = self.query(sql,*(uid,o_num))
        return order_detail

    def delete_order(self,uid,o_num):
        sql = "delete from orders where user_id= %s and order_num=%s"
        success = False
        with self.db as c:
            c.execute(sql,(uid,o_num))
            success = True
        return success
