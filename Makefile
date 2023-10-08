# Python-related Makefile targets

# Define Python interpreter (adjust as needed)
PYTHON = python

# Virtual environment settings
VENV_DIR = .venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate

# Default target: Display help message
help:
	@echo "Available targets:"
	@echo "  install-venv       Create a virtual environment"
	@echo "  install-deps        Install project dependencies"
	@echo "  lint                Run linters (e.g., flake8)"
	@echo "  test                Run tests (e.g., pytest)"
	@echo "  run-script          Run your Python script"
	@echo "  clean               Remove virtual environment and build artifacts"

# Create a virtual environment
install-venv:
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)"

# Install project dependencies
install-deps: install-venv
	@source $(VENV_ACTIVATE) && pip install -r requirements.txt
	@echo "Dependencies installed"

# Run linters (e.g., flake8)
lint: install-deps
	@source $(VENV_ACTIVATE) && flake8 your_module_or_directory
	@echo "Linting complete"

# Run tests (e.g., pytest)
test: install-deps
	@source $(VENV_ACTIVATE) && pytest tests/
	@echo "Tests complete"

# Run your Python script (replace 'your_script.py' with your script name)
run-script: install-deps
	@source $(VENV_ACTIVATE) && python your_script.py
	@echo "Script executed"

# Remove virtual environment and build artifacts
clean:
	@rm -rf $(VENV_DIR) __pycache__ .pytest_cache
	@echo "Cleaned up"

# Define targets that are not associated with files
.PHONY: help install-venv install-deps lint test run-script clean

install-dev-deps:
	sudo apt install tox twine


build-package:
	python3 setup.py sdist bdist_wheel

upload-pip: build-package
	twine upload dist/*

