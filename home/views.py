from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from home.user_input_checkers import *
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from home.promo_dict import ultimate_promo_set
from .models import UltimateCourseCustomer, UserProfile
from django.db.models import F  # for incrementing incorrect promo attempts value - refer to https://stackoverflow.com/questions/447117/django-increment-blog-entry-view-count-by-one-is-this-efficient
from datetime import datetime
from pytz import timezone


MAX_INCORRECT_PROMO_ATTEMPTS = 20

ULTIMATE_COURSE_TITLE = "Ultimate Option Trading Course"    # Course Title
ULTIMATE_COURSE_PRICE_ORIGINAL = 2500         # This price will be strike-through (just a display price)
ULTIMATE_COURSE_PRICE_ACTUAL = 2000           # This is the price before applying promo code
ULTIMATE_COURSE_DISCOUNT = 20                 # Discount in percentage after applying promo code
ULTIMATE_COURSE_PRICE_AFTER_DISCOUNT = 1600   # New price after applying promo code
ULTIMATE_COURSE_IMG_URL = "images/courses/ultimate.jpg"



def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def tnc(request):
    return render(request, 'tnc.html')

def privacy(request):
    return render(request, 'privacy.html')

def refund(request):
    return render(request, 'refund.html')

def beginners_booster_course(request):
    return render(request, 'beginners-booster-course.html')

def advanced_conqueror_course(request):
    return render(request, 'advanced-conqueror-course.html')



def signup(request):
    if request.method == 'POST':
        name = str(request.POST['dzName'])
        email = str(request.POST['dzEmail'])
        mobile = str(request.POST['dzNumber'])
        password1 = str(request.POST['dzPass1'])
        password2 = str(request.POST['dzPass2'])

        name = format_name(name)   # Removes Non-Alphanumeric Letters, and truncates excess 50 letters.
        if not check_name(name):
            messages.error(request, 'Name should be at least 3 letters and less than 50 letters.')
            return redirect('signup')
        
        if not check_mobile(mobile):
            messages.error(request, 'Mobile number should be 10 digits.')
            return redirect('signup')
        
        if not check_email(email):
            messages.error(request, 'Invalid email. Please check your email address again.')
            return redirect('signup')
        
        if not check_password(password1):
            messages.error(request, 'Password should be at least 8 letters.')
            return redirect('signup')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        mobile = "91" + mobile   # Adding country code 91 to mobile number
        if User.objects.filter(username=mobile).exists():
            messages.error(request, 'This mobile number already exists. Please Sign In.')
            return redirect('signup')


        # Note: Since create_user() method needs username, email, password to create a user,
        #       but we don't have username, so I have used mobile as username.
        myuser = User.objects.create_user(mobile, email, password1)
        myuser.first_name = name
        myuser.save()
        messages.success(request, 'Your account has been created successfully! Please login to continue.', {'alert_heading':"Success"})
        return redirect('login')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        mobile = str(request.POST['dzNumber'])
        password = str(request.POST['dzPassword'])

        if not check_mobile(mobile):
            messages.error(request, 'Mobile number should be 10 digits.')
            return redirect('login')
        
        # No need to tell user that login password length should be 8 letters.
        # if not check_password(password):
        #     messages.error(request, 'Password should be at least 8 letters.')
        #     return redirect('login')
        
        mobile = "91" + mobile

        user = authenticate(username=mobile, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect mobile or password. Please try again.')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def dashboard(request):
    user = request.user
    if user.is_authenticated:
        mobile = user.username
        fullname = user.first_name
        email = user.email
        
        # Creating a new userprofile if it doesn't exists
        if not UserProfile.objects.filter(username=mobile).exists():
            UserProfile.objects.create(username=mobile)
        userprofile = UserProfile.objects.get(username=mobile)

        # Getting data from Ultimate Course

        # Creating a row for the user if he doesn't exists in the table
        if not UltimateCourseCustomer.objects.filter(mobile=mobile).exists():
            UltimateCourseCustomer.objects.create(mobile=mobile)

        ucCustomer = UltimateCourseCustomer.objects.get(mobile=mobile)
        ucPriceOriginal = ULTIMATE_COURSE_PRICE_ORIGINAL
        ucPriceActual = ULTIMATE_COURSE_PRICE_ACTUAL
        ucPromoApplied = ucCustomer.promo_applied
        if ucPromoApplied:
            ucPriceActual = ULTIMATE_COURSE_PRICE_AFTER_DISCOUNT
        

        return render(request, 'dashboard.html', {
            'mobile': mobile[-10:],
            'fullname': fullname,
            'email': email,
            'ucPriceOriginal': ucPriceOriginal,
            'ucPriceActual': ucPriceActual,
            'ucPromoApplied': not ucPromoApplied,
            'userprofile': userprofile,
        })
        

    else:
        messages.warning(request, 'You are not logged in. Please login to continue.')
        return redirect('login')
        

def updateprofile(request):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            name = str(request.POST['dzName'])
            email = str(request.POST['dzEmail'])
            mobile = str(request.POST['dzNumber'])
            age = str(request.POST['dzAge'])
            gender = str(request.POST['dzGender'])
            address = str(request.POST['dzAddress'])
            city = str(request.POST['dzCity'])
            state = str(request.POST['dzState'])
            print(mobile)

            name = format_name(name)   # Removes Non-Alphanumeric Letters, and truncates excess 50 letters.
            if not check_name(name):
                messages.error(request, 'Name should be at least 3 letters and less than 50 letters.')
                return redirect('dashboard')
            
            if not check_email(email):
                messages.error(request, 'Invalid email. Please check your email address again.')
                return redirect('dashboard')
            
            # Under construction
            # if not check_mobile(mobile):
            #     messages.error(request, 'Mobile number should be 10 digits.')
            #     return redirect('dashboard')
            # mobile = "91" + mobile   # Adding country code 91 to mobile number
            # if User.objects.filter(username="91"+mobile).exists():

            user.first_name = name
            user.email = email
            user.save()
            if not UserProfile.objects.filter(username=mobile).exists():
                mobileWithCode = "91" + mobile
                if User.objects.filter(username=mobileWithCode).exists():
                    mobile = mobileWithCode
                else:
                    UserProfile.objects.create(username=mobile)
            userprofile = UserProfile.objects.get(username=mobile)
            userprofile.age = age
            userprofile.gender = gender
            userprofile.address = address
            userprofile.city = city
            userprofile.state = state
            userprofile.save()

            messages.success(request, 'Profile updated successfully!', {'alert_heading':"Success"})
            return redirect('dashboard')
        
        messages.warning(request, 'You are not logged in. Please login to continue.')
        return redirect('login')
        
    return redirect('dashboard')
            




def promo(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'You are not logged in. Please login to continue.')
        return redirect('login')

    # if request.method == 'GET':
    course = kwargs.get('course')
    if course == 'ultimate':

        # First check whether this user has already applied promo code or not
        mobile = user.username
        if UltimateCourseCustomer.objects.filter(mobile=mobile, promo_applied=True).exists():
            messages.warning(request, 'You have already applied promo code for this course.')
            return redirect('/dashboard', course='ultimate')


        title = ULTIMATE_COURSE_TITLE
        price = ULTIMATE_COURSE_PRICE_ACTUAL
        discout = ULTIMATE_COURSE_DISCOUNT
        total = ULTIMATE_COURSE_PRICE_AFTER_DISCOUNT
        course_img = ULTIMATE_COURSE_IMG_URL
        return render(request, 'promo.html', {'course':course, 'title':title, 'price':price, 'discount':discout, 'total':total, 'course_img':course_img})
    
    else:
        redirect('/dashboard')

    return redirect('/dashboard')

"""
if len in range(6, 13) and code in ultimate_promo_set and code is not used:
    promo code is correct
if 

"""


def verifypromo(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'You are not logged in. Please login to continue.')
        return redirect('login')
    
    if request.method == 'POST':
        course = request.POST['course']
        code = request.POST['dzPromo']
        code = parse_promo(code)
        if course == 'ultimate':
            
            # Creating a row for the user if he doesn't exists in the table
            mobile = user.username
            if not UltimateCourseCustomer.objects.filter(mobile=mobile).exists():
                UltimateCourseCustomer.objects.create(mobile=mobile)

            # Checking whether the user has already applied promo code or not
            if UltimateCourseCustomer.objects.filter(mobile=mobile, promo_applied=True).exists():
                messages.error(request, 'You have already applied promo code for this course.')
                return redirect('promo', course='ultimate')
            
            # Checking whether the user has exceeded the maximum number of attempts to apply promo code
            if UltimateCourseCustomer.objects.filter(mobile=mobile, promo_attempts__gte=MAX_INCORRECT_PROMO_ATTEMPTS).exists():
                messages.error(request, 'You have exceeded the maximum number of incorrect attempts to apply promo code. Please contact Intelligent Trader Team for help and support.')
                return redirect('promo', course='ultimate')

            # Checking whether the promo code is correct or not
            if (len(code) not in range(6, 13)) or (code not in ultimate_promo_set):
                # Increasing the incorrect promo attempt count
                UltimateCourseCustomer.objects.filter(mobile=mobile).update(promo_attempts=F('promo_attempts')+1)
                messages.error(request,'Invalid promo code. Please check your promo code again.')
                return redirect('promo', course='ultimate')

            # Checking whether the promo code is already used or not
            if UltimateCourseCustomer.objects.filter(promo=code).exists():
                messages.error(request, 'This promo code has already been used.')
                return redirect('promo', course='ultimate')
            
            # Promo code is correct and not used. Applying the promo code
            UltimateCourseCustomer.objects.filter(mobile=mobile).update(promo=code, promo_applied=True, applied_on=datetime.now(timezone("Asia/Kolkata")))
            messages.success(request, 'Promo code applied successfully.')
            return redirect('/dashboard', course='ultimate')


    return redirect('/')


