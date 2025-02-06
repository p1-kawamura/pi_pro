from django.shortcuts import render,redirect
import csv
from .models import Image,Master_all,Master_gsp,Master_shopify,Order_list,Order_detail
from .forms import Image_form
import io
from django.http import JsonResponse
import json
from django.db.models import Max,Min
import datetime
from django.http import HttpResponse
import urllib.parse


def index(request):
    if "kubun" not in request.session:
        request.session["kubun"]=""
    if "order_num" not in request.session:
        request.session["order_num"]=""
    if "gara" not in request.session:
        request.session["gara"]=""
    if "csv_list" not in request.session:
        request.session["csv_list"]=[]

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
    if chumon.kubun=="GSP":
        sender=Master_gsp.objects.filter(gara=gara_list[0])[0]

    item_list=[]
    for i in gara_list:
        detail=Order_detail.objects.filter(kubun=chumon.kubun,order_num=chumon.order_num,gara=i)
        dic={}
        dic["gara"]=i
        dic["img"]=Image.objects.get(title=detail[0].print_img).image.url
        li=[]
        for i in detail:
            k=0
            js_1=json.loads(i.print_point)
            for h in range(len(js_1)):
                js_2=json.loads(i.print_way)
                js_3=json.loads(i.print_size_width)
                js_4=json.loads(i.print_size_height)
                js_5=json.loads(i.print_color)

                li_s=[k,i.maker_hinban,i.maker_hinmei,i.color,i.size,i.suryo,js_1[h],js_2[h],js_3[h],js_4[h],js_5[h],i.fukuro]
                li.append(li_s)
                k+=1
            
        dic["dtl"]=li
        dic["row_all"]=detail.count() * len(js_1)
        dic["row_point"]=len(js_1)

        gara_min=Order_detail.objects.filter(gara=i).aggregate(Min("gara_day"))["gara_day__min"]
        if  gara_min is None:
            dic["gara_first"]=datetime.date.today().strftime("%Y-%m-%d")
        else:
            dic["gara_first"]=gara_min

        gara_max=Order_detail.objects.filter(gara=i).aggregate(Max("gara_day"))["gara_day__max"]
        if  gara_max is None:
            dic["gara_last"]=""
        else:
            dic["gara_last"]=gara_max

        dic["moto_hinban"]=detail[0].shouhin_code
        dic["moto_hinmei"]=detail[0].hinmei

        item_list.append(dic)

    params={
        "chumon":chumon,
        "pk":pk,
        "item_list":item_list,
        "sender":sender,
    }
    return render(request,"app1/detail.html",params)


# 注文内容変更
def detail_update(request):
    pk=request.POST.get("pk")
    od_li=Order_list.objects.get(id=pk)
    od_li.ship_com=request.POST.get("ship_com")
    od_li.ship_name=request.POST.get("ship_name")
    od_li.ship_yubin=request.POST.get("ship_yubin")
    od_li.ship_pref=request.POST.get("ship_pref")
    od_li.ship_city=request.POST.get("ship_city")
    od_li.ship_adress1=request.POST.get("ship_adress1")
    od_li.ship_adress2=request.POST.get("ship_adress2")
    od_li.ship_tel=request.POST.get("ship_tel")
    od_li.ship_limit=request.POST.get("ship_limit")
    od_li.ship_day=request.POST.get("ship_day")
    od_li.ship_time=request.POST.get("ship_time")
    od_li.save()
    d={}
    return JsonResponse(d)


# 指示書CSV作成
def make_shijisho(request):
    chumon_kubun=request.POST.get("chumon_kubun")
    chumon_order_num=request.POST.get("chumon_order_num")
    gara=request.POST.get("gara")
    gara_first=request.POST.get("gara_first")
    gara_last=request.POST.get("gara_last")
    tantou=request.POST.get("tantou")
    seisaku=request.POST.get("seisaku")
    factory=request.POST.get("factory")
    factory_day=request.POST.get("factory_day")
    body_day=request.POST.get("body_day")
    bikou=request.POST.get("bikou")

    shiji_csv=[]
    a=["注文番号","氏名","配送先会社","配送先氏名","配送先郵便番号","配送先都道府県","配送先市町村","配送先番地","配送先ビル名","配送先電話番号",
       "送り主郵便番号","送り主都道府県","送り主市区町村","送り主番地建物","送り主会社名","送り主名前","送り主電話番号","納品期限","納品指定日","時間指定",
       "品番","品名","カラー","サイズ","数量","柄名","初回日","前回日","加工位置","加工方法","画像","画像URL","プリントサイズ_左右","プリントサイズ_天地",
       "プリント色（２次元配列）","袋詰め","加工場","加工場発送日","営業担当","制作担当","ボディ入荷日","備考"]
    shiji_csv.append(a)

    ins_li=Order_list.objects.get(kubun=chumon_kubun,order_num=chumon_order_num)
    ins_det=Order_detail.objects.filter(kubun=chumon_kubun,order_num=chumon_order_num,gara=gara)
    if chumon_kubun =="GSP":
        ins_mas=Master_gsp.objects.filter(gara=gara)[0]

    for i in ins_det:

        # Order_detail
        i.shi_gara_first=gara_first
        i.shi_gara_last=gara_last
        i.shi_factory=factory
        i.shi_factory_day=factory_day
        i.shi_tantou=tantou
        i.shi_seisaku=seisaku
        i.body_day=body_day
        i.shi_bikou=bikou
        i.gara_day=datetime.date.today().strftime("%Y-%m-%d")
        if i.img_url == None or i.img_url=="":
            i.img_url=Image.objects.get(title=i.print_img).image.url
        i.save()

        # CSV作成
        a=[
            chumon_kubun + "_" + str(chumon_order_num), #注文番号
            ins_li.order_name, #氏名
            ins_li.ship_com, #配送先会社
            ins_li.ship_name, #配送先氏名
            ins_li.ship_yubin, #配送先郵便番号
            ins_li.ship_pref, #配送先都道府県
            ins_li.ship_city, #配送先市町村
            ins_li.ship_adress1, #配送先番地
            ins_li.ship_adress2, #配送先ビル名
            ins_li.ship_tel, #配送先電話番号
            ins_mas.sender_yubin, #送り主郵便番号
            ins_mas.sender_pref, #送り主都道府県
            ins_mas.sender_city, #送り主市区町村
            ins_mas.sender_adress1, #送り主番地建物
            ins_mas.sender_com, #送り主会社名
            ins_mas.sender_name, #送り主名前
            ins_mas.sender_tel, #送り主電話番号
            ins_li.ship_limit, #納品期限
            ins_li.ship_day, #納品指定日
            ins_li.ship_time, #時間指定
            i.maker_hinban, #品番
            i.maker_hinmei, #品名
            i.color, #カラー
            i.size, #サイズ
            i.suryo, #数量
            gara, #柄名
            gara_first, #初回日
            gara_last, #前回日
            i.print_point, #加工位置
            i.print_way, #加工方法
            ins_mas.print_img, #画像
            i.img_url, #画像URL
            i.print_size_width, #プリントサイズ_左右
            i.print_size_height, #プリントサイズ_天地
            i.print_color, #プリント色（２次元配列）
            i.fukuro, #袋詰め
            factory, #加工場
            factory_day, #加工場発送日
            tantou, #営業担当
            seisaku, #制作担当
            body_day, #ボディ入荷日
            bikou, #備考
        ]
        shiji_csv.append(a)

    request.session["gara"]=gara
    request.session["kubun"]=chumon_kubun
    request.session["order_num"]=chumon_order_num
    request.session["csv_list"]=shiji_csv
    d={}
    return JsonResponse(d)


# 指示書CSVダウンロード
def download_shijisho(request):
    kubun=request.session["kubun"]
    order_num=request.session["order_num"]
    gara=request.session["gara"]
    shiji_csv=request.session["csv_list"]
    now=datetime.datetime.now()
    filename=urllib.parse.quote("指示書_" + kubun + "_" + str(order_num) +  "_" + gara +"_" + format(now,"%Y%m%d%H%M%S") +".csv")
    response = HttpResponse(content_type='text/csv; charset=CP932')
    response['Content-Disposition'] =  "attachment;  filename='{}'; filename*=UTF-8''{}".format(filename, filename)
    writer = csv.writer(response)
    for line in shiji_csv:
        writer.writerow(line)
    return response


# 出荷CSV作成
def make_ship(request):
    chumon_kubun=request.POST.get("chumon_kubun")
    chumon_order_num=request.POST.get("chumon_order_num")
    gara=request.POST.get("gara")
    tantou=request.POST.get("tantou")
    factory=request.POST.get("factory")
    factory_day=request.POST.get("factory_day")

    ship_csv=[]
    a=["外部サイト名","受注番号","営業担当","送り先郵便番号","送り先都道府県","送り先市区町村","送り先番地建物","送り先会社名","送り先名前","送り先電話番号",
       "送り主郵便番号","送り主都道府県","送り主市区町村","送り主番地建物","送り主会社名","送り主名前","送り主電話番号","送り状品名","柄名","加工場",
       "出荷日","日付指定","納品期限日","時間指定","代引金額","出荷表紙備考"]
    ship_csv.append(a)

    ins_li=Order_list.objects.get(kubun=chumon_kubun,order_num=chumon_order_num)
    if chumon_kubun =="GSP":
        ins_mas=Master_gsp.objects.filter(gara=gara)[0]

    a=[
        "Pi-pro", #外部サイト名
        chumon_kubun + "_" + str(chumon_order_num), #受注番号
        tantou, #営業担当
        ins_li.ship_yubin.replace("-",""), #送り先郵便番号
        ins_li.ship_pref, #送り先都道府県
        ins_li.ship_city, #送り先市区町村
        ins_li.ship_adress1 + ins_li.ship_adress2, #送り先番地建物
        ins_li.ship_com, #送り先会社名
        ins_li.ship_name, #送り先名前
        ins_li.ship_tel.replace("-",""), #送り先電話番号
        ins_mas.sender_yubin.replace("-",""), #送り主郵便番号
        ins_mas.sender_pref, #送り主都道府県
        ins_mas.sender_city, #送り主市区町村
        ins_mas.sender_adress1, #送り主番地建物
        ins_mas.sender_com, #送り主会社名
        ins_mas.sender_name, #送り主名前
        ins_mas.sender_tel.replace("-",""), #送り主電話番号
        "", #送り状品名
        gara, #柄名
        factory, #加工場
        factory_day, #出荷日
        ins_li.ship_day, #日付指定
        "", #納品期限日
        ins_li.ship_time, #時間指定
        "", #代引金額
        "" #出荷表紙備考
    ]
    ship_csv.append(a)

    request.session["gara"]=gara
    request.session["kubun"]=chumon_kubun
    request.session["order_num"]=chumon_order_num
    request.session["csv_list"]=ship_csv
    d={}
    return JsonResponse(d)


# 出荷CSVダウンロード
def download_ship(request):
    kubun=request.session["kubun"]
    order_num=request.session["order_num"]
    gara=request.session["gara"]
    ship_csv=request.session["csv_list"]
    now=datetime.datetime.now()
    filename=urllib.parse.quote("出荷用_" + kubun + "_" + str(order_num) +  "_" + gara +"_" + format(now,"%Y%m%d%H%M%S") +".csv")
    response = HttpResponse(content_type='text/csv; charset=CP932')
    response['Content-Disposition'] =  "attachment;  filename='{}'; filename*=UTF-8''{}".format(filename, filename)
    writer = csv.writer(response)
    for line in ship_csv:
        writer.writerow(line)
    return response


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
                    "sender_yubin":i[20],
                    "sender_pref":i[21],
                    "sender_city":i[22],
                    "sender_adress1":i[23],
                    "sender_com":i[24],
                    "sender_name":i[25],
                    "sender_tel":i[26],
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

