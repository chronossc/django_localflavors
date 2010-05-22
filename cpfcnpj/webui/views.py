# coding: utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from models import CPFCNPJModel
from forms import CPFCNPJForm

def mainview(request,cpfcnpj=None):
    
    CPFSCNPJS = CPFCNPJModel.objects.order_by('-pk')
    
    msg=''
    
    try:
        instance = CPFCNPJModel.objects.get(pk=cpfcnpj)
        if not instance.pk:
            raise CPFCNPJModel.DoesNotExist
    except:
        try:
            instance = CPFCNPJModel.objects.get(cpf=cpfcnpj)
            if not instance.cpf:
                raise CPFCNPJModel.DoesNotExist
        except:
            try:
                instance = CPFCNPJModel.objects.get(cnpj=cpfcnpj)
                if not instance.cnpj:
                    raise CPFCNPJModel.DoesNotExist
            except:
                instance = CPFCNPJModel()
        
    
    print instance
    
    if request.POST:
        
        form = CPFCNPJForm(request.POST,instance = instance)
        
        if form.is_valid():
            
            form.save()
            
            msg = "saved!"
            
            form = CPFCNPJForm()
        
    else:
        msg = "Preencha e salve."
        form = CPFCNPJForm(instance = instance)
        
    return render_to_response('base.html',{'form': form, 'data': CPFSCNPJS, 'msg': msg },context_instance = RequestContext(request))