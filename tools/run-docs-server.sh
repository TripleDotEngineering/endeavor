#!/bin/bash
sphinx-build -b html docs build
python -m http.server --directory build -b 127.0.0.1 8000
