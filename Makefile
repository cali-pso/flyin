NAME = main.py

install:
	uv sync

run:
	@ uv run $(NAME)

debug:
	@ uv run python -m pdb $(NAME)

clean:
	uv cache clean
	rm -rf __pycache__ .mypy_cache .venv uv.lock


lint:
	- flake8 . --exclude '.venv'
	- mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
