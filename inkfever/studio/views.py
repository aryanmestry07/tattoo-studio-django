from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Tattoo, Artist, Review, Studio, TimeSlot, Booking


# 🏠 Home Page (PUBLIC)

def home(request):
    return render(request, "studio/home.html")

# 🎨 Gallery (PUBLIC)
def gallery(request):
    tattoos = Tattoo.objects.all()
    return render(request, "studio/gallery.html", {"tattoos": tattoos})


# 👤 Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "studio/signup.html")


# 🔐 Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_url = request.GET.get('next')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if next_url:
                return redirect(next_url)

            return redirect("home")
        else:
            return render(request, "studio/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "studio/login.html")


# 🚪 Logout
def logout_view(request):
    logout(request)
    return redirect("home")


# 👨‍🎨 Artists
def artists(request):
    artists = Artist.objects.all()
    return render(request, "studio/artists.html", {"artists": artists})


# ⭐ Add Review
@login_required(login_url="login")
def add_review(request):
    artists = Artist.objects.all()
    reviews = Review.objects.select_related('user', 'artist').all().order_by('-id')

    if request.method == "POST":
        artist_id = request.POST.get("artist")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # 🛑 Validation (important)
        if not rating or not comment:
            return render(request, "studio/review.html", {
                "artists": artists,
                "reviews": reviews,
                "error": "Please fill all fields"
            })

        artist = Artist.objects.get(id=artist_id)

        # ✅ Prevent duplicate review (optional but pro)
        Review.objects.update_or_create(
            user=request.user,
            artist=artist,
            defaults={
                "rating": int(rating),
                "comment": comment
            }
        )

        return redirect("review")  # stay on same page

    return render(request, "studio/review.html", {
        "artists": artists,
        "reviews": reviews
    })
# 🏢 Studio Info
def studio_info(request):
    studio = Studio.objects.first()

    return render(request, "studio/studio_info.html", {
        "studio": studio
    })


# 🔥 STEP 1: SELECT ARTIST + DATE
@login_required(login_url="login")
def book_tattoo(request):
    artists = Artist.objects.all()

    return render(request, "studio/book.html", {
        "artists": artists
    })


# 🔥 STEP 2: SHOW AVAILABLE SLOTS
@login_required(login_url="login")
def available_slots(request):
    artist_id = request.GET.get("artist")
    date = request.GET.get("date")

    slots = TimeSlot.objects.filter(
        artist_id=artist_id,
        date=date,
        is_booked=False
    )

    return render(request, "studio/slots.html", {
        "slots": slots,
        "artist_id": artist_id,
        "date": date
    })


# 🔥 STEP 3: BOOK SLOT (REAL LOGIC)
from .forms import BookingForm

@login_required(login_url="login")
@transaction.atomic
def book_slot(request, slot_id):
    slot = TimeSlot.objects.select_for_update().get(id=slot_id)

    # 🚫 Prevent double booking
    if slot.is_booked:
        return render(request, "studio/error.html", {
            "message": "Slot already booked ❌"
        })

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            # 🔥 Assign automatically
            booking.user = request.user
            booking.artist = slot.artist
            booking.slot = slot

            booking.save()

            # 🔥 Mark slot booked
            slot.is_booked = True
            slot.save()

            return render(request, "studio/success.html")

    else:
        form = BookingForm()

    return render(request, "studio/booking_form.html", {
        "slot": slot,
        "form": form
    })

# USER BOOKING HISTORY
@login_required(login_url="login")
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('slot', 'artist')

    return render(request, "studio/my_bookings.html", {
        "bookings": bookings
    })