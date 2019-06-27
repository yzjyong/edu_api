# 详情
from dao import BaseDao


class DetailsDao(BaseDao):
    def list(self,*fileds,
             where=None,args=None,page=1,page_size=20):
        return super(DetailsDao,self).list('courses',*fileds,where=where,args=args)

    def get_course(self,course_id):
        courseinfo = self.list('(name,desc,degree,is_free,study_num)',where='course_id',args=course_id)
        print('')
        if courseinfo:
            return courseinfo[0]

    def get_lesson(self,couse_id):
        sql = 'select ls.lesson_id,ls.name from lessons as ls ' \
            'join courses as cs on cs.id=ls.course_id where cs.course_id = %s'
        lessoninfo = self.query(sql,couse_id)
        if lessoninfo:
            return lessoninfo[0]

    def get_video(self,lesson_id):
        sql = 'select '
