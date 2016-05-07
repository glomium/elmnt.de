#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView

from .conf import settings as appsettings
from .forms import AuthenticationForm
from .forms import PasswordChangeForm
from .forms import EmailCreateForm
from .models import Email


class LoginView(FormView):
    default_redirect_to = settings.LOGIN_REDIRECT_URL
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "useraccounts/login.html"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        # Okay, security check complete. Log the user in.
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )

        # Ensure the user-originating redirection url is safe.
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(self.default_redirect_to)

        return redirect_to


class LogoutView(TemplateView):
    next_page = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "useraccounts/logged_out.html"

    def get(self, request, *args, **kwargs):

        logout(request)

        next_page = None
        if self.next_page is not None:
            next_page = resolve_url(self.next_page)

        if self.redirect_field_name in request.GET:
            next_page = self.request.GET.get(self.redirect_field_name)
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = request.path

        if next_page:
            return HttpResponseRedirect(next_page)

        return super(LogoutView, self).get(request, *args, **kwargs)


class LogoutThenLoginView(LogoutView):
    """
    Logs out the user if he is logged in. Then redirects to the log-in page.
    """
    next_page = settings.LOGIN_URL


class PasswordChangeView(FormView):
    """
    """
    form_class = PasswordChangeForm
    template_name = "useraccounts/password_change_form.html"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save(commit=True)
        return super(PasswordChangeView, self).form_valid(form)


class EmailMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailMixin, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.emails.all()


class EmailEditMixin(EmailMixin):
    slug_field = 'email'
    slug_url_kwarg = 'email'

    def get_queryset(self):
        return super(EmailEditMixin, self).get_queryset().filter(is_primary=False)


class EmailListView(EmailMixin, ListView):
    pass


class EmailDeleteView(EmailEditMixin, DeleteView):
    template_name = "useraccounts/email_delete_view.html"
    success_url = appsettings.REDIRECT_EMAIL_DELETE

    def get_success_url(self):
        if self.success_url:
            return resolve_url(self.success_url)


class EmailCreateView(EmailEditMixin, CreateView):
    form_class = EmailCreateForm
    template_name = "useraccounts/email_create_view.html"
    success_url = appsettings.REDIRECT_EMAIL_CREATE

    def get_form_kwargs(self):
        kwargs = super(EmailCreateView, self).get_form_kwargs()
        kwargs.update({"request": self.request, "user": self.request.user})
        return kwargs

    def get_success_url(self):
        if self.success_url:
            return resolve_url(self.success_url)


class EmailUpdateView(SingleObjectMixin, TemplateView):
    template_name = "useraccounts/email_update_view.html"
    success_url = appsettings.REDIRECT_EMAIL_UPDATE
    slug_field = 'email'
    slug_url_kwarg = 'email'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailUpdateView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.emails.filter(is_primary=False, is_valid=True)

    def get_success_url(self):
        return self.success_url

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_primary = True
        self.object.save()

        success_url = self.get_success_url()
        if success_url:
            next_page = resolve_url(success_url)
            if next_page:
                return HttpResponseRedirect(next_page)
        return super(EmailUpdateView, self).get(request, *args, **kwargs)


class EmailResendView(SingleObjectMixin, TemplateView):
    template_name = "useraccounts/email_resend_view.html"
    success_url = appsettings.REDIRECT_EMAIL_RESEND
    slug_field = 'email'
    slug_url_kwarg = 'email'

    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailResendView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.emails.all().filter(is_valid=False)

    def get_success_url(self):
        if self.success_url:
            return resolve_url(self.success_url)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.send_validation(request=self.request, skip=False)
        success_url = self.get_success_url()
        if success_url:
            return HttpResponseRedirect(next_page)
        return super(EmailResendView, self).get(request, *args, **kwargs)


class EmailValidationView(SingleObjectMixin, TemplateView):
    template_name = "useraccounts/email_validation_view.html"
    success_url = appsettings.REDIRECT_EMAIL_VALIDATE
    slug_field = 'email'
    slug_url_kwarg = 'email'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailValidationView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Email.objects.filter(is_valid=False)

    def get_success_url(self):
        if self.success_url:
            return resolve_url(self.success_url)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.check_validation(self.kwargs.get('stamp', None), self.kwargs.get('crypt', None)):
            raise Http404

        self.object.validate()

        # # autologin user
        # if not self.request.user.is_authenticated():
        #     user = authenticate(username=self.object.user.username, request=self.request, require_password=False)
        #     login(self.request, user)

        success_url = self.get_success_url()
        if success_url:
            return HttpResponseRedirect(success_url)
        return super(EmailResendView, self).get(request, *args, **kwargs)


'''
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
from django.utils.deprecation import RemovedInDjango110Warning
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _

class PasswordChangeView(CurrentAppMixin, generic.UpdateView):
    """
    Prompt the logged-in user for  their old password and a new one and change
    the password if the old password is valid.
    """
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy('django.contrib.auth.views.password_change_done')
    form_class = PasswordChangeForm

    current_app = None
    extra_context = None

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')

        return kwargs

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(request, *args, **kwargs)


class PasswordChangeDoneView(CurrentAppMixin, generic.TemplateView):
    """
    Show a confirmation message that the user's password has been changed.
    """
    template_name = "registration/password_change_done.html"

    current_app = None
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeDoneView, self).get_context_data(**kwargs)
        context.update(self.extra_context or {})
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PasswordChangeDoneView, self).dispatch(request, *args, **kwargs)


# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
# - password_reset_complete shows a success message for the above

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 1.10.",
                    RemovedInDjango110Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {
        'title': _('Password reset sent'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


class CreateEmailView(FormView):
    pass


class ValidateEmailView(FormView):
    pass
'''
