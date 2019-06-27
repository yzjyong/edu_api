# 详情
from dao import BaseDao


class DetailsDao(BaseDao):

    def get_presentation(self,course_id):
        courseinfo = self.list('courses',('id',''),where='course_id',args=course_id)[0] # 获取课程信息
        course_score = self.list('courses_score',('course_score',),where='course_id',args=courseinfo['id'])
        sql = 'select sum(learn_times) from videos where course_id=%s group by course_id'
        course_time = self.query(sql,courseinfo['id'])[0]['sum(learn_times)']
        if all((courseinfo,course_score,course_time)):
            courseinfo['course_score'],courseinfo['course_time'] = course_score,course_time
            return print(courseinfo)
        return None

    def get_lesson(self,couse_id):
        sql = 'select ls.lesson_id,ls.name from lessons as ls ' \
            'join courses as cs on cs.id=ls.course_id where cs.course_id = %s'
        lessoninfo = self.query(sql,couse_id)
        if lessoninfo:
            return lessoninfo[0]

    def get_video(self,lesson_id):
        sql = 'select '

if __name__ == '__main__':
    DetailsDao().get_course(10)