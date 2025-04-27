from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class CadastroForm(UserCreationForm):
    nome_completo = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nome completo"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"placeholder": "E-mail"})
    )
    genero = forms.ChoiceField(
        choices=Usuario.generos,
        required=False,
        widget=forms.Select(attrs={"placeholder": "Gênero"}),
    )
    cargo = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Cargo ou profissão"}),
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"}),
    )
    password2 = forms.CharField(
        label="Confirme a senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
    )

    # Campo username oculto, exigido por UserCreationForm
    username = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Usuario
        fields = [
            "nome_completo",
            "email",
            "genero",
            "cargo",
            "password1",
            "password2",
            "username",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nome_completo = self.cleaned_data["nome_completo"]
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        user.genero = self.cleaned_data.get("genero")
        user.cargo = self.cleaned_data.get("cargo")
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


PERGUNTAS_SRQ = [
    "Você tem se sentido nervoso(a), tenso(a) ou preocupado(a)?",
    "Você tem tido dificuldade para dormir ou tem dormido mal?",
    "Você tem se sentido assustada(o) com facilidade?",
    "Você tem sentido que não consegue desempenhar bem suas atividades?",
    "Você tem se sentido triste ultimamente?",
    "Você tem chorado mais do que o normal?",
    "Você tem achado difícil tomar decisões?",
    "Você tem achado difícil realizar atividades diárias?",
    "Você tem tido dificuldade para pensar com clareza?",
    "Você tem se sentido inútil?",
    "Você tem achado que sua vida está sem esperança?",
    "Você tem se sentido cansado(a) o tempo todo?",
    "Você tem tido dores de cabeça frequentes?",
    "Você tem tido má digestão?",
    "Você tem tido dificuldade para respirar?",
    "Você tem tido palpitações no coração?",
    "Você tem se sentido com tremores nas mãos?",
    "Você tem sentido que está muito nervoso(a)?",
    "Você tem tido problemas no estômago?",
    "Você tem perdido o interesse por coisas que antes achava prazeroso?",
]


class SRQForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SRQForm, self).__init__(*args, **kwargs)
        for idx, pergunta in enumerate(PERGUNTAS_SRQ, start=1):
            self.fields[f"q{idx}"] = forms.ChoiceField(
                label=pergunta,
                choices=[("0", "Não"), ("1", "Sim")],
                widget=forms.RadioSelect,
                required=True,
            )
