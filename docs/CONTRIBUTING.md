### docs/CONTRIBUTING.md

```md project="Twikit Happens" file="docs/CONTRIBUTING.md" type="markdown"
# Contributing to Twikit Happens

Thank you for your interest in contributing to Twikit Happens! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/twikit-happens.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
5. Install development dependencies: `pip install -e ".[dev]"`

## Development Workflow

1. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Format your code: `black src/ tests/`
5. Commit your changes with a descriptive message
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Pull Request Guidelines

- Provide a clear description of the changes
- Include any relevant issue numbers in the PR description
- Ensure all tests pass
- Follow the code style guidelines
- Keep PRs focused on a single change

## Code Style

We follow PEP 8 and use Black for code formatting:

```bash
# Format code
black src/ tests/

# Check code style
flake8 src/ tests/
```

## Testing

Write tests for new features and bug fixes:

```shellscript
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/
```

## Documentation

Update documentation for any new features or changes:

- Update docstrings for new functions and classes
- Update the README.md if necessary
- Add examples for new functionality


## Releasing

Only project maintainers can release new versions:

1. Update version in `src/twikit_happens/__init__.py`
2. Update CHANGELOG.md
3. Create a new git tag: `git tag v0.1.0`
4. Push the tag: `git push origin v0.1.0`
5. Build and upload to PyPI:

```shellscript
python -m build
python -m twine upload dist/*
```


## Questions?

If you have any questions about contributing, please open an issue or contact the maintainers.

Thank you for your contributions!