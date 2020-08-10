import json
import bcrypt
import jwt

from django.views import View
from django.http  import (
    HttpResponse,
    JsonResponse
)
from user.utils     import login_decorator

from user.models    import User
from product.models import (
Product,
Color,
Image,
ImageCategory
)
from .models         import (
Order,
OrderStatus
)

class CartItemView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        if not Order.objects.filter(user_id=request.user.id, product_id=data['product_id']).exists():
            Order.objects.create(
                user_id = request.user.id,
                product_id = Product.objects.get(id=data['product_id']).id,
                order_status_id = OrderStatus.objects.get(name='pending').id,
                quantity = data['quantity']
            ).save

            return JsonResponse({'message':'ADD_CARTITEM'},status=200)

        return JsonResponse({'message':'ALREADY_EXIST_ITEM'}, status=400)
    
    @login_decorator
    def get(self, request):
        try:
            cart_item = Order.objects.filter(user_id = request.user.id, order_status_id=1).prefetch_related('product')
            cart_list = [{
                "id" : product.id,
                "product_id" : product.product.id,
                "name" : product.product.name,
                "color" : product.product.color.name,
                "price" : product.product.price,
                "product_image" : product.product.image_set.get(image_category_id=1).image_url,
                "quantity" : product.quantity
            }for product in cart_item]

            return JsonResponse({'cart_list' : cart_list})

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def patch(self, request):
        data = json.loads(request.body)
        cart_item = Order.objects.get(user_id = request.user.id, order_status_id=1, product_id=data["product_id"])
        quantity = cart_item.quantity

        if data['action'] == 'plus':
            quantity += 1
            print(quantity)
            cart_item.save()
        elif data['action'] == 'minus':
            quantity -= 1
            print(quantity)
            cart_item.save()
            
        print(cart_item.quantity)

        return JsonResponse({'message':'UPDATE_QUANTITY'}, status=200)
        
    @login_decorator
    def delete(self, request):
        data = json.loads(request.body)
        cart_item = Order.objects.get(user_id = request.user.id, id = data['cartitem_id'])
        cart_item.delete()
        
        return JsonResponse({'message':'DELETE_CARTITEM'}, status=200)

