from django.contrib import admin
from django.urls import path, include
from bincom_app import views
from django.conf import settings

urlpatterns = [
    path('', views.p1, name='p1'),
    path("results", views.results, name="results"),
    path("submit_result", views.submit_result, name="submit_result"),
    path("page2", views.page2, name="page2"),

]
