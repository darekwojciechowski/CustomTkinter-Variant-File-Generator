# Poetry Instructions for Project Setup

Poetry is a dependency management and packaging tool for Python. It helps manage your project's dependencies, virtual environments, and packaging. Follow these steps to get started with Poetry:

## Step 1: Install Poetry

**MacOS** Install Poetry: Use Homebrew to install Poetry by running the following command:

```bash
brew install poetry
```

Alternatively, if you're on **Windows**, you can use:

```bash
pip install poetry
```

## Step 2: Initialize a Poetry Project


Navigate to your project directory, which should be the `base location` for your project:

```bash
cd CustomTkinter-Variant-File-Generator
```

Initialize a new Poetry project:

```bash
poetry init
```

Follow the prompts to set up your project. You can specify the package name, version, description, author, license, and dependencies.

## Step 3: Add Dependencies

You can add dependencies to your project using Poetry. For example, to add `customtkinter` you can run:

```bash
poetry add customtkinter
```

## Step 4: Activate the Virtual Environment

Poetry automatically creates a virtual environment for your project. To activate it, use:

```bash
poetry shell
```

## Step 5: Run Your Project

With the virtual environment activated, you can run your Python scripts as usual. For example:

```bash
python main.py
```

## Additional Poetry Commands

Here are some other useful Poetry commands:

- **Install all dependencies**: `poetry install`
- **Update dependencies**: `poetry update`
- **Add development dependencies**: `poetry add --dev pytest`
- **List all dependencies**: `poetry show`
- **Build your package**: `poetry build`
- **Remove a dependency**: `poetry remove customtkinter`
