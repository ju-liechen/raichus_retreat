from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView

from .models import Account, TransactionCategory


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
