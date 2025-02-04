from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index,detail,detail_update,master_img_index,master_csv,img_imp,chumon_imp,free


app_name="app1"
urlpatterns = [
    path('', index, name="index"),
    path('detail/<int:pk>/', detail, name="detail"),
    path('detail_update/', detail_update, name="detail_update"),
    path('master_img_index/', master_img_index, name="master_img_index"),
    path('master_csv/', master_csv, name="master_csv"),
    path('img_imp/', img_imp, name="img_imp"),
    path('chumon_imp/', chumon_imp, name="chumon_imp"),
    path('free/', free, name="free"),
]