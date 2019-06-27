

from dao import BaseDao
from logger import api_logger


class MineDao(BaseDao):

    def order_list(self, table_name, *fileds,
            field=None, sort='desc', page=1, page_size=20):
        sql = "select {} from {} order by  {} {} limit {}, {}".format \
                (','.join(*fileds), table_name, field, sort, (page - 1) * page_size, page_size)
        with self.db as c:
            c.execute(sql)
            result = c.fetchall()
            api_logger.info('%s ok!' % sql)
            return result

    def mine_query(self):
        try:
            main_banner_data = self.list('main_banner', ('id', 'image_url'), page=1, page_size=6)
            combat_courses = self.list('courses', ('course_id', 'name', 'degree','img_url', 'price', 'study_num'),
                                       where='is_free', args='false', page=1, page_size=5)
            new_courses = self.order_list('courses', ('course_id', 'name', 'degree', 'study_num','img_url', 'price'),
                                          field='add_time', sort='desc', page=1, page_size=5)
            free_courses = self.list('courses', ('course_id', 'name', 'degree','img_url', 'study_num'),
                                     where='is_free', args='true', page=1, page_size=5)
            teachers_data = self.list('teachers', ('t_id', 't_name', 't_job', 't_pic'), page=1, page_size=3)
            favourite_courses = self.list('courses', ('course_id', 'name', 'degree', 'img_url', 'study_num'),
                                          where='is_free', args='true', page=1, page_size=10)
        except Exception as e:
            raise Exception({'code': 201, 'msg': e})

        return {
                "main_banner_data": main_banner_data,
                "combat_courses": combat_courses,
                "new_courses": new_courses,
                "free_courses": free_courses,
                "teachers_data": teachers_data,
                "favourite_courses": favourite_courses
                }

if __name__ == '__main__':
    MineDao().mine_query()