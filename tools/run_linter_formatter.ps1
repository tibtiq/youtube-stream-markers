# run script in repo root
Push-Location "$PSScriptRoot/.."

# linter
uvx ruff check

# formatter
uvx ruff format --check .

# type consistency
uv run pyright .

Pop-Location