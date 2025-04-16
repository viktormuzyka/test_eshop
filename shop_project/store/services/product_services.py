from store.models import Product
from django.db.models import Q

def create_product(name, description, price, stock=0):
    return Product.objects.create(
        name=name,
        description=description,
        price=price,
        stock=stock
    )

def get_product(product_id):
    return Product.objects.filter(id=product_id).first()

def list_products(query=None, min_price=None, max_price=None):
    filters = Q()
    if query:
        filters &= Q(name__icontains=query) | Q(description__icontains=query)
    if min_price is not None:
        filters &= Q(price__gte=min_price)
    if max_price is not None:
        filters &= Q(price__lte=max_price)
    return Product.objects.filter(filters)
