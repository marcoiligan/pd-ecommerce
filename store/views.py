from tkinter import E
from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, VariationCategory, Variation, ReviewRating, ProductGallery
from orders.models import OrderProduct
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
# Create your views here.
def home(request):
    products = list(Product.objects.all().filter(is_available=True).order_by('created_date'))
    for i in range(0, len(products)):
        if Variation.objects.filter(product=products[i]).exists():
            print(products[i].product_name)
            reviews = ReviewRating.objects.filter(product_id=products[i].id, status=True)
        else:
            print("False")
            products[i].delete()
    context = {
        'products':products,
        'reviews':reviews
    }
    return render(request, 'home.html', context)

def store(request, category_slug=None):
    category = None
    products = None

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category, is_available=True).order_by('id')
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
    for i in range(0, len(products)):
        if Variation.objects.filter(product=products[i]).exists():
            print(products[i].product_name)
            reviews = ReviewRating.objects.filter(product_id=products[i].id, status=True)
        else:
            print("False")
            products[i].delete()
    context = {
        'products':page_products,
        'product_count': products.count(),
        'reviews': reviews
    }
    return render(request, 'store/store.html', context)

def product(request, category_slug, product_slug):
    product = None
    variation_dict = {}
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        variations = VariationCategory.objects.all().reverse()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
    else:
        orderproduct = None
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    product_gallery = ProductGallery.objects.filter(product_id=product.id)
    
    for variation in reversed(variations):
        if Variation.objects.all().filter(product=product,variation_category=variation):
            variation_dict[variation] = Variation.objects.all().filter(product=product,variation_category=variation).reverse()
    
    context = {
        'product':product,
        'in_cart': in_cart,
        'variations': variation_dict.items,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product-detail.html', context)

def search(request):
    products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword) | Q(slug__icontains=keyword) | Q(description__icontains=keyword))
        else:
            products = Product.objects.all().filter(is_available=True).order_by('id')
    context = {
        'products':products,
        'product_count':products.count(),
    }
    return render(request,'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product = product
                data.user = request.user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
