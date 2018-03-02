from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView

from simplestore.cart.utils import get_cart
from simplestore.checkout.models.order import Order
from simplestore.checkout.models.address import Address
from .forms import RegistrationForm, LoginForm, PersonalAddressForm, HomeForm, BusinessForm
from .models import Profile, Home, Business

User = get_user_model()

def profile_index(request):
    return render(request, "profile_index.html")


# Profile Detail
class ProfileDetail(LoginRequiredMixin, DetailView):
    template_name = "profile_detail.html"
    login_url = reverse_lazy('profiles:login')
    model = Profile

    def get_object(self, queryset=None):
        return Profile.objects.get(pk=self.request.user.pk)


# # Registration Form
# class RegistrationFormView(FormView):
#     template_name = "profile_register.html"
#     form_class = RegistrationForm
#     success_url = reverse_lazy('products:index')
#
#     def form_valid(self, form):
#         self.profile = form.save()
#         self.request.session['user_cart'] = self.request.session.session_key
#
#         user = authenticate(
#             email=self.profile.email,
#             password=self.request.POST['password1']
#         )
#
#         messages.add_message(
#             self.request, messages.SUCCESS,
#             'You were successfully logged in.'
#         )
#
#         login(self.request, user)
#         return super(RegistrationFormView, self).form_valid(form)


def Registration(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        personal_address_form = PersonalAddressForm(request.POST)
        home_form = HomeForm(request.POST)
        business_form = BusinessForm(request.POST)
        # pdb.set_trace()
        if register_form.is_valid() and personal_address_form.is_valid():
            # if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            #     if self.cleaned_data['password1'] == self.cleaned_data['password2']:
            #         raise forms.ValidationError("Passwords do not match")
            #
            profile = register_form.save(commit = False)
            # pdb.set_trace()
            profile.aid = personal_address_form.save()
            profile.save()
            # pdb.set_trace()
            profile.kind = request.POST['kind']
            if profile.kind == 'H':
                if home_form.is_valid():
                    home = home_form.save(commit = False)
                    home.cid = profile
                    home.save()
                else:
                    messages.error(request, ('home form is not valid'))
                    register_form = RegistrationForm()
                    personal_address_form = PersonalAddressForm()
                    home_form = HomeForm()
                    business_form = BusinessForm()
                    context = {'register_form': register_form,
                               'personal_address_form': personal_address_form,
                               'home_form': home_form,
                               'business_form': business_form,}
                    return render(request, "profile_register.html", context)

            else:
                if business_form.is_valid():
                    business = business_form.save(commit = False)
                    business.cid = profile
                    business.save()
                else:
                    messages.error(request, ('business form is not valid.'))
                    register_form = RegistrationForm()
                    personal_address_form = PersonalAddressForm()
                    home_form = HomeForm()
                    business_form = BusinessForm()
                    context = {'register_form': register_form,
                               'personal_address_form': personal_address_form,
                               'home_form': home_form,
                               'business_form': business_form,}
                    return render(request, "profile_register.html", context)
            request.session['user_cart'] = request.session.session_key
            # user = User.objects.create(email=profile.email, password=request.POST['password1'])
            profile.set_password(request.POST['password'])
            profile.save()
            # pdb.set_trace()
            user = authenticate(
                email=profile.email,
                password=request.POST['password']
            )
            # pdb.set_trace()
            login(request, profile)

        else:
            messages.error(request, ('Please correct the errors.'))
            register_form = RegistrationForm()
            personal_address_form = PersonalAddressForm()
            home_form = HomeForm()
            business_form = BusinessForm()
            context = {'register_form': register_form,
                       'personal_address_form': personal_address_form,
                       'home_form': home_form,
                       'business_form': business_form,}
            return render(request, "profile_register.html", context)
    else:
        register_form = RegistrationForm()
        personal_address_form = PersonalAddressForm()
        home_form = HomeForm()
        business_form = BusinessForm()
        context = {'register_form': register_form,
                   'personal_address_form': personal_address_form,
                   'home_form': home_form,
                   'business_form': business_form,}
        return render(request, "profile_register.html", context)
    return render(request, "product_list_1.html", {})





class UpdateProfileForm(LoginRequiredMixin, UpdateView):
    template_name = 'profile_update.html'
    form_class = RegistrationForm
    model = Profile
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('profiles:login')

    def get_object(self, queryset=None):
        return Profile.objects.get(pk=self.request.user.pk)


class ProfileOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'profile_orders.html'
    login_url = reverse_lazy('profiles:login')

    def get_context_data(self, **kwargs):
        context = super(ProfileOrdersView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user.id)

        return context


class ProfileOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'profile_order_detail.html'
    login_url = reverse_lazy('profiles:login')


# Login
class AuthenticationForm(FormView):
    template_name = 'profile_login.html'
    form_class = LoginForm
    success_url = reverse_lazy('products:index')

    def form_valid(self, form):

        cart = get_cart(self.request, create=True)
        user = authenticate(email=self.request.POST['email'], password=self.request.POST['password'])

        if user is not None and user.is_active:
            self.request.session['user_cart'] = self.request.session.session_key
            login(self.request, user)

            if cart is not None:
                cart.user = Profile.objects.get(id=user.id)
                cart.save()
                messages.add_message(self.request, messages.SUCCESS, 'You were successfully logged in.')

            return super(AuthenticationForm, self).form_valid(form)

        else:
            response = super(AuthenticationForm, self).form_invalid(form)
            messages.add_message(self.request, messages.WARNING, 'Wrong email or password. Please try again')
            return response


# Logout View
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
