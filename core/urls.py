from django.urls import path
from . import views
urlpatterns = [
    path("landing/", views.landing_view, name="landing"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("search/", views.search_view, name="search"),
]
