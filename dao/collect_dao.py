from dao import BaseDao


class CollectDao(BaseDao):
    # 将收藏的课程存入用户收藏表中
    def save(self, table_name, **values):
        return super(CollectDao, self).save("user_favorites",**values)

    # 获取当前用户收藏的全部课程信息
    def get_my_collect(self, uid):
        sql = "select courses.name,courses.img_url,courses.degree,courses.study_num,courses.is_free" \
              " from courses join user_favorites on user_favorites.course_id = courses.id " \
              " where user_favorites.user_id =%s "
        my_collect = [my_collect for my_collect in self.query(sql, uid) if my_collect.get("is_free")==0]
        return my_collect

    # 取消收藏则将用户收藏表的用户课程记录删除
    def cancel_user_collect(self, uid, cid):
        sql = "delete from user_favorites where user_id=%s and course_id=%s"
        success = False
        with self.db as c:
            c.execute(sql, (uid, cid))
            success = True
        return success
