# Project Endeavor

> **NOTE:** This project was developed as an internal tool for generating
> professional reports and documentation. It was always a project we hoped to
> open source some day but never really found the time to get the code base into
> a state where we felt that was sustainable. That said, there's been some
> interest from others and we feel it is better to make it available and allow
> others to contribute to the project or fork it for their own use.
>
> We're open to issues, pull requests, or other contributions, but our long-term
> plan is to move away from this project and allow it to be community driven if
> there is interest.


<img src="./src/endeavor/static/img/endeavor-logo_128px.png"
alt="Endeavor project logo"
style="margin: 5px;"
align="middle">
**Hassle-free professional documents for engineers.**


**Endeavor** began as an effort to build a better suite of architecture, design, and documentation tools.

Built by software engineers for software engineers, Endeavor makes
it easy to generate beautiful, professional documentation without a hassle.

# Quickstart

## Prerequisites


- Python/Pip
- Pandoc
- PDFLatex
- mermaid-filter (we aim to make this optional eventually)

##  Installation

1. Clone this repository.
2. Run `pip install -e .`

## Getting Started

### Write your document in Markdown

First write your document as one or more Markdown files. Create `foo.md` and `bar.md` as shown below.

`foo.md`
```md
# Foo
This is part one
```

`bar.md`
```md
# Bar
This is part two
```

### Create a `document.yaml` file

Next, we need to create our `document.yaml` file. This tells Endeavor how to generate the document.

```yaml
DocGen:
    version: 1.0
    template: simple
Document:
    meta:
        title: My Sample Document
        authors:
            - name: Josh Kaplan
              title: Chief Engineer
    config: null
    vars:
        logo: ../../endeavor/static/img/endeavor-logo.png
    body:
        sections:
            - ./examples/foo.md
            - ./examples/bar.md
```

### Build the document

Run

```bash
python -m endeavor.docgen /path/to/document.yaml
```

You run the quickstart example with the following command:

```bash
python -m endeavor.docgen ./examples/quickstart/document.yaml
```

# Design

## Goals & Objectives

Endeavor is design for developers and engineers. It must support the following concepts:

* Architecture diagramming
* Document creation
* Architecture data access
* Version control

It should do the following:

* Leverage diagrams.net (draw.io) for diagramming

## Status

- We're beginning with document generation with embedded diagrams.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

Endeavor's [LaTeX templates](/src/endeavor/templates) are derived from freely
available templates on Overleaf. Templates are copyright their respective
authors and may fall under their own licenses. Some minor modifcations have
been made to support Endeavor's templating system. All notices in the original
templates have been retained.
