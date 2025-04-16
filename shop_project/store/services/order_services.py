from django.contrib.auth import get_user_model
from store.models import Order, OrderItem, Product

User = get_user_model()

def create_order(user_id, items):
    user = User.objects.get(id=user_id)
    order = Order.objects.create(user=user)

    for item in items:
        product = Product.objects.get(id=item['product_id'])
        quantity = item['quantity']
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    order.update_total_price()
    return order

def cancel_order(order):
    if order:
        order.delete() 

def get_order(order_id):
    return Order.objects.filter(id=order_id).prefetch_related('items__product').first()

def list_orders(user=None):
    qs = Order.objects.all()
    if user:
        qs = qs.filter(user=user)
    return qs.prefetch_related('items__product')
