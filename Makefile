.PHONY: install format lint test run deploy-dev deploy-prod clean update-env

# Install dependencies
install:
	poetry install

# Format code
format:
	poetry run black .
	poetry run isort .

# Lint code
lint:
	poetry run flake8 .
	poetry run mypy .

# Run tests
test:
	poetry run pytest

# Run application
run:
	poetry run python run.py

# Deploy infrastructure to dev environment
deploy-dev:
	cd infrastructure && pulumi up --stack dev
	cd infrastructure && python update_env.py dev

# Deploy infrastructure to production environment
deploy-prod:
	cd infrastructure && pulumi up --stack prod
	cd infrastructure && python update_env.py prod

# Clean temporary files
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache

# Update .env file from Pulumi output
update-env:
	cd infrastructure && python update_env.py
