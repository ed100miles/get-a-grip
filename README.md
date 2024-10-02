# ✊ Get-a-grip 🧗

The climbing grip strength tracker.

### Setup

1. install [uv](https://docs.astral.sh/uv/)

2. create an environment with `uv venv`

3. activate it with `source .venv/bin/activate`

4. install the packages with `uv pip install -r pyproject.toml`

5. create a local sqlite db and tables with `uv run python -m app.models`

6. seed it with `uv run python -m app.seed_db`

7. spin up the dev server with `uv run fastapi dev` (or `fastapi run` for prod)

8. you can see the strawberry GraphiQL ui at [http://localhost:8000/graphql](http://localhost:8000/graphql)

9. to start dev frontend, cd into frontend and run `npm run dev`. (alternatively `npm run start` for production build and serve.)

10. you can generate the graphql schema with `uv run strawberry export-schema app.routers.graphql:schema > schema.graphql`

11. you can generate the graphql types by running `npm run codegen` from `/frontend`, or if you're working on updating the frontend queries and mutations, you can use `npm run codegen-watch` for live refreshes.

12. go build the rest of the app...
