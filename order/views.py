import json
import bcrypt
import jwt
import random

from django.views   import View
from django.http    import (
HttpResponse,
JsonResponse
)
from user.utils     import login_decorator

from user.models    import User
from product.models import (
Product,
Applying,
Color,
Image,
ImageCategory
)
from .models        import (
Order,
OrderStatus
)

class CartItemView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        if not Order.objects.filter(user_id=request.user.id, product_id=data['product_id'], order_status_id=1).exists():
            Order.objects.create(
                user_id         = request.user.id,
                product_id      = Product.objects.get(id=data['product_id']).id,
                order_status_id = OrderStatus.objects.get(name='pending').id,
                quantity        = data['quantity']
            )

            return JsonResponse({'message':'ADD_CARTITEM'},status=200)

        return JsonResponse({'message':'ALREADY_EXIST_ITEM'}, status=400)
    
    @login_decorator
    def get(self, request):
        try:
            cart = Order.objects.filter(user_id = request.user.id, order_status_id=1).prefetch_related('product')
            cart_list = [{
                "id"            : product.id,
                "product_id"    : product.product.id,
                "name"          : product.product.name,
                "color"         : product.product.color.name,
                "price"         : product.product.price,
                "product_image" : product.product.image_set.get(image_category_id=1).image_url,
                "quantity"      : product.quantity
            }for product in cart]

            return JsonResponse({'cart_list' : cart_list})

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def patch(self, rquest):
        data= json.loads(request.body)
        cart = Order.objects.filter(user_id = request.user.id, order_status_id=1).prefetch_related('product')
        cart_item = cart.get(id=data['cartitem_id'])
        if data['action'] == 'plus':
            cart_item.quantity += 1
        elif data['action'] == 'minus':
            cart_item.quantity -= 1
            
        cart_item.save(update_fields=['quantity'])
        cart_list = [{
            "id"            : product.id,
            "product_id"    : product.product.id,
            "name"          : product.product.name,
            "color"         : product.product.color.name,
            "price"         : product.product.price,
            "product_image" : product.product.image_set.get(image_category_id=1).image_url,
            "quantity"      : product.quantity
        }for product in cart]

        return JsonResponse({'cart_list':cart_list}, status=200)

    @login_decorator
    def delete(self, request):
        data = json.loads(request.body)
        cart_item = Order.objects.get(user_id = request.user.id, order_status_id=1, id=data['cartitem_id'])
        cart_item.delete()
        
        cart = Order.objects.filter(user_id=request.user.id, order_status_id=1).prefetch_related('product')
        cart_list = [{
            "id"            : product.id,
            "product_id"    : product.product.id,
            "name"          : product.product.name,
            "color"         : product.product.color.name,
            "price"         : product.product.price,
            "product_image" : product.product.image_set.get(image_category_id=1).image_url,
            "quantity"      : product.quantity
        }for product in cart]

        return JsonResponse({'cart_list':cart_list}, status=200)

class RecommendItemView(View):
    def get(self, request):
        PRODUCT_LIMIT  = 18
        product_list   = [i for i in Product.objects.all() if i.id < PRODUCT_LIMIT]
        recommend_list = [i for i in random.sample(product_list, 3)]
        data = [{
            "id"            : i.id,
            "name"          : i.name,
            "color"         : i.color.name,
            "price"         : i.price,
            "product_image" : i.image_set.get(image_category_id=1).image_url
        }for i in recommend_list]

        return JsonResponse({"data" : data})

class QuantityView(View):
    @login_decorator
    def get(self, request):
        cart               = Order.objects.filter(user_id = request.user.id, order_status_id = 1)
        item_quantity_list = [i.quantity for i in cart]
        total_quantity     = sum(item_quantity_list)

        return JsonResponse({"total_quantity":total_quantity})

