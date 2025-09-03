# reproducible-scientific-notebook-configurations

A lightweight framework for enforcing reproducibility and organization in data-driven academic research by leveraging structured YAML configuration files.

In computational research, especially when using notebooks (e.g., Jupyter), it is essential to ensure that all relevant data and metadata are systematically saved for reproducibility and future analysis. However, a structured approach to managing these configurations is often lacking. Here, we introduce a simple YAML-based experimental parameter management system that can easily trace experimental records, figures and data files.

**Please note** that this is NOT about package management. Reproducible computing environment is a separate topic and should be handled with tools like `conda`, `Pkg` or `uv`.

## Features

- **Hot-swappability**: Tired of creating new notebooks for every experiment? Easily swap configurations to run different parameter sets without code changes
- **Automatic Traceability**: Generate unique experiment IDs and consistent file naming conventions
- **Parameter Validation**: Ensure all required parameters are present before experiment execution
- **Human-Readable Configs**: YAML format is easy to read, write, and maintain compared to code-based configuration
- **Version Control Friendly**: Clean diffs for configuration changes in git

## Why YAML?

YAML strikes the perfect balance between human readability and machine parsing:
- More readable than JSON for complex nested configurations
- Less verbose than XML
- Supports comments (unlike JSON)
- Widely supported across programming languages

example YAML configuration:
```yaml
# config.yml
notebook:
  id: "my-notebook" # Unique ID for this experiment
  name: "Model simulation"
  desc: "Simulate and capture the results of ODE models in SBML format"

exp:
  model: "lotka-volterra.xml"
  simulation:
    start: 0
    stop: 1000
    step: 100      
```

## Getting Started

1. **Install Dependencies**: Ensure you have a YAML parser for your programming language (e.g., PyYAML for Python, YAML.jl for Julia)
2. **Create a Configuration File**: Define your experiment parameters in a `.yaml` file
3. **Load and Validate Config**: Use the provided utilities to load and validate your configuration, alternatively, you can implement your own configuration management 