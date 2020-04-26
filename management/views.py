from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail

import calendar

import math
from .models import *
from .forms import *
from .decorators import *


# ------------------------------------------------------------------------------------ #
CONTACTS = 'Telephone:: (910) 514 38 59 \t(910) 514 38 59\nEmail:: chekeydia@gmail.com'
SLOGAN = 'CheKeyDiA, Des vêtements qui parlent en votre nom!'
MAIL_FOOTER = '\n\n\n\n#-------------------------------------------------------------------------------#\n' + CONTACTS + '\n#-------------------------------------------------------------------------------#\n' + SLOGAN
# ------------------------------------------------------------------------------------ #
# Start session I (GENERAL)

# I-1 - Function Dashboard => name='dashboard'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def dashboard(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            search = request.POST.get('search')
            try:
                product = Product.objects.get(code=search.upper())
            except:
                product = None
            
            if product is not None:
                return redirect('management:stock_details', product.stock.pk)
            else:
                return redirect('management:dashboard')



        orders = Order.objects.filter(date_enregistrement__gte=datetime.today().date())
        today_orders = len(orders)
        today_orders_price = week_orders_price = month_orders_price = quater_orders_price = year_orders_price = 0
        for order in orders:
            today_orders_price += order.somme_finale

        date = datetime.today()

        start_week = date - timedelta(date.weekday())
        end_week = start_week + timedelta(7)
        
        week_orders = Order.objects.filter(
            date_enregistrement__gte=start_week
            ).filter(
                    date_enregistrement__lte=end_week
            )
        for order in week_orders:
            week_orders_price += order.somme_finale

        
        first_day_of_month = date.replace(day=1)
        if (date.month) % 2 == 0:
            if date.month == 2:
                    if calendar.isleap(date.year):
                        last_day_of_month = date.replace(day=29)
                    else:
                        last_day_of_month = date.replace(day=28)
            else:
                    last_day_of_month = date.replace(day=30)
        else:
            last_day_of_month = date.replace(day=31)
        
        month_orders = Order.objects.filter(
            date_enregistrement__gte=first_day_of_month
            ).filter(
                    date_enregistrement__lte=last_day_of_month
            )
        for order in month_orders:
            month_orders_price += order.somme_finale
        
        # first_day_of_quater = date.replace(day=1)
        
        if date.month < 4:
            first_day_of_quater = date.replace(day=1, month=1)
            last_day_of_quater = date.replace(day=31, month=3)
            quater_description = 'Jan - Mars'
        elif date.month > 3 and date.month < 7:
            first_day_of_quater = date.replace(day=1, month=4)
            last_day_of_quater = date.replace(day=30, month=6)
            quater_description = 'Avr - Juin'
        elif date.month > 6 and date.month < 10:
            first_day_of_quater = date.replace(day=1, month=7)
            last_day_of_quater = date.replace(day=30, month=9)
            quater_description = 'Juil - Sep'
        else:
            first_day_of_quater = date.replace(day=1, month=10)
            last_day_of_quater = date.replace(day=31, month=12)
            quater_description = 'Oct - Dec'
        
        quater_orders = Order.objects.filter(
            date_enregistrement__gte=first_day_of_quater
            ).filter(
                    date_enregistrement__lte=last_day_of_quater
            )
        for order in quater_orders:
            quater_orders_price += order.somme_finale


        first_day_of_year = date.replace(day=1, month=1)
        last_day_of_year = date.replace(day=31, month=12)
        year_orders = Order.objects.filter(
            date_enregistrement__gte=first_day_of_year
            ).filter(
                    date_enregistrement__lte=last_day_of_year
            )
        for order in year_orders:
            year_orders_price += order.somme_finale
        

        orders = Order.objects.all().order_by('-pk')[:10]
        customers = Customer.objects.filter(statut='actif').order_by('nom_complet')

        return render(request, 'management/dashboard.html', locals())
    else:
        return redirect('management:login')


# I-2 - The log in function => name='login'
@unauthenticated_user
def loginPage(request):
     if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')
          user = authenticate(request, username=username, password=password)

          if user is not None:
               login(request, user)
               return redirect('management:dashboard')
          else:
               messages.info(request, 'Username OR password is incorrect')

     return render(request, 'management/login.html', locals())


# I-3 - the logout function => name='logout'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def logoutUser(request):
    logout(request)
    return redirect('management:login')
    
    
# I-4 - the 404 page function => name='page404'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def page404(request):
    if request.user.is_authenticated:
        return render(request, 'management/error404.html', locals())
    else:
        return redirect('management:login')
    

# I-5 - Email to user function (it takes the user pk) => name='email_customer'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur',])
def emailCustomer(request, customer_pk):
    if request.user.is_authenticated:    

        customer = Customer.objects.get(pk=customer_pk)
        
        if request.method == 'POST':
            subject = 'CheKeyDiA - Notification'
            message = request.POST.get('email_to_customer')
            message += MAIL_FOOTER
            sender = settings.EMAIL_HOST_USER
            receiver = customer.email
            recorder = 'chekeydia@gmail.com'

            if len(message) > 0:
                send_mail(subject, message, sender, [receiver, recorder], fail_silently=False)
                return redirect('management:customer_details', customer.pk)
            else:
                return redirect('management:email_customer', customer.pk)

        return render(request, 'management/send_mail_to_customer_form.html', locals())
    else:
        return redirect('management:login')
    
    
# I-6 - Email broadcast (To all the customers) => name='email_broadcast'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur',])
def emailBroadcast(request):
    if request.user.is_authenticated:    

        customers = Customer.objects.filter(statut='actif')
        
        if request.method == 'POST':
            subject = 'CheKeyDiA - Notification'
            message = request.POST.get('email_broadcast')
            message += MAIL_FOOTER
            sender = settings.EMAIL_HOST_USER
            recorder = 'chekeydia@gmail.com'
        
            if len(message) > 0:
                for customer in customers:
                    receiver = customer.email
                    send_mail(subject, message, sender, [receiver, recorder], fail_silently=False)
                return redirect('management:dashboard')
        
            else:
                return redirect('management:email_broadcast')
        return render(request, 'management/broadcast_mail_form.html', locals())
    else:
        return redirect('management:login')





# End session I
# --------------------------------------------------------------------------------- #
# Start session II (CUSTOMER)


# II - 1 - New customer creation form => name='customer_create'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def customerCreate(request):
    if request.user.is_authenticated:
        form = CustomerCreateForm()
        if request.method == 'POST':
            form = CustomerCreateForm(request.POST)
            if form.is_valid():
                form.save()
                customer = Customer.objects.latest('pk')
                customer.nom_complet = customer.nom_complet.upper()
                customer.save()

                subject = 'AKWABA CheKeyDiA :) !'
                message = "\n#-------------------------------------------------------------------------------#\nCher " +  customer.nom_complet +", \nVotre choix c'est porté sur nous, Toute mon equipe et moi en sommes honorés. \nEn leurs noms et au mien, je vous souhaite la plus cordiale des bienvenues!\nVoici vos informations:: \n\nNom et Prenom:: " + customer.nom_complet + "\nNumero de Tel:: " + customer.telephone + "\nAdresse:: " + customer.adresse + "\nAdresse Email:: " + customer.email + "\nEn cas d'erreur concernant vos informations personnelles, veuillez nous le signaler via l'un de nos contacts.\nMerci de choisir le meilleur pour vous!" + MAIL_FOOTER

                sender = settings.EMAIL_HOST_USER
                receiver = customer.email
                recorder = 'chekeydia@gmail.com'
                send_mail(subject, message, sender, [receiver, recorder], fail_silently=False)

                return redirect('management:customer_details', pk=Customer.objects.latest('pk').pk)
        # print(form)
        return render(request, 'management/customer_create_form.html', locals())
    else:
        return redirect('management:login')


# II - 2 - Customer details function => name='customer_details'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def customerDetails(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all().order_by('date_enregistrement')
    order_count = orders.count()
    return render(request, 'management/customer_details.html', locals()) 


# II - 3 - List view of the customers => name='customer_list'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur',])
def customerList(request):
     if request.user.is_authenticated:
          customers = Customer.objects.filter(statut='actif').order_by('nom_complet')
          return render(request, 'management/customer_list.html', locals())
     else:
          return redirect('management:login')


# II - 4 - Delete (set the status to 'inactif') a customer according to the pk => name='customer_delete'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def customerDelete(request, pk):
     customer = Customer.objects.get(id=pk)

     if request.method == 'POST':          
          customer.statut = 'inactif'
          customer.save()
          return redirect('management:customer_list')

     return render(request, 'management/customer_delete.html', locals())


# II - 5 - Update a Customer according to the pk => name='customer_update'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def customerUpdate(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerCreateForm(instance=customer)
    if request.method == 'POST':
        form = CustomerCreateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            customer.nom_complet = customer.nom_complet.upper()
            customer.save()

            subject = 'CheKeyDiA Notification !'
            message = "\n\n#-------------------------------------------------------------------------------#\nCher " + customer.nom_complet +", \nvotre compte client a été modifié récemment.\nVoici vos nouvelles informations:: \n\nNom et Prenom:: " + customer.nom_complet + "\nNumero de Tel:: " + customer.telephone + "\nAdresse:: " + customer.adresse + "\nAdresse Email:: " + customer.email + "\nEn cas d'erreur concernant vos informations personnelles, veuillez nous le signaler via l'un de nos contacts.\nMerci de choisir le meilleur pour vous!" + MAIL_FOOTER

            sender = settings.EMAIL_HOST_USER
            receiver = customer.email
            recorder = 'chekeydia@gmail.com'
            send_mail(subject, message, sender, [receiver, recorder], fail_silently=False)

            return redirect('management:customer_details', pk=customer.id)

    return render(request, 'management/customer_create_form.html', locals())


# End session II
# --------------------------------------------------------------------------------- #
# Start session III (STOCK)


# III - 1 - List view of the stock => name='stock_list'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def stockList(request):
     if request.user.is_authenticated:
          stocks = []
          stock_remaining = []
          all_prices = products_sold = price_remaining = 0
          all_stock = Stock.objects.all().order_by('-pk')
          for stock in all_stock:
               all_prices += stock.prix_final * stock.quantite
               products_not_sold = stock.product_set.filter(commande=None)
               if len(products_not_sold) > 0:
                    stocks.append(stock)
                    stock_remaining.append(len(products_not_sold))
                    price_remaining += stock.prix_final * len(products_not_sold)
               products_sold += len(stock.product_set.filter(commande__isnull=False))
          sales_amount = all_prices - price_remaining
          unfinished_stocks = len(stocks)
          data = zip(stocks, stock_remaining)


          form = StockCreateForm()
          if request.method == 'POST':
               form = StockCreateForm(request.POST)
               if form.is_valid():
                    form.save()
                    stock = Stock.objects.latest('pk')
                    discount = math.ceil((stock.prix * stock.remise) / 100)
                    stock.prix_final = stock.prix - discount
                    stock.code = stock.code.upper()
                    stock.save()
                    return redirect('management:stock_details', stock.pk)
          return render(request, 'management/stock_list.html', locals())
     else:
          return redirect('management:login')


# III - 2 - Delete a Stock according to the pk => name='stock_delete'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def stockDelete(request, pk):
     stock = Stock.objects.get(id=pk)
     if request.method == 'POST':          
          stock.delete()
          return redirect('management:stock_list')
     return render(request, 'management/stock_delete.html', locals())


# III - 3 - Update a Stock according to the pk => name='stock_update'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def stockUpdate(request, pk):
     stock = Stock.objects.get(id=pk)
     form = StockCreateForm(instance=stock)
     if request.method == 'POST':
          form = StockCreateForm(request.POST, instance=stock)
          if form.is_valid():
               form.save()
            #    stock = Stock.objects.latest('pk')
               discount = math.ceil((stock.prix * stock.remise) / 100)
               stock.prix_final = stock.prix - discount
               stock.code = stock.code.upper()
               stock.save()
               return redirect('management:stock_list',)

     return render(request, 'management/stock_update_form.html', locals())
     

# III - 4 - stock details function => name='stock_details'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def stockDetails(request, pk):
     stock = Stock.objects.get(id=pk)
     products = stock.product_set.filter(commande=None).order_by('-pk')
     products_count = products.count()
     price_remaining = stock.prix_final * products_count

     products_sold = stock.product_set.filter(commande__isnull=False)
     products_sold_count = len(products_sold)
     price_sold = products_sold_count * stock.prix_final

     form = ProductCreateForm()
     if request.method == 'POST':
          form = ProductCreateForm(request.POST)
          if form.is_valid():
               form.save()
               product = Product.objects.latest('pk')
               product.stock = stock
               product.code = product.code.upper()
               product.save()
               stock.quantite += 1
               stock.save()
               return redirect('management:stock_details', pk)
     return render(request, 'management/stock_details.html', locals())



# 5 - Constists of deleting a product from a stock's details view  => name='stock_product_delete'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def stockProductDelete(request, pk):
     product = Product.objects.get(pk=pk)  
     stock = product.stock
     stock.quantite -= 1
     stock.save()       
     product.delete()
     return redirect('management:stock_details', stock.pk)
     # return render(request, 'management/stock_delete.html', locals())


# V - 3 - Update a Poduct according to the pk => name='stock_product_update'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def stockProductUpdate(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductCreateForm(instance=product)
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            product.code = product.code.upper()
            product.save()
            return redirect('management:stock_details', product.stock.pk)

    return render(request, 'management/stock_product_create_form.html', locals())



# End session III
# --------------------------------------------------------------------------------- #
# Start session IV (CATEGORY)


# IV - 1 - List view of the category and new category creation => name='category_list'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur',])
def categoryList(request):
    if request.user.is_authenticated:
        categories = Category.objects.all().order_by('nom')
        form = CategoryCreateForm()
        if request.method == 'POST':
            form = CategoryCreateForm(request.POST)
            if form.is_valid():
                form.save()
                category = Category.objects.latest('pk')
                category.code = category.code.upper()
                category.nom = category.nom.upper()
                category.save()
                return redirect('management:category_list')
        return render(request, 'management/category_list.html', locals())
    else:
        return redirect('management:login')


# IV - 2 - Delete a category according to the pk => name='category_delete'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def categoryDelete(request, pk):
     category = Category.objects.get(id=pk)

     if request.method == 'POST':          
          category.delete()
          return redirect('management:category_list')

     return render(request, 'management/category_delete.html', locals())


# V - 3 - Update a Category according to the pk => name='category_update'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def categoryUpdate(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryCreateForm(instance=category)
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            category.code = category.code.upper()
            category.nom = category.nom.upper()
            category.save()
            return redirect('management:category_list',)

    return render(request, 'management/category_update_form.html', locals())


# End session IV
# --------------------------------------------------------------------------------- #
# Start session V (BRAND)


# V - 1 - List view of the category and new category creation => name='brand_list'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur',])
def brandList(request):
    if request.user.is_authenticated:
        brands = Brand.objects.all().order_by('nom')
        form = BrandCreateForm()
        if request.method == 'POST':
            form = BrandCreateForm(request.POST)
            if form.is_valid():
                form.save()
                brand = Brand.objects.latest('pk')
                brand.code = brand.code.upper()
                brand.nom = brand.nom.upper()
                brand.save()
                return redirect('management:brand_list')
        return render(request, 'management/brand_list.html', locals())
    else:
        return redirect('management:login')


# V - 2 - Delete a brand according to the pk => name='brand_delete'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def brandDelete(request, pk):
     brand = Brand.objects.get(id=pk)

     if request.method == 'POST':          
          brand.delete()
          return redirect('management:brand_list')

     return render(request, 'management/brand_delete.html', locals())


# V - 3 - Update a Brand according to the pk => name='brand_update'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def brandUpdate(request, pk):
    brand = Brand.objects.get(id=pk)
    form = BrandCreateForm(instance=brand)
    if request.method == 'POST':
        form = BrandCreateForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            brand.code = brand.code.upper()
            brand.nom = brand.nom.upper()
            brand.save()
            return redirect('management:brand_list',)

    return render(request, 'management/brand_update_form.html', locals())


# End session V
# --------------------------------------------------------------------------------- #
# Start session VI (USER)


# VI-4 - New Staff member creation form => name='customer_create'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def userCreate(request):
     if request.user.is_authenticated:
          form = UserCreateForm()
          
          if request.method == 'POST':
               form = UserCreateForm(request.POST)
               if form.is_valid():
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    if form.cleaned_data['is_staff'] == True:
                         group = Group.objects.get(name='administrateur')
                         user.groups.add(group)
                    else:
                         group = Group.objects.get(name='employe')
                         user.groups.add(group)

                    employee = User.objects.latest('pk')
                    
                    subject = 'AKWABA CheKeyDiA :) !'
                    message = "\n\n#-------------------------------------------------------------------------------#\nCher" +  employee.first_name + " "+ employee.last_name +", \nVotre choix c'est porté sur nous, Toute l'equipe et moi en sommes honorés. \nEn leurs noms et au mien, je vous souhaite la plus cordiale des bienvenues!\nVoici vos informations:: \n\nNom:: " + employee.last_name + "\nPrenom:: " + employee.first_name + "\nAdresse Email:: " + employee.email + "\n\nEn cas d'erreur concernant vos informations personnelles, veuillez la modifier en vous connectant.\nMerci !" + MAIL_FOOTER

                    sender = settings.EMAIL_HOST_USER
                    receiver = employee.email
                    recorder = 'chekeydia@gmail.com'
                    send_mail(subject, message, sender, [receiver, recorder], fail_silently=False)




                    messages.success(request, 'Account was created for ' + username)
                    return redirect('management:login')
          # print(form)
          return render(request, 'management/user_create_form.html', locals())
     else:
          return redirect('management:login')


# VI - 2 - List view of the users => name='user_list'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur',])
def userList(request):
     if request.user.is_authenticated:
          users = User.objects.filter(is_active=True).order_by('first_name').order_by('last_name').exclude(username=request.user.username)
          return render(request, 'management/user_list.html', locals())
     else:
          return redirect('management:login')


# VI - 3 - Delete (set the 'is_active' to 'False') a user according to the pk => name='user_delete'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def userDelete(request, pk):
     user = User.objects.get(id=pk)

     if request.method == 'POST':          
          user.is_active = False
          user.save()
          return redirect('management:user_list')

     return render(request, 'management/user_delete.html', locals())


# VI - 4 - Delete a User according to the pk => name='user_update'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def userUpdate(request, pk):
    user = User.objects.get(id=pk)
    form = UserCreateForm(instance=user)
    if request.method == 'POST':
        form = UserCreateForm(request.POST, instance=user)
        if form.is_valid():
            if form.cleaned_data['is_staff'] == True:
                group = Group.objects.get(name='administrateur')
                user.groups.add(group)
            form.save()
            
            return redirect('management:user_list')

    return render(request, 'management/user_create_form.html', locals())


# End session VI
# --------------------------------------------------------------------------------- #
# Start session VII (ORDER)


# VII- 1 - New Order creation form => name='order_create'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def orderCreate(request, pk):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=pk)
        form = OrderCreateForm(initial={'client':customer})
        form.fields['client'].widget = forms.HiddenInput()
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                form.save()
                order_pk = Order.objects.latest('pk').pk
                return redirect('management:product_create', order_pk)

        return render(request, 'management/order_create_form.html', locals())
    else:
        return redirect('management:login')


# VII- 2 - Save the current order and apply all the necessary changes (modify to total expense of the customer) => name='order_save'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def orderSave(request, pk, old_total):
    order = Order.objects.get(pk= pk)
    order.client.total_des_depenses += order.somme_finale - old_total
    order.client.save()
    
    subject = 'CheKeyDiA Facture n:: 000' + str(order.pk)
    message = "\n#-------------------------------------------------------------------------------#\nCher " +  order.client.nom_complet +", \n\nMerci d'avoir acheté chez nous.\n Voici les détails de votre commande:: \n \nDate de la commande:: " + order.date_enregistrement.strftime("%A, the %dth %B %Y") + "\nStatut:: " + order.statut + "\nNombre de pièces:: " + str(order.total_pcs) + "\nSomme Total:: " + str(order.montant_total) + " FCFA\nRemise:: " + str(order.remise) + " %\nSomme Finale (après remise):: " + str(order.somme_finale) + " FCFA\n\nEn cas d'erreur concernant vos informations personnelles, veuillez nous le signaler via l'un de nos contacts.\nMerci de choisir le meilleur pour vous!" + MAIL_FOOTER
    sender = settings.EMAIL_HOST_USER
    receiver = order.client.email
    recorder = 'chekeydia@gmail.com'
    send_mail(subject, message, sender, [receiver, recorder], fail_silently=False)
    return redirect('management:customer_details', pk=order.client.pk)


# VII- 3 - Delete the current order from the user details view and apply all the necessary changes => name='order_delete_from_details'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def orderDeleteFromDetails(request, pk):
     order = Order.objects.get(id=pk)
     customer = order.client

     if request.method == 'POST':
          customer.total_des_depenses -= order.somme_finale
          customer.save()
          order.delete()
          return redirect('management:customer_details', customer.pk)

     return render(request, 'management/order_delete_customer.html', locals())


# VII- 4 - Delete the current order from the dashboard and apply all the necessary changes => name='order_delete_from_details'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def orderDeleteFromDash(request, pk):
     order = Order.objects.get(id=pk)
     customer = order.client

     if request.method == 'POST':
          customer.total_des_depenses -= order.somme_finale
          customer.save()
          order.delete()
          return redirect('management:dashboard')

     return render(request, 'management/order_delete_dash.html', locals())


# VII- 4 - Update the current order from the Detail View of the Customer and apply all the necessary changes => name='order_update'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur'])
def orderUpdate(request, pk, old_total):
    order = Order.objects.get(id=pk)
    customer = order.client
    form = OrderCreateForm(instance=order)
    form.fields['client'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
          #   print(old_total)
            return redirect('management:product_update', order.pk, old_total)

    return render(request, 'management/order_create_form.html', locals())


# End session VII
# --------------------------------------------------------------------------------- #
# Start session VIII (PRODUCT)


# VIII- 1 - New Product creation form (with order id) => name='product_create'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def productCreate(request, pk):
     if request.user.is_authenticated:
          error = request.session['error'] = ''
          order = Order.objects.get(pk= pk)
          products = order.product_set.all()
          old_total = 0
          # discount = (order.discount * order.total_amount) / 100
          # a = order.grand_total = order.total_amount - discount
          # print(products)
          # order.save()
          form = ProductAddForm()
          if request.method == 'POST':
               form = ProductAddForm(request.POST)
               if form.is_valid():
                    try:
                         product = Product.objects.get(code=form.cleaned_data['code'].upper())
                    except:
                         product = None
                    
                    if product and product.commande is None:
                         product.commande = order
                         product.save()

                         order.total_pcs += 1
                         order.montant_total += product.stock.prix_final
                         discount = math.ceil((order.remise * order.montant_total) / 100)
                         order.somme_finale = order.montant_total - discount
                         order.save()
                         error = request.session['error'] = ''

                    elif product and product.commande is not None:
                         error = request.session['error'] = 'Produit deja vendu :('
                         return render(request, 'management/product_create_form.html', locals())
                    else:
                         request.session['error'] = 'Produit Inexistant :('
                         error = request.session['error'] 
                         return render(request, 'management/product_create_form.html', locals())
                    # return render(request, 'management/add_item.html', locals())
                    return redirect('management:product_create', pk)
          return render(request, 'management/product_create_form.html', locals())
     else:
          return redirect('management:login')


# VIII- 2 - Delete an Product (item) from the current (selected) Order => name='product_delete'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def productDelete(request, order_pk, product_pk):
    if request.user.is_authenticated:

        order = Order.objects.get(pk= order_pk)
        order.total_pcs -= 1
        product = order.product_set.get(pk=product_pk)
        order.montant_total -= product.stock.prix_final
        discount = math.ceil((order.remise * order.montant_total) / 100)
        order.somme_finale = order.montant_total - discount
        order.save()

        product.commande = None
        product.save()
        return redirect('management:product_create', order_pk)
    else:
        return redirect('management:login')


# VIII- 3 - Consists of mofifying the Products list from a given Order => name='product_update'
@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur',])
def productUpdate(request, order_pk, old_total):
     if request.user.is_authenticated:
          error = request.session['error'] = ''
          order = Order.objects.get(pk= order_pk)
          products = order.product_set.all()
          discount = math.ceil((order.remise * order.montant_total) / 100)
          order.somme_finale = order.montant_total - discount
          order.save()
          form = ProductAddForm()
          if request.method == 'POST':
               form = ProductAddForm(request.POST)
               if form.is_valid():
                    
                    try:
                         product = Product.objects.get(code=form.cleaned_data['code'].upper())
                    except:
                         product = None
                    
                    if product and product.commande is None:
                         product.commande = order
                         product.save()

                         order.total_pcs += 1
                         order.montant_total += product.stock.prix_final
                         discount = math.ceil((order.remise * order.montant_total) / 100)
                         order.somme_finale = order.montant_total - discount
                         order.save()
                         error = request.session['error'] = ''

                    elif product and product.commande is not None:
                         error = request.session['error'] = 'Produit deja vendu'
                         return render(request, 'management/product_update_form.html', locals())
                    else:
                         request.session['error'] = 'Produit Inexistant'
                         error = request.session['error'] 
                         return render(request, 'management/product_update_form.html', locals())
                         # return redirect('management:update_create_item', order_pk, old_total)
                    # return render(request, 'management/add_item.html', locals())
                    return redirect('management:product_update', order_pk, old_total)
          return render(request, 'management/product_update_form.html', locals())
     else:
          return redirect('management:login')


# VIII - 3 - 

@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def productDeleteWhileModifying(request, order_pk, product_pk, old_total):
     if request.user.is_authenticated:
          order = Order.objects.get(pk=order_pk)
          order.total_pcs -= 1
          product = order.product_set.get(pk=product_pk)
          order.montant_total -= product.stock.prix_final
          discount = math.ceil((order.remise * order.montant_total) / 100)
          order.somme_finale = order.montant_total - discount
          order.save()
               
          product.commande = None
          product.save()
          # print(product)
          return redirect('management:product_update', order_pk, old_total)
     else:
          return redirect('management:login')


# VIII - 4 - 

@login_required(login_url='management:login')
@allowed_users(allowed_roles=['administrateur', 'employe'])
def updateCustomerTotalAdd(request, order_pk, old_total):
    order = Order.objects.get(pk= order_pk)
    order.client.total_des_depenses += order.somme_finale
    order.client.total_des_depenses -= old_total
    order.client.save()

    subject = 'CheKeyDiA Facture n:: 000' + str(order.pk)
    message = "\n#-------------------------------------------------------------------------------#\nCher " +  order.client.nom_complet +", \n \nVotre facture 000" + str(order.pk) + " a été modifié.\nVoici les détails de votre commande:: \n\nDate de la commande:: " + order.date_enregistrement.strftime("%A, the %dth %B %Y") + "\nStatut:: " + order.statut + "\nNombre de pièces:: " + str(order.total_pcs) + "\nSomme Total:: " + str(order.montant_total) + " FCFA\nRemise:: " + str(order.remise) + " %\nSomme Finale (après remise):: " + str(order.somme_finale) + " FCFA\nEn cas d'erreur concernant vos informations personnelles, veuillez nous le signaler via l'un de nos contacts.\nMerci de choisir le meilleur pour vous!" + MAIL_FOOTER
    sender = settings.EMAIL_HOST_USER
    receiver = order.client.email
    recorder = 'chekeydia@gmail.com'
    send_mail(subject, message, sender, [receiver, recorder], fail_silently=False)

    return redirect('management:customer_details', pk=order.client.pk)