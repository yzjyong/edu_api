import os,uuid
from flask import Blueprint, request, jsonify
from werkzeug.datastructures import FileStorage
from dao.person_dao import PersonDao
from libs import oss
from libs.cache_ import get_token_user_id

blue = Blueprint('persblue',__name__)


# 展示个人中心
@blue.route('/person/<string:key>',methods=['GET'])
def personinfo(key):
    resp = request.args
    if resp: # 验证请求数据
        token = resp.get('token')
        id = get_token_user_id(token)
        if id:
            perinfo = PersonDao().perlist(id)
            if perinfo:
                img_type = int(request.args.get('type', 0))
                img_url = oss.get_url(key) if img_type == 0 else oss.get_small_url(key)
                perinfo[0]['url'] = img_url
                return jsonify(perinfo)
            return jsonify({'code': 203, 'msg': '查询失败！'})
        else:
            return jsonify({'code': 203, 'msg': '你还未登录！'})
    return jsonify({'code': 304, 'msg': '传入数据为空'})


# 修改个人信息
@blue.route('/change/',methods=['POST'],strict_slashes=False)
def changeinfo():
    resp = eval(request.get_data())
    if resp:
        token = resp.pop('token')
        id = get_token_user_id(token)
        file: FileStorage = request.files.get('img', None)
        if all((bool(token),bool(id))):
            # 验证文件的类型, png/jpeg/jpg, 单张不能超过2M
            # content-type: image/png, image/jpeg
            if bool(file):
                if file.content_type in ('image/png','image/jpeg'):
                    filename = uuid.uuid4().hex + os.path.splitext(file.filename)[-1]
                    file.save(filename)
                    key = oss.upload_file(filename) # 上传到oss云服务器上
                    os.remove(filename)  # 删除临时文件
                    PersonDao().perupdate('u_pic', key, id) # 将key写入到DB中
                    for k,v in resp.items():
                        PersonDao().perupdate(k,v,id)
                    return ({'code':200,'msg':'ok!','file_key': key})
                return jsonify({'code': 201,'msg': '图片格式只支持png或jpeg'})
            for k, v in resp.items():
                PersonDao().perupdate(k, v, id)
            return ({'code': 200, 'msg': 'ok!'})
        else:
            return jsonify({'code': 203, 'msg': 'POST请求参数必须有token！'})
    return jsonify({'code': 304, 'msg': '传入数据为空'})


if __name__ == '__main__':
    d = {'name':'tom','age':18,'sex':'nan'}
    locals().update(d)