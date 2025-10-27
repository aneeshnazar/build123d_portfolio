# Requirements

All this repo uses is [uv](https://docs.astral.sh/uv/). Once installed, simply clone this repo and run:

```uv run experiments```

to launch the jupyterlab server, complete with all the dependencies needed to run the notebooks and view the parts.

# Housekeeping

Add subprojects with

```uv init --lib packages/<name of subproject>```

add the subproject as a workspace under the top-level pyproject.toml's `[tool.uv.sources]` section, with

```<project-name> = { workspace = true }```

and then run

```uv sync``` in order to add them to the virtual environment