from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index,detail,detail_update,master_img_index,master_csv,img_imp,chumon_imp,make_shijisho,download_shijisho, \
                    make_ship,download_ship,free


app_name="app1"
urlpatterns = [
    path('', index, name="index"),
    path('detail/<int:pk>/', detail, name="detail"),
    path('detail_update/', detail_update, name="detail_update"),
    path('master_img_index/', master_img_index, name="master_img_index"),
    path('master_csv/', master_csv, name="master_csv"),
    path('img_imp/', img_imp, name="img_imp"),
    path('chumon_imp/', chumon_imp, name="chumon_imp"),
    path('make_shijisho/', make_shijisho, name="make_shijisho"),
    path('make_ship/', make_ship, name="make_ship"),
    path('download_shijisho/', download_shijisho, name="download_shijisho"),
    path('download_ship/', download_ship, name="download_ship"),
    path('free/', free, name="free"),
]