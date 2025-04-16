from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from store.services.product_services import create_product, get_product, list_products


class CreateProductView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'price', 'stock'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                'stock': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={
            200: openapi.Response(
                description="Product created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'name': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request):
        data = request.data
        product = create_product(**data)
        return Response({'id': product.id, 'name': product.name})


class GetProductView(APIView):
    @swagger_auto_schema(
        operation_description="Get product by ID",
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_PATH, description="Product ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(description="Product details"),
            404: openapi.Response(description="Product not found")
        }
    )
    def get(self, request, product_id):
        product = get_product(product_id)
        if not product:
            return Response({'error': 'Product not found'}, status=404)
        return Response({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'stock': product.stock
        })


class ListProductsView(APIView):
    @swagger_auto_schema(
        operation_description="List all products with optional filters",
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
        ],
        responses={200: openapi.Response(description="List of products")}
    )
    def get(self, request):
        query = request.GET.get('q')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        products = list_products(query, min_price, max_price)
        return Response([
            {'id': p.id, 'name': p.name, 'price': float(p.price)} for p in products
        ])
