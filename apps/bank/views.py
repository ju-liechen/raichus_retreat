import logging

from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView

from .models import Account, TransactionCategory
from .plaid import get_link_token
from .services import import_plaid_account

log = logging.getLogger(__name__)


class BankDashboardView(ListView):
    model = Account
    template_name = 'bank/dashboard.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['tags'] = TransactionCategory.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        if request.htmx:
            html = render_to_string('bank/dashboard.html', context, request)
            return HttpResponse(html)
        return self.render_to_response(context)

    def put(self, request, *args, **kwargs):
        """
        Triggered at the end of the Plaid connection flow. Called from app.js.
        """
        public_token = QueryDict(request.body).get('public_token', '').strip()
        import_plaid_account(request.user, public_token)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


def clear_link_token(request):
    if 'link_token' in request.session:
        del request.session['link_token']
    return HttpResponse()


def plaid_connect(request):
    try:
        request.session['link_token'] = get_link_token(request.user.id)
    except Exception as e:
        log.error(e)
    return render(request, 'bank/welcome.html')
