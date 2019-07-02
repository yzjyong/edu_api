from dao import BaseDao
from logger import api_logger


class UserCourseDao(BaseDao):
    def save(self, table_name, **values):
        api_logger.info("user_courses of %s is ok~" % values["user_id"])
        return super(UserCourseDao, self).save('user_courses', **values)

