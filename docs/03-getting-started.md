# Getting Started

A simple example of generating your first document.


 -e .`

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
version: 1.0
template: simple

document:
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
