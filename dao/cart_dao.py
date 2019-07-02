from dao import BaseDao
from logger import api_logger


class CartDao(BaseDao):
    def save(self,table_name,**values):
        api_logger.info("carts of %s is ok~" % values["user_id"])
        return super(CartDao,self).save('carts',**values)

    # 检查当前用户、当前课程的购物车记录
    def check_cart(self, uid, cid):
        sql = "select user_id,course_id,is_select from carts where user_id= %s and course_id = %s "
        cart = self.query(sql, *(uid, cid))
        print(cart, "cart99999999", type(cart))
        return cart

    # 查询当前用户购物车中的课程信息
    def get_cart_course(self, uid):
        sql = "select carts.is_select,courses.course_id,courses.name,courses.degree,courses.price,courses.img_url" \
              " from carts join courses on carts.course_id = courses.id where carts.user_id=%s"
        course_info = self.query(sql, uid)
        return course_info

    # 计算当前用户购物车中被选中课程的总价格
    def total(self, uid):
        course = self.get_cart_course(uid)
        total_price = 0
        for c in course:
            is_select = c.get("is_select")
            if is_select == 1:
                total_price += c.get("price")
        return total_price

    # 通过参数商品id列表，获取将要付款的课程信息
    def will_pay_course(self, cid, uid):
        course_info = self.get_cart_course(uid)
        course_list = []
        total = 0
        try:
            if len(cid) > 1:
                c_id = cid.split(",")
                for course in course_info:
                    for id in c_id:
                        if course.get("id") ==int(id):
                            total += course.get("price")
                            course_list.append(course)
                return {
                    "course_list": course_list,
                    "total_price": total
                }
            elif len(cid) == 1:
                for course in course_info:
                    if course.get("id") == int(cid):
                        return {
                            "course_list": course,
                            "total_price": course.get("price")
                        }
        except Exception as e:
            return {"code":201, "msg": e}

    # 通过课程id和用户uid删除购物车记录
    def delete_user_cart_course(self, cid, uid):
        api_logger.info("%s have been delete", cid)
        sql = "delete from carts where course_id = %s and user_id=%s"
        try:
            success = False
            with self.db as c:
                c.execute(sql,(cid,uid))
                success = True
            return success
        except Exception as e:
            api_logger.error("delete cart_course failed", e )