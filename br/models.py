from django.db import models
from django_localflavors.br.br_cpfcnpj import CPF,CNPJ
from django_localflavors.br import forms

"""
COMO USAR:

models.py:
from django.db import models
from django_localflavors.br.models import BRCPFField,BRCNPJField

class CPFCNPJ(models.Model):
  
  cpf = BRCPFField()
  cnpj = BRCNPJField()

  def __unicode__(self):
    return "<%s , %s>" % (self.cpf,self.cnpj)

forms.py:
from django import forms
from testapp.models import CPFCNPJ

class CPFCNPJForm(forms.ModelForm):
  class Meta:
    model = CPFCNPJ

exemplo no shell do django:
from django_localflavors.br.br_cpfcnpj import *
from cpfcnpj.webui.forms import CPFCNPJForm
from cpfcnpj.webui.models import CPFCNPJ

cpf=CPFGenerator()
cnpj=CNPJGenerator()

data={'cpf':cpf,'cnpj':cnpj}

x=CPFCNPJForm(data=data)
if x.is_valid():
  x.save()

  x = CPFCNPJ.objects.get(cpf=cpf)
  print i,(x.cpf == CPF(cpf)), x.cpf,CPF(cpf)
  print i,(x.cnpj == CNPJ(cnpj)), x.cnpj,CNPJ(cnpj)

"""


EMPTY_VALUES=(None,'')

class BRCPFField(models.CharField):
    """ CPF Model field """
    description = "The Brazilian CPF Field"

    __metaclass__ = models.SubfieldBase

    def __init__(self,*args,**kwargs):
        self.longformat = kwargs.pop('longformat',False)
        kwargs['max_length'] = 14 if self.longformat else 11
        super(BRCPFField,self).__init__(*args,**kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self,**kwargs):
        defaults = {'form_class': forms.BRCPFField}
        defaults.update(kwargs)
        return super(BRCPFField,self).formfield(**defaults)

    def to_python(self,value):
        """ convert string from base to a CPF instance """
        if isinstance(value,CPF) or value in EMPTY_VALUES:
            return value
        try:
            return CPF(value)
        except TypeError:
            return None
    
    def get_prep_value(self,value):
        value = self.to_python(value)
        if not value:
            return ''
        if self.longformat:
            return value.__unicode__
        else:
            return value.single

    def get_db_prep_value(self, value, connection=None, prepared=False):
        """
        Django <1.2 uses this method and don't send a connection or prepared,
        so, if connection is valid we call parent get_db_prep_value that call
        get_prep_value, if not just return get_prep_value and with that, this
        classes can be used on any version of Django >1.1
        """
        if connection is not None:
            return super(BRCPFField,self).get_db_prep_value(value,connection=connection,prepared=prepared)
        else:
          return self.get_prep_value(value)

class BRCNPJField(models.CharField):
    """ CNPJ Model field """
    description = "The Brazilian CNPJ Field"

    __metaclass__ = models.SubfieldBase

    def __init__(self,*args,**kwargs):
        self.longformat = kwargs.pop('longformat',False)
        kwargs['max_length'] = 18 if self.longformat else 14
        super(BRCNPJField,self).__init__(*args,**kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self,**kwargs):
        defaults = {'form_class': forms.BRCNPJField}
        defaults.update(kwargs)
        return super(BRCNPJField,self).formfield(**defaults)

    def to_python(self,value):
        """ convert string from base to a CNPJ instance """
        if isinstance(value,CNPJ) or value in EMPTY_VALUES:
            return value
        try:
            return CNPJ(value)
        except TypeError:
            return None

    def get_prep_value(self,value):
        value = self.to_python(value)
        if not value:
            return ''
        if self.longformat:
            return value.__unicode__
        else:
            return value.single

    def get_db_prep_value(self, value, connection=None, prepared=False):
        """
        Django <1.2 uses this method and don't send a connection or prepared,
        so, if connection is valid we call parent get_db_prep_value that call
        get_prep_value, if not just return get_prep_value and with that, this
        classes can be used on any version of Django >1.0
        """
        if connection is not None:
          return super(BRCNPJField,self).get_db_prep_value(value,connection=connection,prepared=prepared)
        else:
          return self.get_prep_value(value)

