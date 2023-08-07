# `document.yaml` Specification


## `endeavor`

This is the header section of the document definition. It defines metadata about the document
definition file. For the most part, this section is currently unused.

## `env`

This section defines environment variables. Some templates expect certain environment variables
to tell the template how to render the document. Some environment variables are required, and
some are optional. The template will fail to render if a required environment variable is not
defined.

Environment variables can also be used to define user-defined variables and data such as
frequently used text sections or references.

## `document`

This defines the document itself.

### `document.title`

The document title.

### `document.subtitle`

The document subtitle.

### `document.authors`

```yaml
document:
  authors:
    - name: Joshua D. Kaplan
      email: me@example.com
```

### `document.copyright`

### `document.body`

```yaml
document:
  body:
    - ./index.md
```

### `document.appendices`

```yaml
document:
  appendices:
    - ./index.md
```
