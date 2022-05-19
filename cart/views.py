from django.shortcuts import render

from cart.cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return render(request, "cart/cart_menu.html")