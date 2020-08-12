import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "get_refund.settings")
django.setup()

from product.models import (
    Product,
    DetailInfo
)

CSV_PATH_DETAILINFO = './detail_page_final.csv'

with open(CSV_PATH_DETAILINFO) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        print(row)
        DetailInfo.objects.create(
            text1 = row[0],
            message1 = row[1],
            image_url1 = row[2],
            text2 = row[3],
            message2 = row[4],
            image_url2 = row[5],
            product_id = row[6]
        )
