
import datetime
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.views import View
import pandas as pd

from .models import Colaborador, Projeto

# Create your views here.
class ProjectsIndex(View):
  def get(self, request, *args, **kwargs):
    context = {}

    projetos = [projeto.as_dict() for projeto in Projeto.objects.all()]

    context['projetos'] = json.loads(json.dumps(projetos))

    return TemplateResponse(request, 'base.html', context)
  
  def post(self,request, *args, **kwargs):
    context = {}
    projeto = {}
    if len(request.FILES) <= 0:
      return TemplateResponse(request, self.template, {'info': 'É necessário escolher um arquivo para prosseguir'})
    
    csvFile = pd.read_csv(request.FILES['csv_file'], sep=';', )
    columns = ['matricula', 'nome', 'descricao', 'valor', 'tipo', 'status', 'data_inicial', 'data_final', 'gestor']

    for index, row in csvFile.iterrows():
      projeto['id'] = None
      projeto['nome'] = row['nome'][:255]
      projeto['descricao'] = str(row['descricao'][:255]) if str(row['descricao']) != 'nan' else ''
      projeto['valor'] = float(row['valor'])
      projeto['tipo'] = row['tipo'].upper() 
      projeto['status'] = row['status'].upper() 
      projeto['data_inicial'] = datetime.datetime.strptime(str(row['data_inicial']), "%Y-%m-%d")
      projeto['data_final'] = datetime.datetime.strptime(str(row['data_final']), "%Y-%m-%d")
      projeto['gestor'] = Colaborador.objects.get(id=row['gestor'])
      projeto['matricula'] = Colaborador.objects.filter(matricula="{:06d}".format(row['matricula']))

      try:
        project = Projeto()
        project.nome = projeto['nome']
        project.descricao = projeto['descricao']
        project.data_inicial = projeto['data_inicial']
        project.data_final = projeto['data_final']
        project.valor = projeto['valor']
        project.gestor = projeto['gestor']
        project.tipo = projeto['tipo']
        project.status = projeto['status']
        project.save()
        project.colaboradores = projeto['matricula']
        project.save()
      except Exception as e:
        context['error'] = 'Erro ao importar projetos'
        context['erroDetail'] = str(e)
        context['code'] = '400'
        raise HttpResponseNotFound(context['error'], context)
    
    return redirect('/projects')
  
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