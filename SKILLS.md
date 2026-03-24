# 📚 Skills & Arquitetura do ENS_Daily

## Visão Geral

O ENS_Daily segue uma **arquitetura em camadas** baseada em **Domain-Driven Design (DDD)**, com separação clara de responsabilidades.

```
┌─────────────────────────────┐
│    Apresentação (Flask)     │  app.py
├─────────────────────────────┤
│    Aplicação (Services)     │  application/
├─────────────────────────────┤
│    Domínio (Modelos)        │  domain/
├─────────────────────────────┤
│    Persistência (Repository)│  repository/
├─────────────────────────────┤
│    Dados (JSON/BD)          │  game_state.json
└─────────────────────────────┘
```

---

## 🏗️ Estrutura por Camada

### 1. **Domain** (`domain/`)
Contém a **lógica de negócio pura**, independente de frameworks.

- `game.py` - Entidade principal, gerencia estado do jogo (streak, missões)
- `daily_mission.py` - Missão diária com status de progresso
- `reading_text.py` - Texto de leitura

**Características:**
- Sem dependências de Flask/BD
- Métodos que implementam regras de negócio
- Estado é transformável e persistível

### 2. **Application** (`application/`)
Camada de **orquestração** entre controllers e domínio.

- `game_service.py` - Coordena operações do Game (get, complete, save)
- `reading_text_service.py` - Gerencia textos de leitura

**Responsabilidades:**
- Chamar repositórios
- Orquestar chamadas ao domínio
- Persistir mudanças

### 3. **Repository** (`repository/`)
Implementa o **padrão Repository** para abstração de persistência.

- `game_repository.py` - Load/save do Game state
- `reading_text_repository.py` - Acesso aos textos

**Vantagem:** Trocar JSON por BD é fácil-implementar apenas aqui

### 4. **Apresentação** (`app.py`)
Rotas Flask e **API REST**.

- `GET /api/mission/daily` - Busca missão do dia
- `GET /api/mission/daily/complete` - Marca como completa
- `GET /api/text/<id>` - Busca texto específico

---

## 🎯 Padrões Utilizados

### Repository Pattern
```python
# ✅ Certo: Usar injeção de dependência
class GameService:
    def __init__(self, repository):
        self.repository = repository
        
    def get_daily_mission(self):
        game = self.repository.get()
        return game.get_daily_mission()
```

### Estados e Persistência
```python
# ✅ Certo: Usar métodos to_dict() e from_persistence()
mission_dict = mission.to_dict()
mission = DailyMission.from_persistence(data, text)
```

### Serviços Stateless
```python
# ✅ Certo: Services apenas orquestram
class GameService:
    def complete_daily_mission(self):
        game = self.repository.get()
        success = game.complete_daily_mission()
        self.repository.save()
        return success, game.streak
```

---

## 🚀 Como Adicionar uma Nova Feature

### Exemplo: Nova skill "Grammar Exercises"

#### 1️⃣ Criar Modelo no Domain
```python
# domain/grammar_exercise.py
class GrammarExercise:
    def __init__(self, id, question, options, correct_answer):
        self.id = id
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.answered = False
        
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer
        
    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "options": self.options,
            "answered": self.answered
        }
```

#### 2️⃣ Criar Repository
```python
# repository/grammar_repository.py
from domain.grammar_exercise import GrammarExercise

class GrammarRepository:
    def __init__(self, data_file='grammar_data.json'):
        self.data_file = data_file
        
    def get_all(self):
        # Carregar do JSON
        exercises = []
        for data in self._load_json():
            exercises.append(GrammarExercise(**data))
        return exercises
```

#### 3️⃣ Criar Service
```python
# application/grammar_service.py
class GrammarService:
    def __init__(self, repository):
        self.repository = repository
        
    def get_exercise(self, exercise_id):
        exercises = self.repository.get_all()
        return next((e for e in exercises if e.id == exercise_id), None)
        
    def submit_answer(self, exercise_id, user_answer):
        exercise = self.get_exercise(exercise_id) 
        is_correct = exercise.check_answer(user_answer)
        return {"correct": is_correct}
```

#### 4️⃣ Registrar Rotas
```python
# app.py
from application.grammar_service import GrammarService
from repository.grammar_repository import GrammarRepository

grammar_repository = GrammarRepository()
grammar_service = GrammarService(grammar_repository)

@app.route('/api/grammar/<int:exercise_id>', methods=['GET'])
def get_grammar_exercise(exercise_id):
    exercise = grammar_service.get_exercise(exercise_id)
    return jsonify(exercise.to_dict()), 200

@app.route('/api/grammar/<int:exercise_id>/submit', methods=['POST'])
def submit_grammar(exercise_id):
    user_answer = request.json.get('answer')
    result = grammar_service.submit_answer(exercise_id, user_answer)
    return jsonify(result), 200
```

---

## 📋 Convenções de Código

| Aspecto | Padrão |
|--------|--------|
| **Nomes de Métodos** | snake_case (`get_daily_mission`) |
| **Nomes de Classes** | PascalCase (`GameService`) |
| **Métodos de Conversão** | `to_dict()` (output), `from_persistence()` (input) |
| **Testes de Lógica** | Devem ficar em `domain/` (sem BD) |
| **Injeção de Dependência** | Via `__init__` no Service |
| **Persistência** | Abstrair no Repository, nunca na lógica |

---

## ✅ Checklist para Nova Feature

- [ ] Criar modelo(ns) em `domain/`
- [ ] Criar repository em `repository/` (se novo tipo de dado)
- [ ] Criar service em `application/`
- [ ] Registrar rotas em `app.py`
- [ ] Implementar `to_dict()` nos modelos
- [ ] Testar isoladamente (sem BD)

---

## 🔄 Fluxo de uma Requisição

```
[Cliente HTTP]
      ↓
[GET /api/mission/daily]
      ↓
[app.py - Route Handler]
      ↓
[GameService.get_daily_mission()]
      ↓
[GameRepository.get()] → Carrega game_state.json
      ↓
[Game Model] → Lógica de negócio
      ↓
[Retorna JSON] → Cliente
```

---

## 🎓 Próximas Evoluções

1. **Testes Unitários** - Pytest com mocks
2. **Autenticação** - JWT para múltiplos usuários
3. **Persistência** - Migrar para PostgreSQL
4. **Cache** - Redis para rankings/dados quentes
5. **Logging** - Estruturado com contexto
6. **API Versioning** - `/api/v1/`

