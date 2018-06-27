from flask import request
from flask_restplus import Namespace, Resource
from flask_login import login_user, logout_user, current_user
from app.login import login_required
from app import restrts_upload_set, dishes_upload_set

api = Namespace('photos')

@api.route('/restrt')
class PhotosRestrt(Resource):

    #上传店铺头像
    @login_required(authority="manager")
    def post(self):
        try:
            filename = restrts_upload_set.save(request.files.get('file'))

            return {'url': restrts_upload_set.url(filename)}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


@api.route('/dish')
class PhotosDish(Resource):

    #上传菜品图片
    @login_required(authority="manager")
    def post(self):
        try:
            filename = dishes_upload_set.save(request.files.get('file'))

            return {'url': dishes_upload_set.url(filename)}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500