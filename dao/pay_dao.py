from dao import BaseDao


class PayDao(BaseDao):

    def get_pay_course(self,uid,cid):  #获取当前用户立即购买的课程信息和价格
        sql = "select courses.id,courses.name,courses.price,courses.img_url from courses join " \
              "user_courses on courses.id=user_courses.course_id where user_courses.user_id=%s and courses.id=%s"
        print(sql,"sql")
        try:
            pay_course = self.query(sql,uid,cid)
            print(pay_course,"111111122333")
            return {
                "pay_course":pay_course,
                "total_price":pay_course[0].get("price")
            }
        except Exception as e:
            raise Exception(e)