from itertools import cycle

from django import forms
from django.core.exceptions import ValidationError

from fornecedor.models import Fornecedor


class PesquisaFornecedorForm(forms.Form):
    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100'}),
        required=False)

def is_cnpj_valido(cnpj: str) -> bool:
    LENGTH_CNPJ = 14
    if len(cnpj) != LENGTH_CNPJ:
        return False
    if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
        return False
    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            return False
    return True

class FornecedorForm(forms.ModelForm):
    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        if is_cnpj_valido(cnpj):
            return cnpj
        else:
            raise ValidationError("CNPJ inválido")


    class Meta:
        model = Fornecedor
        fields = ('nome', 'endereco', 'telefone', 'cnpj')
    #Metodo construtor
    def __init__(self, *args, **kwargs):
        # Estamos mandando executar o construtor da classe fornecedor form
        super().__init__(*args, **kwargs)

        self.fields['nome'].error_messages = {'required': 'Campo obrigatório',
                                              'unique': 'Nome de fornecedor duplicado'}
        self.fields['nome'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['endereco'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['endereco'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['telefone'].error_messages = {'required': 'Campo obrigatório'}
        self.fields['telefone'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['cnpj'].error_messages = {'required': 'Campo obrigatório',
                                              'unique': 'CNPJ de fornecedor duplicado'}
        self.fields['cnpj'].widget.attrs.update({'class': 'form-control form-control-sm',
                                                 'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'})





    # nome = forms.CharField(
    #         error_messages={'required': 'campo obrigatório', 'unique': 'Nome de fornecedor duplicado'},
    #         widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100'})
    #     )
    #
    # endereco = forms.CharField(
    #     error_messages={'required': 'campo obrigatório'},
    #     widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100'})
    # )
    #
    # telefone = forms.CharField(
    #     error_messages={'required': 'campo obrigatório'},
    #     widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '15'})
    # )
    #
    # cnpj = forms.CharField(
    #     error_messages={'required': 'campo obrigatório', 'unique': 'CNPJ duplicado'},
    #     widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '15',
    #                                   'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'})
    # )