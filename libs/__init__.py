from redis import Redis

<<<<<<< HEAD
r = Redis(host='121.199.63.71',port=6373,db=1)
=======
r = Redis(host='121.199.63.71',port=6373,db=0)
>>>>>>> 32447f1237677f9b09476e1a9177c2704ad70005

if __name__ == '__main__':
    print(r.get('abc'))
