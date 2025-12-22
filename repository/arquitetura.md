project/
│
├── app.py # Camada de interface (Flask)
│
├── domain/
│   └── game.py # Entidade + regras
│
├── application/
│   └── game_service.py # Casos de uso
│
└── repository/
    └── game_repository.py  # Armazenamento em memória