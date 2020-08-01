from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products':products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = { 'items': items, 'order': order, 'cartItems': cartItems}
    # print(context)
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = { 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # print('Action:', action)
    # print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #get_or_createにすることですでにあるorderItemを重複して作成するのを防ぐ
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1 
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
    # print('Data1:', request.body)
    # print('Data2:', json.loads(request.body))
    transaction_id = datetime.datetime.now().timestamp()
    print("Now", datetime.datetime.now())
    print("Timestamp", datetime.datetime.now().timestamp())
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
         customer, order = guestOrder(request, data)

    print("total", data['form']['total'])
    total = float(data['form']['total'])
    print("total",total)
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment completed', safe=False)



# promise