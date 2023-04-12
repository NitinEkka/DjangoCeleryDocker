from django import forms
from .models import Spraying, Drenching, Recipe, Farm, User, Inventory, RocketChatConversation

class SprayingForm(forms.ModelForm):
    class Meta:
        model = Spraying
        fields = ('spraying_id', 'spray_content', 'spray_name', 'farm')

class DrenchingForm(forms.ModelForm):
    class Meta:
        model = Drenching
        fields = ('drenching_id', 'drench_content', 'drench_name', 'farm')

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_id', 'recipe_name', 'recipe_content', 'number_of_compound')

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ('farm_id', 'farm_name', 'farm_location')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('role', 'first_name', 'last_name', 'phone_number', 'email', 'farm')

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('category_name', 'quantity', 'farm')

# class RocketForm(forms.ModelForm):
#     class Meta:
#         model = RocketChatConversation
#         fields = ('conversation_id', 'message', 'timestamp')