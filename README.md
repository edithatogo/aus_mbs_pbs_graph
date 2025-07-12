# Australian Healthcare Knowledge Graph (aus-health-knowledge-graph)

## Project Overview

This project aims to build a comprehensive knowledge graph from publicly available Australian Medicare Benefits Schedule (MBS) and Pharmaceutical Benefits Scheme (PBS) XML data. The goal is to represent healthcare services, drug items, associated fees, restrictions, and their relationships in a graph database. This will enable complex queries, deeper analysis, and the generation of insights relevant to healthcare policy, utilization, and interactions between services and medications.

The project will integrate key medical ontologies such as SNOMED CT-AU (Australian extension), Australian Medicines Terminology (AMT), and ATC (Anatomical Therapeutic Chemical Classification) to standardize and enrich the data. Natural Language Processing (NLP) and Named Entity Recognition (NER) techniques will be employed to extract relevant terms and classify information from textual fields within the XML (e.g., explanatory notes, restrictions).

## Core Objectives

1.  **Data Ingestion & Parsing:** Develop robust pipelines to parse MBS and PBS XML files, handling their complex hierarchical structures and regular updates.
2.  **Ontology Integration:** Integrate SNOMED CT-AU, AMT, and ATC to provide semantic structure and enable standardized querying.
3.  **NLP for Textual Data:** Extract and link medical conditions, procedures, drug indications, and other relevant entities from free-text fields (notes, restrictions).
4.  **Graph Construction:** Model and populate a graph database (e.g., Neo4j) with entities and relationships derived from the data sources and ontologies.
5.  **Temporal Analysis:** Incorporate the temporal nature of MBS/PBS data (effective dates, cessation dates) to allow for analysis over time.
6.  **Querying & Analysis:** Enable complex queries to uncover relationships between MBS services and PBS medications, analyze service pathways, and explore policy-relevant questions.

## Technology Stack (Initial Considerations)

*   **Programming Language:** Python
*   **XML Parsing:** `lxml`
*   **Data Manipulation:** `pandas`
*   **Graph Database:** Neo4j (using Cypher query language)
*   **Ontology Management:** Direct parsing of RF2 (SNOMED CT-AU) and other relevant formats.
*   **NLP:** `spaCy` (with `scispaCy` for biomedical models), potentially `Hugging Face Transformers` for advanced NER.
*   **Workflow & Orchestration (Optional, for larger scale):** Apache Airflow, or custom scripting.
*   **Distributed Processing (Design for Flexibility):** The project design will aim for flexibility. Initial development will focus on Python scripts suitable for single-node execution. If data volumes or NLP complexity necessitate, components can be adapted to leverage Apache Spark (PySpark, `spark-xml`, Spark NLP).

## Data Sources

*   **MBS XML:** From [mbsonline.gov.au](https://www.mbsonline.gov.au/) (Specific link: `https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/650f3eec0dfb990fca25692100069854/0b61e1e80b332754ca258c9e0000c7d8/$FILE/MBS-XML-20250701%20Version%203.XML`)
*   **PBS XML:** From [pbs.gov.au](https://m.pbs.gov.au/downloads/) (Specific link: `https://m.pbs.gov.au/downloads/2025/07/2025-07-01-xml-V3.zip`)
*   **SNOMED CT-AU & AMT:** From the National Clinical Terminology Service (NCTS) / Australian Digital Health Agency (ADHA) at [healthterminologies.gov.au](https://www.healthterminologies.gov.au/)
*   **ATC Classification:** From WHO Collaborating Centre for Drug Statistics Methodology or other reputable sources.

## Project Structure (Initial Idea)

```
/aus-health-knowledge-graph  # Chosen repository name
|-- data/                     # Raw data, processed data (not versioned if large)
|   |-- raw/                  # Downloaded XML, ontology files (e.g., from NCTS)
|   |-- processed/            # Intermediate data files (e.g., CSVs for bulk import)
|-- notebooks/                # Jupyter notebooks for exploration, analysis, prototyping
|-- scripts/                  # Python scripts for core ETL and NLP tasks
|   |-- parsing/              # Scripts for parsing MBS, PBS, ontologies
|   |-- loading/              # Scripts for loading data into the graph database
|   |-- nlp/                  # Scripts for NLP tasks (NER, entity linking)
|   |-- ontology_processing/  # Scripts for preparing/transforming ontology data
|   |-- utils/                # Utility functions
|-- src/                      # Source code for any custom Python modules/libraries developed
|-- tests/                    # Unit tests, integration tests for scripts/modules
|-- AGENTS.MD                 # Instructions for AI agents
|-- CHANGELOG.MD              # Log of significant changes to the project
|-- README.MD                 # This file
|-- ROADMAP.MD                # High-level project phases and future goals
|-- TODO.MD                   # Current and pending tasks
|-- session_log.md            # Log of key discussions, decisions, and AI interactions
|-- requirements.txt          # Python dependencies
|-- .gitignore                # Specifies intentionally untracked files that Git should ignore
```

## Getting Started

(To be filled in once initial scripts for environment setup and data acquisition are developed.)

## Contributing

(Details on how to contribute if this becomes a collaborative project.)

## License

(To be decided. Important to consider the licenses of the data sources, especially SNOMED CT-AU and other terminologies. Defaulting to a permissive license like MIT or Apache 2.0 for the code itself is common, but data redistribution needs care.)
