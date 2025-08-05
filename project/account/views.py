import random

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from . import forms
from .forms import ProfileForm, AddressForm
from .models import User, City, Province, Address
from django.http import JsonResponse
from django.core.mail import send_mail

from tests.models import Order


def login_mobile(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            request.session['phone'] = phone
            if cache.get('phone'):
                return redirect(reverse('account:verify-otp'))
            send_otp(phone)
            return redirect(reverse('account:verify-otp'))
    return render(request, 'login.html')

def login_password(request):
    password_wrong = False
    if request.method == 'POST':
        phone = request.session.get('phone')
        password = request.POST['password']
        user = authenticate(request,phone=phone, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request,'index.html')
        else:
            password_wrong = True
    return render(request,'login-password.html', {'password_wrong': password_wrong})

def verify_otp(request):
    phone = request.session.get('phone')
    user = User.objects.filter(phone=phone).exists()
    otp_wrong = False
    #####
    show_login_wpass = False
    if user:
        this_user = User.objects.get(phone=phone)
        if this_user.password != "":
            show_login_wpass = True
    #####

    if not phone:
        return redirect(reverse('account:login'))
    if request.method == 'POST':
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        otp = str(otp1+otp2+otp3+otp4)
        cache_otp = cache.get(phone)
        if cache_otp and str(cache_otp) == otp:
            user, _ = User.objects.get_or_create(phone=phone,
                                              defaults={'username':phone,
                                                        'email':f'{phone}@mail.com'})
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            cache.delete('phone')
            return redirect(reverse('shop:index'))
        else:
            otp_wrong = True
    return render(request, 'verify-otp.html', {'show_login_wpass': show_login_wpass, 'otp_wrong': otp_wrong})

def send_otp(phone):
    otp = random.randint(1000,9999)
    cache.set(phone,otp,120)
    print("this is your otp:",otp)

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('shop:index'))

@login_required
def profile_edit(request):
    # form = ProfileForm()
    # if request.method == 'POST':
    #     form = ProfileForm(request.POST)
    #     profile = User.objects.filter(id=request.user.id).first()
    #     if 'change_first_last_name' in request.POST:
    #         profile.first_name = request.POST.get('first_name')
    #         profile.last_name = request.POST.get('last_name')
    #     elif 'change_phone' in request.POST:
    #         profile.phone = request.POST.get('phone')
    #     elif 'change_email' in request.POST:
    #         profile.email = request.POST.get('email')
    #     # elif 'change_birth_date' in request.POST:
    #         # profile.birth_date = request.POST.get('birth_date')
    #     profile.save()
    #     return render(request,'profile-edit.html')
    # return render(request, 'profile-edit.html')
    password_form = SetPasswordForm(user=request.user)
    change_password_form = SetPasswordForm(user=request.user)
    # Other forms like email_form = ChangeEmailForm(...)
    is_password = False
    if request.user.password != "":
        is_password = True
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'set_password':
            password_form = SetPasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                # You could set a success message here too
                return redirect('account:profile-edit')

        elif form_type == 'change_fullname':
            profile_form = ProfileForm(request.POST)
            profile = User.objects.filter(id=request.user.id).first()
            profile.first_name = request.POST.get('first_name')
            profile.last_name = request.POST.get('last_name')
            profile.save()
        elif form_type == 'change_password':
            change_password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if change_password_form.is_valid():
                change_password_form.save()
                update_session_auth_hash(request, request.user)
                return HttpResponseRedirect(reverse('profile-edit'))
        elif form_type == 'change_number':
            phone = request.POST.get('phone')
            if phone:
                request.session['phone'] = phone
                if cache.get('phone'):
                    return redirect(reverse('account:verify-otp'))
                send_otp(phone)
                return redirect(reverse('account:verify-otp'))

    context = {
        'password_form': password_form,
        'is_password':is_password,
        # 'email_form': email_form,
    }

    return render(request, 'profile-edit.html', context)


@login_required
def profile_dashboard(request):
    return render(request, 'profile-dashboard.html')

@login_required
def profile_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            # Optional: redirect or show a success message
            return redirect('account:profile-address')  # better UX than re-rendering
    else:
        form = AddressForm()

    addresses = Address.objects.filter(user=request.user)
    context = {
        'form': form,
        'provinces': Province.objects.all(),
        'addresses': addresses,
    }
    return render(request, 'profile-address.html', context)

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        # Get form data directly from POST
        address.recipient_firstname = request.POST.get('recipient_firstname')
        address.recipient_lastname = request.POST.get('recipient_lastname')
        address.recipient_phone = request.POST.get('recipient_phone')
        address.address = request.POST.get('address')
        address.province_id = request.POST.get('province')
        address.city_id = request.POST.get('city')
        address.number = request.POST.get('number')
        address.unit = request.POST.get('unit')
        address.postal_code = request.POST.get('postal_code')

        address.save()
        return redirect('account:profile-address')  # or wherever your address list is shown

    return redirect('account:profile-address')  # don't allow GET, just redirect


@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)

    if request.method == 'POST':
        address.delete()

    return redirect('account:profile-address')  # or wherever you want to send them

def get_citys(request):
    province_id = request.GET.get('province_id')
    if not province_id:
        return JsonResponse({'error':'province is empty'}, status=400)
    citys = City.objects.filter(province_id= province_id).values('id', 'title')
    return JsonResponse(list(citys), safe = False)

def profile_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('orderdetail_set__product')
    return render(request, 'profile-orders.html', {'orders':orders})

def profile_orders_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderdetail_set.select_related('product')  # optimize DB access

    return render(request, 'profile-orders-detail.html', {
        'order': order,
        'order_items': order_items,
    })
