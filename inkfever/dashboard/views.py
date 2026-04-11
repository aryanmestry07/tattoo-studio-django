from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from studio.models import Artist, Tattoo, Booking, Category, TimeSlot
from datetime import datetime, timedelta, time


# 🔒 Admin-only decorator
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return redirect("/admin-login/")
    return wrapper


# 🏠 Dashboard Home (UPDATED 🔥)
@admin_required
def dashboard_home(request):
    artists_count = Artist.objects.count()
    tattoos_count = Tattoo.objects.count()
    bookings_count = Booking.objects.count()

    # 🔥 Recent bookings
    recent_bookings = Booking.objects.select_related(
        'slot', 'artist', 'user'
    ).order_by('-id')[:5]

    return render(request, "dashboard/home.html", {
        "artists_count": artists_count,
        "tattoos_count": tattoos_count,
        "bookings_count": bookings_count,
        "recent_bookings": recent_bookings
    })


# 🔑 Admin Login
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("/dashboard/")
        else:
            return render(request, "dashboard/admin_login.html", {
                "error": "Invalid admin credentials"
            })

    return render(request, "dashboard/admin_login.html")


# 🚪 Admin Logout
def admin_logout(request):
    logout(request)
    return redirect("/admin-login/")


# 👤 Manage Artists
@admin_required
def manage_artists(request):

    if request.method == "POST":
        name = request.POST.get("name")
        specialty = request.POST.get("specialty")
        bio = request.POST.get("bio")
        image = request.FILES.get("image")

        Artist.objects.create(
            name=name,
            specialty=specialty,
            bio=bio,
            image=image
        )

        return redirect("/dashboard/artists/")

    artists = Artist.objects.all()
    return render(request, "dashboard/artists.html", {"artists": artists})


# ❌ Delete Artist
@admin_required
def delete_artist(request, id):
    artist = get_object_or_404(Artist, id=id)
    artist.delete()
    return redirect("/dashboard/artists/")


# ✏️ Edit Artist
@admin_required
def edit_artist(request, id):
    artist = get_object_or_404(Artist, id=id)

    if request.method == "POST":
        artist.name = request.POST.get("name")
        artist.specialty = request.POST.get("specialty")
        artist.bio = request.POST.get("bio")

        if request.FILES.get("image"):
            artist.image = request.FILES.get("image")

        artist.save()
        return redirect("/dashboard/artists/")

    return render(request, "dashboard/edit_artist.html", {"artist": artist})


# 🎨 Manage Tattoos
@admin_required
def manage_tattoos(request):

    artists = Artist.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        artist_id = request.POST.get("artist")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        # 🔥 Validation
        if not category_id:
            return render(request, "dashboard/tattoos.html", {
                "tattoos": Tattoo.objects.all(),
                "artists": artists,
                "categories": categories,
                "error": "Please select a category"
            })

        Tattoo.objects.create(
            title=title,
            description=description,
            artist_id=artist_id,
            category_id=category_id,
            image=image
        )

        return redirect("/dashboard/tattoos/")

    tattoos = Tattoo.objects.all()

    return render(request, "dashboard/tattoos.html", {
        "tattoos": tattoos,
        "artists": artists,
        "categories": categories
    })


# 📅 Manage Bookings
@admin_required
def manage_bookings(request):
    bookings = Booking.objects.select_related('slot', 'artist', 'user')

    return render(request, "dashboard/bookings.html", {
        "bookings": bookings
    })


# 🔥 Generate Slots
@admin_required
def generate_slots(request):

    artists = Artist.objects.all()

    if request.method == "POST":
        artist_id = request.POST.get("artist")
        date = request.POST.get("date")

        artist = Artist.objects.get(id=artist_id)

        start = time(10, 0)   # 10 AM
        end = time(20, 0)     # 8 PM

        current = datetime.combine(
            datetime.strptime(date, "%Y-%m-%d").date(),
            start
        )

        end_datetime = datetime.combine(
            datetime.strptime(date, "%Y-%m-%d").date(),
            end
        )

        while current < end_datetime:
            slot_end = current + timedelta(hours=1)

            TimeSlot.objects.get_or_create(
                artist=artist,
                date=date,
                start_time=current.time(),
                end_time=slot_end.time()
            )

            current = slot_end

        return render(request, "dashboard/generate_slots.html", {
            "artists": artists,
            "success": "Slots generated successfully ✅"
        })

    return render(request, "dashboard/generate_slots.html", {
        "artists": artists
    })


# 🔄 Update Booking Status
@admin_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = status
    booking.save()

    return redirect("/dashboard/bookings/")