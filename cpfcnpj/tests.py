from django.test import TestCase
from models import BRCPFCNPJ
from forms import BRCPFCNPJForm
from django.contrib.localflavor.br.br_cpfcnpj import CPF, CNPJ, CPFGenerator,\
    CNPJGenerator
from random import choice

class BRCPFCNPJTests(TestCase):

    @property
    def randomcpf(self):
        return CPFGenerator()

    @property
    def randomcnpj(self):
        return CNPJGenerator()

    def test_cpf_type(self):
        """ make tests on cpf class """
        cpf = '43502207046'

        # test wrong size
        try:
            CPF(cpf[:-1])
        except ValueError,err:
            self.assertEqual(err.args,(CPF.error_messages['max_digits'],))

        # test digits only
        try:
            CPF(cpf.replace('0','a'))
        except ValueError,err:
            self.assertEqual(err.args,(CPF.error_messages['digits_only'],))

        # test invalid cpf
        try:
            CPF(cpf[:-1]+'5')
        except ValueError,err:
            self.assertEqual(err.args,(CPF.error_messages['invalid'],))

        # test valid cpf
        try:
            cpfn = CPF(cpf)
        except ValueError,err:
            self.fail(str(err))
    
    def test_cnpj_type(self):
        """ make tests on cnpj type """
        cnpj = '59430995000173'

        # test wrong size
        try:
            CNPJ(cnpj[:-1])
        except ValueError,err:
            self.assertEqual(err.args,(CNPJ.error_messages['max_digits'],))

        # test digits only
        try:
            CNPJ(cnpj.replace('0','a'))
        except ValueError,err:
            self.assertEqual(err.args,(CNPJ.error_messages['digits_only'],))

        # test invalid cnpj
        try:
            CNPJ(cnpj[:-1]+'5')
        except ValueError,err:
            self.assertEqual(err.args,(CNPJ.error_messages['invalid'],))

        # test valid cnpj
        try:
            cnpjn = CNPJ(cnpj)
        except ValueError,err:
            self.fail(str(err))

    def test_cpf_generator(self):
        # create 100 CPFS with generator
        for i in xrange(100):
            try:
                CPF(self.randomcpf)
            except ValueError,err:
                self.fail(str(err))

    def test_cnpj_generator(self):
        # create 100 CNPJS with generator
        for i in xrange(100):
            try:
                CNPJ(self.randomcnpj)
            except ValueError,err:
                self.fail(str(err))

    def test_cpfcnpj_form_and_model(self):
        # inserts 100 register on cpfcnpj model with form
        for i in xrange(100):
            cpf = self.randomcpf
            cnpj = self.randomcnpj

            # just choice over full number cpf/cnpj, normal string or with
            # additional characters, so we test with that various formats on
            # form input
            cpf_to_form = choice([cpf,str(CPF(cpf)),CPF(cpf).single])
            cnpj_to_form = choice([cnpj,str(CNPJ(cnpj)),CNPJ(cnpj).single])
            
            f = BRCPFCNPJForm(data={'cpf':cpf_to_form,'cnpj':cnpj_to_form})

            if f.is_valid():
                f.save()
            else:
                # show any errors
                self.fail(u"\n".join(["\n%s: %s" % (k.upper(),u', '.join(v)) for k,v in f.errors.items()]))
                break

            try:
                inst = BRCPFCNPJ.objects.get(cpf=cpf,cnpj=cnpj)
            except BRCPFCNPJ.DoesNotExist:
                self.fail("Failed on get saved cpf/cnpj with form")
                break
            else:
                # check if numbers are equal
                self.assertEqual(cpf,inst.cpf.single)
                self.assertEqual(cnpj,inst.cnpj.single)


