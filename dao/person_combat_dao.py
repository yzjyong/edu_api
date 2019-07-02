from dao import BaseDao


class PersonCombatDao(BaseDao): # 我的实战
    def comlist(self,where,args): # 获取用户课程表
        return super(PersonCombatDao,self).list('user_courses',('course_id','video_name_id','add_time'
                                                                ),where=where,args=args)

    def u_course(self,course_id): # 根据课程id,获取课程信息
        course_data = self.list('courses',('id','name','img_url','description','study_num',
                                'course_type_id','course_child_type_id'),where='course_id',args=course_id)
        if course_data:
            type_id = course_data[0]['course_type_id']
            child_type_id = course_data[0]['course_child_type_id']
            c_type = self.list('courses_type', ('id', 'name'), where='id', args=type_id)
            c_child_type = self.list('courses_child_type',('name',), where='id', args=child_type_id)
            if all((c_type,c_child_type)):
                course_data[0]['c_type'],course_data[0]['c_child_type'] = c_type[0],c_child_type[0]
                return course_data
            return None
        return None


if __name__ == '__main__':
    l = [{'name':'tom','age':12}]