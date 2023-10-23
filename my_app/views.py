import random as rand
import pyotp
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from ninja import NinjaAPI
from rest_framework.decorators import api_view
from .models import userProfiles,categories,products,orders
from django.core.serializers import serialize

@api_view(['POST'])
def enter_mobile(request):
    if request.method == 'POST':
        userName = request.GET['userName']
        phoneNumber = request.GET['phoneNumber']
        email = request.GET['email']
        if phoneNumber:
            # Generate a random 6-digit OTP
            otp = str(rand.randint(1000, 9999))

            # Create a TOTP object using the generated OTP

            # Store the OTP in the user's session
            request.session['otp'] = otp
            request.session['userName'] = userName
            request.session['phoneNumber'] = phoneNumber
            request.session['email'] = email
            # Simulate sending the OTP to the user's mobile (replace with your SMS gateway)
            print(f'Sending OTP {otp} to {phoneNumber}')
            return JsonResponse({'message': f'OTP {otp} sent to {phoneNumber}'})
        else:
            return JsonResponse({'message': 'Invalid mobile number'})


@api_view(['POST'])
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.GET['otp']

        if entered_otp:
            # Get the stored OTP from the session
            stored_otp = request.session.get('otp')
            print(stored_otp)

            if entered_otp == stored_otp:
                # OTP is verified
                usersList = userProfiles.objects.all()
                if (usersList):
                    Id=userProfiles.objects.last().userId+1
                else:
                    Id = 0
                request.session['userId']=Id
                Name = request.session.get('userName')
                Number = request.session.get('phoneNumber')
                Mail = request.session.get('email')
                user=userProfiles(userId=Id,userName=Name,phoneNumber=Number,email=Mail)
                user.save()
                return JsonResponse({'message': 'OTP verified successfully'})
            else:
                # OTP verification failed
                return JsonResponse({'message': 'OTP verification failed'})


@api_view(['GET'])
def list_categories(request):
    categoryList = categories.objects.all()
    data = [{"category id":category.categoryId,"name": category.categoryName} for category in categoryList]
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def list_products(request):
    productList = products.objects.all()
    print(productList[0].categoryId)
    data = [{"product id":product.productId,"name": product.productName, "price":product.price} for product in productList]
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def list_products_by_category(request, categoryId):
    productList = products.objects.filter(categoryId__categoryId=categoryId)
    data = [{"product id":product.productId,"product name": product.productName,"price": str(product.price)} for product in productList]
    return JsonResponse(data, safe=False)

@api_view(['POST'])
def place_order(request):
    pName=request.GET['productName']
    user=request.GET['userId']
    productList = products.objects.filter(productName=pName)
    print(productList[0].price)
    if(productList):
        order=orders.objects.all()
        if(order):
            Id = orders.objects.last().orderId + 1
        else:
            Id=0
        price=productList[0].price
        user_id = get_object_or_404(userProfiles, userId=user)
        order = orders(userId=user_id,productName=pName,orderId=Id, total=price)
        order.save()
        return JsonResponse({'message': 'product ordered successfully'})
    return JsonResponse({'message': 'no product found'})


@api_view(['POST'])
def update_profile(request):
    Id=request.GET['userId']
    userName=request.GET['userName']
    phoneNumber=request.GET['phoneNumber']
    email = request.GET['email']
    if(len(phoneNumber)<10):
        return JsonResponse({'message':'phone number should be 10 digits'})
    if('@' not in email):
        return JsonResponse({'message': 'invalid email'})
    profile=userProfiles.objects.filter(userId=Id)
    for result in profile:
        result.userName=userName
        result.phoneNumber=phoneNumber
        result.email=email
        result.save()
    return JsonResponse({'message':'success'})
