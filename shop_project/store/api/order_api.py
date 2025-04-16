from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from store.services.order_services import create_order, cancel_order, get_order, list_orders
from django.contrib.auth import get_user_model
from store.models import Product, Order

User = get_user_model()


class CreateOrderView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new order",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'items'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['product', 'quantity'],
                        properties={
                            'product': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    )
                )
            }
        ),
        responses={
            200: openapi.Response(
                description='Order created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'order_id': openapi.Schema(type=openapi.TYPE_INTEGER)}
                )
            ),
            400: openapi.Response(
                description='Error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            )
        }
    )
    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        items_data = data.get('items', [])

        items = []
        for i in items_data:
            try:
                Product.objects.get(id=i['product'])  # Перевірка наявності продукту
                items.append({'product_id': i['product'], 'quantity': i['quantity']})
            except Product.DoesNotExist:
                return Response({'error': f"Product with id {i['product']} not found."}, status=400)

        order = create_order(user_id, items)
        return Response({'order_id': order.id}, status=status.HTTP_200_OK)


class CancelOrderView(APIView):
    @swagger_auto_schema(
        operation_description="Cancel an order",
        manual_parameters=[
            openapi.Parameter('order_id', openapi.IN_PATH, description="Order ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={'user_id': openapi.Schema(type=openapi.TYPE_INTEGER)}
        ),
        responses={
            200: openapi.Response(description="Order cancelled"),
            400: openapi.Response(description="Invalid request"),
            404: openapi.Response(description="Order not found")
        }
    )
    def post(self, request, order_id):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Invalid user_id'}, status=400)

        order = Order.objects.filter(id=order_id, user=user).first()
        if not order:
            return Response({'error': 'Order not found'}, status=404)

        cancel_order(order)
        return Response({'message': 'Order cancelled'}, status=200)


class GetOrderView(APIView):
    @swagger_auto_schema(
        operation_description="Get order details",
        manual_parameters=[
            openapi.Parameter('order_id', openapi.IN_PATH, description="Order ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(description="Order details"),
            404: openapi.Response(description="Order not found")
        }
    )
    def get(self, request, order_id):
        order = get_order(order_id)
        if not order:
            return Response({'error': 'Order not found'}, status=404)

        return Response({
            'id': order.id,
            'items': [{'product': i.product.name, 'qty': i.quantity} for i in order.items.all()]
        })


class ListOrdersView(APIView):
    @swagger_auto_schema(
        operation_description="List orders for a user",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: openapi.Response(description="List of orders")}
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        orders = list_orders(user=user)
        return Response([
            {
                'id': o.id,
                'total_price': float(o.total_price),
                'items': [
                    {
                        'product_id': item.product.id,
                        'product_name': item.product.name,
                        'quantity': item.quantity,
                        'unit_price': float(item.product.price),
                        'total': float(item.product.price * item.quantity)
                    }
                    for item in o.items.all()
                ]
            }
            for o in orders
        ])
