from django.contrib import admin
from .models import Image,Master_all,Master_gsp,Master_shopify,Order_list,Order_detail
from django.contrib.admin import ModelAdmin

class A_image(ModelAdmin):
    model=Image
    list_display = ["id","title"]

class A_Master_all(ModelAdmin):
    model=Master_all
    list_display = ["master_id","name"]

class A_Master_gsp(ModelAdmin):
    model=Master_gsp
    list_display = ["unq_id","color","size","maker"]

class A_Master_shopify(ModelAdmin):
    model=Master_shopify
    list_display = ["unq_id","color","size"]

class A_Order_list(ModelAdmin):
    model=Order_list
    list_display = ["kubun","order_num"]

class A_Order_detail(ModelAdmin):
    model=Order_detail
    list_display = ["kubun","order_num"]


admin.site.register(Image, A_image)
admin.site.register(Master_all, A_Master_all)
admin.site.register(Master_gsp, A_Master_gsp)
admin.site.register(Master_shopify, A_Master_shopify)
admin.site.register(Order_list, A_Order_list)
admin.site.register(Order_detail, A_Order_detail)