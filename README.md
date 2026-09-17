# 🚀 Registro de Despesas

Aplicação web para gerenciamento de despesas, desenvolvida com **FastAPI, PostgreSQL, Docker, Nginx e AWS**, com infraestrutura provisionada utilizando **Terraform** e pipeline de integração contínua utilizando **GitHub Actions**.

O projeto foi desenvolvido com foco em práticas de **Cloud, DevOps, Infrastructure as Code (IaC), containers, CI/CD, segurança, observabilidade e gerenciamento de banco de dados**.

---

## 📚 Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Arquitetura](#-arquitetura)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Fluxo da aplicação](#-fluxo-da-aplicação)
- [CI com GitHub Actions](#-ci-com-github-actions)
- [Gerenciamento do banco de dados com Alembic](#-gerenciamento-do-banco-de-dados-com-alembic)
- [Infraestrutura com Terraform](#-infraestrutura-com-terraform)
- [Execução local](#-execução-local)
- [Execução com Docker Compose](#-execução-com-docker-compose)
- [Build manual das imagens Docker](#-build-manual-das-imagens-docker)
- [Deploy na AWS](#-deploy-na-aws)
- [Validação da aplicação](#-validação-da-aplicação)
- [Endpoints da API](#-endpoints-da-api)
- [Monitoramento e logs](#-monitoramento-e-logs)
- [Segurança](#-segurança)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Boas práticas aplicadas](#-boas-práticas-aplicadas)
- [Melhorias futuras](#-melhorias-futuras)
- [Autor](#-autor)

---

# 📌 Sobre o projeto

O **Registro de Despesas** é uma aplicação web desenvolvida para permitir o cadastro, consulta e exclusão de despesas.

Além da aplicação, o projeto foi estruturado como um laboratório prático de **Cloud e DevOps**, utilizando serviços AWS e ferramentas modernas de infraestrutura, automação, containers, segurança e observabilidade.

A aplicação utiliza uma arquitetura baseada em containers e serviços gerenciados da AWS.

O fluxo principal da aplicação é:

```text
                    Internet
                       │
                       ▼
              ┌─────────────────┐
              │  Application    │
              │  Load Balancer  │
              │      (ALB)      │
              └────────┬────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
      ┌─────────────┐     ┌─────────────┐
      │  Frontend   │     │   Backend   │
      │    Nginx    │     │   FastAPI   │
      │ ECS Fargate │     │ ECS Fargate │
      └─────────────┘     └──────┬──────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │ PostgreSQL RDS │
                         └────────────────┘

A infraestrutura é provisionada utilizando Terraform.

As imagens Docker são construídas e publicadas no Amazon ECR através do GitHub Actions.

🏗️ Arquitetura

A arquitetura AWS utiliza os seguintes componentes:

Rede
Amazon VPC
Subnets públicas
Subnets privadas
Internet Gateway
NAT Gateway
Security Groups
Compute
Amazon ECS
AWS Fargate
Load Balancing
Application Load Balancer
Target Groups
Health Checks
Banco de dados
Amazon RDS
PostgreSQL
Containers
Docker
Docker Compose
Amazon ECR
Nginx
FastAPI
Segurança
AWS IAM
GitHub OIDC
AWS Secrets Manager
Security Groups
Observabilidade
Amazon CloudWatch
ECS Container Logs
ALB Health Checks
Infrastructure as Code
Terraform
CI/CD
GitHub Actions
Docker Build
Amazon ECR
📁 Estrutura do projeto
Registro-de-despesas/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── 001_create_despesas.py
│   │   │
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   └── models.py
│   │
│   ├── tests/
│   │   └── ...
│   │
│   ├── alembic.ini
│   ├── Dockerfile
│   └── requirements.txt
│
├── terraform/
│   ├── alb.tf
│   ├── ecs.tf
│   ├── ecr.tf
│   ├── iam.tf
│   ├── logs.tf
│   ├── rds.tf
│   ├── secrets.tf
│   ├── security_groups.tf
│   ├── variables.tf
│   ├── vpc.tf
│   └── ...
│
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── index.html
├── .env
├── .gitignore
└── README.md
🔄 Fluxo da aplicação

A aplicação funciona seguindo o seguinte fluxo:

Usuário
   │
   ▼
Application Load Balancer
   │
   ├── / ───────────────► Frontend
   │                       Nginx
   │
   └── /api/* ──────────► Backend
                           FastAPI
                              │
                              ▼
                         PostgreSQL
                              │
                              ▼
                          Amazon RDS

O frontend utiliza:

API_URL = '/api'

Dessa forma, as requisições destinadas à API são encaminhadas pelo Application Load Balancer para o serviço backend.

🔁 CI com GitHub Actions

O projeto possui um pipeline de Integração Contínua (CI) utilizando GitHub Actions.

Arquivo:

.github/workflows/ci.yml

O workflow é executado em:

Push na branch main
Push na branch feat/devops-migration
Pull Requests direcionados para main

O pipeline possui duas etapas principais:

GitHub
   │
   ▼
Tests
   │
   ├── Python
   ├── Pytest
   ├── Docker Build
   │
   ▼
Push Images
   │
   ├── Backend → ECR
   └── Frontend → ECR
🔹 1. Checkout do código

O pipeline começa realizando o checkout do repositório:

- name: Checkout repository
  uses: actions/checkout@v4
🔹 2. Configuração do Python

O ambiente Python utilizado no pipeline é o Python 3.12:

- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
🔹 3. Instalação das dependências

As dependências são instaladas através do arquivo:

backend/requirements.txt

Também são instalados:

pytest
httpx

para execução dos testes automatizados.

🔹 4. Execução dos testes

Os testes são executados através do comando:

PYTHONPATH=backend pytest backend/tests -v

Os testes cobrem atualmente:

Health Check
Criação de despesas
Listagem de despesas
Exclusão de despesas

Resultado validado:

4 passed
🔹 5. Build da imagem Docker do Backend

Após os testes, o pipeline realiza o build da imagem Docker do backend:

docker build \
  -t registro-despesas-backend:${{ github.sha }} \
  ./backend

A imagem é identificada pelo SHA do commit.

Isso permite relacionar uma imagem Docker diretamente ao código responsável pela build.

🔹 6. Build da imagem Docker do Frontend

O frontend também é construído durante o processo de CI:

docker build \
  -t registro-despesas-frontend:${{ github.sha }} \
  .
📦 Push das imagens para Amazon ECR

Após a conclusão dos testes, o segundo job realiza a publicação das imagens Docker no Amazon ECR.

O job depende do sucesso dos testes:

needs: tests

Dessa forma:

Tests
  │
  ├── Falhou → Pipeline interrompido
  │
  └── Sucesso
        │
        ▼
     Build
        │
        ▼
      ECR
🔐 Autenticação AWS utilizando GitHub OIDC

O projeto utiliza GitHub OIDC para autenticação do GitHub Actions na AWS.

O fluxo é:

GitHub Actions
      │
      ▼
GitHub OIDC
      │
      ▼
AWS IAM Role
      │
      ▼
Recursos AWS

A configuração evita a necessidade de armazenar Access Keys diretamente nos Secrets do GitHub.

A IAM Role possui uma política de confiança restrita ao repositório e branch utilizados pelo projeto.

🔹 Login no Amazon ECR

O pipeline realiza autenticação no ECR utilizando:

- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v2
🔹 Build e Push do Backend

A imagem do backend é criada utilizando o SHA do commit:

docker build \
  -t <ECR_REGISTRY>/registro-despesas-backend:${{ github.sha }} \
  ./backend

Depois é publicada:

docker push \
  <ECR_REGISTRY>/registro-despesas-backend:${{ github.sha }}
🔹 Build e Push do Frontend

O frontend também utiliza o SHA do commit:

docker build \
  -t <ECR_REGISTRY>/registro-despesas-frontend:${{ github.sha }} \
  .

Depois:

docker push \
  <ECR_REGISTRY>/registro-despesas-frontend:${{ github.sha }}
🗄️ Gerenciamento do banco de dados com Alembic

O projeto utiliza Alembic para controle de alterações do schema do PostgreSQL.

Inicialmente, a aplicação utilizava:

Base.metadata.create_all(...)

Essa abordagem foi removida.

Atualmente o schema do banco é controlado através de migrations.

📋 Migration inicial

A primeira migration do projeto cria a tabela:

despesas

Com as seguintes colunas:

id
ano
mes
dia
tipo
descricao
valor

A migration está localizada em:

backend/alembic/versions/001_create_despesas.py
🔄 Execução da migration

A migration pode ser executada através do comando:

alembic -c /app/alembic.ini upgrade head

No ambiente AWS, a migration foi executada através de uma ECS Task utilizando a imagem Docker do backend.

O histórico validado foi:

<base> -> 001_create_despesas (head)
🐳 Alembic dentro do container

O Dockerfile do backend copia os arquivos do Alembic:

COPY alembic ./alembic
COPY alembic.ini ./alembic.ini

Dessa forma, a imagem contém:

/app
│
├── app/
├── alembic/
├── alembic.ini
└── requirements.txt

A imagem pode executar tanto a aplicação quanto os comandos de migration.

🏗️ Infraestrutura com Terraform

Toda a infraestrutura principal da aplicação é definida utilizando Terraform.

O objetivo é aplicar o conceito de:

Infrastructure as Code

permitindo que os recursos AWS sejam versionados juntamente com o projeto.

🌐 VPC

A aplicação utiliza uma VPC:

10.0.0.0/16

A rede é dividida entre subnets públicas e privadas.

VPC
10.0.0.0/16
│
├── Public Subnet A
│   10.0.1.0/24
│
├── Public Subnet B
│   10.0.2.0/24
│
├── Private Subnet A
│   10.0.11.0/24
│
└── Private Subnet B
    10.0.12.0/24
🌍 Subnets públicas

As subnets públicas são utilizadas pelos componentes que precisam de acesso direto ao Internet Gateway.

Entre eles:

Application Load Balancer
NAT Gateway
🔒 Subnets privadas

Os serviços ECS e o banco de dados RDS são executados em subnets privadas.

Private Subnets
      │
      ├── ECS Frontend
      │
      ├── ECS Backend
      │
      └── RDS PostgreSQL

Os containers ECS não recebem IP público.

🌐 NAT Gateway

O NAT Gateway permite que recursos localizados nas subnets privadas realizem conexões de saída para a Internet quando necessário.

Fluxo:

Private Subnet
      │
      ▼
NAT Gateway
      │
      ▼
Internet Gateway
      │
      ▼
Internet
⚖️ Application Load Balancer

O Application Load Balancer é o ponto de entrada da aplicação.

O ALB possui regras de roteamento baseadas no caminho da requisição.

/
│
└──► Frontend

/api/*
│
└──► Backend
🎯 Target Groups

O frontend possui um Target Group configurado na porta:

80

O backend possui um Target Group configurado na porta:

8000
❤️ Health Checks

O backend possui um endpoint específico para verificar a saúde da aplicação:

GET /health

Resposta:

{
  "status": "ok",
  "service": "registro-de-despesas-api"
}

O Target Group do backend utiliza:

/health

como health check.

O frontend utiliza:

/

como health check.

🚀 ECS Fargate

A aplicação é executada utilizando Amazon ECS com AWS Fargate.

Arquitetura:

ECS Cluster
│
├── Frontend Service
│   │
│   └── Nginx Container
│
└── Backend Service
    │
    └── FastAPI Container

Cada serviço possui seu próprio container e Target Group.

🐳 Frontend

O frontend utiliza uma imagem baseada em:

nginx:alpine

Dockerfile:

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY . /usr/share/nginx/html

EXPOSE 80

O Nginx é responsável por servir os arquivos estáticos da aplicação.

🐍 Backend

O backend utiliza:

Python 3.12
FastAPI
Uvicorn
SQLAlchemy
PostgreSQL
Alembic

A aplicação é iniciada através de:

uvicorn app.main:app --host 0.0.0.0 --port 8000
🗄️ Amazon RDS PostgreSQL

O banco de dados utiliza:

Amazon RDS
PostgreSQL 17

O banco está localizado em subnets privadas.

Configuração utilizada no projeto:

Engine: PostgreSQL
Instance: db.t3.micro
Storage: 20 GB
Storage Type: gp3
Port: 5432

O acesso ao banco é restrito através de Security Groups.

🔐 Security Groups

A comunicação entre os componentes é controlada através de Security Groups.

Arquitetura:

Internet
   │
   │ HTTP :80
   ▼
┌──────────────┐
│     ALB      │
└──────┬───────┘
       │
       ├──────────────► Frontend :80
       │
       └──────────────► Backend :8000
                              │
                              │ PostgreSQL :5432
                              ▼
                           RDS

Regras principais:

ALB
 └── HTTP 80 ← Internet

Frontend
 └── HTTP 80 ← ALB

Backend
 └── TCP 8000 ← ALB

RDS
 └── TCP 5432 ← ECS Backend
🔑 AWS Secrets Manager

As informações utilizadas para conexão com o banco de dados são armazenadas no AWS Secrets Manager.

O Secret contém informações como:

username
password
database
host
port

A aplicação não precisa armazenar essas credenciais diretamente no código.

O ECS recebe os valores através da integração com Secrets Manager.

🧑‍💻 IAM

O projeto utiliza IAM Roles para controlar o acesso aos recursos AWS.

Entre os principais usos:

ECS Task Execution Role
GitHub Actions Role
Acesso ao Amazon ECR
Acesso ao CloudWatch Logs
Acesso ao Secrets Manager
💻 Execução local

Para executar o projeto localmente é necessário possuir:

Git
Python 3.12+
Docker
Docker Compose
🔹 Clone do projeto
git clone https://github.com/bbomfimti/Registro-de-despesas.git

Entre no diretório:

cd Registro-de-despesas
🐍 Executando o Backend localmente

Crie o ambiente virtual:

python3 -m venv backend/.venv

Ative:

source backend/.venv/bin/activate

Instale as dependências:

pip install -r backend/requirements.txt

Execute a aplicação:

uvicorn backend.app.main:app --reload --port 8000

A API estará disponível em:

http://localhost:8000
📖 Swagger

A documentação interativa da API pode ser acessada em:

http://localhost:8000/docs

Também é possível verificar:

curl -I http://localhost:8000/docs

Resultado esperado:

HTTP/1.1 200 OK
❤️ Health Check local

Execute:

curl http://localhost:8000/health

Resposta esperada:

{
  "status": "ok",
  "service": "registro-de-despesas-api"
}
🐳 Execução com Docker Compose

O projeto possui um ambiente Docker Compose contendo:

Frontend
Backend
PostgreSQL

Para iniciar todos os serviços:

docker compose up -d --build

Verifique os containers:

docker compose ps
🌐 Frontend local

O frontend estará disponível em:

http://localhost:8080
🔌 Backend local

O backend estará disponível em:

http://localhost:8000

Swagger:

http://localhost:8000/docs
🗄️ PostgreSQL local

O PostgreSQL utilizado pelo Docker Compose está disponível na porta:

5432
📋 Logs do Docker Compose

Para visualizar os logs do backend:

docker compose logs backend

Frontend:

docker compose logs frontend

PostgreSQL:

docker compose logs postgres

Para acompanhar os logs em tempo real:

docker compose logs -f
🛑 Parando os containers

Para parar os serviços:

docker compose down

Para parar e remover também os volumes:

docker compose down -v
🔨 Build manual das imagens Docker

Além do Docker Compose, é possível criar as imagens individualmente.

Backend

Build:

docker build \
  -t registro-despesas-backend:latest \
  ./backend

Executar:

docker run \
  --name registro-despesas-backend \
  -p 8000:8000 \
  registro-despesas-backend:latest
Frontend

Build:

docker build \
  -t registro-despesas-frontend:latest \
  .

Executar:

docker run \
  --name registro-despesas-frontend \
  -p 8080:80 \
  registro-despesas-frontend:latest
🧪 Testes automatizados

Os testes podem ser executados localmente utilizando Pytest.

Execute:

PYTHONPATH=backend pytest backend/tests -v

Resultado esperado:

4 passed

Os testes atualmente cobrem:

Health Check
Criação de despesa
Listagem de despesas
Exclusão de despesa
☁️ Deploy na AWS

A arquitetura de deploy utiliza:

Developer
    │
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Tests
    │
    ├── Docker Build
    │
    └── Push
         │
         ▼
     Amazon ECR
         │
         ▼
    ECS Fargate
         │
         ▼
        ALB
         │
         ▼
      Usuário

A infraestrutura é provisionada através do Terraform.

As imagens Docker são construídas e publicadas no ECR pelo GitHub Actions.

⚠️ Estado atual do processo de deploy

Atualmente o pipeline automatiza:

Testes
   ↓
Docker Build
   ↓
Push para ECR

A atualização do serviço ECS ainda é realizada como uma etapa operacional/manual.

Da mesma forma, a execução das migrations Alembic ainda é realizada separadamente através de uma ECS Task.

Portanto, o projeto atualmente possui CI automatizado e publicação das imagens no ECR, enquanto a automação completa do CD para ECS está planejada como evolução futura.

🗃️ Processo atual de migration no ambiente AWS

Quando uma nova migration precisa ser aplicada, uma ECS Task pode ser executada utilizando a imagem atualizada do backend.

O comando utilizado é:

alembic -c /app/alembic.ini upgrade head

O processo utiliza as configurações de banco disponibilizadas através do AWS Secrets Manager.

Após a execução, o Alembic registra a migration aplicada na tabela de controle do banco.

🔍 Validação da aplicação em produção

Após o deploy, a aplicação pode ser validada através do Application Load Balancer.

Primeiramente, o Health Check:

GET /health

Depois:

GET /api/despesas

A validação permite verificar o fluxo completo:

Internet
   ↓
ALB
   ↓
ECS
   ↓
FastAPI
   ↓
RDS PostgreSQL
➕ Criando uma despesa

Endpoint:

POST /api/despesas

Exemplo:

{
  "ano": 2026,
  "mes": 9,
  "dia": 16,
  "tipo": "Alimentação",
  "descricao": "Almoço",
  "valor": 35.90
}
📋 Listando despesas

Endpoint:

GET /api/despesas

Exemplo:

curl http://localhost:8000/api/despesas
🗑️ Removendo uma despesa

Endpoint:

DELETE /api/despesas/{despesa_id}

Exemplo:

curl -X DELETE http://localhost:8000/api/despesas/1
🧪 Validação end-to-end

Durante a validação do ambiente AWS foram realizados testes completos do fluxo da aplicação.

Health Check
GET /health
→ HTTP 200
Consulta inicial
GET /api/despesas
→ HTTP 200
→ []
Criação
POST /api/despesas
→ HTTP 200
Consulta
GET /api/despesas
→ HTTP 200
→ registro criado
Exclusão
DELETE /api/despesas/1
→ HTTP 200
Consulta final
GET /api/despesas
→ HTTP 200
→ []

Esse processo validou a comunicação entre:

ALB
 ↓
ECS Fargate
 ↓
FastAPI
 ↓
RDS PostgreSQL
🔌 Endpoints da API
Método	Endpoint	Descrição
GET	/health	Verifica a saúde da aplicação
GET	/api/despesas	Lista todas as despesas
POST	/api/despesas	Cria uma nova despesa
DELETE	/api/despesas/{despesa_id}	Remove uma despesa
📊 Monitoramento e logs

Os containers ECS enviam logs para o:

Amazon CloudWatch Logs

A aplicação utiliza logs para auxiliar na identificação de problemas relacionados a:

Inicialização do container
Erros da aplicação
Conexão com PostgreSQL
Falhas nos health checks
Problemas de infraestrutura
Falhas no serviço ECS
❤️ Health Checks

O Application Load Balancer monitora a disponibilidade dos serviços através dos Target Groups.

Backend:

/health

Frontend:

/

Caso um container não responda corretamente ao health check, o ALB pode deixar de encaminhar tráfego para o target considerado unhealthy.

🔒 Segurança

O projeto utiliza diferentes mecanismos de segurança.

IAM

Utilização de IAM Roles para controlar o acesso aos serviços AWS.

GitHub OIDC

O GitHub Actions utiliza OIDC para autenticação na AWS.

Isso evita armazenar Access Keys diretamente no GitHub Actions.

Secrets Manager

Informações sensíveis relacionadas ao banco são armazenadas no:

AWS Secrets Manager
Security Groups

O acesso entre os componentes é limitado através de regras específicas.

Internet
   │
   ▼
ALB :80
   │
   ├──► Frontend :80
   │
   └──► Backend :8000
             │
             ▼
          RDS :5432
Subnets privadas

Os serviços internos da aplicação são executados em subnets privadas:

ECS Backend
ECS Frontend
RDS
🧱 Infrastructure as Code

A infraestrutura AWS é definida através de Terraform.

Exemplo de organização:

terraform/
│
├── alb.tf
├── ecs.tf
├── ecr.tf
├── iam.tf
├── logs.tf
├── rds.tf
├── secrets.tf
├── security_groups.tf
├── variables.tf
└── vpc.tf

Isso permite que a infraestrutura seja:

Versionada
Reproduzível
Auditável
Documentada
Automatizável
🧰 Tecnologias utilizadas
Backend
Python 3.12
FastAPI
Uvicorn
SQLAlchemy
PostgreSQL
Alembic
Pytest
HTTPX
Frontend
HTML
CSS
JavaScript
Nginx
Containers
Docker
Docker Compose
AWS
Amazon VPC
Amazon ECS
AWS Fargate
Amazon ECR
Application Load Balancer
Amazon RDS
PostgreSQL
AWS Secrets Manager
AWS IAM
Amazon CloudWatch
NAT Gateway
Internet Gateway
DevOps
Terraform
Git
GitHub
GitHub Actions
GitHub OIDC
CI/CD
Infrastructure as Code
Containerization
🧠 Boas práticas aplicadas

Durante o desenvolvimento foram aplicadas práticas relacionadas a:

Infrastructure as Code
Containerization
CI
Docker Image Versioning
GitHub Actions
GitHub OIDC
IAM
Secrets Management
AWS Networking
Private Subnets
Health Checks
CloudWatch Logs
Database Migrations
Automated Tests
Environment Variables
Separation of Frontend and Backend
Load Balancing
📈 Evolução do projeto

O projeto foi desenvolvido de forma incremental.

Etapa 1 — Aplicação
FastAPI
PostgreSQL
Frontend
Etapa 2 — Containers
Docker
Docker Compose
Etapa 3 — Cloud
AWS
ECS
Fargate
RDS
ECR
ALB
Etapa 4 — Infrastructure as Code
Terraform
Etapa 5 — CI
GitHub Actions
Pytest
Docker Build
ECR Push
Etapa 6 — Segurança
IAM
GitHub OIDC
Secrets Manager
Security Groups
Private Subnets
Etapa 7 — Database Migration
Alembic
ECS Migration Task
Próxima evolução
Continuous Deployment
Reusable Workflows
Custom Actions
Automated Migration
Smoke Tests
Observability
Kubernetes
Helm
🚧 Melhorias futuras
CI/CD
 Automatizar o deploy do ECS através do GitHub Actions
 Atualizar automaticamente a ECS Task Definition
 Atualizar automaticamente o ECS Service
 Implementar rollout controlado
 Implementar rollback automático
 Adicionar smoke tests após deploy
Alembic
 Integrar migrations ao pipeline de deploy
 Criar job específico para database migration
 Validar migration antes do rollout da aplicação
 Controlar migrations por ambiente
GitHub Actions
 Criar workflows reutilizáveis
 Criar Custom Actions
 Separar CI e CD
 Criar pipeline específico para Pull Requests
 Adicionar validação de infraestrutura Terraform
 Adicionar Terraform Plan no Pull Request
Segurança
 Adicionar SAST
 Adicionar Dependency Scanning
 Adicionar Docker Image Scanning
 Melhorar políticas IAM seguindo Least Privilege
 Adicionar validações de segurança no pipeline
Observabilidade
 Criar dashboards no CloudWatch
 Criar CloudWatch Alarms
 Criar métricas customizadas
 Implementar Prometheus
 Implementar Grafana
 Implementar tracing distribuído
Kubernetes

Como evolução da arquitetura, está prevista a criação de uma versão utilizando Kubernetes:

 Criar manifests Kubernetes
 Criar Deployment
 Criar Service
 Criar ConfigMap
 Criar Secret
 Criar Ingress
 Criar Helm Chart
 Executar aplicação no Amazon EKS
🎯 Objetivo técnico do projeto

O objetivo deste projeto é demonstrar, através de uma aplicação prática, conhecimentos relacionados a:

Infrastructure
      │
      ▼
Cloud Computing
      │
      ▼
Containers
      │
      ▼
Infrastructure as Code
      │
      ▼
Continuous Integration
      │
      ▼
Security
      │
      ▼
Database Migration
      │
      ▼
Observability
      │
      ▼
DevOps

A proposta é continuar evoluindo a aplicação em direção a uma arquitetura cada vez mais próxima de ambientes reais de produção.

👨‍💻 Autor

Bruno dos Santos Bomfim

Profissional de Infraestrutura em transição para Cloud & DevOps.

Experiência prática com:

AWS
Terraform
Docker
Kubernetes
Linux
GitHub Actions
CI/CD
Infrastructure as Code
Cloud Computing
Redes
Automação
🔗 Repositório

GitHub:

git clone -b feat/devops-migration https://github.com/bbomfimti/Registro-de-despesas.git

📌 Status do projeto

🚧 Em evolução

O projeto continua recebendo melhorias relacionadas a:

DevOps
Cloud
CI/CD
Segurança
Observabilidade
Automação
Kubernetes
Infrastructure as Code