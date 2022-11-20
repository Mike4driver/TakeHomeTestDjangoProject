from django.urls import path
from incrementer.views import key_list, key_create, key_inc, key

urlpatterns = [
    path('', key_create),
    path('list/', key_list),
    path('inc/<str:key>', key_inc),
    path('key/<str:key>/', key),

]