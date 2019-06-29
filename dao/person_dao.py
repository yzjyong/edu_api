from dao import BaseDao


class PersonDao(BaseDao):
    def perupdate(self,key,value, where, args):
        return super(PersonDao,self).update('users',key,value,where,args)

    def perlist(self,args):
        return super(PersonDao,self).list('users','u_pname','u_gender','address',
                                          'u_pic','u_sign',where='id',args=args)