from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Public Pages
    path('', views.home, name="home"),
    path('gallery/', views.gallery, name="gallery"),
    path('artists/', views.artists, name="artists"),
    path('studio/', views.studio_info, name="studio"),

    # 🔐 Auth
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),

    # 🔒 Protected Features
    path('review/', views.add_review, name="review"),
    path('book/', views.book_tattoo, name="book"),
    path('slots/', views.available_slots, name='slots'),
    path('book-slot/<int:slot_id>/', views.book_slot, name='book_slot'),

    # 🔥 NEW
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]