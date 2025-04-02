# Contributors Guide

## Welcome

Thank you for considering contributing to this project! Your help is appreciated, whether you're fixing bugs, adding features, or improving documentation.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Pull Requests](#pull-requests)
3. [Development Setup](#development-setup)
4. [Style Guides](#style-guides)
    - [Git Commit Messages](#git-commit-messages)
    - [Code Style](#code-style)
5. [Additional Resources](#additional-resources)
6. [Contact](#contact)
7. [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to [Contact](#contact).

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by following these steps:

1. **Search for existing issues** to ensure it hasn’t already been reported.
2. If no existing issue matches, [open a new issue](https://gitup.uni-potsdam.de/henschel1/rse-group-project/-/issues) and include:
    - A clear, descriptive title.
    - Steps to reproduce the bug.
    - Expected and actual results.
    - Screenshots, if applicable.
    - Any other relevant information.

### Suggesting Enhancements

Enhancements can be new features or improvements to existing features. To suggest an enhancement:

1. **Search for existing issues** to see if the suggestion has already been made.
2. If no existing issue matches, [open a new issue](https://gitup.uni-potsdam.de/henschel1/rse-group-project/-/issues) and include:
    - A clear, descriptive title.
    - A detailed description of the proposed enhancement.
    - Any relevant examples, screenshots, or links.

### Pull Requests

We welcome pull requests! Please follow these steps:

1. Fork the repository and create your branch from `main`.
2. If you’ve added code, ensure that it is covered by tests.
3. Ensure the test suite passes.
4. Follow the [style guides](#style-guides).
5. Create a descriptive pull request.

## Development Setup

To get a local copy of the project up and running, follow these instructions:

1. Clone the repository:
    ```sh
    git clone https://gitup.uni-potsdam.de/henschel1/rse-group-project.git
    ```
2. Navigate to the project directory:
    ```sh
    cd rse-group-project
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Download one required language model:
   ```sh
   python -m spacy download de_core_news_lg
   ```
5. Run the snakemake workflow:
    ```sh
    snakemake --cores 1
    ```

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move button" not "Moves button").
- Limit the first line to 79 characters or fewer.
- Reference issues and pull requests liberally after the first line.

### Code Style

- Follow the coding conventions of the python PEP 8 style guide.
- Ensure your code passes the linting rules. 
  - max line length: 79 characters
- Write clear and concise comments.
  - especially doc strings of each function


## Contact

### You can reach our team via e-mail:<br>
- [konrad.brüggemann@uni-potsdam.de](mailto:konrad.brüggemann@uni-potsdam.de)<br>
- [leon.hauch@uni-potsdam.de](mailto:leon.hauch@uni-potsdam.de)<br>
- [marvin.henschel@uni-potsdam.de](mailto:marvin.henschel@uni-potsdam.de)<br>
- [alina.imtiaz@uni-potsdam.de](mailto:alina.imtiaz@uni-potsdam.de)<br>
- [tilman.ripke@uni-potsdam.de](mailto:tilman.ripke@uni-potsdam.de)


## License

By contributing, you agree that your contributions will be licensed under the [![License](https://img.shields.io/badge/License-MIT-red)](LICENSE) file of the repository.
