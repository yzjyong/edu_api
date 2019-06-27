from dao import BaseDao
from logger import api_logger
class CartDao(BaseDao):

    def save(self,table_name,**values):
        api_logger.info("cart of %s is ok~" % values['user_id'])
        return super(CartDao,self).save('carts',**values)

    def check_cart(self,uid,cid):
        #检查当前用户、当前课程的购物车记录
        sql = "select user_id,course_id from carts where user_id= %s and course_id = %s "
        cart = self.query(sql,*(uid,cid))
        return cart

    def get_cart_course(self,u_id):
        #查询当前用户购物车中的课程信息
        sql = "select cart.user_id,cart.is_select,courses.course_id,courses.name,courses.degree,courses.price,courses.img_url" \
              " from carts join courses on carts.course_id = course.course_id where cart.user_id=%s"
        course_info = self.query(sql,u_id)
        return course_info

    def total(self,uid):
        #计算当前用户购物车中被选中课程的总价格
        course = self.get_cart_course(uid)
        total_price = 0
        for c in course:
            is_select = c.get("is_select")
            if is_select==1:
                total_price += c.get("price")
        return total_price