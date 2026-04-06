# AI Test Case Generator

This project is a modular GitHub Action that automatically generates unit tests for your code if your code coverage drops below a specified threshold (e.g., 75%). 

It supports **any programming language** by letting powerful Language Models (Groq, Claude, Gemini, etc.) inspect the low-coverage source code and automatically decide where to put the tests based on conventional file locations (e.g. `tests/test_x.py` for Python, `src/test/java/...` for Java).

## Features
- **Language Agnostic**: Uses LLMs to generate tests exactly formatted to your target language.
- **Pluggable LLMs**: Uses a modular provider design (`src/llm/provider.py`). Out-of-the-box it supports Groq, Anthropic Claude, and Google Gemini.
- **Automated PR Management**:
  - Automatically identifies the current feature branch.
  - Commits generated tests directly backed to that same feature branch.
  - Disables (closes) the **previous** triggering Pull Request.
  - Automatically opens a **new** Pull Request from that exact same branch to `dev`, so reviewers only see fully tested PRs.
- **Coverage Parser**: Works with standard `coverage.xml` (Cobertura style). Can easily be extended in `src/coverage/parser.py`.

## Usage Example

Add the following file to your repository at `.github/workflows/ai-test-generation.yml`:

```yaml
name: AI Test Generation Workflow

on:
  pull_request:
    branches:
      - dev

permissions:
  contents: write
  pull-requests: write

jobs:
  test-and-generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Example: Run your tests to generate coverage.xml
      - name: Setup Python & Run Pytest (Example)
        run: |
          pip install pytest coverage
          coverage run -m pytest
          coverage xml -o coverage.xml

      - name: AI Test Generator
        uses: Sahilnaik1234/TestCasesGeneration@main
        with:
          coverage_file: 'coverage.xml'
          threshold: '75.0'
          provider: 'groq' # or 'gemini', 'claude'
          github_token: ${{ secrets.GITHUB_TOKEN }}
          pr_number: ${{ github.event.pull_request.number }}
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Adding a New LLM Provider
To add a new LLM (e.g., OpenAI):
1. Open `src/llm/provider.py`
2. Extend `LLMProvider` class.
3. Add the logic to `get_llm_provider`.
4. Run!

## Requirements
- You need to generate a `coverage.xml` file *before* this action runs.
- Appropriate API key stored in your GitHub Repository Secrets (e.g. `GROQ_API_KEY`).