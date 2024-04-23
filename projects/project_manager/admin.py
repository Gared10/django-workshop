from django.contrib import admin

from project_manager.models import Colaborador, Projeto

# Register your models here.
class ProjectManagerAdmin(admin.AdminSite):
  list_filter = ['status']
  list_display = ['nome','descricao','valor','tipo']
  search_fields = ['nome','descricao']
  filter_horizontal = ['colaboradores']

admin.site.register(Projeto)
admin.site.register(Colaborador)