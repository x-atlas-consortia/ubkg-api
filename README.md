# Unified Biomedical Knowledge Graph

## UBKG-API

The components of the UBKG include:
- The **source framework** that extracts ontology information from the UMLS to create a set of CSV files (**UMLS CSVs**)
- The **generation framework** that appends to the UMLS CSVs assertion data from other ontologies to create a set of **ontology CSVs**.
- A neo4j **ontology knowledge graph** populated from the ontology CSVS.
- An **API server** that provides RESTful endpoints to query the ontology knowledge graph.

This repository contains the source for the API.

# SmartAPI documentation

The specification for the UBKG API can be found [here](https://smart-api.info/ui/96e5b5c0b0efeef5b93ea98ac2794837/).

# Developer Information

## Build and publish to PyPI

```
python -m build
python3 -m twine upload dist/*
```

## Requirements
Python 3.9 or newer
