from django.core.urlresolvers import reverse
from django.db import models
from django.http.response import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ssapp.models import *
from django.contrib.admin.widgets import AdminDateWidget
class CreateSellerView(CreateView):
    model=Products
    fields=["pname","description","pimage","finaldate","price","list"]

    def get_form(self, form_class):
        form = super(CreateSellerView, self).get_form(form_class)
        form.fields['finaldate'].widget.attrs.update({'class': 'datepick'})
        return form

    #To DISPLAY PARTICULAR USER KEPT ON SALE INFORMATION
    def form_valid(self, form):
        products = form.save(commit=False)
        products.current_id = self.request.user.id
        products.save()
        return super(CreateSellerView, self).form_valid(form)


    def get_success_url(self):
        return reverse('sellerdetails')


class CategoriesView(ListView):
    model = Categories

class CategoriesDisplay(CreateView):
    model = Categories
    fields = ["name"]

    def get_success_url(self):
        return reverse('create')


class DeleteProductView(DeleteView):
    model=Products
    template_name = 'ssapp/products_confirm_delete.html'
    def get_success_url(self):
        return reverse('sellerdetails')


class UpdateProductView(UpdateView):
    model=Products
    fields=["description","finaldate","price"]
    template_name = 'ssapp/products_update.html'

    def get_success_url(self):
        return reverse('sellerdetails')

class ProductsUpdateView(CreateView):
    model = BidDetails

    fields = ["userbid"]

    def form_valid(self, form):
        details = form.save(commit=False)
        details.userinfo_id = self.request.user.id
        url=self.request.get_full_path()
        val=url.split('/')[5]        # GETTING THE PRODUCT ID FROM THE URL PATH
        val=int(val)
        product = Products.objects.get(pk=val)
        if product.bidprice < details.userbid:
            product.bidprice = details.userbid
            product.save()
        details.bid_id=val
        details.save()
        return super(ProductsUpdateView,self).form_valid(form)


    def get_success_url(self):
        return reverse('Homepage')
