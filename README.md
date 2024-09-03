# ✊ Get-a-grip 🧗

The climbing grip strength tracker.

### Setup

1. install [uv](https://docs.astral.sh/uv/)
2. create an environment with `uv venv`
3. activate it with `source venv/bin/activate`
4. install the packages with `uv pip install -r pyproject.toml`
5. create a local sqlite db and tables with `uv run app/models.py`
6. spin up the dev server with `fastapi dev app/main.py` (or `fastapi run` for prod)
7. go build the rest of the app...
