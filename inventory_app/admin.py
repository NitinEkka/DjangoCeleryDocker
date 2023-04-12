from django.contrib import admin
from .models import *
from .forms import *
from django.core.mail import send_mail
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# from rocketchat_API.rocketchat import RocketChat
# Register your models here.
from rocketchat.api import RocketChatAPI
from django.core.mail import EmailMultiAlternatives
from .signals import threshold_signal

class RecipeFormAdmin(admin.ModelAdmin):
    form = RecipeForm

    list_display = ('recipe_name', 'recipe_content')
    
    def field1(self, obj):
        return obj.recipe_name
    field1.short_description = 'Recipe Name'
    
    def field2(self, obj):
        return obj.recipe_content
    field2.short_description = 'Content'

    search_fields = ['recipe_name']
    def save_model(self, request, obj, form, change):
        obj.save()

class SprayFormAdmin(admin.ModelAdmin):
    form = SprayingForm
    
    autocomplete_fields = ['spray_content']
    
    list_display = ('spray_name', 'status', 'farm')
    
    def field1(self, obj):
        return obj.spray_name
    field1.short_description = 'Spray Name'
    
    def field2(self, obj):
        return obj.status
    field2.short_description = 'Status'
    
    def field3(self, obj):
        return obj.farm
    field3.short_description = 'Farm'

    def save_model(self, request, obj, form, change):
        recipe_object = Recipe.objects.get(recipe_name = form.cleaned_data['spray_content'])
        json_data = recipe_object.recipe_content
        print(json_data)
        json_string = json.dumps(json_data).replace("'", '"')
        print(json_string)
        
        count_compound = 0
        
        for key, value in json_data.items():
            inventory_item = Inventory.objects.filter(farm=form.cleaned_data['farm']).get(category_name=key)
            if inventory_item.quantity > value:
                count_compound = count_compound + 1

        if count_compound == recipe_object.number_of_compound:
            for key, value in json_data.items():
                inventory_item = Inventory.objects.filter(farm=form.cleaned_data['farm']).get(category_name=key)
                if inventory_item.quantity < value:
                    obj.status = 'failure'
                    
                    
                else:
                    inventory_item.quantity = inventory_item.quantity - value
                    inventory_item.save()
                    obj.status = 'success'

                Usage_obj = StockUsage()
                Usage_obj.stock_name = key
                Usage_obj.stock_quantity = value
                Usage_obj.transaction_type = 'use'
                Usage_obj.farm = form.cleaned_data['farm']
                Usage_obj.save()
            
            threshold = 10
            items = Inventory.objects.filter(quantity__lte=threshold)
            if items.exists():
                threshold_signal.send(sender=None)
            

            json_data_obj = json.loads(json_string)
            list_inventory_manager = []
            manager = User.objects.filter(role='inventorymanager', farm=form.cleaned_data['farm'])
            for user in manager:
                list_inventory_manager.append(user.email)
            
           
            context = {'data': json_data_obj, 'farm': form.cleaned_data['farm']}
            email_body = render_to_string('inventory_app/spray_email.html', context)
            # reciever_list = ['nitin.ekka30@gmail.com']

            html_content = email_body
            msg = EmailMultiAlternatives('Spray Inventory Usage', 'This is HTML version', 'nitin.ekka30@gmail.com',list_inventory_manager)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        
            obj.save()
        else:
            obj.status = 'failure'
            obj.save()
            threshold = 10
            items = Inventory.objects.filter(quantity__lte=threshold)
            if items.exists():
                threshold_signal.send(sender=None)



        
    
class DrenchFormAdmin(admin.ModelAdmin):
    form = DrenchingForm

    autocomplete_fields = ['drench_content']

    list_display = ('drench_name', 'status', 'farm')
    
    def field1(self, obj):
        return obj.drench_name
    field1.short_description = 'Drench Name'
    
    def field2(self, obj):
        return obj.status
    field2.short_description = 'Status'

    def field3(self, obj):
        return obj.farm
    field3.short_description = 'Farm'

    def save_model(self, request, obj, form, change):
        recipe_object = Recipe.objects.get(recipe_name = form.cleaned_data['drench_content'])
        json_data = recipe_object.recipe_content
        print(json_data)
        json_string = json.dumps(json_data).replace("'", '"')
        print(json_string)

        count_compound = 0
        
        for key, value in json_data.items():
            inventory_item = Inventory.objects.filter(farm=form.cleaned_data['farm']).get(category_name=key)
            if inventory_item.quantity > value:
                count_compound = count_compound + 1
        
        if count_compound == recipe_object.number_of_compound:
            for key, value in json_data.items():
                inventory_item = Inventory.objects.filter(farm=form.cleaned_data['farm']).get(category_name=key)
                if inventory_item.quantity < value:
                    obj.status = 'failure'
                    
                else:
                    inventory_item.quantity = inventory_item.quantity - value
                    inventory_item.save()
                    obj.status = 'success'

                Usage_obj = StockUsage()
                Usage_obj.stock_name = key
                Usage_obj.stock_quantity = value
                Usage_obj.transaction_type = 'use'
                Usage_obj.farm = form.cleaned_data['farm']
                Usage_obj.save()
            
            threshold = 10
            items = Inventory.objects.filter(quantity__lte=threshold)
            if items.exists():
                threshold_signal.send(sender=None)

            
            json_data_obj = json.loads(json_string)
            list_inventory_manager = []
            manager = User.objects.filter(role='inventorymanager', farm=form.cleaned_data['farm'])
            for user in manager:
                list_inventory_manager.append(user.email)
            context = {'data': json_data_obj, 'farm': form.cleaned_data['farm']}
            email_body = render_to_string('inventory_app/drench_email.html', context)
            # reciever_list = ['nitin.ekka30@gmail.com']

            html_content = email_body
            msg = EmailMultiAlternatives('Drench Inventory Usage', 'This is HTML version', 'nitin.ekka30@gmail.com',list_inventory_manager)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        
            obj.save()
        else:
            obj.status = 'failure'
            obj.save()
            threshold = 10
            items = Inventory.objects.filter(quantity__lte=threshold)
            if items.exists():
                threshold_signal.send(sender=None)

        


class FarmFormAdmin(admin.ModelAdmin):
    form = FarmForm

    list_display = ('farm_name', 'farm_location')
    
    def field1(self, obj):
        return obj.farm_name
    field1.short_description = 'Farm Name'

    def field1(self, obj):
        return obj.farm_location
    field1.short_description = 'Farm Location'

    def save_model(self, request, obj, form, change):
        obj.save()

class UserFormAdmin(admin.ModelAdmin):
    form = UserForm

    list_display = ('first_name', 'role', 'farm', 'email')
    
    def field1(self, obj):
        return obj.first_name
    field1.short_description = 'First Name'

    def field1(self, obj):
        return obj.role
    field1.short_description = 'Role'

    def field1(self, obj):
        return obj.farm
    field1.short_description = 'Farm'

    def field1(self, obj):
        return obj.email
    field1.short_description = 'Email'

    def save_model(self, request, obj, form, change):
        obj.save()

class InventoryFormAdmin(admin.ModelAdmin):
    form = InventoryForm
    
    list_display = ('category_name', 'quantity', 'farm')
    
    def field1(self, obj):
        return obj.category_name
    field1.short_description = 'Stock Name'

    def field1(self, obj):
        return obj.quantity
    field1.short_description = 'Quantity'

    def field1(self, obj):
        return obj.farm
    field1.short_description = 'Farm'

    
    def save_model(self, request, obj, form, change):
        form_data = form.cleaned_data
        queryset = Inventory.objects.filter(category_name=form_data.get('category_name'))

        if queryset:
            item = Inventory.objects.get(category_name=form_data.get('category_name'))
            item.quantity = item.quantity + form.cleaned_data['quantity']
            item.save()
        else:
            super().save_model(request, obj, form, change)

        Usage_obj = StockUsage()
        Usage_obj.stock_name = form.cleaned_data['category_name']
        Usage_obj.stock_quantity = form.cleaned_data['quantity']
        Usage_obj.transaction_type = 'add'
        Usage_obj.save()
        
            
class StockUsageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super(StockUsageAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    list_display = ('stock_name', 'stock_quantity', 'farm')
    
    def field1(self, obj):
        return obj.stock_name
    field1.short_description = 'Stock Name'
    
    def field2(self, obj):
        return obj.testock_quantityxt
    field2.short_description = 'Quantity'

    def field2(self, obj):
        return obj.farm
    field2.short_description = 'Farm'
    

class RocketAdmin(admin.ModelAdmin):
    list_display = ('sender', 'text')
    
    def field1(self, obj):
        return obj.sender
    field1.short_description = 'Sender Name'
    
    def field2(self, obj):
        return obj.text
    field2.short_description = 'Message'

class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['farm', 'receiver', 'body']
    
    def field1(self, obj):
        return obj.farm
    field1.short_description = 'Farm Name'
    

admin.site.register(RocketChatConversation, RocketAdmin)
admin.site.register(Farm, FarmFormAdmin)
admin.site.register(Inventory, InventoryFormAdmin)
admin.site.register(StockUsage, StockUsageAdmin)
admin.site.register(User, UserFormAdmin)
admin.site.register(Spraying, SprayFormAdmin)
admin.site.register(Drenching, DrenchFormAdmin)
admin.site.register(Recipe, RecipeFormAdmin)
admin.site.register(EmailLog, EmailLogAdmin)

