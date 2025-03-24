from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MaintenanceOrder, Equipment
from django.views.generic import DetailView, ListView
from django.db.models import Q
from datetime import datetime

class CreateOrderView(LoginRequiredMixin, CreateView):
    model = MaintenanceOrder
    template_name = 'maintenance/order_form.html'
    fields = [
        'equipment',
        'status',
        'service_provider',
        'completion_date',
        'cost',
        'description',
        'warranty_expiration',
        'warranty_terms',
        'invoice_number',
        'invoice_file',
        'notes'
    ]
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CreateEquipmentView(LoginRequiredMixin, CreateView):
    model = Equipment
    template_name = 'maintenance/equipment_form.html'
    fields = ['name', 'type', 'brand', 'model', 'serial_number', 'purchase_date', 'notes']
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class DetailOrderView(LoginRequiredMixin, DetailView):
    model = MaintenanceOrder
    template_name = 'maintenance/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return MaintenanceOrder.objects.filter(created_by=self.request.user)

class DeleteOrderView(LoginRequiredMixin, DeleteView):
    model = MaintenanceOrder
    success_url = reverse_lazy('dashboard:home')
    template_name = 'maintenance/order_confirm_delete.html'

    def get_queryset(self):
        return MaintenanceOrder.objects.filter(created_by=self.request.user)

class UpdateOrderView(LoginRequiredMixin, UpdateView):
    model = MaintenanceOrder
    template_name = 'maintenance/order_form.html'
    fields = [
        'equipment',
        'status',
        'service_provider',
        'completion_date',
        'cost',
        'description',
        'warranty_expiration',
        'warranty_terms',
        'invoice_number',
        'invoice_file',
        'notes'
    ]

    def get_success_url(self):
        return reverse_lazy('maintenance:order_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return MaintenanceOrder.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

class MaintenanceOrderListView(LoginRequiredMixin, ListView):
    model = MaintenanceOrder
    template_name = 'maintenance/order_list.html'
    context_object_name = 'maintenance_orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = MaintenanceOrder.objects.filter(created_by=self.request.user)
        
        # Filtro por equipamento
        equipment_id = self.request.GET.get('equipment')
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        
        # Filtro por data
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(completion_date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(completion_date__lte=end_date)
            except ValueError:
                pass
        
        return queryset.order_by('-completion_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipments'] = Equipment.objects.filter(owner=self.request.user)
        context['selected_equipment'] = self.request.GET.get('equipment')
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        return context