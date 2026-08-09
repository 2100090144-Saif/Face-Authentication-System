# ============================================================
# Face Authentication System - Makefile
# ============================================================

IMAGE   = face_auth_system
TAG     = latest
CONTAINER = face_auth_app

.PHONY: build run stop verify shell logs clean rebuild help

## Build the Docker image (takes 5-10 min - dlib compiles from source)
build:
	docker build -t $(IMAGE):$(TAG) --progress=plain .

## Run the container
run:
	docker-compose up -d

## Run in foreground (see logs live)
run-fg:
	docker-compose up

## Stop the container
stop:
	docker-compose down

## Verify Python version and all dependencies inside container
verify:
	docker exec $(CONTAINER) python verify_setup.py

## Open a shell inside the running container
shell:
	docker exec -it $(CONTAINER) /bin/bash

## View live logs
logs:
	docker logs -f $(CONTAINER)

## View face auth audit log
audit:
	docker exec $(CONTAINER) tail -f logs/face_auth_audit.log

## Check Python version inside container
python-version:
	docker exec $(CONTAINER) python --version

## Test face_recognition import inside container
test-face-recognition:
	docker exec $(CONTAINER) python -c "\
import face_recognition, dlib; \
print(f'dlib version: {dlib.__version__}'); \
print(f'face_recognition: OK'); \
print(f'CUDA: {dlib.DLIB_USE_CUDA}')"

## Remove container and image
clean:
	docker-compose down --rmi all --volumes

## Rebuild from scratch (no cache)
rebuild:
	docker build --no-cache -t $(IMAGE):$(TAG) --progress=plain .

## Show help
help:
	@echo ""
	@echo "Face Authentication System - Docker Commands"
	@echo "============================================"
	@echo "  make build          - Build Docker image"
	@echo "  make run            - Start container (background)"
	@echo "  make run-fg         - Start container (foreground)"
	@echo "  make stop           - Stop container"
	@echo "  make verify         - Verify all dependencies"
	@echo "  make shell          - Open shell in container"
	@echo "  make logs           - View live logs"
	@echo "  make audit          - View face auth audit log"
	@echo "  make python-version - Check Python version"
	@echo "  make test-face-recognition - Test face_recognition"
	@echo "  make clean          - Remove container and image"
	@echo "  make rebuild        - Rebuild from scratch"
	@echo ""


