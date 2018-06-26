from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Rule, Promotion, db
from app.login import login_required

api = Namespace('promotions')

@api.route('/')
class Promotions(Resource):

    @login_required(authority="manager")
    def get(self):
        try:
            promotions_list = []
            promotions = Promotion.query.all()
            for promotion in promotions:
                promotions_list.append(promotion.json())

            return promotions_list, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority="manager")
    def post(self):
        try:
            form = request.get_json(force=True)

            theme = form.get('theme')
            if theme is None :
                return {'message': 'Theme is required.'}, 400

            begin = form.get('begin')
            if begin is not None:
                try:
                    begin = datetime.strptime(begin, "%Y-%m-%d %H:%M")
                except Exception as e:
                    print(e)
                    return {'message': 'Wrong format of time'}, 400
            else:
                return {'message': 'Begin date is required.'}, 400

            end = form.get('end')
            if end is not None:
                try:
                    end = datetime.strptime(end, "%Y-%m-%d %H:%M")
                except Exception as e:
                    print(e)
                    return {'message': 'Wrong format of time'}, 400
            else:
                return {'message': 'End date is required.'}, 400

            isend = form.get('isend')
            if (int(isend) != 1 and int(isend) != 0) or isend is None:
                return {'message': 'Isend is required.'}, 400

            promotion = Promotion()
            promotion.theme = theme
            promotion.begin = begin
            promotion.end = end
            promotion.isend = int(isend)

            db.session.add(promotion)
            db.session.commit()

            return {'id': promotion.id}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/<int:pid>')
class Promotions(Resource):

    @login_required(authority="manager")
    def get(self, pid):
        try:
            promotion = Promotion.query.filter_by(id=pid).first()

            if promotion is None:
                return {'message': 'promotion not found.'}, 404

            return promotion.json(), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority="manager")
    def put(self, pid):
        try:
            form = request.get_json(force=True)

            theme = form.get('theme')
            if theme is None:
                return {'message': 'Theme is required.'}, 400

            begin = form.get('begin')
            if begin is not None:
                try:
                    begin = datetime.strptime(begin, "%Y-%m-%d %H:%M")
                except Exception as e:
                    print(e)
                    return {'message': 'Wrong format of time'}, 400
            else:
                return {'message': 'Begin date is required.'}, 400

            end = form.get('end')
            if end is not None:
                try:
                    end = datetime.strptime(end, "%Y-%m-%d %H:%M")
                except Exception as e:
                    print(e)
                    return {'message': 'Wrong format of time'}, 400
            else:
                return {'message': 'End date is required.'}, 400

            isend = form.get('isend')
            if (int(isend) != 0 and int(isend) != 1) or isend is None:
                return {'message': 'Isend is required.'}, 400

            promotion = Promotion.query.filter_by(id=pid).first()
            if promotion is None:
                return {'message': 'promotion not found.'}, 404

            promotion.theme = theme
            promotion.begin = begin
            promotion.end = end
            promotion.isend = int(isend)

            db.session.commit()

            return {"message": "modify promotion successfully"}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority="manager")
    def delete(self, pid):
        promotion = Promotion.query.filter_by(id=pid).first()
        if promotion is None:
            return {'message': 'promotion not found'}, 404
        db.session.delete(promotion)
        db.session.commit()

        return {'message': 'delete promotion successfully.'}, 200