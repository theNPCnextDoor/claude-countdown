from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [path("solve/", views.solve_view)]
