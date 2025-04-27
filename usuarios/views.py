import io
import json

import matplotlib.pyplot as plt
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, Count, F, Func, Q
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import CadastroForm
from .models import RespostaSRQ, Usuario


# Cadastro de novo usuário
def cadastro_view(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redireciona para o login
    else:
        form = CadastroForm()
    return render(request, "usuarios/cadastro.html", {"form": form})


# Login de usuário
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")
        senha = request.POST.get("password")
        try:
            user = Usuario.objects.get(email=email)
            usuario = authenticate(request, username=user.username, password=senha)
            if usuario is not None:
                login(request, usuario)
                return redirect("home")
            else:
                messages.error(request, "E-mail ou senha incorretos.")
        except Usuario.DoesNotExist:
            messages.error(request, "E-mail ou senha incorretos.")
    form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})


# Página principal (home)
@login_required
def home_view(request):
    return render(request, "usuarios/home.html")


# Página para responder o SRQ-20
@login_required
def aplicar_srq(request):
    if request.method == "POST":
        respostas = []
        for i in range(1, 21):  # As 20 perguntas
            resposta = request.POST.get(f"q{i}", "nao")
            respostas.append(resposta)

        # Calcula o número de respostas 'sim' (score)
        score = sum(1 for resposta in respostas if resposta == "sim")

        # Salva as respostas no banco de dados
        usuario = request.user
        RespostaSRQ.objects.create(usuario=usuario, respostas=respostas, score=score)

        return redirect(
            "resultado_srq",
            resultado="bom" if score <= 7 else ("médio" if score <= 12 else "ruim"),
        )

    return render(request, "usuarios/srq.html")  # Renderiza a página do questionário


# Exibe o resultado do questionário
@login_required
def resultado_srq(request):
    resposta = RespostaSRQ.objects.filter(usuario=request.user).last()

    # Calcula o score com base nas respostas armazenadas
    score = 0
    if resposta:
        score = sum(1 for r in resposta.respostas if r == "sim")

    # Classificação do resultado (Bom, Médio ou Ruim)
    if score <= 7:
        resultado = "Bom"
    elif 8 <= score <= 12:
        resultado = "Médio"
    else:
        resultado = "Ruim"

    return render(
        request,
        "usuarios/resultado.html",
        {"resultado": resultado, "score": score},  # Passa o resultado para o template
    )


@login_required
def resultado_view(request, resultado):
    return render(request, "usuarios/resultado.html", {"resultado": resultado})


@login_required
def dashboard_view(request):
    # Obter parâmetros da URL
    sort_by = request.GET.get(
        "sort_by", "data_resposta"
    )  # Ordenar por data_resposta por padrão
    order = request.GET.get("order", "desc")  # Ascendente ou descendente

    # Determinar a direção da ordenação
    if order == "asc":
        order_direction = ""
        next_order = "desc"
    else:
        order_direction = "-"
        next_order = "asc"

    # Ordenar as respostas conforme os parâmetros, incluindo os campos da tabela 'usuario'
    todas_respostas = RespostaSRQ.objects.select_related("usuario").order_by(
        f"{order_direction}{sort_by}"
    )

    # Calcular KPIs
    # 1. Média de respostas "sim" na população geral
    total_respostas = RespostaSRQ.objects.count()
    total_respostas_sim = RespostaSRQ.objects.filter(respostas__icontains="sim").count()
    media_respostas_sim_populacao = (
        (total_respostas_sim / total_respostas) * 100 if total_respostas > 0 else 0
    )

    # 2. Média de respostas "sim" para homens
    total_homens = RespostaSRQ.objects.filter(usuario__genero="M").count()
    total_homens_sim = RespostaSRQ.objects.filter(
        usuario__genero="M", respostas__icontains="sim"
    ).count()
    media_respostas_sim_homens = (
        (total_homens_sim / total_homens) * 100 if total_homens > 0 else 0
    )

    # 3. Média de respostas "sim" para mulheres
    total_mulheres = RespostaSRQ.objects.filter(usuario__genero="F").count()
    total_mulheres_sim = RespostaSRQ.objects.filter(
        usuario__genero="F", respostas__icontains="sim"
    ).count()
    media_respostas_sim_mulheres = (
        (total_mulheres_sim / total_mulheres) * 100 if total_mulheres > 0 else 0
    )

    # 4. Cargo com maior média de respostas "sim"
    cargo_media_respostas_sim = (
        RespostaSRQ.objects.values("usuario__cargo")
        .annotate(media_respostas=Avg(Q(respostas__icontains="sim")))
        .order_by("-media_respostas")
        .first()
    )
    cargo_com_maior_media = (
        cargo_media_respostas_sim["usuario__cargo"]
        if cargo_media_respostas_sim
        else "N/A"
    )

    # Preparar os dados para enviar ao template
    respostas_data = []
    for resposta in todas_respostas:
        respostas_data.append(
            {
                "usuario": resposta.usuario.username,
                "email": resposta.usuario.email,
                "data_resposta": resposta.data_resposta,
                "score": resposta.score,
                "respostas": resposta.respostas,
            }
        )

    respostas_json = json.dumps(respostas_data, cls=DjangoJSONEncoder)

    def get_classificacoes(queryset):
        counts = {"Bom": 0, "Médio": 0, "Ruim": 0}
        for resposta in queryset:
            if resposta.score <= 7:
                counts["Bom"] += 1
            elif 8 <= resposta.score <= 12:
                counts["Médio"] += 1
            else:
                counts["Ruim"] += 1
        return counts

        class Lower(Func):
            function = "LOWER"
            template = "%(function)s(%(expressions)s)"

    # Obter cargos únicos (case insensitive)
    cargos_distintos = (
        RespostaSRQ.objects.annotate(lower_cargo=Lower("usuario__cargo"))
        .values("lower_cargo")
        .annotate(original_cargo=F("usuario__cargo"))
        .distinct()
        .order_by("lower_cargo")
    )

    # Criar dicionário de cargos (chave lower, valor original)
    cargos_dict = {c["lower_cargo"]: c["original_cargo"] for c in cargos_distintos}

    # Classificações existentes
    classificacoes = {
        "Geral": get_classificacoes(RespostaSRQ.objects.all()),
        "Masculino": get_classificacoes(
            RespostaSRQ.objects.filter(usuario__genero="M")
        ),
        "Feminino": get_classificacoes(RespostaSRQ.objects.filter(usuario__genero="F")),
    }

    # Adicionar classificações para cada cargo
    for lower_cargo, original_cargo in cargos_dict.items():
        classificacoes[original_cargo] = get_classificacoes(
            RespostaSRQ.objects.filter(usuario__cargo__iexact=lower_cargo)
        )

    # Preparar opções para o filtro
    filter_options = ["Geral", "Masculino", "Feminino"] + list(cargos_dict.values())

    # Serializar para JSON
    classificacoes_json = json.dumps(classificacoes, ensure_ascii=False)

    # Calcular classificação das médias
    def get_classificacao_porcentagem(porcentagem):
        if porcentagem <= 35:  # ≤35% = Bom
            return {"texto": "Baixa", "cor": "#4CAF50", "classe": "bom"}
        elif porcentagem <= 60:  # 36-60% = Médio
            return {"texto": "Média", "cor": "#FFC107", "classe": "medio"}
        else:  # >60% = Ruim
            return {"texto": "Alta", "cor": "#F44336", "classe": "ruim"}

    # Classificar cada KPI
    class_populacao = get_classificacao_porcentagem(media_respostas_sim_populacao)
    class_homens = get_classificacao_porcentagem(media_respostas_sim_homens)
    class_mulheres = get_classificacao_porcentagem(media_respostas_sim_mulheres)

    return render(
        request,
        "usuarios/dashboard.html",
        {
            "respostas": todas_respostas,
            "respostas_json": respostas_json,
            "sort_by": sort_by,
            "order": order,
            "next_order": next_order,
            # Passando os KPIs para o template
            "media_respostas_sim_populacao": media_respostas_sim_populacao,
            "media_respostas_sim_homens": media_respostas_sim_homens,
            "media_respostas_sim_mulheres": media_respostas_sim_mulheres,
            "cargo_com_maior_media": cargo_com_maior_media,
            "classificacoes": classificacoes,
            "classificacoes_json": classificacoes_json,
            "filter_options": filter_options,
            "class_populacao": class_populacao,
            "class_homens": class_homens,
            "class_mulheres": class_mulheres,
        },
    )
