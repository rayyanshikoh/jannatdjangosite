from django.db import models

# Create your models here.
class Listing(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField()
    catchphrase = models.TextField(null=True, blank=True)
    picture_0 = models.ImageField(upload_to = "mainimages")
    picture_1 = models.ImageField(null=True, blank=True, upload_to = "./product/static/product/imgs")
    picture_2 = models.ImageField(null=True, blank=True, upload_to = "./product/static/product/imgs")
    short_term_price = models.IntegerField(default=0)
    long_term_price = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    # tag = models.ForeignKey('Tag', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length = 150)
    dateofbirth = models.DateField()
    email = models.TextField()
    phone_number = models.CharField(max_length=150)

    def __str__(self):
        return self.first_name


class Product(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    lease_date = models.DateField()
    clear_date = models.DateField()
    price = models.IntegerField(default=0) #cents
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    def __str__(self):
        return self.listing.name
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Tag(models.Model):
    label = models.CharField(max_length=255)
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    def __str__(self):
        return self.label