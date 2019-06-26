from dao import BaseDao
from logger import api_logger


class PhoneDao(BaseDao):

    def save(self,table_name,**values):
        api_logger.info('db replace users:<%s>' % values['u_phone'])
        super(PhoneDao,self).save('phone_records',**values)