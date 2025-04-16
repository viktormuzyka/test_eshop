from django.urls import path
from store.api.auth_api import RegisterView, LoginView
from store.api.order_api import  CreateOrderView, GetOrderView, ListOrdersView, CancelOrderView
from store.api.product_api import CreateProductView, GetProductView, ListProductsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
    path('orders/<int:order_id>/', GetOrderView.as_view(), name='get-order'),
    path('orders/<int:order_id>/cancel/', CancelOrderView.as_view(), name='cancel-order'),
    path('orders/user/<int:user_id>/', ListOrdersView.as_view(), name='list-orders'),
    path('products/create/', CreateProductView.as_view(), name='create-product'),
    path('products/', ListProductsView.as_view(), name='get-all-products'),
    path('products/<int:product_id>/', GetProductView.as_view(), name='get-product'),
]
 