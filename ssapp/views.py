from django.contrib.auth import authenticate, login, update_session_auth_hash, get_user_model
from django.contrib.auth.admin import sensitive_post_parameters_m
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import deprecate_current_app
from django.core.urlresolvers import reverse
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, resolve_url
from datetime import *
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.template.context import RequestContext
from ssapp.forms import *
from ssapp.models import *



@login_required
def searchitem(request):
    context=RequestContext(request)
    search_query = request.GET.get('search_ box')
    info=Products.objects.all().exclude(current_id=request.user.id).filter(pname__startswith=search_query)
    context = {'data': info}
    template = loader.get_template('ssapp/search.html')
    return HttpResponse(template.render(context, request))

@login_required
def ItemInfo(request,pk):
    context=RequestContext(request)
    info=Products.objects.all().filter(pk=pk)
    context={'data':info}
    template = loader.get_template('ssapp/singleproduct.html')
    return HttpResponse(template.render(context,request))

from django.db.models import Max

@login_required
def MyBids(request):
    context = RequestContext(request)
    info = BidDetails.objects.all().filter(userinfo_id=request.user.id).order_by('-bid__postdate','-userbid','bid__pname')
    context ={'data': info}
    template = loader.get_template('ssapp/mybids.html')
    return HttpResponse(template.render(context,request))


@login_required
def userprofile(request):
    context=RequestContext(request)
    info=UserProfile.objects.get(pk=request.user.id)
    context={'data':info}
    template = loader.get_template('ssapp/userprofile.html')
    return HttpResponse(template.render(context, request))


@login_required
def homepage(request):
    context = RequestContext(request)
    #TO UPDATE THE DATA EVERYTIME
    import datetime
    product = Products.objects.all().filter(current__id=request.user.id)
    datevar = datetime.date.today()
    for content in product:
        if content.finaldate and (content.bidprice > 0):

            if content.finaldate.year < datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
            elif content.finaldate.month < datevar.month and content.finaldate.year == datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
            elif content.finaldate.day <= datevar.day and content.finaldate.month == datevar.month and content.finaldate.year == datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
    #MAIN PAGE DISPLAYING
    info = Products.objects.all().exclude(current_id=request.user.id).filter(sold=False).order_by('-postdate')[0:5]
    context = {'data': info}
    template = loader.get_template('ssapp/homepage.html')
    return HttpResponse(template.render(context, request))

#BID FOR AN ITEM, HERE ITEMS ARE DISPLAYED
@login_required
def selleritems(request):
    context=RequestContext(request)
    import datetime
    info=Products.objects.all().filter(current__id=request.user.id)
    datevar = datetime.date.today()
    for content in info:
        if content.finaldate and (content.bidprice > 0):
            # CONDITIONS IF THE TIME ENDS THE AUCTION SHOULD BE CLOSED
            if content.finaldate.year < datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
            elif content.finaldate.month < datevar.month and content.finaldate.year == datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
            elif content.finaldate.day <= datevar.day and content.finaldate.month == datevar.month and content.finaldate.year == datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
    context = {'data': info}
    template=loader.get_template('ssapp/seller_details.html')
    return HttpResponse(template.render(context, request))


#Apparently ListView IS NOT WORKING SO USING THIS, WILL CHANGE IT LATER.


@login_required
def ProductsView(request, pk):
    info = Products.objects.all().filter(list_id=pk,sold=False).exclude(current_id=request.user.id).order_by('-postdate')
    context={'data':info}
    template = loader.get_template('ssapp/products_list.html')
    return HttpResponse(template.render(context, request))


#DISPLAY USER DETAILS OF WHO HAD THE HIGHEST BID
@login_required
def BuyerView(request, pk):
    data = Products.objects.get(pk=pk)
    if data.bidprice == 0:
        info =[False,pk]
        context = {'data' : info}
        template = loader.get_template('ssapp/buyer_view.html')
        return HttpResponse(template.render(context, request))
    else:
        data.sold = True
        data.save()
        info = BidDetails.objects.get(bid_id=data.id, userbid=data.bidprice)
        info.won = True
        info.save()
        info = UserProfile.objects.get(user_id=info.userinfo_id)
        context = {'data' : info}
        template = loader.get_template('ssapp/buyer_view.html')
        return HttpResponse(template.render(context, request))

#DISPLAY THE PRODUCTS WHICH THE USER HAS WON IN BIDDING.
@login_required
def UserProducts(request):
    cur= request.user.id
    info = BidDetails.objects.all().filter(userinfo_id=request.user.id,won=True)
    context = {'data' : info }
    template = loader.get_template('ssapp/purchased_products.html')
    return HttpResponse(template.render(context,request))


#Registration Page
def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST,request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'userimage' in request.FILES:
                 profile.userimage=request.FILES['userimage']
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'ssapp/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)



def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/homepage/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response('ssapp/login.html', {}, context)
    return render_to_response('ssapp/login.html', {}, context)

def index(request):
    context = RequestContext(request)
    # TO UPDATE THE DATA EVERYTIME
    import datetime
    product = Products.objects.all().filter(current__id=request.user.id,sold=False)
    datevar = datetime.date.today()
    for content in product:
        if content.finaldate and (content.bidprice > 0):
            # CONDITIONS IF THE TIME ENDS THE AUCTION SHOULD BE CLOSED
            if content.finaldate.year < datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
            elif content.finaldate.month < datevar.month and content.finaldate.year == datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
            elif content.finaldate.day <= datevar.day and content.finaldate.month == datevar.month and content.finaldate.year == datevar.year:
                content.sold = True
                content.save()
                info = BidDetails.objects.get(bid_id=content.id, userbid=content.bidprice)
                info.won = True
                info.save()
    # MAIN PAGE DISPLAYING
    info = Products.objects.all().exclude(current_id=request.user.id).filter(sold=False).order_by('-postdate')[0:5]
    context = {'data': info}
    template = loader.get_template('ssapp/index.html')
    return HttpResponse(template.render(context, request))




from django.contrib.auth import logout


# THIS IS FOR THE LOG OUT PAGE VIEW

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
