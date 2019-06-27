from flask import jsonify

from dao import BaseDao


class MineDao(BaseDao):

    def mine_query(self):
        try:
            sql1 = 'select id, image_url from main_banner limit 1, 6 '
            sql2 = 'select course_id, name, degree,img_url, price, study_num from courses where is_free=false limit 1, 5'
            sql3 = 'select course_id, name, degree, study_num,img_url, price from courses order by add_time desc limit 1, 5'
            sql4 = 'select course_id, name, degree,img_url, study_num from courses where is_free=true limit 1, 5'
            sql5 = 'select t_id, t_name, t_job, t_pic from teachers limit 0, 3'
            sql6 = 'select course_id, name, degree, img_url, study_num from courses where is_free=true limit 1, 10'
            main_banner_data = self.query(sql1)
            combat_courses = self.query(sql2)
            new_courses = self.query(sql3)
            free_courses = self.query(sql4)
            teachers_data = self.query(sql5)
            favourite_courses = self.query(sql6)
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