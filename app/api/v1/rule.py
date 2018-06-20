from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Rule, Promotion, db
from app.login import login_required
from .promotion import api as api

# api = Namespace('promotions')

@api.route('/<pid>/rules')
class CreateRules(Resource):

    @login_required(authority="manager")
    def post(self, pid):

        try:
            form = request.form

            mode = int(form.get('mode'))
            if mode is None :
                return {'message': 'Mode is required.'}, 400

            if mode != 1 and mode != 2:
                return {'message': 'Mode is required to be 1 or 2.'}, 400

            requirement = float(form.get('requirement'))
            if requirement is None or requirement < 0:
                return {'message': 'Requirement is required and not negative.'}, 400

            discount = int(form.get('discount'))
            if discount is None or discount < 0:
                return {'message': 'Discount is required and not negative.'}, 400

            promotion_id = pid

            rule = Rule()
            rule.mode = mode
            rule.requirement = requirement
            rule.discount = discount
            rule.promotion_id = promotion_id

            db.session.add(rule)
            db.session.commit()

            return {'id': rule.id}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


@api.route('/<int:pid>/rules/<int:rid>')
class ModifyRules(Resource):

    @login_required(authority="manager")
    def get(self, pid, rid):
        try:
            # promotion = Promotion.filter_bu(id=pid).first()

            # if promotion is None:
            #     return {'message': 'promotion not found.'}, 404

            # for rule in promotion.rules:
            #     if rule.id == rid:
            #         return rule.json(), 200

            rule = Rule.query.filter_by(id=rid).first()
            if rule is None:
                return {'message': 'rule not found.'}, 404

            return rule.json()

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority="manager")
    def put(self, pid, rid):
        try:
            # promotion = Promotion.filter_by(id=pid).first()

            # if promotion is None:
            #     return {'message': 'rule not found.'}, 404


            rule = Rule.query.filter_by(id=rid).first()
            # for tmp_rule in promotion.rules:
            #     if tmp_rule.id == rid:
            #         rule = tmp_rule

            if rule is None:
                return {'message': 'rule not found.'}, 404

            form = request.form

            mode = int(form.get('mode'))
            if mode is None :
                return {'message': 'Mode is required.'}, 400
            if mode != 1 and mode != 2:
                return {'message': 'Mode is required to be 1 or 2.'}, 400

            requirement = float(form.get('requirement'))
            if requirement is None or requirement < 0:
                return {'message': 'Requirement is required and not negative.'}, 400

            discount = int(form.get('discount'))
            if discount is None or discount < 0:
                return {'message': 'Discount is required and not negative.'}, 400

            promotion_id = pid

            rule.mode = mode
            rule.requirement = requirement
            rule.discount = discount
            rule.pid = promotion_id
            db.session.commit()

            return rule.json(), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority="manager")
    def delete(self, pid, rid):
        rule = Rule.query.filter_by(id=rid).first()
        if rule is None:
            return {'message': 'rule not found'}, 404
        db.session.delete(rule)
        db.session.commit()

        return {'message': 'delete rule successfully.'}, 200