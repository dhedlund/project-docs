# Project docs — portable build entry point.
# Runs everything through the universal toolkit image on Podman or Docker
# (auto-detected; override with ENGINE=docker), so it works the same on Linux and
# macOS with no host tooling beyond a container engine + make.
#
#   make build     # build the static site into ./site (offline, strict)
#   make serve     # live-reload preview at http://localhost:8000
#   make shell     # shell inside the toolkit (tsp / prism / oasdiff / d2 / schemathesis)
#   make versions  # print the resolved tool versions
#   make image     # (re)build the toolkit image
#   make clean     # remove ./site

IMAGE := localhost/project-docs-toolkit:latest
PORT  ?= 8000

# Container engine: auto-detect Podman, else Docker. Override with: make ENGINE=docker
ENGINE ?= $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)

# Hardened, portable run: no extra capabilities, no privilege escalation.
# (The same flags work on both Podman and Docker.)
RUN := $(ENGINE) run --rm \
       -v "$(CURDIR)":/docs:rw -w /docs \
       --cap-drop=ALL --security-opt no-new-privileges

.PHONY: image build serve shell versions check report clean

image:
	$(ENGINE) build -t $(IMAGE) -f Containerfile .

# Building docs needs zero network — enforce that (and prove no exfiltration).
build: image
	$(RUN) --network none $(IMAGE) mkdocs build --strict

# Lint frontmatter + cross-link graph (complements `mkdocs --strict`). Offline.
check: image
	$(RUN) --network none $(IMAGE) docs-check docs

# Coverage & staleness report — which pages are low-confidence or stale.
report: image
	$(RUN) --network none $(IMAGE) docs-report docs

serve: image
	$(RUN) -it -p $(PORT):8000 $(IMAGE) mkdocs serve -a 0.0.0.0:8000

shell: image
	$(RUN) -it $(IMAGE) bash

versions: image
	$(RUN) --network none $(IMAGE) bash -lc '\
	  echo "mkdocs:      $$(mkdocs --version)"; \
	  echo "d2:          $$(d2 --version 2>/dev/null)"; \
	  echo "oasdiff:     $$(oasdiff --version 2>/dev/null)"; \
	  echo "typespec:    $$(tsp --version 2>/dev/null | head -1)"; \
	  echo "prism:       $$(prism --version 2>/dev/null)"; \
	  echo "asyncapi:    $$(asyncapi --version 2>/dev/null)"; \
	  echo "schemathesis:$$(schemathesis --version 2>/dev/null)"'

clean:
	rm -rf site
