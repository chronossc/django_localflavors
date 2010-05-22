# coding: utf-8
from django import forms
from models import CPFCNPJModel


class CPFCNPJForm(forms.ModelForm):
    class Meta:
        model = CPFCNPJModel

    def clean(self):

        data = self.cleaned_data
        if not self.errors and not self.data.get('cpf') and not self.data.get('cnpj'):
            raise forms.ValidationError("Preencha ou CPF ou CNPJ chará!")

        cpf = data.get('cpf')
        cnpj = data.get('cnpj')

        if cpf != self.instance.cpf or cnpj != self.instance.cnpj:

            try:
                CPFCNPJModel.objects.get(cpf=cpf or None,cnpj=cnpj or None)
            except CPFCNPJModel.DoesNotExist:
                pass
            else:
                raise forms.ValidationError("Este já existe chará!")
        
        return data
