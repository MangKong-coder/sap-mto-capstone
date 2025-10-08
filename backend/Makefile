# Makefile to generate requirements.txt using uv pip freeze

.PHONY: requirements

requirements.txt:
	uv pip freeze > requirements.txt

requirements: requirements.txt
	@echo "Generated requirements.txt"
