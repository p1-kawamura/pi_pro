from django.shortcuts import render,redirect
import csv
from .models import Image,Master_all,Master_gsp,Master_shopify,Order_list,Order_detail
from .forms import Image_form
import io
from django.http import JsonResponse
import json


def index(request):
    master_all=Master_all.objects.all()
    chumon_list=Order_list.objects.all()
    params={
        "master_all":master_all,
        "chumon_list":chumon_list,
    }
    return render(request,"app1/index.html",params)


# 注文詳細
def detail(request,pk):
    chumon=Order_list.objects.get(pk=pk)
    gara_list=list(Order_detail.objects.filter(kubun=chumon.kubun,order_num=chumon.order_num).values_list("gara",flat=True).order_by("gara").distinct())

    item_list=[]
    for i in gara_list:
        detail=Order_detail.objects.filter(kubun=chumon.kubun,order_num=chumon.order_num,gara=i)
        dic={}
        dic["gara"]=i
        dic["img"]=Image.objects.get(title=detail[0].print_img).image.url
        li=[]
        for i in detail:
            js_1=json.loads(i.print_point)
            for h in range(len(js_1)):
                js_2=json.loads(i.print_way)
                js_3=json.loads(i.print_size_width)
                js_4=json.loads(i.print_size_height)
                js_5=json.loads(i.print_color)

                li_s=[i.maker_hinmei,i.color,i.size,i.suryo,js_1[h],js_2[h],js_3[h],js_4[h],js_5[h],i.fukuro]
                li.append(li_s)
            
        dic["dtl"]=li
        item_list.append(dic)

    params={
        "chumon":chumon,
        "pk":pk,
        "item_list":item_list,
    }
    return render(request,"app1/detail.html",params)


# 注文内容変更
def detail_update(request):
    pk=request.POST.get("pk")
    od_li=Order_list.objects.get(id=pk)
    od_li.ship_name=request.POST.get("ship_name")
    od_li.ship_yubin=request.POST.get("ship_yubin")
    od_li.ship_pref=request.POST.get("ship_pref")
    od_li.ship_city=request.POST.get("ship_city")
    od_li.ship_adress1=request.POST.get("ship_adress1")
    od_li.ship_adress2=request.POST.get("ship_adress2")
    od_li.ship_tel=request.POST.get("ship_tel")
    od_li.ship_day=request.POST.get("ship_day")
    od_li.ship_time=request.POST.get("ship_time")
    od_li.save()
    d={}
    return JsonResponse(d)


# 注文CSV取込
def chumon_imp(request):
    master_name=request.POST["master_name"]
    h=0

    ok_oder_num=""
    ######### GSP ########
    if master_name=="GSP":
        data = io.TextIOWrapper(request.FILES['csv1'].file, encoding="cp932")
        csv_content = csv.reader(data)
        csv_list=list(csv_content)
        for i in csv_list:
            if h!=0:
                
                if Order_list.objects.filter(kubun=master_name,order_num=i[1]).count()==0:
                    ok_oder_num=i[1]

                    # order_list
                    Order_list.objects.create(
                        kubun=master_name,
                        order_num=i[1],
                        order_day=i[2],
                        order_mail=i[4],
                        order_name=i[5],
                        order_yubin=i[7],
                        order_pref=i[9],
                        order_city=i[10],
                        order_adress1=i[11],
                        order_adress2=i[12],
                        order_tel=i[13],
                        ship_name=i[15],
                        ship_yubin=i[17],
                        ship_pref=i[19],
                        ship_city=i[20],
                        ship_adress1=i[21],
                        ship_adress2=i[22],
                        ship_tel=i[23],
                        ship_day=i[29],
                        ship_time=i[30],
                        money=i[34],
                        bikou=i[40],
                    )

                # order_detail
                if i[1] == ok_oder_num:
                    try:
                        con=Master_gsp.objects.get(gsp_hinban=i[41],gsp_sku=i[44])
                        color=con.color
                        size=con.size
                        maker_name=con.maker
                        maker_sku=con.maker_sku
                        maker_hinban=con.maker_hinban
                        maker_hinmei=con.maker_hinmei
                        maker_color_code=con.color_code
                        maker_size_code=con.size_code
                        genka=con.price
                        gara=con.gara
                        print_point=con.print_point
                        print_way=con.print_way
                        print_img=con.print_img
                        print_size_width=con.print_size_width
                        print_size_height=con.print_size_height
                        print_color=con.print_color
                        fukuro=con.fukuro
                        
                    except:
                        color=""
                        size=""
                        maker_name=""
                        maker_sku=""
                        maker_hinban=""
                        maker_hinmei=""
                        maker_color_code=""
                        maker_size_code=""
                        genka=0
                        gara=""
                        print_point=""
                        print_way=""
                        print_img=""
                        print_size_width=""
                        print_size_height=""
                        print_color=""
                        fukuro=""

                    Order_detail.objects.create(
                        kubun=master_name,
                        order_num=i[1],
                        shouhin_code=i[41],
                        sku_code=i[42],
                        hinmei=i[43],
                        color=color,
                        size=size,
                        suryo=i[46],
                        tanka=i[47],
                        maker_name=maker_name,
                        maker_sku=maker_sku,
                        maker_hinban=maker_hinban,
                        maker_hinmei=maker_hinmei,
                        maker_color_code=maker_color_code,
                        maker_size_code=maker_size_code,
                        genka=genka,
                        gara=gara,
                        print_point=print_point,
                        print_way=print_way,
                        print_img=print_img,
                        print_size_width=print_size_width,
                        print_size_height=print_size_height,
                        print_color=print_color,
                        fukuro=fukuro
                    )

            h+=1

    ######### Shopify ########
    elif master_name=="Shopify":
        data = io.TextIOWrapper(request.FILES['csv1'].file, encoding="UTF-8")
        csv_content = csv.reader(data)
        csv_list=list(csv_content)
        for i in csv_list:
            if h!=0:

                if Order_list.objects.filter(kubun=master_name,order_num=i[0]).count()==0:
                    ok_oder_num=i[0]

                    # order_list
                    Order_list.objects.create(
                        kubun=master_name,
                        order_num=i[0],
                        order_day=i[15],
                        order_mail=i[1],
                        order_name=i[24],
                        order_yubin=i[30],
                        order_pref="",
                        order_city=i[29],
                        order_adress1=i[26],
                        order_adress2=i[27],
                        order_tel=i[33],
                        ship_name=i[34],
                        ship_yubin=i[40],
                        ship_pref="",
                        ship_city=i[39],
                        ship_adress1=i[36],
                        ship_adress2=i[37],
                        ship_tel=i[43],
                        ship_day="",
                        ship_time="",
                        money=i[11],
                        bikou=i[44],
                    )

                # order_detail
                if i[0] == ok_oder_num:
                    try:
                        hinmei=i[17].split(" - ")[0]
                        color=i[17].split(" - ")[1].split(" / ")[0]
                        size=i[17].split(" - ")[1].split(" / ")[1]
                        con=Master_shopify.objects.get(hinmei=hinmei,color=color,size=size)
                        img_url=con.img_url
                        maker_name=con.maker
                        maker_sku=con.maker_sku
                        maker_hinban=con.maker_hinban
                        maker_hinmei=con.maker_hinmei
                        maker_color_code=con.color_code
                        maker_size_code=con.size_code
                        genka=con.price
                    except:
                        color=""
                        size=""
                        img_url=""
                        maker_name=""
                        maker_sku=""
                        maker_hinban=""
                        maker_hinmei=""
                        maker_color_code=""
                        maker_size_code=""
                        genka=0

                    Order_detail.objects.create(
                        kubun=master_name,
                        order_num=i[0],
                        shouhin_code=i[17],
                        sku_code=i[20],
                        hinmei=i[17],
                        color=color,
                        size=size,
                        suryo=i[16],
                        tanka=i[18],
                        img_url=img_url,
                        maker_name=maker_name,
                        maker_sku=maker_sku,
                        maker_hinban=maker_hinban,
                        maker_hinmei=maker_hinmei,
                        maker_color_code=maker_color_code,
                        maker_size_code=maker_size_code,
                        genka=genka,
                    )

            h+=1

    return redirect("app1:index")


# マスタ、画像取り込みページ
def master_img_index(request):
    image_all=Image.objects.all()
    image_form=Image_form()
    master_all=Master_all.objects.all()
    params={
        "image_all":image_all,
        "image_form":image_form,
        "master_all":master_all,
    }
    return render(request,"app1/master_img_index.html",params)


# 画像取込
def img_imp(request):
    form=Image_form(request.POST, request.FILES)
    form.save()
    return redirect("app1:master_img_index")


# マスタ取込
def master_csv(request):

    master_name=request.POST["master_name"]
    data = io.TextIOWrapper(request.FILES['csv1'].file, encoding="cp932")
    csv_content = csv.reader(data)
    csv_list=list(csv_content)
    h=0

    if master_name=="GSP":
        for i in csv_list:
            if h!=0:
                Master_gsp.objects.update_or_create(
                unq_id=i[0],
                defaults={
                    "unq_id":i[0],
                    "gsp_hinban":i[1],
                    "gsp_sku":i[2],
                    "color":i[3],
                    "size":i[4],
                    "price":i[5],
                    "maker":i[6],
                    "maker_sku":i[7],
                    "maker_hinban":i[8],
                    "maker_hinmei":i[9],
                    "color_code":i[10],
                    "size_code":i[11],
                    "gara":i[12],
                    "print_point":i[13],
                    "print_way":i[14],
                    "print_img":i[15],
                    "print_size_width":i[16],
                    "print_size_height":i[17],
                    "print_color":i[18],
                    "fukuro":i[19],
                    }
                )
            h+=1

    elif master_name=="Shopify":
        for i in csv_list:
            if h!=0:
                Master_shopify.objects.update_or_create(
                unq_id=i[0],
                defaults={
                    "unq_id":i[0],
                    "hinmei":i[1],
                    "color":i[2],
                    "size":i[3],
                    "sku":i[4],
                    "img_url":i[5],
                    "price":i[6],
                    "maker":i[7],
                    "maker_sku":i[8],
                    "maker_hinban":i[9],
                    "maker_hinmei":i[10],
                    "color_code":i[11],
                    "size_code":i[12],
                    }
                )
            h+=1

    return redirect("app1:master_img_index")



# その都度、自由に使う用
def free(request):
    Master_shopify.objects.all().delete()
    return redirect("app1:index")

