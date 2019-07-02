from dao import BaseDao


# 详情
class DetailsDao(BaseDao):
    def c_list(self,fields,where,args):
        return super(DetailsDao,self).list('courses',fields,where=where,args=args)

    def c_info(self,course_id):  # 所有章节信息
        courseinfo = self.c_list('*','course_id',course_id)  # 获取详情页顶部信息，图片，类名，title
        return courseinfo

    def c_type(self,type_id,child_type_id):  # 大类小类名称
        c_type = self.list('courses_type',('id','name'),where='id',args=type_id)
        c_child_type = self.list('courses_child_type',('name',),where='id',args=child_type_id)
        return c_type,c_child_type

    def c_presentation(self,course): # 介绍页
        clist = ['id', 'name', 'img_url','description','degree', 'course_time',
                 'study_num', 'course_score','youneed_know', 'teacher_tell',
                 'teacher_id']
        precourse = {k:course[k] for k in clist}    # 对返回数据按前端需求筛选
        t_info = BaseDao().list('teachers',('t_name','t_job','t_pic'),
                                    where='id',args=precourse['teacher_id'])[0]
        return {'precourse':precourse,'t_info':t_info}

    def c_lesson(self,c_id): # 免费章节页
        lesson = self.list('chapters',('id','name'),where='course_id',args=c_id)
        videos = self.list('videos',('name','video_url','lesson_id'),where='course_id',args=c_id)
        print(lesson,videos)
        data = []
        for i in lesson: # 对返回数据做组装，将lesson对应的video组装在一起
            i['videos'] = [j for j in videos if j['lesson_id'] == i['id']]
            data.append(i)
        return data

    def pay_detail(self,course): # 付费详情页
        clist = ['id', 'name','price','degree', 'course_time',
                 'study_num', 'course_score','detail_url']
        precourse = {k: course[k] for k in clist}
        detail_url = precourse.pop('detail_url').split("#") # 取出所有详情页中的url，并做组装
        precourse['detail_url'] = {i:detail_url[i] for i in range(len(detail_url))}
        lesson = self.list('chapters', ('id', 'name'), where='course_id', args=precourse['id'])
        videos = self.list('videos', ('name', 'video_url', 'lesson_id'), where='course_id', args=precourse['id'])
        if all((precourse,lesson,videos)):
            precourse['video_url'] = videos[0][0]['videos'][0]  # 取第一章第一个视频作为试看视频,插入详情字典
            del videos['video_url'] # 删除videos中的video_url字段
            lesson = []
            for i in lesson:  # 对返回数据做组装，将lesson对应的video组装在一起
                i['videos'] = [j.re for j in videos if j['lesson_id'] == i['id']]
                lesson.append(i)
            data = {'precourse':precourse,'lesson':lesson}
            return data
        return None


if __name__ == '__main__':
    DetailsDao().c_lesson(50)
    str1 = '1#2#3'
    print(str1.split("#"))