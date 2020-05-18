# Install Python3
choco install python3

# Install Poetry
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python

# Install VSCode
choco install vscode

# Install VSCode extensions
## For python development

### Python extension
code --install-extension ms-python.python

### Toml syntax extension
code --install-extension bungcip.better-toml

## General

### Spelling
code --install-extension ban.spellright

### Api testing
code --install-extension humao.rest-client

### Code coverage
code --install-extension ryanluker.vscode-coverage-gutters