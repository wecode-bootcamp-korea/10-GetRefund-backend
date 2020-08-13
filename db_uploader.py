import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "get_refund.settings")
django.setup()

from product.models import (
    Product,
    Applying,
    Category,
    Color
)

CSV_PATH_PRODUCT = './get_super_fluid_product.csv'

with open(CSV_PATH_PRODUCT) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Product.objects.create(
            name = row[0],
            group = row[1],
            price = row[2],
            volume = row[3],
            description = row[4],
            note = row[5], 
            applying_id = Applying.objects.get(id = 1).id,
            category_id = Category.objects.get(id = 1).id,
            color_id = Color.objects.get(id = 1).id
        )


