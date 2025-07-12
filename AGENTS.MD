# Agent Instructions for `aus-health-knowledge-graph`

This document provides guidance for AI agents contributing to the `aus-health-knowledge-graph` project.

## 1. Project Goal & Context

*   **Primary Goal:** To build a knowledge graph from Australian MBS and PBS XML data, integrated with SNOMED CT-AU, AMT, and ATC ontologies. The graph should support complex queries for healthcare policy and research.
*   **Key Data Sources:** MBS XML, PBS XML, SNOMED CT-AU RF2, AMT, ATC hierarchy. Refer to `README.md` for specific source links.
*   **Core Technologies:** Python, `lxml` for XML, `pandas` for data manipulation, Neo4j graph database (Cypher), `spaCy`/`scispaCy` for NLP.

## 2. Coding Conventions & Standards

*   **Language:** All scripts should be written in Python 3.x.
*   **Style:** Follow PEP 8 Python style guide. Use a linter (e.g., Flake8, Pylint) and formatter (e.g., Black, autopep8) if possible.
*   **XML Parsing:** Use the `lxml` library for its robustness and performance with large XML files. Employ iterative parsing (`iterparse`) for memory efficiency when processing MBS and PBS XML.
*   **Data Manipulation:** Use `pandas` DataFrames for intermediate data structuring, cleaning, and transformation before loading into the graph.
*   **Graph Database Interaction:**
    *   Use the official `neo4j` Python driver for interacting with Neo4j.
    *   Employ parameterized Cypher queries to prevent injection vulnerabilities and improve query readability.
    *   Use transactions for write operations to ensure data integrity.
*   **Modularity:** Write small, focused functions and classes. Aim for reusable components.
*   **Configuration:** Externalize configurations (file paths, database credentials, API keys if any) into configuration files (e.g., `.env`, `config.ini`, `config.yaml`) rather than hardcoding in scripts.
*   **Logging:** Implement comprehensive logging using Python's `logging` module in all scripts. Log key actions, errors, and processing statistics.
*   **Error Handling:** Implement robust error handling (e.g., `try-except` blocks) to manage issues like missing files, network errors, parsing errors, or database connection problems.
*   **Dependencies:** List all Python dependencies in `requirements.txt`.

## 3. Handling Data and Ontologies

*   **Data Ingestion:**
    *   Scripts for downloading data should be robust to network issues and provide clear feedback.
    *   Store raw downloaded files in `data/raw/`.
    *   Processed or intermediate files (e.g., CSVs for Neo4j bulk import) should go into `data/processed/`.
*   **Temporality & Versioning:**
    *   MBS, PBS, and ontologies (SNOMED CT-AU, AMT) are versioned and updated regularly.
    *   Graph nodes and relationships representing this data **must** include `effectiveFrom` and `effectiveTo` date properties (or similar, like `startDate`, `endDate`, `cessationDate`) to capture their validity period.
    *   When new data/ontology versions are processed:
        *   Existing entities that are changed should have their `effectiveTo` date set.
        *   New versions of these entities should be created with a new `effectiveFrom` date.
        *   Entities that are removed in a new version should have their `effectiveTo` date set accordingly (do not physically delete from the graph to maintain history).
*   **Ontology Processing:**
    *   **SNOMED CT-AU:** Parse RF2 files (Concepts, Descriptions, Relationships). Focus on relevant hierarchies (procedures, conditions, substances, etc.).
    *   **AMT:** Parse according to NCTS specifications. Prioritize linking AMT concepts to SNOMED CT-AU using official mappings if available from NCTS.
    *   **ATC:** Parse ATC hierarchy files. Create parent-child relationships.
*   **NLP Integration:**
    *   Use `spaCy` with `scispaCy` models as a baseline for NER on textual data (MBS notes, PBS restrictions).
    *   Focus on extracting entities like conditions, procedures, drugs, anatomical sites, and key criteria.
    *   Map extracted entities to SNOMED CT-AU concepts. Store mapping confidence or method if possible.
    *   Consider fine-tuning models if out-of-the-box performance is insufficient for specific terms.

## 4. Apache Spark Considerations

*   **Flexibility by Design:** The project aims for flexibility. Initial development and smaller-scale processing should primarily use standard Python scripts (`lxml`, `pandas`).
*   **When to Consider Spark:** If processing times for XML parsing, NLP tasks, or large-scale data transformations become prohibitive on a single node, these components can be migrated or adapted to use Apache Spark.
*   **Spark Implementation:**
    *   Use PySpark.
    *   For XML, use `com.databricks:spark-xml`.
    *   For NLP, consider `Spark NLP` (especially `Spark NLP for Healthcare` if licensed and available, for its advanced clinical entity recognition and linking).
*   **Agent Responsibility:** If a task is being adapted for Spark, clearly document the rationale and the changes made. Ensure Spark jobs are configurable and can be run in different environments. By default, assume a non-Spark Python environment unless explicitly stated for a task.

## 5. Testing

*   Write unit tests for critical functions (e.g., complex parsing logic, transformation functions). Use `pytest` or Python's `unittest` module.
*   Aim for integration tests for data loading processes (e.g., load a small sample file and verify graph content).

## 6. Documentation & Commits

*   **Code Comments:** Add comments to explain complex logic or non-obvious decisions.
*   **Docstrings:** Write docstrings for all modules, classes, and functions.
*   **Commit Messages:** Write clear, concise commit messages following conventional formats (e.g., imperative mood: "Add parser for MBS fees", "Fix bug in SNOMED relationship loading"). Reference issue numbers if applicable.
*   **Update Documentation:** If changes to scripts or processes impact overall project documentation (`README.md`, `ROADMAP.md`, etc.), update these as well.
*   **`session_log.md`:** The user will primarily maintain this file by pasting summaries of key AI interactions. If the AI is asked to summarize a specific technical discussion for this log, it should do so clearly and concisely.

## 7. Communication

*   Clearly state assumptions made.
*   If a task is ambiguous, ask for clarification before proceeding.
*   Report errors or issues encountered during development promptly.
*   When providing code, ensure it's complete enough to be testable or clearly state any missing parts or dependencies.

By following these guidelines, AI agents can contribute effectively and consistently to the development of the `aus-health-knowledge-graph`.
