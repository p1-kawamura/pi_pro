from django.db import models

class Image(models.Model):
    title=models.CharField("タイトル",max_length=255)
    image=models.ImageField("イメージ図",upload_to="image",blank=True,null=True)
    create_day=models.DateTimeField("作成日",auto_now=True)

    def __str__(self):
        return self.title


class Master_all(models.Model):
    master_id=models.AutoField(primary_key=True)
    name=models.CharField("クライアント名",max_length=255,blank=True,null=True)

    def __str__(self):
        return self.name


class Master_gsp(models.Model):
    unq_id=models.CharField("UNQ_ID",max_length=255)
    gsp_hinban=models.CharField("GSP_商品コード",max_length=255,blank=True,null=True)
    gsp_sku=models.CharField("GSP_SKUコード",max_length=255,blank=True,null=True)
    color=models.CharField("カラー",max_length=255,blank=True,null=True)
    size=models.CharField("サイズ",max_length=255,blank=True,null=True)
    price=models.IntegerField("原価",default=0,blank=True,null=True)
    maker=models.CharField("メーカー",max_length=255,blank=True,null=True)
    maker_sku=models.CharField("メーカー_SKU",max_length=255,blank=True,null=True)
    maker_hinban=models.CharField("品番",max_length=255,blank=True,null=True)
    maker_hinmei=models.CharField("品名",max_length=255,blank=True,null=True)
    color_code=models.CharField("カラーコード",max_length=255,blank=True,null=True)
    size_code=models.CharField("サイズコード",max_length=255,blank=True,null=True)
    gara=models.CharField("柄名",max_length=255,blank=True,null=True)
    print_point=models.CharField("加工位置",max_length=255,blank=True,null=True)
    print_way=models.CharField("加工方法",max_length=255,blank=True,null=True)
    print_img=models.CharField("プリント画像",max_length=255,blank=True,null=True)
    print_size_width=models.CharField("プリントサイズ_左右",max_length=255,blank=True,null=True)
    print_size_height=models.CharField("プリントサイズ_天地",max_length=255,blank=True,null=True)
    print_color=models.CharField("プリント色",max_length=255,blank=True,null=True)
    fukuro=models.CharField("袋詰め",max_length=255,blank=True,null=True)
    sender_yubin=models.CharField("送り主_郵便番号",max_length=255,blank=True,null=True)
    sender_pref=models.CharField("送り主_都道府県",max_length=255,blank=True,null=True)
    sender_city=models.CharField("送り主_市区町村",max_length=255,blank=True,null=True)
    sender_adress1=models.CharField("送り主_番地",max_length=255,blank=True,null=True)
    sender_com=models.CharField("送り主_会社",max_length=255,blank=True,null=True)
    sender_name=models.CharField("送り主_氏名",max_length=255,blank=True,null=True)
    sender_tel=models.CharField("送り主_電話番号",max_length=255,blank=True,null=True)


    def __str__(self):
        return self.unq_id
    

class Master_shopify(models.Model):
    unq_id=models.CharField("UNQ_ID",max_length=255)
    hinmei=models.CharField("商品名",max_length=255,blank=True,null=True)
    color=models.CharField("カラー",max_length=255,blank=True,null=True)
    size=models.CharField("サイズ",max_length=255,blank=True,null=True)
    sku=models.CharField("SKU",max_length=255,blank=True,null=True)
    img_url=models.CharField("画像URL",max_length=255,blank=True,null=True)
    price=models.IntegerField("原価",default=0,blank=True,null=True)
    maker=models.CharField("メーカー",max_length=255,blank=True,null=True)
    maker_sku=models.CharField("メーカー_SKU",max_length=255,blank=True,null=True)
    maker_hinban=models.CharField("品番",max_length=255,blank=True,null=True)
    maker_hinmei=models.CharField("品名",max_length=255,blank=True,null=True)
    color_code=models.CharField("カラーコード",max_length=255,blank=True,null=True)
    size_code=models.CharField("サイズコード",max_length=255,blank=True,null=True)

    def __str__(self):
        return self.unq_id
    

class Order_list(models.Model):
    kubun=models.CharField("販売区分",max_length=255)
    order_num=models.CharField("注文番号",max_length=255,blank=True,null=True)
    order_day=models.CharField("注文日時",max_length=255,blank=True,null=True)
    order_mail=models.CharField("Eメール",max_length=255,blank=True,null=True)
    order_com=models.CharField("会社",max_length=255,blank=True,null=True)
    order_name=models.CharField("氏名",max_length=255,blank=True,null=True)
    order_yubin=models.CharField("郵便番号",max_length=255,blank=True,null=True)
    order_pref=models.CharField("都道府県",max_length=255,blank=True,null=True)
    order_city=models.CharField("市区町村",max_length=255,blank=True,null=True)
    order_adress1=models.CharField("番地",max_length=255,blank=True,null=True)
    order_adress2=models.CharField("ビル名",max_length=255,blank=True,null=True)
    order_tel=models.CharField("電話番号",max_length=255,blank=True,null=True)
    ship_com=models.CharField("配送先_会社名",max_length=255,blank=True,null=True)
    ship_name=models.CharField("配送先_氏名",max_length=255,blank=True,null=True)
    ship_yubin=models.CharField("配送先_郵便番号",max_length=255,blank=True,null=True)
    ship_pref=models.CharField("配送先_都道府県",max_length=255,blank=True,null=True)
    ship_city=models.CharField("配送先_市区町村",max_length=255,blank=True,null=True)
    ship_adress1=models.CharField("配送先_番地",max_length=255,blank=True,null=True)
    ship_adress2=models.CharField("配送先_ビル名",max_length=255,blank=True,null=True)
    ship_tel=models.CharField("配送先_電話番号",max_length=255,blank=True,null=True)
    ship_limit=models.CharField("納品期限",max_length=255,blank=True,null=True)
    ship_day=models.CharField("納品指定日",max_length=255,blank=True,null=True)
    ship_time=models.CharField("時間指定",max_length=255,blank=True,null=True)
    money=models.IntegerField("合計金額",blank=True,null=True)
    bikou=models.CharField("備考",max_length=255,blank=True,null=True)

    def __str__(self):
        return self.order_num
    

class Order_detail(models.Model):
    kubun=models.CharField("販売区分",max_length=255)
    order_num=models.CharField("注文番号",max_length=255,blank=True,null=True)
    shouhin_code=models.CharField("商品コード",max_length=255,blank=True,null=True)
    sku_code=models.CharField("SKUコード",max_length=255,blank=True,null=True)
    hinmei=models.CharField("商品名",max_length=255,blank=True,null=True)
    color=models.CharField("カラー",max_length=255,blank=True,null=True)
    size=models.CharField("サイズ",max_length=255,blank=True,null=True)
    suryo=models.IntegerField("数量",blank=True,null=True)
    tanka=models.IntegerField("単価",blank=True,null=True)
    img_url=models.CharField("画像URL",max_length=255,blank=True,null=True)
    maker_name=models.CharField("メーカー名",max_length=255,blank=True,null=True)
    maker_sku=models.CharField("メーカー_SKU",max_length=255,blank=True,null=True)
    maker_hinban=models.CharField("メーカー_品番",max_length=255,blank=True,null=True)
    maker_hinmei=models.CharField("メーカー_品名",max_length=255,blank=True,null=True)
    maker_color_code=models.CharField("メーカー_カラーコード",max_length=255,blank=True,null=True)
    maker_size_code=models.CharField("メーカー_サイズコード",max_length=255,blank=True,null=True)
    genka=models.IntegerField("原価",blank=True,null=True)
    body_day=models.CharField("入荷予定日",max_length=255,blank=True,null=True)
    gara=models.CharField("柄名",max_length=255,blank=True,null=True)
    gara_day=models.CharField("柄名_使用日",max_length=255,blank=True,null=True)
    print_point=models.CharField("加工位置",max_length=255,blank=True,null=True)
    print_way=models.CharField("加工方法",max_length=255,blank=True,null=True)
    print_img=models.CharField("プリント画像",max_length=255,blank=True,null=True)
    print_size_width=models.CharField("プリントサイズ_左右",max_length=255,blank=True,null=True)
    print_size_height=models.CharField("プリントサイズ_天地",max_length=255,blank=True,null=True)
    print_color=models.CharField("プリント色",max_length=255,blank=True,null=True)
    fukuro=models.CharField("袋詰め",max_length=255,blank=True,null=True)

    def __str__(self):
        return self.order_num