# Configuration
#--------------
PYTHON := python3
VENV := .venv

PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

MAIN := main.py
REQ := requirements.txt
INSTALL_STAMP := $(VENV)/.installed

# The user must provide the map like this:
# make run MAP=maps/easy/map.txt
MAP ?= 

MYPY_FLAGS := --warn-return-any \
			  --warn-unused-ignores \
			  --ignore-missing-imports \
			  --disallow-untyped-defs \
			  --check-untyped-defs


# Main Rules
#-----------
all: install lint

install: $(INSTALL_STAMP)

run: install check-map
	$(PY) $(MAIN) "$(MAP)"

debug: install check-map
	$(PY) -m pdb $(MAIN) "$(MAP)"

visual: install check-map
	$(PY) $(MAIN) "$(MAP)" --visual

#Environment and dependencies
#----------------------------
$(PY):
	$(PYTHON) -m venv $(VENV)

$(INSTALL_STAMP): $(PY) $(REQ)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQ)
	@touch $(INSTALL_STAMP)

#Validation
#----------
check-map:
	@if [ -z "$(MAP)" ]; then \
		echo "Error: a map is required."; \
		echo "Usage: make run MAP=maps/example.txt"; \
		exit 1; \
	fi
	@if [ ! -f "$(MAP)" ]; then \
		echo "Error: map file '$(MAP)' does not exist."; \
		exit 1; \
	fi

#Code quality
#------------
lint: install
	$(PY) -m flake8 . --exclude=$(VENV)
	$(PY) -m mypy . $(MYPY_FLAGS) --exclude $(VENV)

lint-strict: install
	$(PY) -m flake8 . --exclude=$(VENV)
	$(PY) -m mypy . --strict $(MYPY_FLAGS) --exclude $(VENV)

#Cleaning
#--------
clean:
	rm -rf $(VENV)
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

re: clean install

#Help
#----
help:
	@echo "make install      -> Create venv and install dependencies"
	@echo "make run          -> Run program"
	@echo "make visual       -> Run program with visual mode"
	@echo "make debug        -> Run program with debug mode"
	@echo "make lint         -> Run flake8 and mypy"
	@echo "make lint-strict  -> Run strict mypy"
	@echo "make clean        -> Remove venv and cache files"

.PHONY: all install run debug visual lint lint-strict clean re help