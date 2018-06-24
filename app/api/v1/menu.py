# *-* coding: utf-8 *-*
from flask import request, json, Response
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Menu, Category, Dish, Restaurant, db
from app.login import login_required
import json
from flask_login import current_user
from PIL import Image
import hashlib
from .utils import getImageFromBase64

api = Namespace('menus')

# Menu
@api.route('/')
class Menus(Resource):

    # 新建菜单
    @login_required(authority='manager')
    def post(self):

        try:
            form = request.get_json(force=True)
            # print(form)
            name = form.get('name')
            if name is None:
                ret = {'message': 'Menu name is required'}
                return Response(json.dumps(ret), 
                        status=400, 
                        mimetype='application/json')


            used = form.get('used')
            if used is None:
                used = 0
            try:
                used = int(used)
            except Exception as e:
                print(e)
                ret = {'message': ('Used must be 0 or 1,'
                            ' 1 means in use')}
                return Response(json.dumps(ret), 
                        status=400, 
                        mimetype='application/json')

            if used != 0 and used != 1:
                ret = {'message': ('Used must be 0 or 1,'
                            ' 1 means in use')}
                return Response(json.dumps(ret), 
                        status=400, 
                        mimetype='application/json')

            menu = Menu()
            menu.name = name
            menu.used = used
            menu.restId = 1
            menu.delete = False
            db.session.add(menu)
            db.session.commit()

            ret = {
                'message': 'Add a new menu successfully',
                'id': menu.id
                }
            return Response(json.dumps(ret), 
                        status=200, 
                        mimetype='application/json')
        except Exception as e:
            print(e)
            ret = {'message': 'Internal Server Error'}
            return Response(json.dumps(ret), 
                        status=500,
                        mimetype='application/json')
    
    # 获取所有菜单
    @login_required(authority='manager')
    def get(self):

        try:
            restaurant = Restaurant.query.filter_by(id=1).first()
            if restaurant is None:
                return {
                    'message': 'No restaurant found, thus no menus'
                    }, 404
            # tmp_menus = Menu.query.filter_by(delete=False).all()
            ret = []
            for menu in restaurant.menus:
                ret.append(menu.json())

            return {'menus': ret}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/cuser')
class Menus(Resource):
    @login_required(authority='customer')
    def get(self):
        menu = Menu.query.filter_by(used=1).first()
        if menu is None or menu.delete is True:
            return {'message': 'Menu not found'}, 404
        
        content = []
        for cat in menu.cats:
            t_dishes = []
            for dish in cat.dishes:
                if dish.avaliable == 1:
                    t_dishes.append(dish.json())

            cat_json = {
                'id': cat.id,
                'name': cat.name,
                'rank': cat.rank,
                'dishes': t_dishes
            }
            content.append(cat_json)

        return {
            'id': menu.id,
            'name': menu.name,
            'used': menu.used,
            'content': content
        }, 200

@api.route('/<int:menuid>')
class Menus(Resource):

    # 获取单个菜单
    @login_required(authority='customer')
    def get(self, menuid):
        menu = Menu.query.filter_by(id=menuid).first()
        if menu is None or menu.delete is True:
            return {'message': 'Menu not found'}, 404

        return menu.json(), 200

    # 修改菜单
    @login_required(authority='manager')
    def put(self, menuid):
        menu = Menu.query.filter_by(id=menuid).first()
        if menu is None or menu.delete is True:
            return {'message': 'Menu not found'}, 404

        try:
            form = request.get_json(force=True)
            name = form.get('name')
            if name is not None:
                menu.name = name

            used = form.get('used')
            if used is not None:
                try:
                    used = int(used)
                except Exception as e:
                    print(e)
                    return {'message': 'Used must be 0 or 1, 1 means in use'}, 400
                if used != 0 and used != 1:
                    return {'message': 'Used must be 0 or 1, 1 means in use'}, 400
                menu.used = used

            db.session.commit()

            return {'message': 'Successfully update.', 'menuId': menu.id}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    #删除某一菜单
    @login_required(authority='manager')
    def delete(self, menuid):
        menu = Menu.query.filter_by(id=menuid).first()
        if menu is None or menu.delete is True:
            return {'message': 'Menu not found'}, 404
        
        menu.delete = True
        menu.restId = -1
        db.session.commit()
        return {'message': 'Successfully delete.'}, 200

# Category
@api.route('/<int:menuid>/categories/')
class Categories(Resource):

    #新建类别
    @login_required(authority='manager')
    def post(self, menuid):

        try:
            form = request.get_json(force=True)

            name = form.get('name')
            if name is None:
                return {'message': 'Dish name is required'}, 400

            rank = form.get('rank')
            if rank is None:
                return {'message': 'Dish rank is required'}, 400
            try:
                rank = int(rank)
            except Exception as e:
                print(e)
                return {'message': 'Dish rank must be integer'}, 400

            category = Category()
            category.name = name
            category.rank = rank
            category.menuId = menuid
            category.delete = False
            db.session.add(category)
            db.session.commit()

            return {
                'message': 'Add a new category successfully',
                'id': category.id
                }, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/<int:menuid>/categories/<int:catid>')
class Categories(Resource):

    #删除类别
    @login_required(authority='manager')
    def delete(self, menuid, catid):

        category = Category.query.filter_by(id=catid).first()
        if category is None or category.delete is True:
            return {'message': 'Category not found'}, 404
        
        if category.menuId != menuid:
            return {'message': 'Category not in menu'}, 400
        
        category.delete = True
        category.menuId = -1
        db.session.commit()
        return {'message': 'Successfully delete.'}, 200
    
    # 修改类别
    @login_required(authority='manager')
    def put(self, menuid, catid):

        try:
            category = Category.query.filter_by(id=catid).first()
            if category is None or category.delete is True:
                return {'message': 'Category not found'}, 404
            
            if category.menuId != menuid:
                return {'message': 'Category not in menu'}, 400
                
            form = request.get_json(force=True)

            name = form.get('name')
            if name is not None:
                category.name = name

            rank = form.get('rank')
            if rank is not None:
                try:
                    rank = int(rank)
                except Exception as e:
                    print(e)
                    return {'message': 'Dish rank must be integer'}, 400
                category.rank = rank

            db.session.commit()

            return {
                'message': 'Modify a category successfully',
                }, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

# Dish
@api.route('/<int:menuid>/categories/<int:catid>/dishes/')
class Dishes(Resource):
    
    # 新建菜品
    @login_required(authority='manager')
    def post(self, menuid, catid):

        try:
            dish = Dish()

            category = Category.query.filter_by(id=catid).first()
            if category is None or category.delete is True:
                return {'message': 'Bad category'}, 400
            
            if category.menuId != menuid:
                return {'message': 'Bad menu'}, 400

            form = request.get_json(force=True)

            name = form.get('name')
            if name is None:
                return {'message': 'Dish name is required'}, 400

            rank = form.get('rank')
            if rank is None:
                return {'message': 'Dish rank is required'}, 400
            try:
                rank = int(rank)
            except Exception as e:
                print(e)
                return {'message': 'Dish rank must be integer'}, 400
            
            # img = form.get('img')
            # if img is None:
            #     img = 'https://raw.githubusercontent.com/OrderEase/Server/master/assets/default.png'
            
            dataURI = form.get('img')
            path = 'static/images/dishes/default.png'
            if dataURI is not None:
                hl = hashlib.md5()
                hl.update(('%s.png' % dish.id).encode(encoding='utf-8'))

                avatar = '%s.png' % hl.hexdigest()

                path = 'static/images/dishes/' + avatar
                image = getImageFromBase64(dataURI)
                image.save(path)

            price = form.get('price')
            if price is None:
                return {'message': 'Price is required'}, 400
            try:
                price = float(price)
            except Exception as e:
                print(e)
                return {'message': 'Price must be float number'}, 400
            
            stock = form.get('stock')
            if stock is None:
                return {'message': 'Dish stock is required'}, 400
            try:
                stock = int(stock)
            except Exception as e:
                print(e)
                return {'message': 'Dish stock must be integer'}, 400

            avaliable = form.get('avaliable')
            if avaliable is None:
                return {'message': 'Dish avaliable is required'}, 400
            try:
                avaliable = int(avaliable)
            except Exception as e:
                print(e)
                return {
                    'message': 'Avaliable must be 0 or 1, 1 means avaliable'
                    }, 400
            if avaliable != 0 and avaliable != 1:
                return {
                    'message': 'Avaliable must be 0 or 1, 1 means avaliable'
                    }, 400
            
            description = form.get('description')
            if description is None:
                description = ""

            
            dish.img = path
            dish.name = name
            dish.rank = rank
            # dish.img = img
            dish.price = price
            dish.stock = stock
            dish.avaliable = avaliable
            dish.description = description
            dish.likes = 0
            dish.catId = catid
            dish.delete = False
            db.session.add(dish)
            db.session.commit()

            return {
                'message': 'Add a new dish successfully',
                'id': dish.id
                }, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

# @api.route('/<int:menuid>/categories/<int:catid>/dishes/<int:dishid>/avatar')
# class Dishesr(Resource):

#     @login_required(authority="customer")
#     def get(self):
#         try:
#             buser = User.query.filter_by(id=current_user.id).first()
#             return {"path": 'static/images/users/' + buser.avatar}, 200

#         except Exception as e:
#             print(e)
#             return {'message': 'Internal Server Error'}, 500

@api.route('/<int:menuid>/categories/<int:catid>/dishes/<int:dishid>')
class Dishes(Resource):
    
    # 修改菜品
    @login_required(authority='manager')
    def put(self, menuid, catid, dishid):

        try:
            dish = Dish.query.filter_by(id=dishid).first()
            if dish is None or dish.delete is True:
                return {'message': 'Dish not found'}, 404
            if dish.catId != catid:
                return {'message': 'Bad category'}, 400

            category = Category.query.filter_by(id=catid).first()
            if category is None or category.delete is True:
                return {'message': 'Category not found'}, 404
            
            if category.menuId != menuid:
                return {'message': 'Category not in menu'}, 400

            form = request.get_json(force=True)

            name = form.get('name')
            if name is not None:
                dish.name = name

            rank = form.get('rank')
            if rank is not None:
                try:
                    rank = int(rank)
                except Exception as e:
                    print(e)
                    return {'message': 'Dish rank must be integer'}, 400
                dish.rank = rank
            
            
            # img = form.get('img')
            # if img is not None:
            #     dish.img = img
            dataURI = form.get('img')
            if dataURI is not None:
                hl = hashlib.md5()
                hl.update(('%s.png' % dish.id).encode(encoding='utf-8'))

                avatar = '%s.png' % hl.hexdigest()
                path = 'static/images/dishes/' + avatar
                dish.img = path
                image = getImageFromBase64(dataURI)
                image.save(path)
            
            price = form.get('price')
            if price is not None:
                try:
                    price = float(price)
                except Exception as e:
                    print(e)
                    return {'message': 'Price must be float number'}, 400
                dish.price = price
            
            stock = form.get('stock')
            if stock is not None:
                try:
                    stock = int(stock)
                except Exception as e:
                    print(e)
                    return {'message': 'Dish stock must be integer'}, 400
                dish.stock = stock
            
            avaliable = form.get('avaliable')
            if avaliable is not None:
                try:
                    avaliable = int(avaliable)
                except Exception as e:
                    print(e)
                    return {
                        'message': 'Avaliable must be 0 or 1, 1 means avaliable'
                        }, 400
                if avaliable != 0 and avaliable != 1:
                    return {
                        'message': 'Avaliable must be 0 or 1, 1 means avaliable'
                        }, 400
                dish.avaliable = avaliable
            
            description = form.get('description')
            if description is not None:
                dish.description = description

            db.session.commit()

            return {
                'message': 'Modify a dish successfully',
                }, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500
    
    # 获取一个菜
    @login_required(authority='customer')
    def get(self, menuid, catid, dishid):
        dish = Dish.query.filter_by(id=dishid).first()
        if dish is None or dish.delete is True:
            return {'message': 'Dish not found'}, 404
        if dish.catId != catid:
            return {'message': 'Bad category'}, 400

        category = Category.query.filter_by(id=catid).first()
        if category is None or category.delete is True:
            return {'message': 'Category not found'}, 404
        
        if category.menuId != menuid:
            return {'message': 'Category not in menu'}, 400

        return dish.json(), 200

    #删除菜品
    @login_required(authority='manager')
    def delete(self, menuid, catid, dishid):

        dish = Dish.query.filter_by(id=dishid).first()
        if dish is None or dish.delete is True:
            return {'message': 'Dish not found'}, 404
        if dish.catId != catid:
            return {'message': 'Bad category'}, 400

        category = Category.query.filter_by(id=catid).first()
        if category is None or category.delete is True:
            return {'message': 'Category not found'}, 404
        
        if category.menuId != menuid:
            return {'message': 'Category not in menu'}, 400
        
        dish.delete = True
        dish.catId = -1
        db.session.commit()
        return {'message': 'Successfully delete.'}, 200
