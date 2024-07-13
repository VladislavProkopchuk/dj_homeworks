from django.shortcuts import render, redirect

from phones.models import Phone

TYPE_SORTS = {
    'name': 'name',
    'min_price': 'price',
    'max_price': '-price',
}


def index(request):
    return redirect('catalog')


def show_catalog(request):
    type_sort = request.GET.get('sort', 'name')
    sort_ = TYPE_SORTS[type_sort]
    template = 'catalog.html'
    # phones = Phone.objects.all()
    phones = Phone.objects.order_by(sort_)
    context = {
        'phones': phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {
        'phone': phone,
    }
    return render(request, template, context)
