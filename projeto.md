Criação do projeto SQR-20 Better you:


#Abri o vs-code
No terminal:
# Cria a estrutura inicial
django-admin startproject betteryou
cd betteryou

# Cria a app para login/cadastro
python manage.py startapp usuarios

#Ativei a app no settings.py

No arquivo betteryou/settings.py, adicione 'usuarios', em INSTALLED_APPS:

INSTALLED_APPS = [
    ...
    'usuarios',
]

#Configuração do MySQL (em settings.py)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario_mysql',
        'PASSWORD': ' ', <- para o meu caso que não tenho senha mesmo
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Criar um ambiente virtual (venv)

python3 -m venv venv

# Ativar o ambiente virtual

source venv/bin/activate

# Certifique-se de ter o MySQL rodando e o banco criado. Também precisa instalar o conector do MySQL:
pip install mysqlclient
# Instalar o Django no ambiente virtual
pip install django

# Criando o Model para usuários (em usuarios/models.py)

from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Se quiser campos extras:
    idade = models.IntegerField(null=True, blank=True)
    genero = models.CharField(max_length=20, null=True, blank=True)

# E depois registra ele como modelo principal no settings.py:

AUTH_USER_MODEL = 'usuarios.Usuario'

#Criar formulários para cadastro e login (em usuarios/forms.py)

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class CadastroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'idade', 'genero', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

# Criar views (em usuarios/views.py)

# URLs (em usuarios/urls.py)

# Criar templates HTML
# edite o betteryou/urls.py para incluir as rotas da sua app
#Rodar o projeto

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver


"""Agora o projet entende as rotas:
URL	Função
/usuarios/cadastro/	Cadastro de usuário
/usuarios/login/	Login de usuário
/usuarios/logout/	Logout de usuário"""

# PRIMEIRO TESTE ATÉ AQUI: 
(venv) gabrielle@Gabrielle-Tomaszewski:~/Gabrielle- central/Estudos/00-Faculdade/Semestre 3/Projeto Integrador/betteryou$ python3 manage.py makemigrations
/home/gabrielle/Gabrielle- central/Estudos/00-Faculdade/Semestre 3/Projeto Integrador/betteryou/venv/lib/python3.12/site-packages/django/core/management/commands/makemigrations.py:161: RuntimeWarning: Got an error checking a consistent migration history performed for database connection 'default': (1045, "Access denied for user 'usuario_mysql'@'localhost' (using password: NO)")
  warnings.warn(
Migrations for 'usuarios':
  usuarios/migrations/0001_initial.py
    + Create model Usuario
    
    
# esqueci de criar o banco: 
mysql -u root -p

CREATE DATABASE betteryou_db;


 CREATE USER 'betteryou_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'BetterYou@2025';

GRANT ALL PRIVILEGES ON *.* TO 'betteryou_user'@'localhost' WITH GRANT OPTION;

FLUSH PRIVILEGES;

EXIT;

#RESULTADO DO SEGUNDO TESTE COM O : python3 manage.py migrate
 python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, usuarios
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying usuarios.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying sessions.0001_initial... OK



# Criei o  HTML com os formulários de login e cadastro e rodei o projeto com python3 manage.py runserver, entrei no link e testei 

#FALTA: CORRIGIR E FAZER AJUSTES NO CSS E TELAS DE LOGIN E CADASTRO


python manage.py createsuperuser

    E-mail: gabriellelibano@teste.com

    Senha: teste
    
    
Username: betteryou_user
Email: gabriellelibano@teste.com
Nome completo: Gabrielle
Password: gedrf343


--------
#Atividades 5 e 6:
 
# planejamento visual das próximas telas do sistema. 


# já temos:

- Login e Cadastro com Django + MySQL e Estilização com CSS delas
- Redirecionamento pós-login para tela de home 


#ATIVIDADE 5: Desenvolvimento das Telas (com validações front-end)

fazer mockups para: (Sugestão gabrielle)

1. **Tela de Aplicação do Questionário SRQ-20**
   - 20 perguntas com respostas "Sim" (1) ou "Não" (0)
   - Botão de **"Enviar Respostas"**
   - Validação JavaScript: garantir que todas as 20 questões foram respondidas

2. **Tela de Resultado Individual**
   - Exibir:
     - Nome do usuário
     - Pontuação total (de 0 a 20)
     - Nível de sofrimento (leve, moderado, grave)
     - Sugestão personalizada

3. **Tela de Dashboard**
   - Gráficos (ex: Chart.js) com:
     - Histórico pessoal do usuário
     - Média geral da população
     - Filtros (idade, gênero, período)
   - Botões de exportar CSV ou PDF (opcional)


#  MOCKUPS 

### 1. Tela: **Aplicar Questionário SRQ-20**

```
╔════════════════════════════╗
║       BetterYou           ║
╠════════════════════════════╣
║  Responda as questões    ║
║                            ║
║ Q1: Você tem sentido triste?   ( ) Sim  ( ) Não    ║
║ Q2: Você tem dormido bem?      ( ) Sim  ( ) Não    ║
║ ... até Q20                                      ║
║                            ║
║ [ Enviar Respostas ]       ║
╚════════════════════════════╝
```

### 2. Tela: **Resultado Individual**

```
╔════════════════════════════╗
║        Resultado SRQ-20    ║
╠════════════════════════════╣
║ Nome: Gabrielle            ║
║ Pontuação: 12              ║
║ Classificação: Moderado 🟡 ║
║                            ║
║    Recomendação:           ║
║ Faça pausas durante o dia.║
╚════════════════════════════╝
```

### 3. Tela: **Dashboard com Gráficos**

```
╔════════════════════════════════════╗
║ 📊 Painel do Usuário - BetterYou   ║
╠════════════════════════════════════╣
║ [Filtro por data] [Gênero] [Idade] ║
║                                    ║
║ 📈 Gráfico de Pontuações Individuais║
║ 📊 Gráfico de Média Geral           ║
║ 📥 [ Exportar PDF ] [ Exportar CSV ]║
╚════════════════════════════════════╝
```

 Arquitetura (MVC)
Camada	Responsabilidade
Model	Salvar respostas e usuários
View	Renderizar as telas mencionadas
Controller	views.py: lógica para salvar e processar respostas
