from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from order.models import Order
from product.models import Category, Products


@staff_member_required()
def dashboard(request):
    return render(
        request,
        "dashboard/dashboard.html",
        {"orders": Order.objects.all().filter(status="Commander", paid=True)},
    )


@staff_member_required()
def product(request):
    products = Products.objects.all()
    query = request.GET.get("query")

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        ).distinct()

    paginator = Paginator(products, 50)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    return render(
        request, "dashboard/product.html", {"products": products, "page": products}
    )


@staff_member_required()
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("product_name")
        price = request.POST.get("product_price")
        description = request.POST.get("product_description")
        category = Category.objects.get(name=request.POST.get("product_category"))
        slug = slugify(name)
        rarity = request.POST.get("product_rarity")
        edition = request.POST.get("product_edition")
        image = request.FILES.get("product_image")
        thumbnail = request.FILES.get("product_image")

        if (
            name
            and price
            and description
            and category
            and slug
            and rarity
            and edition
            and image
        ):
            product = Products.objects.create(
                name=name,
                price=price,
                description=description,
                category=category,
                slug=slug,
                rarity=rarity,
                edition=edition,
                image=image,
                thumbnail=thumbnail,
            )
            product.save()
            return redirect("dashboard")
        else:
            return render(
                request,
                "dashboard/add_product.html",
                {"errors": "Renseignez tous les champs"},
            )

    context = {
        "categories": Category.objects.all(),
        "rarity": Products.MTG_RARE_CHOICES,
    }
    return render(request, "dashboard/add_product.html", context)


@staff_member_required()
def edit_product(request, product_id):
    product = get_object_or_404(Products, pk=product_id)

    if request.method == "POST":
        product.name = request.POST.get("product_name")
        product.price = request.POST.get("product_price")
        product.description = request.POST.get("product_description")
        product.category = Category.objects.get(id=request.POST.get("product_category"))
        product.slug = slugify(product.name)
        product.rarity = request.POST.get("product_rarity")
        product.edition = request.POST.get("product_edition")
        product.image = request.FILES.get("product_image")
        product.thumbnail = request.FILES.get("product_image")

        product.save()
        return redirect("dashboard")
    else:
        context = {
            "product": product,
            "categories": Category.objects.all(),
            "rarity": Products.MTG_RARE_CHOICES,
        }
        return render(request, "dashboard/edit_product.html", context)


@staff_member_required()
def delete_product(product_id):
    product = get_object_or_404(Products, id=product_id)

    if product.image and product.thumbnail:
        product.image.delete()
        product.thumbnail.delete()
    product.delete()

    return redirect("dashboard")


@staff_member_required()
def order(request):
    orders = Order.objects.all()
    query = request.GET.get("query")

    if query:
        orders = orders.filter(
            Q(id__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__email__icontains=query)
        ).distinct()

    paginator = Paginator(orders, 50)
    page = request.GET.get("page")
    orders = paginator.get_page(page)

    return render(request, "dashboard/order.html", {"orders": orders, "page": orders})


@staff_member_required()
def edit_order(request, order_id):
    orders = get_object_or_404(Order, pk=order_id)

    if request.method == "POST":
        orders.status = request.POST.get("order_status")
        orders.save()
        
        return redirect("order")
    else:
        return render(
            request,
            "dashboard/edit_order.html",
            {
                "order": orders,
                "status": Order.STATUS_CHOICES,
            },
        )
