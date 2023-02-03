from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('listings/', views.products, name='products'),
    path('listing_bydate/<str:start_date>/<str:end_date>/', views.search_products, name='datesearch'),
    path('listing_bydate/<str:start_date>/<str:end_date>/<str:product_name>/', views.search_listing, name='dateproducts'),
    path('store/', views.store, name='store'),
    path('listings/<str:product_name>/', views.listing, name='listing'),
    path('listings/<str:product_name>/<str:lease_date>/<str:clear_date>/', views.customerform, name='customerform'),
    path('listings/<str:product_name>/<str:lease_date>/<str:clear_date>/<str:customer>/<int:price>/', views.confirm, name="confirmation_page")
]
