# Example (Beacon) docs — builds with the SAME shared toolkit image as the root
# project, proving the toolchain end-to-end on the fiction. Uses port 8001 so it
# can run alongside the root site. Run `make` for help.
#
# `make image` builds the shared image from the repo root (../Containerfile).

# Optional local overrides for working inside example/ (gitignored; see
# .env.example). Its own .env — not the root's — so its PORT stays 8001 and can
# run alongside the root site. Included first so it beats the ?= defaults.
-include .env

IMAGE := localhost/project-docs-toolkit:latest
PORT  ?= 8001
# Host interface the preview binds to — localhost only by default.
# Override to expose on the LAN, e.g.  make serve BIND=0.0.0.0
BIND  ?= 127.0.0.1

# Container engine: auto-detect Podman, else Docker. Override with: make ENGINE=docker
ENGINE ?= $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)

RUN := $(ENGINE) run --rm \
       -v "$(CURDIR)":/docs:rw -w /docs \
       --cap-drop=ALL --security-opt no-new-privileges \
       $(if $(filter docker,$(ENGINE)),--user $(shell id -u):$(shell id -g),)

TTY := $(shell [ -t 0 ] && echo -it)

.DEFAULT_GOAL := help
.PHONY: help image build check report drift ci serve shell clean

help: ## Show this help
	@echo "Beacon example docs — make targets (engine: $(ENGINE)):"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-9s\033[0m %s\n", $$1, $$2}'

image: ## Build the shared toolkit image from the repo root
	$(ENGINE) build -t $(IMAGE) -f ../Containerfile ..

build: image ## Build the Beacon site into ./site (offline, strict)
	$(RUN) --network none $(IMAGE) mkdocs build --strict

check: image ## Lint frontmatter + cross-link graph
	$(RUN) --network none $(IMAGE) docs-check docs

report: image ## Coverage & staleness report
	$(RUN) --network none $(IMAGE) docs-report docs

drift: image ## Drift vs source repos: make drift SRC=/path/to/code
	$(RUN) $(if $(SRC),-v "$(SRC)":/src:ro,) --network none $(IMAGE) docs-drift docs /src

ci: build check ## The local gate: build + lint

serve: image ## Live-reload preview (http://localhost:8001; LAN via BIND=0.0.0.0)
	$(RUN) $(TTY) -p $(BIND):$(PORT):8000 $(IMAGE) mkdocs serve -a 0.0.0.0:8000

shell: image ## Shell inside the toolkit
	$(RUN) $(TTY) $(IMAGE) bash

clean: ## Remove the built site
	rm -rf site
