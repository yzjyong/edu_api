from dao import BaseDao


# 详情
class DetailsDao(BaseDao):
    def list(self,*fileds,args):
        return super(DetailsDao,self).list('courses',*fileds,where='course_id',args=args)

    def get_top(self,course_id):
        topcourse = self.list(('name','course_type_id','course_child_type_id','img_url'),
                              args=course_id)  # 获取详情页顶部信息，图片，类名，title
        topcourse=topcourse[0] if topcourse else None # 判定是否为空，空则返回Mone
        return topcourse

    def get_presentation(self,course_id):
        precourse = self.list(('id','description','degree','course_time','study_num','course_score',
                               'youneed_know','teacher_tell','teacher_id'),args=course_id)[0]  # 获取课程信息
        print(precourse)
        t_info = BaseDao().list('teachers',('t_name','t_job','t_pic'),
                                    where='t_id',args=precourse['teacher_id'])[0]
        return precourse, t_info


if __name__ == '__main__':
    DetailsDao().get_top(10)