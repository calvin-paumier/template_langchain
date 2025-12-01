# Variables
PYTHON_VERSION := 3.12.4
PROJECT_NAME := template-langchain
UV_VERSION := latest

# Couleurs pour l'affichage
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

.PHONY: help env deploy install-models fill-db clean test lint

# Aide par défaut
help:
    @echo "$(GREEN)📋 Commandes disponibles :$(RESET)"
	@echo "	$(YELLOW)make env$(RESET)				- Télécharge UV et crée l'environnement"
	@echo "	$(YELLOW)make deploy$(RESET)			- Déploie le docker-compose"
	@echo "	$(YELLOW)make install-models$(RESET)	- Installe les modèles depuis .env"
	@echo "	$(YELLOW)make fill-db$(RESET)			- Remplit la base de données"
	@echo "	$(YELLOW)make clean$(RESET)				- Nettoie l'environnement"
	@echo "	$(YELLOW)make lint$(RESET)				- Lance le linting"

# Installation d'UV et création de l'environnement
env:
	@echo "$(GREEN)🚀 Installation d'UV...$(RESET)"
	@command -v uv >/dev/null 2>&1 || { \
		echo "$(YELLOW)📦 Téléchargement d'UV...$(RESET)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		export PATH="$$HOME/.cargo/bin:$$PATH"; \
	}
	@echo "$(GREEN)🔧 Création de l'environnement UV...$(RESET)"
	uv venv --python $(PYTHON_VERSION)
	@echo "$(GREEN)📦 Installation des dépendances...$(RESET)"
	uv sync --extra dev --extra test --extra notebooks
	@echo "$(GREEN)✅ Environnement prêt !$(RESET)"

# Déploiement Docker Compose
deploy:
	@echo "$(GREEN)🐳 Déploiement du docker-compose...$(RESET)"
	@if [ ! -f docker-compose.yml ]; then \
		echo "$(RED)❌ docker-compose.yml non trouvé !$(RESET)"; \
		exit 1; \
	fi
	@if [ ! -f .env ]; then \
		echo "$(RED)❌ Fichier .env non trouvé !$(RESET)"; \
		exit 1; \
	fi
	docker-compose down --remove-orphans
	docker-compose up -d
	@echo "$(GREEN)✅ Services déployés !$(RESET)"

# Installation des modèles depuis .env
install-models:
	@echo "$(GREEN)🤖 Installation des modèles Ollama...$(RESET)"
	@if [ ! -f .env ]; then \
		echo "$(RED)❌ Fichier .env non trouvé !$(RESET)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)📋 Lecture des modèles depuis .env...$(RESET)"
	@export $$(cat .env | grep -v '^#' | xargs) && \
	echo "$(GREEN)📦 Installation du modèle principal : $$OLLAMA_MODEL$(RESET)" && \
	(docker exec $$(docker-compose ps -q ollama) ollama pull $$OLLAMA_MODEL 2>/dev/null || \
	 ollama pull $$OLLAMA_MODEL 2>/dev/null || \
	 echo "$(RED)⚠️  Impossible d'installer $$OLLAMA_MODEL$(RESET)") && \
	echo "$(GREEN)📦 Installation du modèle tool binding : $$OLLAMA_TOOL_BINDING_MODEL$(RESET)" && \
	(docker exec $$(docker-compose ps -q ollama) ollama pull $$OLLAMA_TOOL_BINDING_MODEL 2>/dev/null || \
	 ollama pull $$OLLAMA_TOOL_BINDING_MODEL 2>/dev/null || \
	 echo "$(RED)⚠️  Impossible d'installer $$OLLAMA_TOOL_BINDING_MODEL$(RESET)") && \
	echo "$(GREEN)📦 Installation du modèle d'embedding : $$OLLAMA_EMBEDDING_MODEL$(RESET)" && \
	(docker exec $$(docker-compose ps -q ollama) ollama pull $$OLLAMA_EMBEDDING_MODEL 2>/dev/null || \
	 ollama pull $$OLLAMA_EMBEDDING_MODEL 2>/dev/null || \
	 echo "$(RED)⚠️  Impossible d'installer $$OLLAMA_EMBEDDING_MODEL$(RESET)")
	@echo "$(GREEN)✅ Installation des modèles terminée !$(RESET)"
	@echo "$(YELLOW)📊 Modèles installés :$(RESET)"
	@docker exec $$(docker-compose ps -q ollama) ollama list 2>/dev/null || ollama list 2>/dev/null || echo "$(YELLOW)Impossible de lister les modèles$(RESET)"

# Remplissage de la base de données
fill-db:
	@echo "$(GREEN)🗄️  Remplissage de la base de données...$(RESET)"
	uv run python sources/agent_multi_tools/launch/cli/app_fill_in_database.py
	uv run python sources/agent_multi_tools/launch/cli/app_fill_in_vector_db.py
	@echo "$(GREEN)✅ Base de données remplie !$(RESET)"

# Nettoyage
clean:
	@echo "$(GREEN)🧹 Nettoyage...$(RESET)"
	docker-compose down --remove-orphans --volumes
	rm -rf .venv
	rm -rf __pycache__ **/__pycache__ **/**/__pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info
	@echo "$(GREEN)✅ Nettoyage terminé !$(RESET)"

# Auto-correction avec Ruff et mypy
lint:
	@echo "$(YELLOW)🔨 Correction automatique des erreurs...$(RESET)"
	uv run ruff check --fix sources/
	@echo "$(YELLOW)🎨 Formatage automatique du code...$(RESET)"
	uv run ruff format sources/
	@echo "$(GREEN)✅ Code corrigé et formaté !$(RESET)"
	
# Lancement de l'application Streamlit
streamlit:
	@echo "$(GREEN)🚀 Lancement de l'application Streamlit...$(RESET)"
	uv run streamlit run sources/agent_multi_tools/launch/web/app_streamlit.py
	@echo "$(GREEN)✅ Application Streamlit arrêtée !$(RESET)"
