from redis import Redis

r = Redis(host='121.199.63.71',port=6373,db=1)

if __name__ == '__main__':
    print(r.get('abc'))