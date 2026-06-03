"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from collections import defaultdict
from dataclasses import dataclass
from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

@dataclass
class OrderRedis:
    id: int
    user_id: int
    total_amount: float

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders from Redis"""
    r = get_redis_conn()
    keys = r.keys("order:*")
    orders = []
    for key in keys[:limit]:
        data = r.hgetall(key)
        order_id = int(key.split(":")[1])
        orders.append(OrderRedis(
            id=order_id,
            user_id=int(data.get("user_id", 0)),
            total_amount=float(data.get("total", 0))
        ))
    orders.sort(key=lambda o: o.id, reverse=True)
    return orders

def get_highest_spending_users():
    """Get top 10 users by total spending from Redis"""
    r = get_redis_conn()
    keys = r.keys("order:*")
    expenses_by_user = defaultdict(float)
    for key in keys:
        data = r.hgetall(key)
        user_id = data.get("user_id")
        expenses_by_user[user_id] += float(data.get("total", 0))
    return sorted(expenses_by_user.items(), key=lambda item: item[1], reverse=True)[:10]

def get_best_sellers():
    """Get best selling products from Redis, sorted by quantity sold"""
    r = get_redis_conn()
    keys = r.keys("product:*")
    products = []
    for key in keys:
        product_id = int(key.split(":")[1])
        quantity = int(r.get(key) or 0)
        products.append((product_id, quantity))
    return sorted(products, key=lambda item: item[1], reverse=True)