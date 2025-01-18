# run script in repo root
Push-Location "$PSScriptRoot/.."

uv run pytest --cov-report term-missing:skip-covered --cov=src "tests" -s -v

Pop-Location