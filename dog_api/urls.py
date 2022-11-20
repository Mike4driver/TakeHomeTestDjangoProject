from django.urls import path

from dog_api.views import dog_delete, dog_list, dog_show, populate, dog_image_pair_by_id

urlpatterns = [
    path('populate/', populate),
    path('list/', dog_list),
    path('show/', dog_show),
    path('show/<str:dog_id>/', dog_image_pair_by_id),
    path('delete/<str:dog_id>/',dog_delete)
]
