from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *


# Form to create a new customer
class CustomerCreateForm(ModelForm):
     class Meta:
          model = Customer
          fields = ['nom_complet', 'date_de_naissance', 'telephone', 'email', 'adresse',]


# Form for creating a new staff member (either an admin or an employee)
class UserCreateForm(UserCreationForm):
     class Meta:
          model = User
          fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','is_staff']
     
     def __init__(self, *args, **kwargs):
          super(UserCreateForm, self).__init__(*args, **kwargs)

          for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',]:
               self.fields[fieldname].help_text = None

          self.fields['is_staff'].label = 'Membre du staff ?' 
          self.fields['is_staff'].help_text = 'Précise si Membre du staff peut se connecter au site d\'administration.' 


# Form to create a new customer
class CategoryCreateForm(ModelForm):
     class Meta:
          model = Category
          fields = ['code', 'nom',]


# Form to create a new customer
class BrandCreateForm(ModelForm):
     class Meta:
          model = Brand
          fields = ['code', 'nom',]


# Form to create a new stock
class StockCreateForm(ModelForm):
     class Meta:
          model = Stock
          fields = ['code', 'prix', 'remise', 'description', 'categorie', 'marque']

     
# Form to create a new product
class ProductCreateForm(ModelForm):
     class Meta:
          model = Product
          fields = ['code', 'taille',]


class ProductAddForm(forms.Form):
     code = forms.CharField(max_length=50, required=True)

     
# Form to create a new order
class OrderCreateForm(ModelForm):
     class Meta:
          model = Order
          fields = ['client', 'remise', 'note', 'statut',]