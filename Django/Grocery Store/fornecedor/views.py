from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify

from fornecedor.forms import PesquisaFornecedorForm, FornecedorForm
from fornecedor.models import Fornecedor

# Create your views here.
def lista_fornecedor(request):
    #Instancia do objeto form
    form = PesquisaFornecedorForm(request.GET)
    #O campo nome de PesquisaFornecedorForm será inicializado com uma string vazia ao acessar pesquisa_fornecedor.html pela primeira vez
    if form.is_valid():

        #Se nenhuma regra de validação foi violada, o parametro de requisição é adicionado ao dicionário do objeto form.
        nome = form.cleaned_data['nome']

        #Vai filtrar dentre os fornecedores, aqueles cuja string tem o valor digitado no campo 'nome' informado no form.
        lista_de_fornecedores = Fornecedor.objects. \
            filter(nome__icontains=nome) \
            .order_by('nome')
        #Instancia do objeto paginator, cujos parametros são: objetos a serem paginados, numero de objetos por pagina
        paginator = Paginator(lista_de_fornecedores, 3)

       #request.GET Faz referencia a todos os parametros de requisição que vieram do browser através de uma requisiçao do tipo GET
        #get('pagina') dentre os parametros que foram enviados por uma requisiçao do tipo get um parametro de requisiçao denominado pagina
        #Se a requisiçao for fornecedor/lista_fornecedor o objeto pagina será "none" pois não terá em sua url  "?pagina="
        #Caso contrário, se na url houver "?pagina=2", por exemplo, pagina 2 será recuperada. É como se pagina fosse uma variavel, e ele recuperasse seu valor a partir url
        pagina = request.GET.get('pagina')

        #.get_page ira retornar um objeto do tipo page que ira representar a pagina atual
        page_obj = paginator.get_page(pagina)

        print(page_obj.object_list)
        return render(request, 'fornecedor/pesquisa_fornecedor.html', {'fornecedores': page_obj,
                                                                 'form': form,
                                                                 'nome': nome})

    else:
        #Se houve algum erro na vlaidação, por enquanto não há como ter erro apenas com o campo nome no form. =)
        raise ValueError('Ocorreu ao tentar recuperar um fornecedor.')


def cadastra_fornecedor(request):
    #Se a requisiçao é do tipo post
    if request.POST:
        #Tentativa de recuperar do objeto sessão o id do fornecedor associado a chave 'fornecedor_id'
        fornecedor_id=request.session.get('fornecedor_id')
        print('id da sessão='+str(fornecedor_id))

        #Se for encontrado um valor para a chave fornecedor_id, significa que está sendo feita a alteração de um fornecedor
        if fornecedor_id:
            #Recupera o fornecedor do BD
            fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)
            fornecedor_form = FornecedorForm(request.POST, instance=fornecedor)
        else:
            #Caso contrário, é pq é uma adição no BD
            #Instancia um objeto form com os parametros da requisiçao post
            fornecedor_form = FornecedorForm(request.POST)

        #Se o form não tem erro de validaçao, então:
        if fornecedor_form.is_valid():
            #Cria um objeto do tipo fornecedor mas sem inseri-lo no BD
            fornecedor = fornecedor_form.save(commit=False)
            fornecedor.slug = slugify(fornecedor.nome)
            fornecedor.save() #.save() irá executar um comando sql insert se for um cadastro e executará update se for uma alteração

            if fornecedor_id:
                messages.add_message(request, messages.INFO, 'Fornecedor alterado com sucesso!')
                del request.session['fornecedor_id']
            else:
                 messages.add_message(request, messages.INFO, 'Fornecedor cadastrado com sucesso!')

            #Redirect para evitar o problema do duplo post. Assim que um fornecedor for cadastrado(POST), o servidor
            #efetuará um redirect, enviando uma resposta http de volta ao brwoser. E assim que ela for recebida
            # uma requisiçao GET será enviada de volta ao servidor requisitando que o fornecedor cadastrado seja exibido
            return redirect('fornecedor:exibe_fornecedor', id=fornecedor.id)
    else:
        #Caso a requisiçao enviada seja do tipo GET, então devemos remover do objeto sessão a chave fornecedor_id
        try:
            del request.session['fornecedor_id']
        except KeyError:
            pass
        #Instancia objeto form com construtor padrão, sem nenhum parâmetro
        fornecedor_form = FornecedorForm()

    #Render retorna um objeto do tipo htttresponse
    # Ele combina o  template com o dicionário que vai referenciar o objeto fornecedor form em forma de httpresponse
    return render(request, 'fornecedor/cadastra_fornecedor.html', {'form':fornecedor_form})

#Para um url /fornecedor/exibe_fornecedor/4/ o parametro id será igual a 4 id=4
def exibe_fornecedor(request, id):

    #Recupera o fornecedor através dos seguintes parametros: Classe do objeto, primary key(id)
    fornecedor = get_object_or_404(Fornecedor, pk=id)

    request.session['fornecedor_id_del'] = id

    #Renderiza a pagina exibe_fornecedor
    return render(request, 'fornecedor/exibe_fornecedor.html',{'fornecedor': fornecedor})

def edita_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, pk=id)

    #Aqui passamos uma instancia de fornecedor para o objeto fornecedor_form
    fornecedor_form = FornecedorForm(instance=fornecedor)

    #Salvamos o id de fornecedor no objeto sessão, no servidor
    #Para cada objeto sessão existente no servidor vai haver uma entrada com o id da sessão e um
    # ponteiro para o objeto sessão que possui aquele id. E no objeto sessão será armazenado um par de chave/valor
    #'fornecedor_id' = 1
    request.session['fornecedor_id'] = id

    return render(request, 'fornecedor/cadastra_fornecedor.html', {'form': fornecedor_form})

def remove_fornecedor(request):
    #Dessa vez a chave tem um nome diferente para facilitar o debug caso ocorra algum problema.
    fornecedor_id = request.session.get('fornecedor_id_del')
    fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)
    fornecedor.delete()

    #Se fornecedor não for encontrado, esta linha nao sera executada pois terá dado um erro 404
    del request.session['fornecedor_id_del']
    messages.add_message(request, messages.INFO, 'Fornecedor removido com sucesso.')

    #redirect nao foi usado pois a view exibe_fornecedor não encontraria mais o objeto que foi deletado
    return render(request, 'fornecedor/exibe_fornecedor.html', {'fornecedor': fornecedor})