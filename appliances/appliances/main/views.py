from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Category, Product, Order, OrderItem
from .forms import OrderForm
from decimal import Decimal


def special_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('special_access_granted'):
            return redirect('no_access')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def is_superuser(user):
    return user.is_superuser

def get_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0')
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        subtotal = product.price * Decimal(str(quantity))
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    
    return cart_items, total

@login_required(login_url='login')
def index(request):
    featured_products = Product.objects.filter(available=True, featured=True).order_by('featured_order', '-created')[:8]
    if featured_products.exists():
        products = featured_products
    else:
        products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    admin_products = Product.objects.filter(available=True) if request.user.is_superuser else None
    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'admin_products': admin_products,
    })

@login_required(login_url='login')
@permission_required('main.request_employee_data', raise_exception=True)
def toggle_featured(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.featured = not product.featured
        if product.featured and product.featured_order == 0:
            product.featured_order = Product.objects.filter(featured=True).count() + 1
        product.save()
    return redirect('index')

@login_required(login_url='login')
def catalog(request):
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
    else:
        products = Product.objects.filter(available=True)
        category = None
    
    categories = Category.objects.all()
    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
    })

@login_required(login_url='login')
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'product_detail.html', {'product': product})

@login_required(login_url='login')
@special_access_required
@permission_required('main.request_employee_data', raise_exception=True)
def cart_view(request):
    cart_items, total = get_cart(request)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required(login_url='login')
@special_access_required
@permission_required('main.request_employee_data', raise_exception=True)
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = 1
    request.session['cart'] = cart

    return redirect('cart')

@login_required(login_url='login')
@special_access_required
@permission_required('main.request_employee_data', raise_exception=True)
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('cart')

@login_required(login_url='login')
@special_access_required
@permission_required('main.request_employee_data', raise_exception=True)
def cart_update(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
        request.session['cart'] = cart
  
    return redirect('cart')

@login_required(login_url='login')
@special_access_required
@permission_required('main.request_employee_data', raise_exception=True)
def checkout(request):
    cart_items, total = get_cart(request)
    
    if not cart_items:
        return redirect('catalog')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = Decimal('0')
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )
            
            request.session['cart'] = {}
       
            return redirect('order_success', order_id=order.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderForm(initial=initial_data)
    
    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    })

@login_required(login_url='login')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})