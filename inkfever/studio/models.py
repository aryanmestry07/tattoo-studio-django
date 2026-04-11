from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    specialty = models.CharField(max_length=100)
    image = models.ImageField(upload_to='artists/')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tattoo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tattoos/')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# 🔥 NEW MODEL (CORE OF SLOT SYSTEM)
class TimeSlot(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.artist.name} | {self.date} | {self.start_time}"


# 🔥 UPDATED BOOKING MODEL (IMPORTANT CHANGE)
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    # 🔥 LINK TO SLOT (PREVENTS DOUBLE BOOKING)
    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)

    tattoo = models.ForeignKey(Tattoo, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.artist} ({self.status})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)  # 🔥 bonus

    def __str__(self):
        return f"{self.user.username} - {self.artist.name}"

class Studio(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    map_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name