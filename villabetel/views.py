from django.shortcuts import render
from django.views import View
# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
import json
from django.db import transaction
from decimal import Decimal
from django.db.models import F

from .forms import UserLoginForm, UserSignUpForm,ProductForm, ProductFormEdit, AreaForm, TableForm, TableFormEdit, AreaFormEdit, CategoryForm, CategoryFormEdit, WaiterForm, WaiterFormEdit
from .models import Product, Category, Area, Table, Category, Waiter, UserProfile, Invoice, Account, ProductQuantity

def home(request):
    return render(request, 'views/index.html')

def index(request):
    loginForms = UserLoginForm()
    return render(request, 'views/auth/login.html', {'loginForms' : loginForms })
def signupview(request):
    signupForms = UserSignUpForm()
    return render(request, 'views/auth/register.html', {'signupForms' : signupForms })

def login_view(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                # El usuario ha sido autenticado, puedes redirigirlo a una página de bienvenida
                return redirect('villabetel:home')  # Cambia 'welcome_view' por la URL de tu página de bienvenida
    else:
        loginForms = UserLoginForm()
    loginForms = UserLoginForm()
    return render(request, 'views/auth/login.html', {'loginForms': loginForms})



def signup(request):
    signup_form = UserSignUpForm(request.POST or None)
    if signup_form.is_valid():
        email = signup_form.cleaned_data.get('email')
        first_name = signup_form.cleaned_data.get('first_name')
        document_number = signup_form.cleaned_data.get('document_number')
        last_name = signup_form.cleaned_data.get('last_name')
        password = signup_form.cleaned_data.get('password')
        try:
            user = get_user_model().objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                document_number=document_number,
                password=make_password(password),
                is_active=True
            )
            login(request, user)
            return redirect('villabetel:home')

        except Exception as e:
            print(e)
            return JsonResponse({'detail': f'{e}'})

    messages.warning(request, 'Las Contrasenas no coinciden')
    return redirect('inde')

def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='index')
def profile_view(request):
    return render(request, 'user/profile.html')


def user_detail(request, slug):
    user_detail = get_object_or_404(get_user_model(), slug=slug)
    if not request.user.is_authenticated:
        messages.warning(request, 'Debes Iniciar sesion para mas funcionalidades')

    return render(request, 'user/user_detail.html', {'user_detail': user_detail})


# Funciones para Parametros
# Productos
def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    forms = ProductForm()
    product_forms = [(product, ProductFormEdit(instance=product)) for product in products]
    return render(request, 'views/parameters/products/product_list.html', {'product_forms': product_forms, 'categories': categories, 'forms': forms})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'views/products/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el producto en la base de datos
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('villabetel:productlist')  # Redirigir a la lista de productos
        else:
            messages.error(request, 'Hubo un error al crear el producto. Verifica los datos ingresados.')
    return redirect('villabetel:productlist')  # Redirigir a la lista de productos si no es un POST

def product_update(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_name = request.POST.get('category')  # Obtener el nombre de la categoría desde el formulario

        # Buscar la instancia de Category correspondiente por nombre
        category = Category.objects.get(name=category_name)

        # Obtener la instancia de Product a actualizar
        product = get_object_or_404(Product, pk=pk)

        # Asignar los nuevos valores
        product.name = name
        product.description = description
        product.price = price
        product.category = category  # Asignar la instancia de Category

        product.save()

    return redirect('villabetel:productlist')

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    
    return redirect('villabetel:productlist')  # Redirigir a la lista de productos


# Zonas
def area_list(request):
    areas = Area.objects.all()
    forms = AreaForm()
    product_forms = [(area, AreaFormEdit(instance=area)) for area in areas]
    return render(request, 'views/parameters/areas/area_list.html', {'product_forms': product_forms, 'forms': forms})

def area_detail(request, pk):
    area = get_object_or_404(Area, pk=pk)
    return render(request, 'views/areas/area_detail.html', {'area': area})

def area_create(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el producto en la base de datos
            messages.success(request, 'Area creado exitosamente.')
            return redirect('villabetel:arealist')  # Redirigir a la lista de productos
        else:
            messages.error(request, 'Hubo un error al crear el area. Verifica los datos ingresados.')
    return redirect('villabetel:arealist')  # Redirigir a la lista de productos si no es un POST

def area_update(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        # Obtener la instancia de Area a actualizar
        area = get_object_or_404(Area, pk=pk)

        # Asignar los nuevos valores
        area.name = name
        area.save()

    return redirect('villabetel:arealist')

def area_delete(request, pk):
    product = get_object_or_404(Area, pk=pk)
    if request.method == 'POST':
        product.delete()
    
    return redirect('villabetel:arealist')  # Redirigir a la lista de productos



# Categorias
def category_list(request):
    categorias = Category.objects.all()
    forms = CategoryForm()
    product_forms = [(category, CategoryFormEdit(instance=category)) for category in categorias]
    return render(request, 'views/parameters/categories/category_list.html', {'product_forms': product_forms, 'forms': forms})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'views/parameters/categories/area_detail.html', {'category': category})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el producto en la base de datos
            messages.success(request, 'Category creado exitosamente.')
            return redirect('villabetel:categorylist')  # Redirigir a la lista de productos
        else:
            messages.error(request, 'Hubo un error al crear el area. Verifica los datos ingresados.')
    return redirect('villabetel:categorylist')  # Redirigir a la lista de productos si no es un POST

def category_update(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        # Obtener la instancia de Category a actualizar
        category = get_object_or_404(Category, pk=pk)

        # Asignar los nuevos valores
        category.name = name
        category.save()

    return redirect('villabetel:categorylist')

def category_delete(request, pk):
    product = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        product.delete()
    
    return redirect('villabetel:categorylist')  # Redirigir a la lista de productos


# Mesas
def table_list(request):
    areas = Area.objects.all()
    tables = Table.objects.all()
    forms = TableForm()
    product_forms = [(table, TableFormEdit(instance=table)) for table in tables]
    return render(request, 'views/parameters/tables/table_list.html', {'product_forms': product_forms, 'areas': areas, 'forms': forms})

def table_detail(request, pk):
    table = get_object_or_404(Table, pk=pk)
    return render(request, 'views/tables/table_detail.html', {'table': table})

def table_create(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el producto en la base de datos
            messages.success(request, 'Mesa creado exitosamente.')
            return redirect('villabetel:tablelist')  # Redirigir a la lista de productos
        else:
            messages.error(request, 'Hubo un error al crear la mesa. Verifica los datos ingresados.')
    return redirect('villabetel:tablelist')  # Redirigir a la lista de productos si no es un POST

def table_update(request, pk):
    if request.method == 'POST':
        number = request.POST.get('number')
        area = request.POST.get('area') 

        # Buscar la instancia de Category correspondiente por nombre
        area = Area.objects.get(name=area)

        # Obtener la instancia de Product a actualizar
        table = get_object_or_404(Table, pk=pk)

        # Asignar los nuevos valores
        table.number = number

        table.area = area  # Asignar la instancia de Category

        table.save()

    return redirect('villabetel:tablelist')

def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        table.delete()
    
    return redirect('villabetel:tablelist')  # Redirigir a la lista de productos


# Meseros
def waiter_list(request):
    waiters = Waiter.objects.all()
    forms = WaiterForm()
    waiter_forms = [(waiter, WaiterFormEdit(instance=waiter)) for waiter in waiters]
    return render(request, 'views/parameters/waiters/waiter_list.html', {'waiter_forms': waiter_forms, 'forms': forms})

def waiter_detail(request, pk):
    waiter = get_object_or_404(Waiter, pk=pk)
    return render(request, 'views/parameters/waiters/waiter_detail.html', {'waiter': waiter})

def waiter_create(request):
    if request.method == 'POST':
        form = WaiterForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el mesero en la base de datos
            messages.success(request, 'Mesero creado exitosamente.')
            return redirect('villabetel:waiterlist')  # Redirige a la lista de meseros
        else:
            messages.error(request, 'Hubo un error al crear el mesero. Verifica los datos ingresados.')
    return redirect('villabetel:waiterlist')  # Redirige a la lista de meseros si no es un POST

def waiter_update(request, pk):
    if request.method == 'POST':
        user_profile_id = request.POST.get('user_profile')
        nickname = request.POST.get('nickname')
        
        # Obtén el objeto UserProfile seleccionado
        user_profile = UserProfile.objects.get(pk=user_profile_id)
        
        # Obtén el mesero a actualizar
        waiter = get_object_or_404(Waiter, pk=pk)
        
        # Asigna los nuevos valores
        waiter.user_profile = user_profile
        waiter.nickname = nickname
        
        # Guarda los cambios
        waiter.save()
        
        # Redirige a la página que desees después de la edición
        return redirect('villabetel:waiterlist')
    waiters = Waiter.objects.all()
    waiter_forms = [(waiter, WaiterFormEdit(instance=waiter)) for waiter in waiters]
    return render(request, 'views/parameters/waiters/edit_waiter_form.html', {'waiter_forms': waiter_forms})


def waiter_delete(request, pk):
    waiter = get_object_or_404(Waiter, pk=pk)
    if request.method == 'POST':
        waiter.delete()

    return redirect('villabetel:waiterlist')  # Redirigir a la lista de meseros

def load_create_form(request):
    forms = WaiterForm()
    return render(request, 'views/parameters/waiters/create_waiter_form.html', {'forms': forms})


def search_user_profile(request):
    if request.method == 'GET':
        search_term = request.GET.get('search_term', '')

        # Realiza una búsqueda en los perfiles de usuario donde el número de documento coincide exactamente con el término de búsqueda
        results = UserProfile.objects.filter(document_number=search_term)

        # Crea una lista de resultados
        results = [{'id': profile.pk, 'text': profile.__str__()} for profile in results]

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)


def sale_home(request):
    # Obtiene todas las áreas
    areas = Area.objects.all()

    # Crea un diccionario que asocia cada área con sus mesas
    area_tables = {area: Table.objects.filter(area=area) for area in areas}

    context = {
        'areas': areas,
        'area_tables': area_tables,
    }

    return render(request, 'views/sales/sale_home.html', context)

def sale_account(request, table_id):
    # Obtén la mesa asociada al ID proporcionado
    table = get_object_or_404(Table, id=table_id)

    # Obtén la lista de productos disponibles agrupados por categoría
    categories = Category.objects.all()
    products_by_category = {category: Product.objects.filter(category=category) for category in categories}

    # Obtén la lista de meseros
    waiters = Waiter.objects.all()

    # Obtén la fecha actual
    current_date = datetime.now()

    # Renderiza la plantilla 'sale_account.html', pasando la información necesaria
    return render(request, 'views/sales/sale_account.html', {
        'table': table,
        'products_by_category': products_by_category,
        'waiters': waiters,
        'current_date': current_date,
    })
    
def get_account_json(request, mesa_id):
    try:
        # Obtener la cuenta pendiente para la mesa específica
        account = Account.objects.filter(table__id=mesa_id, state='Pendiente').first()

        if account:
            # Obtener los productos y cantidades asociados a la cuenta
            products_and_quantities = ProductQuantity.objects.filter(account=account)
            print(products_and_quantities)
            # Construir la respuesta JSON
            response_data = {
                'waiter_id': account.waiter.pk,
                'products': [
                    {
                        'product_id': pq.product.pk,
                        'product_name': pq.product.name,
                        'product_price': pq.product.price,
                        'quantity': pq.quantity,
                    }
                    for pq in products_and_quantities
                ],
                'total': account.price,
                'account_state': account.state,
            }

            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'No se encontró una cuenta pendiente para esta mesa.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    
def update_account(request):
    try:
        mesa_id = request.POST.get('table_id')
        waiter_id = request.POST.get('waiter')
        products_json = request.POST.get('products')
        inputtotal = request.POST.get('total')
        print("Products JSON:", products_json) 
        products_list = json.loads(products_json) if products_json else []
        print("Products List:", products_list)

        with transaction.atomic():
            account = Account.objects.filter(table__id=mesa_id, state='Pendiente').first()
            print(account)

            if account:
                print('paso1')
                account.waiter = get_object_or_404(Waiter, pk=waiter_id)
                total = Decimal('0.00')  # Inicializar el total como un Decimal

                for product_data in products_list:
                    product_id = product_data['id']
                    quantity = product_data['quantity']
                    product = get_object_or_404(Product, pk=product_id)

                    # Intentar obtener el objeto ProductQuantity existente
                    product_quantity, created = ProductQuantity.objects.get_or_create(
                        account=account,
                        product=product,
                        defaults={'quantity': quantity}
                    )

                    # Si ya existe, actualiza la cantidad y el total, de lo contrario, crea un nuevo registro
                    if not created:
                        product_quantity.quantity = quantity
                        product_quantity.save()

                    

                # Actualizar el total de la cuenta
                print(inputtotal)
                account.price = inputtotal
                account.save()
            else:
                print('paso2')
                table = get_object_or_404(Table, pk=mesa_id)
                waiter = get_object_or_404(Waiter, pk=waiter_id)
                total = Decimal('0.00')  # Inicializar el total como un Decimal

                new_account = Account.objects.create(
                    table=table,
                    waiter=waiter,
                    state='Pendiente',
                    price=total  # Asegúrate de asignar el total al campo price
                )

                for product_data in products_list:
                    product_id = product_data['id']
                    quantity = product_data['quantity']
                    product = get_object_or_404(Product, pk=product_id)
                    ProductQuantity.objects.create(account=new_account, product=product, quantity=quantity)

                    

                # Actualizar el total de la cuenta
                new_account.price = inputtotal
                new_account.save()

        return redirect('villabetel:sale_home')  # Redirigir a la lista de meseros
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



