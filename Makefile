# Project docs — portable build entry point.
# Runs everything through the universal toolkit image on Podman or Docker
# (auto-detected; override with ENGINE=docker), so it works the same on Linux and
# macOS with no host tooling beyond a container engine + make. Run `make` for help.

IMAGE := localhost/project-docs-toolkit:latest
PORT  ?= 8000
# Host interface the preview binds to — localhost only by default.
# Override to expose on the LAN, e.g.  make serve BIND=0.0.0.0
BIND  ?= 127.0.0.1

# Container engine: auto-detect Podman, else Docker. Override with: make ENGINE=docker
ENGINE ?= $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)

# Hardened, portable run: no extra capabilities, no privilege escalation.
# (The same flags work on both Podman and Docker.)
RUN := $(ENGINE) run --rm \
       -v "$(CURDIR)":/docs:rw -w /docs \
       --cap-drop=ALL --security-opt no-new-privileges \
       $(if $(filter docker,$(ENGINE)),--user $(shell id -u):$(shell id -g),)

# Allocate a TTY only when stdin is one, so serve/shell also work non-interactively.
TTY := $(shell [ -t 0 ] && echo -it)

.DEFAULT_GOAL := help
.PHONY: help image build check report drift ci serve shell versions clean

help: ## Show this help
	@echo "Project docs — make targets (engine: $(ENGINE)):"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-9s\033[0m %s\n", $$1, $$2}'

image: ## (Re)build the toolkit image
	$(ENGINE) build -t $(IMAGE) -f Containerfile .

build: image ## Build the static site into ./site (offline, strict)
	$(RUN) --network none $(IMAGE) mkdocs build --strict

check: image ## Lint frontmatter + cross-link graph (complements mkdocs --strict)
	$(RUN) --network none $(IMAGE) docs-check docs

report: image ## Coverage & staleness report (low-confidence / stale pages)
	$(RUN) --network none $(IMAGE) docs-report docs

drift: image ## Drift vs source repos: make drift SRC=/path/to/code
	$(RUN) $(if $(SRC),-v "$(SRC)":/src:ro,) --network none $(IMAGE) docs-drift docs /src

ci: build check ## The local gate: build + lint (what CI runs)

serve: image ## Live-reload preview (http://localhost:8000; LAN via BIND=0.0.0.0)
	# Host-published on $(BIND) only. The container-internal 0.0.0.0 bind is not
	# network-exposed except through this publish.
	$(RUN) $(TTY) -p $(BIND):$(PORT):8000 $(IMAGE) mkdocs serve -a 0.0.0.0:8000

shell: image ## Shell inside the toolkit (tsp / prism / oasdiff / d2 / schemathesis)
	$(RUN) $(TTY) $(IMAGE) bash

versions: image ## Print the resolved tool versions
	@$(RUN) --network none $(IMAGE) bash -lc '\
	  echo "mkdocs:      $$(mkdocs --version)"; \
	  echo "d2:          $$(d2 --version 2>/dev/null)"; \
	  echo "oasdiff:     $$(oasdiff --version 2>/dev/null)"; \
	  echo "typespec:    $$(tsp --version 2>/dev/null | head -1)"; \
	  echo "prism:       $$(prism --version 2>/dev/null)"; \
	  echo "asyncapi:    $$(asyncapi --version 2>/dev/null)"; \
	  echo "schemathesis:$$(schemathesis --version 2>/dev/null)"'

clean: ## Remove the built site
	rm -rf site
