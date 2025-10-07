# 💻 Desafio Técnico Fullstack - Pokédex Digital

Este projeto implementa o Back-End (Python/Flask) e o Front-End (Angular) para o desafio técnico da Kogui.

## 🚀 Back-End (API)

A API foi desenvolvida em Python 3.10+ utilizando o framework **Flask**, seguindo os princípios **SOLID** e **Orientação a Objetos (POO)** com uma arquitetura em camadas (Model, Repository, Service, API).

### Requisitos

* Python 3.10+
* pip (gerenciador de pacotes)

### Configuração e Execução

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd pokedex-backend
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate   # Windows Powershell
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o arquivo de configurações (`.env`):**
    Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

    ```env
    SECRET_KEY="SUA_CHAVE_SECRETA_LONGA"
    FLASK_ENV=development
    DATABASE_URL="sqlite:///pokedex.db"
    ```

5.  **Execute o servidor Flask:**
    ```bash
    python run.py
    ```

    A API estará acessível em `http://127.0.0.1:5000/api/v1/`.

### Endpoints Principais

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Cria um novo usuário. |
| `POST` | `/auth/login` | Gera o Token JWT. |
| `GET` | `/pokemon/` | Lista Pokémon com Paginação e Filtros (Nome/Geração). **(Requer JWT)** |
| `POST` | `/pokemon/<code_pokemon>/favorite` | Adiciona/Remove de Favoritos. **(Requer JWT)** |
| `POST` | `/pokemon/<code_pokemon>/team` | Adiciona/Remove da Equipe de Batalha (Máx. 6). **(Requer JWT)** |
| `GET` | `/pokemon/favorites` | Lista todos os favoritos do usuário. **(Requer JWT)** |
| `GET` | `/pokemon/team` | Lista a equipe de batalha do usuário. **(Requer JWT)** |

---

### Contato e Contribuição

Autor: **Aylla Scaglia**

Contato: [Linkedin](https://www.linkedin.com/in/aylla-scaglia/)