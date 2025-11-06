from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Client
from .forms import ClientForm

class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')

    def get_initial(self):
        """ Pré-preenche o campo 'client_type' com base no query parameter. """
        initials = super().get_initial()
        
        # Pega o 'tipo' da URL (ex: ?tipo=pf)
        client_type_slug = self.request.GET.get('tipo')
        
        if client_type_slug == 'pf':
            initials['client_type'] = Client.TYPE_PF
        elif client_type_slug == 'pj':
            initials['client_type'] = Client.TYPE_PJ
            
        return initials

    def get_context_data(self, **kwargs):
        """ Adiciona a variável 'tipo' ao contexto do template. """
        context = super().get_context_data(**kwargs)
        
        # Passa o 'tipo' (pf ou pj) para o template
        context['tipo'] = self.request.GET.get('tipo', 'pf') # 'pf' como padrão
        
        return context

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:client_list')

