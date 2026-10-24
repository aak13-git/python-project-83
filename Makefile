PORT ?= 8000

setup:
	install build-css

install:
	uv sync
	npm install

build:
	./build.sh

build-css:
	npm run build:css

watch-css:
	npm run watch:css

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


run_db:
	docker-compose up -d

stop_db:
	docker-compose down