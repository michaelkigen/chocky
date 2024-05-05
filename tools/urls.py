from django.urls import path

from .views import (
    CategoryListView,CategoryDetailView
    ,ToolsListView , ToolsDetailView 
    , FunctionalityDetailView ,FunctionalityListView
    , KitsListView ,KitsDetailView 
    ,BrandListView ,BrandDetailView
    )
urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('category/<uuid:pk>', CategoryDetailView.as_view()),
    path('tool/', ToolsListView.as_view()),
    path('tool/<uuid:pk>', ToolsDetailView.as_view()),
    path('functionality/', FunctionalityListView.as_view()),
    path('functionality/<uuid:pk>', FunctionalityDetailView.as_view()),
    path('kits/', KitsListView.as_view()),
    path('kits/<uuid:pk>', KitsDetailView.as_view()),
    path('brand/', BrandListView.as_view()),
    path('brand/<uuid:pk>', BrandDetailView.as_view()),
]
