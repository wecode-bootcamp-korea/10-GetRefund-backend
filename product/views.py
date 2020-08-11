import json
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

from .models import (
    Product,
    Category,
    Applying,
    Color,
    Image,
    ImageCategory,
    DetailInfo
)

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

