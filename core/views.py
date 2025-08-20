from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import CadastroForm, CorridaForm
from .models import Corrida, Usuario, Localizacao
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Motoboy
from django.http import HttpResponse


def index(request):
    return render(request, 'core/index.html')


class MeuLoginView(LoginView):
    template_name = 'core/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.tipo == 'cliente':
            return reverse_lazy('painel_cliente')
        elif user.tipo == 'mototaxista':
            return reverse_lazy('painel_mototaxista')
        else:
            return super().get_success_url()


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.tipo == 'cliente':
                return redirect('painel_cliente')
            else:
                return redirect('painel_mototaxista')
    else:
        form = CadastroForm()
    return render(request, 'core/cadastro.html', {'form': form})


@login_required
def painel_mototaxista(request):
    corridas_pendentes = Corrida.objects.filter(status='pendente')
    corridas_aceitas = Corrida.objects.filter(status='aceita', mototaxista=request.user)
    return render(request, 'core/painel_mototaxista.html', {
        'corridas_pendentes': corridas_pendentes,
        'corridas_aceitas': corridas_aceitas,
    })


@login_required
def painel_cliente(request):
    corridas = Corrida.objects.filter(cliente=request.user)
    return render(request, 'core/painel_cliente.html', {'corridas': corridas})


@login_required
def solicitar_corrida(request):
    if request.method == 'POST':
        form = CorridaForm(request.POST)
        if form.is_valid():
            corrida = form.save(commit=False)
            corrida.cliente = request.user
            corrida.save()
            return redirect('painel_cliente')
    else:
        form = CorridaForm()
    return render(request, 'core/solicitar_corrida.html', {'form': form})


@login_required
def aceitar_corrida(request, corrida_id):
    corrida = get_object_or_404(Corrida, id=corrida_id)
    corrida.mototaxista = request.user
    corrida.status = 'aceita'
    corrida.save()
    return redirect('painel_mototaxista')


@csrf_exempt
@login_required
def atualizar_localizacao(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            Localizacao.objects.update_or_create(
                usuario=request.user,
                defaults={'latitude': latitude, 'longitude': longitude}
            )
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'error': 'Usuário não autenticado'}, status=403)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# aqui fica a função que determina a localização do motoxiclista
'''def obter_localizacao_motoboy(request, username):
    try:
        user = User.objects.get(username=username)
        localizacao = Localizacao.objects.get(usuario=user)
        data = {
            'latitude': localizacao.latitude,
            'longitude': localizacao.longitude
        }
        return JsonResponse(data)
    except (User.DoesNotExist, Localizacao.DoesNotExist):
        return JsonResponse({'erro': 'Motoboy não encontrado'}, status=404)
'''

def localizacao_motoboy(request, username):
    return render(request, 'core/localizacao.html', {'username': username})

def localizacao_motoboy_padrao(request):
    # Exemplo: retorna a última localização registrada
    motoboy = Motoboy.objects.last()
    if motoboy:
        return JsonResponse({'lat': motoboy.latitude, 'lng': motoboy.longitude})
    return JsonResponse({'error': 'Motoboy não encontrado'}, status=404)

def localizacao_motoboys_ativos(request):
    localizacoes = Localizacao.objects.filter(usuario__tipo='mototaxista')

    dados = []
    for loc in localizacoes:
        if loc.latitude is not None and loc.longitude is not None:
            dados.append({
                "nome": loc.usuario.username,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
            })

    return JsonResponse({"motoboys": dados})
def mapa_motoboys(request):
    return render(request, 'core/mapa.html')

def painel(request):
    return render(request, 'core/painel.html')

def tela(request):
    return render(request, 'core/frente_tela.html')

def sair(request):
    return render(request, 'core/fim.html')
