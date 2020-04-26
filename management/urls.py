from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [

# I - GENERAL LINKS

     # 1 - if the field is still empty, return the dashboard fuction
     path('', views.dashboard, name='dashboard'),

     # 2 - Consists of displaying the loging page if the user is not already logged in
     path('login/', views.loginPage, name='login'),

     # 3 - Consits of logging out the current user connected
     path('logout/', views.logoutUser, name='logout'),
     
     # 4 - Consits of displaying the 404 page
     path('page404/', views.page404, name='page404'),
     
     # 5 - Consits of sending a customed email to a specified customer
     path('email_customer/<int:customer_pk>', views.emailCustomer, name='email_customer'),
     
     # 6 - Consits of sending a customed email to a specified customer
     path('email_broadcast/', views.emailBroadcast, name='email_broadcast'),
     

# ------------------------------------------------------------------------------------- #

# II - CUSTOMER LINKS

     # 1 - Constists of creating a new customer 
     path('customer_create/', views.customerCreate, name='customer_create'),

     # 2 - Constists of generating the details view of a specified customer 
     path('customer_details/<int:pk>', views.customerDetails, name='customer_details'),

     # 3 - Constists of generating the list of all the customers 
     path('customer_list/', views.customerList, name='customer_list'),

     # 4 - Consists of deleting a given customer according to the pk
     path('customer_delete/<int:pk>/', views.customerDelete, name='customer_delete'),

     # 5 - Consists of updating a given customer according to the pk
     path('customer_update/<int:pk>/', views.customerUpdate, name='customer_update'),

# ------------------------------------------------------------------------------------- #

# III - STOCK LINKS

     # 1 - Consits of returning the general informations concerning the stocks
     path('stock_list', views.stockList, name='stock_list'),

     # 2 - Consists of deleting a given Stock according to the pk
     path('stock_delete/<int:pk>/', views.stockDelete, name='stock_delete'),
     
     # 3 - Consists of updating a given Stock according to the pk
     path('stock_update/<int:pk>/', views.stockUpdate, name='stock_update'),

     # 4 - Constists of generating the details view of a specified stock 
     path('stock_details/<int:pk>', views.stockDetails, name='stock_details'),
     
     # 5 - Constists of deleting a product from a stock's details view  
     path('stock_product_delete/<int:pk>/', views.stockProductDelete, name='stock_product_delete'),

     # 6 - Constists of updating a product from a stock's details view  
     path('stock_product_update/<int:pk>/', views.stockProductUpdate, name='stock_product_update'),

# ------------------------------------------------------------------------------------- #

# IV - CATEGORY LINKS

     # 1 - Consits of returning the general informations concerning the categories
     path('category_list', views.categoryList, name='category_list'),
     
     # 2 - Consists of deleting a given category according to the pk
     path('category_delete/<int:pk>/', views.categoryDelete, name='category_delete'),

     # 3 - Consists of updating a given Category according to the pk
     path('category_update/<int:pk>/', views.categoryUpdate, name='category_update'),

# ------------------------------------------------------------------------------------- #

# V - BRAND LINKS

     # 1 - Consits of returning the general informations concerning the brands
     path('brand_list', views.brandList, name='brand_list'),
     
     # 2 - Consists of deleting a given brand according to the pk
     path('brand_delete/<int:pk>/', views.brandDelete, name='brand_delete'),

     # 3 - Consists of updating a given Brand according to the pk
     path('brand_update/<int:pk>/', views.brandUpdate, name='brand_update'),

# ------------------------------------------------------------------------------------- #

# VI - USER LINKS
     
     # 1 - Constists of creating a new staff member (User) 
     path('user_create/', views.userCreate, name='user_create'),

     # 2 - Constists of generating the list of all the users 
     path('user_list/', views.userList, name='user_list'),

     # 3 - Consists of deleting a given User according to the pk
     path('user_delete/<int:pk>/', views.userDelete, name='user_delete'),

     # 4 - Consists of updating a given User according to the pk
     path('user_update/<int:pk>/', views.userUpdate, name='user_update'),
     
# ------------------------------------------------------------------------------------- #

# VII - ORDER LINKS
     # 1 - Constists of creating a new Order (Customer pk)
     path('order_create/<int:pk>/', views.orderCreate, name='order_create'),  

     # 2 - Constists of making all the changes to the current (last) bill (pk:order pk)
     path('order_save/<int:pk>/<int:old_total>/', views.orderSave, name='order_save'),   

     # 3 - Consists of deleting an Order according to the user pk (From: customer_details)
     path('order_delete_from_details/<int:pk>/', views.orderDeleteFromDetails, name='order_delete_from_details'),
     
     # 4 - Consists of deleting an Order according to the user pk (From: customer_details)
     path('order_delete_from_dash/<int:pk>/', views.orderDeleteFromDash, name='order_delete_from_dash'),

     # 5 - Consists of updating an existing order and change the customer expenditure 
     path('order_update/<int:pk>/<int:old_total>/', views.orderUpdate, name='order_update'),

# ------------------------------------------------------------------------------------- #

# VIII - PRODUCT LINKS
     # 1 - Constists of creating a new Product (order.pk) 
     path('product_create/<int:pk>/', views.productCreate, name='product_create'),

     # 2 - Consists of deleting a Product from an Order
     path('product_delete/<int:order_pk>/<int:product_pk>', views.productDelete, name='product_delete'),

     # 3 - Consists of mofifying the Products list from a given Order
     path('product_update/<int:order_pk>/<int:old_total>/', views.productUpdate, name='product_update'),

     # 3 - Consists of mofifying the Products list from a given Order while updating
     path('product_delete_while_modifying/<int:order_pk>/<int:product_pk>/<int:old_total>/', views.productDeleteWhileModifying, name='product_delete_while_modifying'),
     
     # 4 - 
     path('update_bill_validation/<int:order_pk>/<int:old_total>/', views.updateCustomerTotalAdd, name='update_bill_validation'),

]