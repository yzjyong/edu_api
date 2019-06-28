from dao import BaseDao


# 详情
class DetailsDao(BaseDao):
    def c_list(self,*fileds,where,args):
        return super(DetailsDao,self).list('courses',*fileds,where=where,args=args)

    def c_top(self,course_id):  # 顶部信息
        topcourse = self.c_list(('id','name','course_type_id','course_child_type_id','img_url'),
                              where='course_id',args=course_id)  # 获取详情页顶部信息，图片，类名，title
        topcourse=topcourse[0] if topcourse else None # 判定是否为空，空则返回Mone
        return topcourse

    def c_presentation(self,c_id): # 介绍页
        precourse = self.c_list(('description','degree','course_time','study_num','course_score',
                               'youneed_know','teacher_tell','teacher_id'),where='id',args=c_id)[0]  # 获取课程信息
        t_info = BaseDao().list('teachers',('t_name','t_job','t_pic'),
                                    where='id',args=precourse['teacher_id'])[0]
        return precourse, t_info

    def c_lesson(self,c_id): # 章节页
        lesson = BaseDao().list('lessons',('lesson_id','name'),where='course_id',args=c_id)
        videos = BaseDao().list('videos',('video_id','name','video_url'),where='course_id',args=c_id)
        data = {'lesson':lesson,'videos':videos}
        return data


if __name__ == '__main__':
    print(DetailsDao().c_lesson(50))