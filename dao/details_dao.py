from dao import BaseDao


# 详情
class DetailsDao(BaseDao):
    def c_list(self,fileds,where,args):
        return super(DetailsDao,self).list('courses',fileds,where=where,args=args)

    def c_info(self,course_id):  # 顶部信息
        courseinfo = self.c_list('*','course_id',course_id)  # 获取详情页顶部信息，图片，类名，title
        return courseinfo

    def c_presentation(self,course): # 介绍页
        clist = ['id', 'name', 'course_type_id', 'course_child_type_id', 'img_url','description',
                 'degree', 'course_time', 'study_num', 'course_score','youneed_know', 'teacher_tell',
                 'teacher_id']
        precourse = {k:course[k] for k in clist}
        t_info = BaseDao().list('teachers',('t_name','t_job','t_pic'),
                                    where='id',args=precourse['teacher_id'])[0]
        return {'precourse':precourse,'t_info':t_info}

    def c_lesson(self,c_id): # 章节页
        lesson = self.list('lessons',('id','name'),where='course_id',args=c_id)
        videos = self.list('videos',('name','video_url','lesson_id'),where='course_id',args=c_id)
        data = []
        for i in lesson:
            i['videos'] = [j for j in videos if j['lesson_id'] == i['id']]
            data.append(i)
        return data


if __name__ == '__main__':
    DetailsDao().c_lesson(50)