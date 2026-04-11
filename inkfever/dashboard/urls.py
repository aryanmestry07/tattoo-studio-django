from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name="dashboard_home"),
    path('artists/', views.manage_artists, name="manage_artists"),
    path('tattoos/', views.manage_tattoos, name="manage_tattoos"),
    path('bookings/', views.manage_bookings, name="manage_bookings"),

    path('artist/delete/<int:id>/', views.delete_artist, name="delete_artist"),
    path('artist/edit/<int:id>/', views.edit_artist, name="edit_artist"),

    path('logout/', views.admin_logout, name="admin_logout"),
    path('generate-slots/', views.generate_slots, name='generate_slots'),

    # NEW (STATUS CONTROL)
    path('booking/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
]