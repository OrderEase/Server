from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import User, Order, OrderItem, Dish, Category, Menu, Rule, Promotion, Restaurant, Carousel, db
from app.login import login_required
from datetime import datetime
import operator

api = Namespace('analytics')

"""APIs:
analytics/turnover/?days=7  turnoverSevenDays  交易金额
analytics/turnover/?days=30  turnoverThirtyDays
analytics/count/card  countCard  今天的数据
analytics/count/orders  orderCount
analytics/count/payWay  payWay
analytics/count/finishTime  finishTime  分钟
analytics/count/summary  summaryData  指定时间段
analytics/rank/sale  saleRank
analytics/rank/likes  likeRank
"""

def change_format(origin_dict):
    name_value_list = []
    for key in origin_dict.keys():
        name_value_list.append({'name': key, 'value': origin_dict[key]})
    return name_value_list

# ok
@api.route('/turnover')
class GetTurnover(Resource):

    # @login_required(authority="manager")
    def get(self):
        try:
            days = int(request.args.get('days'))
            # print(days)
            if days != 7 and days != 30:
                return {'message': 'Only support 7 or 30 query days.'}, 400

            categories = Category.query.filter(Category.id > 0).all()
            # categories_dict = {}
            data_dict = {}

            # print(categories)
            for category in categories:
                data_dict[category.name] = {'name': category.name, 'data': [0 for x in range(days)]}
                # categories_dict[category.id] =

            dishes = Dish.query.order_by(Dish.id).all()
            dishes_dict = {}
            for dish in dishes:
                dishes_dict[dish.id] = dish
            # print(dishes_dict)

            xAxis = []
            for i in range(days):
                date = datetime.today().date() - timedelta(days=days - i)
                xAxis.append("%d月%d日" % (date.month, date.day))

                orders = Order.query.filter(Order.payDate >= date, Order.payDate < date + timedelta(days=1)).all()
                for order in orders:
                    for item in order.items:
                        # print(item)
                        # print(data_dict[dishes_dict[item.dishId].categories.name])
                        data_dict[dishes_dict[item.dishId].categories.name]['data'][i] += dishes_dict[item.dishId].price
                        # print(data_dict[dishes_dict[item.dishId].categories].price)
                        # data_dict[dishes_dict[item.dishId].categories] = dishes_dict[item.dishId].price
            # print(list(data_dict.values()))
            return {"xAxis": xAxis, "data": list(data_dict.values())}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

# ok
@api.route('/count/card')
class CountCard(Resource):

    # @login_required(authority="manager")
    def get(self):
        try:
            date = datetime.today().date()
            next_date = date + timedelta(days=1)
            orders = Order.query.filter(Order.payDate >= date).all()
            today_users_list = []
            for order in orders:
                if order.uid not in today_users_list:
                    today_users_list.append(order.uid)

            today_new_users = User.query.filter(User.register_date >= date).all()
            today_orders = Order.query.filter(Order.payDate >= date).all()

            today_due = 0
            today_dish_quantity = 0
            for order in today_orders:
                today_due += order.due
                for item in order.items:
                    today_dish_quantity += item.quantity

            return {'totalUser': len(today_users_list), "newUser": len(today_new_users), "turnover": today_due, "dish": today_dish_quantity}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

# ok
@api.route('/count/orders')
class CountOrders(Resource):

    # @login_required(authority="manager")
    def get(self):
        try:
            weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            count = [0 for x in range(7)]
            orders = Order.query.all()

            for order in orders:
                count[order.payDate.weekday()] += 1

            # print(change_format(dict(zip(weekday, count))))
            return change_format(dict(zip(weekday, count))), 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


# ok
@api.route('/count/payway')
class CountPayWay(Resource):

    # @login_required(authority="manager")
    def get(self):
        try:
            payway_dict = {}
            orders = Order.query.filter().all()
            for order in orders:
                if order.payWay not in payway_dict.keys():
                    payway_dict[order.payWay] = 0
                payway_dict[order.payWay] += 1

            return change_format(payway_dict), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


# ok
@api.route('/count/finishtime')
class CountFinishTime(Resource):

    # @login_required(authority="manager")
    def get(self):
        try:
            max_order_finish_time = 0
            total_order_time = 0

            max_dish_finish_time = 0
            total_dish_finish_time = 0
            total_dish_num = 0

            orders = Order.query.all()
            for order in orders:
                if order.finished == 0:
                    continue
                last_dish_finish_time = 0
                for dish in order.items:
                    dish_finish_time = (dish.time - order.payDate).seconds / 60
                    # print(dish.time - order.payDate)

                    if dish_finish_time > last_dish_finish_time:
                        last_dish_finish_time = dish_finish_time

                    if dish_finish_time > max_dish_finish_time:
                        max_dish_finish_time = dish_finish_time

                    total_dish_num += dish.quantity
                    total_dish_finish_time += dish_finish_time

                total_order_time += last_dish_finish_time

                if last_dish_finish_time > max_order_finish_time:
                    max_order_finish_time = last_dish_finish_time

            return {"order": {"avg": round(total_order_time / len(orders), 1), "max": max_order_finish_time}, "dish": {"avg": round(total_dish_finish_time / total_dish_num, 1), "max": max_dish_finish_time}}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


@api.route('/summary')
class CountSummary(Resource):

    # @login_required(authority="manager")
    def get(self):
        try:
            # 两端都是包含
            start = end = None
            if request.args.get('start') is not None:
                start = datetime.strptime(request.args.get('start'), "%Y-%m-%d")
                end = datetime.strptime(request.args.get('end'), "%Y-%m-%d")
            else:
                tmp_orders = Order.query.order_by(Order.payDate).all()
                start = tmp_orders[0].payDate.date()
                end = tmp_orders[len(tmp_orders) - 1].payDate.date()
                # print(start)
                # print(end)

            summary_list = []

            day_count = (end - start).days + 1
            for date in [d for d in (start + timedelta(n) for n in range(day_count))]:
                next_date = date + timedelta(days=1)
                orders = Order.query.filter(Order.payDate > date, Order.payDate < next_date).all()

                total_order_time = 0
                total_dish_finish_time = 0
                total_dish_num = 0
                total_due = 0
                total = 0

                for order in orders:
                    total += order.total
                    total_due += order.due
                    last_dish_finish_time = 0
                    for dish in order.items:
                        dish_finish_time = (dish.time - order.payDate).seconds / 60
                        # print(dish.time - order.payDate)

                        if dish_finish_time > last_dish_finish_time:
                            last_dish_finish_time = dish_finish_time

                        total_dish_num += dish.quantity
                        total_dish_finish_time += dish_finish_time

                    total_order_time += last_dish_finish_time

                summary_list.append({"date": date.strftime("%Y-%m-%d"),
                                     "order": len(orders),
                                     "dish": total_dish_num,
                                     "avgOrder": round(total_order_time / len(orders), 1) if len(orders) > 0 else 0, # 平均完成时间
                                     "avgDish": round(total_dish_finish_time / total_dish_num, 1) if total_dish_num > 0 else 0,
                                     "due": total_due,
                                     "total": total})

            return summary_list, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


# ok
@api.route('/rank/likes')
class CreateRules(Resource):

    # @login_required(authority="manager")
    def get(self):
        try:
            dishes = Dish.query.order_by(Dish.likes.desc()).all()

            likes_rank_dict = {}
            for dish in dishes:
                likes_rank_dict[dish.name] = dish.likes

            return change_format(likes_rank_dict), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


# ok
@api.route('/rank/sales')
class CreateRules(Resource):

    # @login_required(authority="manager")
    def get(self):
        try:
            dishes = Dish.query.order_by(Dish.id).all()
            dish_sale_dict = {}
            dishes_dict = {}
            for dish in dishes:
                dish_sale_dict[dish.name] = 0
                dishes_dict[dish.id] = dish

            orders = Order.query.all()

            for order in orders:
                for item in order.items:
                    dish_sale_dict[dishes_dict[item.dishId].name] += item.quantity

            dish_sale_dict = dict(sorted(dish_sale_dict.items(), key=lambda k: k[1], reverse=True))
            # print(change_format(dish_sale_dict))
            return change_format(dish_sale_dict), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500