# Example (Beacon) docs — builds with the SAME shared toolkit image as the root
# project, proving the toolchain end-to-end on the fiction. Uses port 8001 so it
# can run alongside the root site.
#
#   make build     # build the Beacon site into ./site
#   make serve     # preview at http://localhost:8001
#
# `make image` builds the shared image from the repo root (../Containerfile).

IMAGE := localhost/project-docs-toolkit:latest
PORT  ?= 8001

# Container engine: auto-detect Podman, else Docker. Override with: make ENGINE=docker
ENGINE ?= $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)

RUN := $(ENGINE) run --rm \
       -v "$(CURDIR)":/docs:rw -w /docs \
       --cap-drop=ALL --security-opt no-new-privileges

.PHONY: image build serve shell check report clean

image:
	$(ENGINE) build -t $(IMAGE) -f ../Containerfile ..

build: image
	$(RUN) --network none $(IMAGE) mkdocs build --strict

check: image
	$(RUN) --network none $(IMAGE) docs-check docs

report: image
	$(RUN) --network none $(IMAGE) docs-report docs

serve: image
	$(RUN) -it -p $(PORT):8000 $(IMAGE) mkdocs serve -a 0.0.0.0:8000

shell: image
	$(RUN) -it $(IMAGE) bash

clean:
	rm -rf site
