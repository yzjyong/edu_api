from dao import BaseDao


class PayDao(BaseDao):

    def get_pay_course(self,cid):  #获取当前用户立即购买的课程信息和价格
        sql = "select courses.id,courses.course_id,courses.name,courses.price,courses.img_url from courses " \
              "where courses.course_id=%s"
        print(sql,"sql")
        try:
            pay_course = self.query(sql,cid)
            print(pay_course,"111111122333")
            return {
                "pay_course":pay_course,
                "total_price":pay_course[0].get("price")
            }
        except Exception as e:
            raise Exception(e)

    def get_course_id(self, cid):
        sql = "select id from courses where course_id = %s"
        data = self.query(sql, (cid,))
        print(data[0], '----------')
        return data[0].get('id')