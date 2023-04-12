from django.db import models


class Farm(models.Model):
    farm_id = models.IntegerField(primary_key=True)
    farm_name = models.CharField(max_length=250)
    farm_location = models.CharField(max_length=250)

    def __str__(self):
        return self.farm_name
    
class Inventory(models.Model):
    category_name = models.CharField(max_length=250)
    quantity = models.IntegerField()
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.category_name
    
class StockUsage(models.Model):
    TYPE_CHOICES = [
        ('add', 'Add'),
        ('use', 'Use'),
    ]
    stock_name = models.CharField(max_length=20)
    transaction_type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    transaction_time = models.DateTimeField(auto_now_add=True)
    stock_quantity = models.IntegerField()
    farm = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.stock_name
    
    
class Recipe(models.Model):
    recipe_id = models.IntegerField(primary_key=True, auto_created=True)
    recipe_name = models.CharField(max_length=30)
    recipe_content = models.JSONField(default=None)
    number_of_compound = models.IntegerField()
        
    def __str__(self):
        return self.recipe_name
    
class Spraying(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]
    spraying_id = models.IntegerField(primary_key=True, auto_created=True)
    spray_content = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    spray_name = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.spray_name
    
class Drenching(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]
    drenching_id = models.IntegerField(primary_key=True, auto_created=True)
    drench_content = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    drench_name = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.drench_name 
    
class User(models.Model):
    ROLES = (('labour', 'Labour'), ('farmexecutive', 'Farm Executive'), ('inventorymanager', 'Inventory Manager'))
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='labour'
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.first_name

class RocketChatConversation(models.Model):
    text = models.TextField()
    sender = models.CharField(max_length=255)
    created_at = models.CharField(max_length=100)

    def __str__(self):
        return self.sender
    
class EmailLog(models.Model):
    body = models.TextField()
    receiver = models.TextField()
    farm = models.CharField(max_length=250)

    def __str__(self):
        return self.body
    
# https://wireone.rocket.chat/home