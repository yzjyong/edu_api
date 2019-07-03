from redis import Redis


r = Redis(host='localhost',port=6373,db=0)

if __name__ == '__main__':
    print()