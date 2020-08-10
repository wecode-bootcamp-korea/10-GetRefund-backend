import json
import random
import bcrypt
import jwt

from django.views import View
from django.http import (
    HttpResponse,
    JsonResponse
)

from my_settings import(
    SECRET_KEY,
    ALGORITHM
)

from user.models import User
from .models     import (
    Product,
    Applying,
    Category,
    Color,
    Image,
    ImageCategory,
    DetailInfo
)

class ProductDetailView(View):
    def get(self, request, product_id):
        PRODUCT_LIMIT = 17
        if product_id < PRODUCT_LIMIT:
            product = Product.objects.select_related("color").prefetch_related("image_set").get(id = product_id)
            product_color  = Product.objects.select_related("color").filter(group = product.group)
            data = {
                "id"          : product.id,
                "name"        : product.name,
                "group"       : product.group,
                "price"       : product.price,
                "volume"      : product.volume,
                "description" : product.description,
                "note"        : product.note,
                "color"       : {  
                    "name" : product.color.name
                },
                "color_group" :[{
                    "product_id" : i.id,
                    "name"    : i.color.name,
                    "hexcode" : i.color.hexcode
                }for i in product_color],
                "product_image" : product.image_set.get(image_category_id=1).image_url,
                "detail_image"  : [i.image_url for i in product.image_set.filter(image_category_id=3)],
            }

            return JsonResponse({"data" : data})

        else:
            gift_card = Product.objects.prefetch_related("image_set").get(id=product_id)
            data = {
                "id"            : gift_card.id,
                "name"          : gift_card.name,
                "group"         : gift_card.group,
                "price"         : gift_card.price,
                "volume"        : gift_card.volume,
                "description"   : gift_card.description,
                "product_image" : gift_card.image_set.get(image_category_id=1).image_url,
                "detail_image"  : gift_card.image_set.get(image_category_id=3).image_url
            }

            return JsonResponse({"data" : data})

class PairWithView(View):
    def get(self, request, product_id):
        product_applying_id = Product.objects.get(id = product_id).applying_id
        PRODUCT_LIMIT = 18
        product_list = [i for i in Product.objects.all() if i.id < PRODUCT_LIMIT]
        product_filter = [i for i in product_list if i.applying_id != product_applying_id]
        pair_list = [i for i in random.sample(product_filter, 2)]
        data = [{
            "id"            : i.id,
            "name"          : i.name,
            "group"         : i.group,
            "price"         : i.price,
            "product_image" : i.image_set.get(image_category_id=1).image_url
        }for i in pair_list]

        return JsonResponse({"data" : data})

class DetailInfoView(View):
    def get(self, request, product_id):
        try:
            detail_info = DetailInfo.objects.select_related("product").get(id=product_id)
            
            data = {
                "text1": detail_info.text1,
                "message1": detail_info.message1,
                "image_url1": detail_info.image_url1,
                "text2": detail_info.text2,
                "message2": detail_info.message2,
                "image_url2" : detail_info.image_url2
            }
            
            return JsonResponse({"data" : data})
        
        except DetailInfo.DoesNotExist:
            return HttpResponse(status=404)

