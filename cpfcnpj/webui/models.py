from django.db import models
from django_localflavors.br.models import BRCPFField,BRCNPJField

class CPFCNPJModel(models.Model):
    cnpj = BRCNPJField()
    cpf = BRCPFField()

    def __unicode__(self):
        return u"cpf: %s ,  cnpj: %s" % (self.cpf or u'',self.cnpj or u'')
