from dao import BaseDao
from logger import api_logger


class PhoneDao(BaseDao):

    def save(self,**values):
        api_logger.info('db update users:<%s>' % values['phone'])
        super(PhoneDao,self).save('phone_records',**values)