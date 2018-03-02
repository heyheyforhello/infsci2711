from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from simplestore.checkout.models.order import OrderItem

from simplestore.cart.forms import AddToCartForm
from .models.product import Product, Category
from django.db.models import Sum

import pdb

#
# class CategoryDetailView(DetailView):
#     model = Category
#     slug_url_kwarg = 'category_slug'
#     template_name = "product_list.html"
#     print(slug_url_kwarg)
#     def get_context_data(self, **kwargs):
#         context = super(CategoryDetailView, self).get_context_data(**kwargs)
#         products = Product.objects.filter(category=self.slug_url_kwarg
#         ).prefetch_related('image')
#
#         context.update({
#             'products': products
#         })
#         return context
def CategoryDetailView(request, category_slug = None):
    # 过滤指定目录的商品
    products = Product.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product_list_1.html',
                  {'products': products})

class CategoryView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = "category_view.html"
#
class ProductsListView(ListView):
    model = Product
    queryset = Product.objects.all().active().prefetch_related('image')
    template_name = "product_list.html"


# def ProductsListView(request, category_slug = None):
#     category = None
#     categories = Category.objects.all()
#     # 过滤指定目录的商品
#     products = Product.objects.filter(is_active=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category_icontains=category)
#
#     return render(request,
#                   'product_list_1.html',
#                   {'category': category,
#                    'categories': categories,
#                    'products': products})

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = AddToCartForm
        return context

class HotProductView(ListView):
    model = OrderItem
    queryset = OrderItem.objects.all().values('product').annotate(total=Sum('quantity')).order_by('-total')[:3]
    #pdb.set_trace()
    template_name = "hot_product_list.html"

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    item_list = Product.objects.filter(Q(name__icontains=q)|Q(name__icontains=q))
    if len(item_list) == 0:
        error_msg = 'The book you have searched dose not exist'
        return render(request, "search.html", {'error_msg': error_msg})
    return render(request, "search.html",{'item_list': item_list})
