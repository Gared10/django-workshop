import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Colaborador(models.Model):

    matricula = models.CharField(max_length=6, blank=False, null=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    nome_completo = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)
    situacao_folha = models.CharField(max_length=1, blank=True, default='')
    admissao = models.DateField(blank=False, null=False)
    demissao = models.DateField(blank=True, null=True)
    vencto_exp = models.DateField(blank=True, null=True)
    salario = models.FloatField(blank=False, null=False)
    funcao = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=5, blank=False, null=False)
    protocolo = models.CharField(max_length=10, blank=True, null=False, default='')
    usuario = models.ForeignKey(User, blank=True, null=True,on_delete=models.SET_NULL)
    funcao_descricao = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.matricula + ' - ' + self.nome

    def __str__(self):
        return self.matricula + ' - ' + self.nome
    
class Projeto(models.Model):
    STATUS = [
        ('E', 'Em andamento'),
        ('P', 'Pendente'),
        ('A', 'Adiado'),
        ('C', 'Concluído'),
        ('F', 'Finalizado')
    ]
    
    TIPOS = [
        ('N', 'Normal'),
        ('E', 'Extra')
    ]

    nome = models.CharField(max_length=255, blank=False, null=False)
    descricao = models.CharField(max_length=255, blank=True, null=False)
    status = models.CharField(max_length=1, blank=False, null=False, default='P', choices=STATUS)
    data_inicial = models.DateTimeField(blank=False, null=False)
    data_final = models.DateTimeField(blank=False, null=False)
    valor = models.FloatField(blank=False, null=False, default=0)
    tipo = models.CharField(max_length=1, blank=False, null=False, default='N', choices=TIPOS)

    # user = models.ForeignKey(User, blank=False, null=False,on_delete=models.CASCADE)
    gestor = models.ForeignKey(Colaborador, blank=False, related_name='gestor',on_delete=models.CASCADE)
    colaboradores = models.ManyToManyField(Colaborador, blank=True, related_name='colaboradores')

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return self.nome
    
    def as_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "status": self.status,
            "data_inicial": datetime.datetime.strftime(self.data_inicial, '%Y-%m-%d'),
            "data_final": datetime.datetime.strftime(self.data_final, '%Y-%m-%d'),
            "valor": self.valor,
            "tipo": self.tipo,
            "gestor": self.gestor.id,
            "colaboradores": [colaborador.id for colaborador in self.colaboradores.all()]
        }