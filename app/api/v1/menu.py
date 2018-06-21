from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Menu, Category, Dish, Restaurant, db
from app.login import login_required

api = Namespace('menu')

# Menu
@api.route('/')
class Menus(Resource):

    # 新建菜单
    @login_required(authority='manager')
    def post(self):

        try:
            form = request.form

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

            used = form.get('used')
            if used is None:
                used = 0
            try:
                used = int(used)
            except Exception as e:
                print(e)
                return {'message': ('Used must be 0 or 1, 1 means in use')}, 400
            if used != 0 or used != 1:
                return {'message': ('Used must be 0 or 1, 1 means in use')}, 400

            menu = Menu()
            menu.name = name
            menu.rank = rank
            menu.used = used
            menu.restId = 1
            menu.delete = False
            db.session.add(menu)
            db.session.commit()

            return {
                'message': 'Add a new menu successfully',
                'id': menu.id
                }, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500
    
    # 获取所有菜单
    @login_required(authority='customer')
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

@api.route('/<int:menuid>')
class Menus(Resource):

    # 获取单个菜单
    @login_required(authority='customer')
    def get(self, menuid):
        menu = Menu.query.filter_by(id=menuid).first()
        if menu is None:
            return {'message': 'Menu not found'}, 404

        return menu.json(), 200

    # 修改菜单
    @login_required(authority='manager')
    def put(self, menuid):
        menu = Menu.query.filter_by(id=menuid).first()
        if menu is None:
            return {'message': 'Menu not found'}, 404

        try:
            form = request.form
            name = form.get('name')
            if name is not None:
                menu.name = name

            rank = form.get('rank')
            if rank is not None:
                try:
                    rank = int(rank)
                except Exception as e:
                    print(e)
                    return {'message': 'Rank should be integer'}, 400
                menu.rank = rank

            used = form.get('used')
            if used is not None:
                try:
                    used = int(used)
                except Exception as e:
                    print(e)
                    return {'message': 'Used must be 0 or 1, 1 means in use'}, 400
                if used != 0 or used != 1:
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
        if menu is None:
            return {'message': 'Menu not found'}, 404
        
        menu.delete = True
        menu.restId = -1
        db.session.commit()
        return {'message': 'Successfully delete.'}, 200

# Category
@api.route('/<menuid>/categories')
class Categories(Resource):

    #新建类别
    @login_required(authority='manager')
    def post(self, menuid):

        try:
            form = request.form

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

@api.route('/<menuid>/categories/<catid>')
class Categories(Resource):

    #删除类别
    @login_required(authority='manager')
    def delete(self, menuid, catid):

        category = Category.query.filter_by(id=catid).first()
        if category is None:
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
            if category is None:
                return {'message': 'Category not found'}, 404
            
            if category.menuId != menuid:
                return {'message': 'Category not in menu'}, 400
                
            form = request.form

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
@api.route('/<menuid>/categories/<catid>/dishes/')
class Dishes(Resource):
    
    # 新建菜品
    @login_required(authority='manager')
    def post(self, menuid, catid):

        try:
            category = Category.query.filter_by(id=catid).first()
            if category is None:
                return {'message': 'Bad category'}, 400
            
            if category.menuId != menuid:
                return {'message': 'Bad menu'}, 400

            form = request.form

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
            
            img = form.get('img')
            if img is None:
                return {'message': 'Img is required'}, 400
            
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
            if avaliable != 0 or avaliable != 1:
                return {
                    'message': 'Avaliable must be 0 or 1, 1 means avaliable'
                    }, 400
            
            description = form.get('description')
            if description is None:
                description = ""

            dish = Dish()
            dish.name = name
            dish.rank = rank
            dish.img = img
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

@api.route('/<menuid>/categories/<catid>/dishes/<dishid>')
class Dishes(Resource):
    
    # 修改菜品
    @login_required(authority='manager')
    def put(self, menuid, catid, dishid):

        try:
            dish = Dish.query.filter_by(id=dishid).first()
            if dish is None:
                return {'message': 'Dish not found'}, 404
            if dish.catId != catid:
                return {'message': 'Bad category'}, 400

            category = Category.query.filter_by(id=catid).first()
            if category is None:
                return {'message': 'Category not found'}, 404
            
            if category.menuId != menuid:
                return {'message': 'Category not in menu'}, 400

            form = request.form

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
            
            
            img = form.get('img')
            if img is not None:
                dish.img = img
            
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
                if avaliable != 0 or avaliable != 1:
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
        if dish is None:
            return {'message': 'Dish not found'}, 404
        if dish.catId != catid:
            return {'message': 'Bad category'}, 400

        category = Category.query.filter_by(id=catid).first()
        if category is None:
            return {'message': 'Category not found'}, 404
        
        if category.menuId != menuid:
            return {'message': 'Category not in menu'}, 400

        return dish.json(), 200

    #删除菜品
    @login_required(authority='manager')
    def delete(self, menuid, catid, dishid):

        dish = Dish.query.filter_by(id=dishid).first()
        if dish is None:
            return {'message': 'Dish not found'}, 404
        if dish.catId != catid:
            return {'message': 'Bad category'}, 400

        category = Category.query.filter_by(id=catid).first()
        if category is None:
            return {'message': 'Category not found'}, 404
        
        if category.menuId != menuid:
            return {'message': 'Category not in menu'}, 400
        
        dish.delete = True
        dish.catId = -1
        db.session.commit()
        return {'message': 'Successfully delete.'}, 200
