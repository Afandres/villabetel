from django import forms
from .models import Product, Table, Area, Category, Waiter, Account


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'id': 'loginEmail',
                'type': 'email',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'loginPassword',
            'type': 'password',
            'class': 'form-control',
        })
    )


class UserSignUpForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'id': 'signupEmail',
                'type': 'email',
                'class': 'form-control'
            }
        )
    )

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control'
            }
        ))
    
    document_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'form-control'
            }
        ))

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control'
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'signupPassword',
                'type': 'password',
                'class': 'form-control'
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control'
            }
        ))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las Contraseñas no coinciden')
        return cd['password2']

# Formulario Produtos
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = None  # Esto elimina la opción vacía

class ProductFormEdit(forms.ModelForm):
    class Meta:
        model = Product  # Relaciona el formulario con un modelo si es necesario
        fields = ['name', 'description', 'price', 'category']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
class CategoryFormEdit(forms.ModelForm):
    class Meta:
        model = Category  # Relaciona el formulario con un modelo si es necesario
        fields = ['name']
        
class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name']
        
class AreaFormEdit(forms.ModelForm):
    class Meta:
        model = Area  # Relaciona el formulario con un modelo si es necesario
        fields = ['name']
        
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'area']
        widgets = {
            'area': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].empty_label = None  # Esto elimina la opción vacía
        
class TableFormEdit(forms.ModelForm):
    class Meta:
        model = Table  # Relaciona el formulario con un modelo si es necesario
        fields = ['number', 'area']
        
class WaiterForm(forms.ModelForm):
    class Meta:
        model = Waiter
        fields = ['user_profile', 'nickname']  # Agrega otros campos relacionados a UserProfile si es necesario

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_profile'].widget = forms.Select(attrs={'class': 'form-control'})  # Personaliza el widget según tus necesidades
        self.fields['user_profile'].empty_label = None  # Elimina la opción vacía en el campo user_profile
        
class WaiterFormEdit(forms.ModelForm):
    class Meta:
        model = Waiter
        fields = ['user_profile', 'nickname']  # Agrega otros campos relacionados a UserProfile si es necesario

class AccountForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Account
        fields = ['table', 'products', 'ammount', 'price', 'state']