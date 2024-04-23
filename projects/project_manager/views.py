
import datetime
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.views import View

from .models import Colaborador, Projeto

# Create your views here.
class ProjectsIndex(View):
  def get(self, request, *args, **kwargs):
    context = {}

    projetos = [projeto.as_dict() for projeto in Projeto.objects.all()]

    context['projetos'] = json.loads(json.dumps(projetos))

    return TemplateResponse(request, 'base.html', context)
  
class ProjectIndex(View):
  template = 'project.html'

  def get(self, request, *args, **kwargs):
    context = {}
    
    context['gestores'] = Colaborador.objects.all()
    context['colaboradores'] = Colaborador.objects.all()

    project_id = request.GET.get('project_id') if request.GET.get('project_id') is not None else kwargs['project_id']
    if project_id and (request.GET.get('acao') == 'criar' or not request.GET.get('acao')):
      projetos = [projeto.as_dict() for projeto in Projeto.objects.filter(id=project_id)]

      context['projeto'] = json.loads(json.dumps(projetos))
    elif project_id and request.GET.get('acao') == 'deletar':
      return self.delete(request, *args, **kwargs)

    return TemplateResponse(request, self.template, context)
  
  def post(self, request, *args, **kwargs):
    context = {}
    project = {}

    project['nome'] = request.POST.get('nome')
    project['descricao'] = request.POST.get('descricao')
    project['data_inicial'] = datetime.datetime.strptime(request.POST.get('data_inicial'), '%Y-%m-%d')
    project['data_final'] = datetime.datetime.strptime(request.POST.get('data_final'), '%Y-%m-%d')
    project['valor'] = request.POST.get('valor')
    project['status'] = request.POST.get('status')
    project['tipo'] = request.POST.get('tipo')
    project['gestor'] = request.POST.get('gestor')
    project['colaboradores'] = request.POST.getlist('colaboradores')
    try:
      gestor = Colaborador.objects.get(id=project['gestor'])
    except Exception as e:
      context['error'] = 'Gestor não encontrado ou mais de um registro'
      return TemplateResponse(request, self.template, context)

    projeto = Projeto()
    projeto.nome = project['nome']
    projeto.descricao = project['descricao']
    projeto.data_inicial = project['data_inicial']
    projeto.data_final = project['data_final']
    projeto.valor = project['valor']
    projeto.status = project['status']
    projeto.tipo = project['tipo']
    projeto.gestor = gestor
    projeto.save()
    projeto.colaboradores = project['colaboradores']
    projeto.save()

    context['projeto'] = json.loads(json.dumps(projeto.as_dict()))

    return TemplateResponse(request, self.template, context)
  
  def delete(self, request, *args, **kwargs):
    context = {}
    project_id = project_id = request.GET.get('project_id') if request.GET.get('project_id') is not None else kwargs['project_id']
    try:
      projeto = Projeto.objects.get(id=project_id)
    except Exception as e:
      context['error'] = 'Projeto não encontrado!'
      return TemplateResponse(request, self.template, context)
    
    context['projeto'] = projeto.delete()

    return redirect('/projects')