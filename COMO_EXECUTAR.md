# Como Executar a Aplicação ENS_Daily

## 📋 Pré-requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)
- Git

## 🚀 Instalação e Execução

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd ENS_Daily
```

### 2. Criar um ambiente virtual (Recomendado)

#### No Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install flask
```

Ou, se existir um arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
python app.py
```

Ou alternativamente:
```bash
flask run
```

A aplicação estará disponível em: **http://localhost:5000**

## 📁 Estrutura do Projeto

```
ENS_Daily/
├── app.py                          # Arquivo principal (Flask)
├── static/
│   ├── app.js                      # JavaScript frontend
│   └── style.css                   # Estilos CSS
├── templates/
│   └── index.html                  # Template HTML principal
├── domain/
│   ├── daily_mission.py            # Entidade DailyMission
│   ├── game.py                     # Lógica do jogo
│   └── reading_text.py             # Entidade ReadingText
├── application/
│   ├── game_service.py             # Serviço de jogo
│   └── reading_text_service.py     # Serviço de textos
├── repository/
│   ├── game_repository.py          # Persistência de jogo
│   └── reading_text_repository.py  # Persistência de textos
├── game_state.json                 # Estado da aplicação
└── README.md                       # Documentação
```

## 🔌 Endpoints da API

### Missão Diária
- **GET** `/api/mission/daily` - Obtém a missão diária atual
- **GET** `/api/mission/daily/complete` - Marca a missão como completa

### Textos
- **GET** `/api/text/<text_id>` - Obtém um texto específico por ID

### Interface Web
- **GET** `/` - Retorna a página principal (index.html)

## 🌐 Acessar a Aplicação

Após executar `python app.py`, abra seu navegador e vá para:

```
http://localhost:5000
```

## 🛠️ Desenvolvimento

### Modo Debug (Desenvolvimento)

Para ativar o modo debug com auto-reload:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Variáveis de Ambiente

A aplicação roda em:
- **Host**: 0.0.0.0 (acessível de qualquer máquina da rede)
- **Porta**: 5000
- **Debug**: Desativado (pode ser alterado em `app.py`)

## 📝 Exemplo de Requisição

### Obter missão diária

```bash
curl http://localhost:5000/api/mission/daily
```

Resposta esperada:
```json
{
  "streak": 0,
  "mission": {
    "id": 1,
    "title": "Exemplo de Missão"
  }
}
```

## ❌ Troubleshooting

### "Porta 5000 já está em uso"
```bash
# Mude a porta no app.py ou use:
flask run --port 5001
```

### "ModuleNotFoundError: No module named 'flask'"
```bash
# Instale as dependências:
pip install flask
```

### Ambiente virtual não ativa
```bash
# Certifique-se de estar no diretório correto:
cd ENS_Daily
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

## 🧪 Testando a Aplicação

A aplicação está pronta para receber requisições HTTP. Você pode testar usando:

- **cURL** (linha de comando)
- **Postman** (cliente HTTP)
- **Frontend web** (acessando http://localhost:5000)

## 📚 Arquitetura

A aplicação segue o padrão de arquitetura em camadas:

- **Camada de Apresentação**: `app.py` (Flask routes) + `templates/` + `static/`
- **Camada de Aplicação**: `application/` (Game Service, Reading Text Service)
- **Camada de Domínio**: `domain/` (Entidades e regras de negócio)
- **Camada de Dados**: `repository/` (Persistência e acesso a dados)

## 📖 Para mais informações

Consulte o arquivo [arquitetura.md](./arquitetura.md) para detalhes sobre a arquitetura do projeto.
