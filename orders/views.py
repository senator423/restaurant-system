import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from requests.auth import HTTPBasicAuth

from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .models import Category, RegularPizza, SicilianPizza, Toppings, Sub, Pasta, Salad, DinnerPlatters, UserOrder, SavedCarts
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, authenticate, login
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        #we are passing in the data from the category model
        return render(request, "placements/home.html", {"categories":Category.objects.all})
    else:
        return redirect("orders:login")

def login_request(request):

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('/')

    form = AuthenticationForm()
    return render(request = request,
                  template_name ="placements/login.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    return redirect("orders:login")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("orders:index")

        return render(request = request,
                      template_name ="placements/register.html",
                      context={"form":form})

    return render(request = request,
                  template_name ="placements/register.html",
                  context={"form":UserCreationForm})

def pizza(request):
    if request.user.is_authenticated:
        return render(request, "placements/pizza.html", context = {"regular_pizza":RegularPizza.objects.all, "sicillian_pizza":SicilianPizza.objects.all , "toppings":Toppings.objects.all, "number_of_toppings":[1, 2, 3]})
    else:
        return redirect("orders:login")

def pasta(request):
    if request.user.is_authenticated:
        return render(request, "placements/pasta.html", context = {"dishes":Pasta.objects.all})
    else:
        return redirect("orders:login")


def salad(request):
    if request.user.is_authenticated:
        return render(request, "placements/salad.html", context = {"dishes":Salad.objects.all})
    else:
        return redirect("orders:login")


def subs(request):
    if request.user.is_authenticated:
        return render(request, "placements/sub.html", context = {"dishes":Sub.objects.all})
    else:
        return redirect("orders:login")


def dinner_platters(request):
    if request.user.is_authenticated:
        return render(request, "placements/dinner_platters.html", context = {"dishes":DinnerPlatters.objects.all})
    else:
        return redirect("orders:login")

def directions(request):
    if request.user.is_authenticated:
        return render(request, "placements/directions.html")
    else:
        return redirect("orders:login")

def hours(request):
    if request.user.is_authenticated:
        return render(request, "placements/hours.html")
    else:
        return redirect("orders:login")

def contact(request):
    if request.user.is_authenticated:
        return render(request, "placements/contact.html")
    else:
        return redirect("orders:login")

def cart(request):
    if request.user.is_authenticated:
        return render(request, "placements/cart.html")
    else:
        return redirect("orders:save_cart")

def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart'))
        price = request.POST.get('price_of_cart')
        username = request.user.username
        response_data = {}
        list_of_items = [item["item_description"] for item in cart]

        order = UserOrder(username=username, order=list_of_items, price=float(price), delivered=False) #create the row entry
        order.save() #save row entry in database

        response_data['result'] = 'Order Recieved!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def view_orders(request):
    if request.user.is_superuser:
        #make a request for all the placements in the database
        rows = UserOrder.objects.all().order_by('-time_of_order')
        #placements.append(row.order[1:-1].split(","))

        return render(request, "placements/orders.html", context = {"rows":rows})
    else:
        rows = UserOrder.objects.all().filter(username = request.user.username).order_by('-time_of_order')
        return render(request, "placements/orders.html", context = {"rows":rows})

def mark_order_as_delivered(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        UserOrder.objects.filter(pk=id).update(delivered=True)
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def save_cart(request):
    if request.method == 'POST':
        cart = request.POST.get('cart')
        saved_cart = SavedCarts(username=request.user.username, cart=cart) #create the row entry
        saved_cart.save() #save row entry in database
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def retrieve_saved_cart(request):
    saved_cart = SavedCarts.objects.get(username = request.user.username)
    return HttpResponse(saved_cart.cart)

def check_superuser(request):
    print(f"User super??? {request.user.is_superuser}")
    return HttpResponse(request.user.is_superuser)

def home(request):
    return render(request, 'payment/main.html', {'navbar': 'home'})


def token(request):
    consumer_key = 'tXVfRGu4bfzHA1Ix84RFYn8Y2DPuTYYAjUz9d3KM210kWQg6'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'payment/token.html', {"token": validated_mpesa_access_token})


def pay(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "mpishi-bora",
            "TransactionDesc": "food consumption charges"
        }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse("success")


def stk(request):
    return render(request, 'payment/pay.html', {'navbar': 'stk'})

import requests
import json

def get_mpesa_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    headers = {"Authorization": "Basic YOUR_AUTH_HERE"}

    response = requests.get(url, headers=headers)  # Fetch token

    print("Response Status:", response.status_code)  # Check status
    print("Response Text:", response.text)  # Debug response content

    try:
        data = response.json()  # Attempt to parse JSON
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}

    return data
def payment_token(request):
    response = get_mpesa_token()

    if "error" in response:
        return JsonResponse({"error": "Failed to fetch token"}, status=500)

    return JsonResponse(response)
