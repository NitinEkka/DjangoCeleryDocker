from django.shortcuts import render, redirect
# from .models import Inventory,StockUsage, User
# from .forms import *
# from django.core.mail import send_mail
# from django.http import HttpResponse
# from .tasks import check_threshold

# def add_stock(request):
#     if request.method == 'POST':
#         category_name = request.POST['category_name']
#         add_quantity = request.POST['quantity']
#         if Inventory.objects.get(category_name=category_name):
#             stock_item = Inventory.objects.get(category_name=category_name)
#             old_quantity = stock_item.quantity
#             stock_item.quantity = old_quantity + add_quantity
#             stock_item.save()
#             StockUsage.objects.create(stock_name=category_name, transaction_type='add', stock_quantity=add_quantity)
#         else:    
#             Inventory.objects.create(category_name=category_name, quantity=add_quantity)
#             StockUsage.objects.create(stock_name=category_name, transaction_type='add', stock_quantity=add_quantity)
#         return redirect('success')
#     else:
#         return render (request, 'inventory_app/add_product.html')
    
# def use_product(request):
#     if request.method == 'POST':
#         category_name = request.POST['category_name']
#         quantity = request.POST['quantity']
#         product = Inventory.objects.get(category_name=category_name)
#         if product.quantity < quantity:
#             return render (request, 'inventory_app/error.html')
#         product.quantity -= quantity
#         product.save()
#         StockUsage.objects.create(stock_name=category_name, transaction_type='use', stock_quantity=quantity)
#         list_inventory_manager = []
#         manager = User.objects.filter(role='inventorymanager')
#         for user in manager:
#             list_inventory_manager.append(user.email)
#         send_mail(
#                 subject='Stock Usage',
#                 message=f'{quantity} items of {category_name} has been used',
#                 from_email='nitin.ekka30@gmail.com',
#                 recipient_list=list_inventory_manager,
#                 fail_silently=False
#         )

#         return redirect('success')
#     else:
#         inventory = Inventory.objects.all()
#         return render (request, 'inventory_app/all_product.html', {'inventory': inventory})
    
# def success(request):

#     return render(request, 'inventory_app/success.html')

# def create_spray(request):
#     form = SprayingForm(request.POST)
#     if form.is_valid():
#         form.save()
#     context = {'form': form}
#     return render(request, 'inventory_app/create_spray.html', context)

# def create_drenching(request):
#     form = DrenchingForm(request.POST)
#     if form.is_valid():
#         form.save()
#     context = {'form': form}
#     return render(request, 'inventory_app/create_drench.html', context)



# def start_celery_beat(request):
#     check_threshold.delay()
#     return HttpResponse("Celery Beat has Started")
