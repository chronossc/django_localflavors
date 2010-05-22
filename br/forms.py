# -*- coding: utf-8 -*-
from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _
from django_localflavors.br.br_cpfcnpj import CPF,CNPJ
import re

# this fields are from http://code.djangoproject.com/ticket/13473
class BRCPFField(CharField):
    """
    This field validate a CPF number or a CPF string. A CPF number is
    compounded by XXX.XXX.XXX-VD. The two last digits are check digits.

    More information:
    http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas

    TODO: Make error messages customizable
    """
    default_error_messages = {
        'invalid': _("Invalid CPF number."),
        'max_digits': _("This field requires at most 11 digits or 14 characters."),
        'digits_only': _("This field requires only numbers."),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        kwargs['min_length'] = 11
        super(BRCPFField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Value can be either a string in the format XXX.XXX.XXX-XX or an
        11-digit number.
        """
        value = super(BRCPFField, self).clean(value)

        try:
            cpf = CPF(value)
        except ValueError,err:
            # CPF class already raise internal erros if cpf isn't valid
            raise ValidationError(err.message)

        return value

class BRCNPJField(CharField):
    """
    This field validate a CNPJ number or a CNPJ string. A CNPJ number is
    compounded by XX.XXX.XXX/XXXX-VD. The two last digits are check digits.

    TODO: Make error messages customizable
    """

    def __init__(self,*args,**kwargs):
        kwargs['max_length'] = 18
        kwargs['min_length'] = 14
        super(BRCNPJField,self).__init__(*args,**kwargs)

    def clean(self, value):
        """
        Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
        group of 14 characters.
        """
        value = super(BRCNPJField, self).clean(value)

        try:
            cnpj = CNPJ(value)
        except ValueError,err:
            # CNPJ class already raise internal errors if CNPJ isn't valid
            raise ValidationError(err.message)

        return value

# vim: tw=79 ts=4 sts=4 sw=4 ai et
