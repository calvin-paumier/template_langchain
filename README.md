# 🤖 Template LangChain Agent

Un template d'agent conversationnel intelligent basé sur LangChain et LangGraph, capable de router automatiquement entre différents outils selon le type de question.

## 🎯 Fonctionnalités

- **🔀 Routing intelligent** : Choix automatique entre RAG et TextToSQL selon le contexte
- **🗄️ Text-to-SQL** : Génération et exécution de requêtes SQL sur une base Sanrio
- **📚 RAG (Retrieval-Augmented Generation)** : Recherche vectorielle pour questions générales
- **💭 Mémoire conversationnelle** : Gestion de l'historique par session
- **⚡ Optimisé UV** : Installation et gestion rapide des dépendances

## 🚀 Installation rapide

### Prérequis
- Python 3.12.4+
- Docker & Docker Compose
- Git

### Setup complet en une commande
```bash
# 1. Clonage du projet
git clone <votre-repo>
cd template_langchain

# 2. Installation d'UV et environnement Python
make env

# 3. Démarrage des services (PostgreSQL, Ollama)
make deploy

# 4. Téléchargement des modèles IA
make install-models

# 5. Population de la base de données
make fill-db
```

## 🔧 Configuration

### Fichier `.env`
Créez un fichier `.env` à la racine :

```bash
# Base de données PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=my_db
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_password

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
```

### Services Docker
Les services suivants sont automatiquement démarrés :
- **PostgreSQL** : Base de données principale
- **Ollama** : Serveur de modèles LLM locaux

## 💬 Utilisation

Test possible en lançant la commande :
```bash
make streamlit
```

## 🛠️ Commandes Makefile

```bash
make help              # Affiche l'aide
make env               # Setup environnement UV
make deploy            # Démarre docker-compose  
make install-models    # Télécharge les modèles IA
make fill-db           # Remplit la base de données
make lint              # Lance Ruff
make streamlit         # Lance l'application Streamlit
```