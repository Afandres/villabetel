from django.urls import path

from . import views


app_name = 'villabetel'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<slug:slug>', views.user_detail, name='user_detail'),
    path('signupview/', views.signupview, name='signupview'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # ------------Parametros--------------
    # Productos
    path('products/', views.product_list, name='productlist'),
    path('products/<int:pk>/', views.product_detail, name='productdetail'),
    path('products/create/', views.product_create, name='productcreate'),
    path('products/<int:pk>/update/', views.product_update, name='productupdate'),
    path('products/<int:pk>/delete/', views.product_delete, name='productdelete'),
    
    # Zonas
    path('areas/', views.area_list, name='arealist'),
    path('areas/<int:pk>/', views.area_detail, name='areadetail'),
    path('areas/create/', views.area_create, name='areacreate'),
    path('areas/<int:pk>/update/', views.area_update, name='areaupdate'),
    path('areas/<int:pk>/delete/', views.area_delete, name='areadelete'),
    
    # Categorias
    path('categorias/', views.category_list, name='categorylist'),
    path('categorias/<int:pk>/', views.category_detail, name='categorydetail'),
    path('categorias/create/', views.category_create, name='categorycreate'),
    path('categorias/<int:pk>/update/', views.category_update, name='categoryupdate'),
    path('categorias/<int:pk>/delete/', views.category_delete, name='categorydelete'),
    
    # Mesas
    path('mesas/', views.table_list, name='tablelist'),
    path('mesas/<int:pk>/', views.table_detail, name='tabledetail'),
    path('mesas/create/', views.table_create, name='tablecreate'),
    path('mesas/<int:pk>/update/', views.table_update, name='tableupdate'),
    path('mesas/<int:pk>/delete/', views.table_delete, name='tabledelete'),
    
    # Meseros
    path('waiters/', views.waiter_list, name='waiterlist'),
    path('waiters/<int:pk>/', views.waiter_detail, name='waiterdetail'),
    path('load_create_form/', views.load_create_form, name='load_create_form'),
    path('waiters/create/', views.waiter_create, name='waitercreate'),
    path('waiters/<int:pk>/update/', views.waiter_update, name='waiterupdate'),
    path('waiters/<int:pk>/delete/', views.waiter_delete, name='waiterdelete'),
      

    # Ruta para buscar perfiles de usuario
    path('search_user_profile/', views.search_user_profile, name='search_user_profile'),
    
    # Ventas
    path('sales/home/', views.sale_home, name='sale_home'),
    path('sale_account/<int:table_id>/', views.sale_account, name='sale_account'),
    path('api/get_account/<int:mesa_id>/', views.get_account_json, name='get_account_json'),
    path('api/update_account/', views.update_account, name='update_account'),

]
