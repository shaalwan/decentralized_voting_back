from django.urls import path

from .views import *

urlpatterns = [
    path('',cropter.as_view(),name='upload'),
    path('<str:filename>',cropter.as_view(),name='upload'),
    # path('upload', views.upload, name='upload'),
    # path('download/<path:filename>',views.download,name='download'),
]   