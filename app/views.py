from plistlib import loads

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Order
import json
# Create your views here.
def orders_list(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        orders = Order.objects.all().values()
        formatted_orders = []
        for order in orders:
            try:
                items = json.loads(order['items'])
                formatted_items = [f'{item}' for item in items]
                print(formatted_items)
            except json.JSONDecodeError:
                items = []

            formatted_orders.append({
                'id':order['id'],
                'table_number':order['table_number'],
                'items':formatted_items,
                'total_price':float(order['total_price']),
                'status':order['status']
            })

        return JsonResponse(formatted_orders, safe=False)
    return render(request, 'index.html')

def crate_order(request):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        items_text = request.POST.get('items')
        if items_text:
            items_list = [item.strip() for item in items_text.split(',')]
        else:
            items_list = []
        total_price = len(items_list) *10
        Order.objects.create(
            table_number = table_number,
            items = items_list,
            total_price = total_price
        )
        return redirect('orders_list')
    return JsonResponse({'error':'Онли пост запросы бро'})

def delete_order(request, pk):
    if request.method == 'POST':
        order = Order.objects.filter(id=pk).first()
        order.delete()
        return redirect('orders_list')
    return JsonResponse({'error':'only post zapros'})

def update_order(request, pk):
    if request.method == 'POST':
        order = Order.objects.filter(id=pk).first()
        print(request.body)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('orders_list')
    return redirect('orders_list')