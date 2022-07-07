from django.db import models


class UltimateCourseCustomer(models.Model):
    mobile = models.CharField(max_length=13)
    promo_applied = models.BooleanField(default=False)
    promo = models.CharField(max_length=12, default='')
    # course = models.CharField(max_length=20)
    promo_attempts = models.IntegerField(default=0)
    applied_on = models.DateTimeField(default=None, null=True)
    purchased = models.BooleanField(default=False)
    purchased_on = models.DateTimeField(default=None, null=True)
    price_paid = models.IntegerField(default=-1)

    def __str__(self):
        display_name = self.mobile
        if self.mobile.isdigit():
            display_name = "+" + self.mobile[:-10] + " " + self.mobile[-10:]
        
        code_applied = "Yes" if self.promo_applied else "No "
        purchased = "Yes" if self.purchased else "No "

        return f"{display_name} || Promo Code Applied: {code_applied} || Purchased: {purchased}"



'''
This is a model for storing extra information about the user, like age, gender, address, city, state
This model is not created during signup. It is created when the user fills the form in the dashboard
username (mobile no.) is used for linking the UserProfile with the User model
Email and full name are not stored here because they are already stored in the User model
'''
class UserProfile(models.Model):
    username = models.CharField(max_length=13)
    age = models.CharField(max_length=3, default='', blank=True)
    gender = models.CharField(max_length=10, default='', blank=True)
    address = models.CharField(max_length=100, default='', blank=True)
    city = models.CharField(max_length=50, default='', blank=True)
    state = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return self.username
