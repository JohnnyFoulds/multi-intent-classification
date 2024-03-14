SHELL=/bin/bash

# set the project path variable
PROJECT_PATH := "."
VENV_NAME := "multi-intent"

.PHONY: install-miniconda create-venv


# install miniconda
install-miniconda:
	@echo "Checking for Miniconda..."
	@command -v conda >/dev/null 2>&1 || { \
		echo "Miniconda not found, installing..."; \
		wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda3-latest-Linux-x86_64.sh; \
		bash Miniconda3-latest-Linux-x86_64.sh -b -p $$HOME/miniconda; \
		echo "export PATH=\"$$HOME/miniconda/bin:$$PATH\"" >> $$HOME/.bashrc; \
		rm -f Miniconda3-latest-Linux-x86_64.sh; \
		echo "Miniconda installed."; \
	}

# create the virtual environment
venv: install-miniconda
	@echo "Creating virtual environment..." && \
	export PATH="$$HOME/miniconda/bin:$$PATH" && \
	conda init; \
	conda env create -f environment.yml || conda env update -f environment.yml; \
	echo "Setup complete. Copy-paste the following command to finalize the setup:"; \
	echo "source ~/.bashrc && conda activate $(VENV_NAME)" \