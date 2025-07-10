# Project Roadmap: aus-health-knowledge-graph

This document outlines the high-level phases for the development of the Australian Healthcare Knowledge Graph. Each phase builds upon the previous one, incrementally adding data sources, features, and analytical capabilities.

## Phase 1: Core MBS Data Ingestion and Initial Graph Foundation

*   **Objective:** Establish the foundational infrastructure, parse MBS XML data, integrate SNOMED CT-AU as the core clinical terminology, and build the initial graph structure for MBS services.
*   **Key Deliverables:**
    1.  **Environment Setup:** Working Python environment with necessary libraries; Graph Database (Neo4j) instance running.
    2.  **SNOMED CT-AU Integration:**
        *   Scripts to download the latest SNOMED CT-AU RF2 release from NCTS.
        *   Scripts to parse and load SNOMED CT-AU concepts, descriptions, and relevant relationships (e.g., `IS_A`) into the graph database.
    3.  **MBS Data Processing:**
        *   Scripts to download and parse the latest MBS XML file.
        *   Extraction of key MBS item details (ID, description, fees, notes, effective dates, etc.).
        *   Transformation of MBS data into a graph model (nodes for items, fees, notes; relationships).
        *   Loading MBS data into the graph database, including temporal properties.
    4.  **Initial MBS-SNOMED CT Linking:**
        *   Basic NLP techniques applied to MBS descriptions/notes to identify and map conditions/procedures to SNOMED CT-AU concepts.
    5.  **Basic Querying & Validation:** Ability to perform simple Cypher queries on MBS data and its links to SNOMED CT-AU.

## Phase 2: PBS Data Integration and Cross-Scheme Linkage

*   **Objective:** Incorporate PBS data, integrate AMT and ATC terminologies, and establish meaningful links between MBS services and PBS medications, primarily through shared clinical conditions.
*   **Key Deliverables:**
    1.  **AMT & ATC Integration:**
        *   Scripts to download the latest AMT release from NCTS and ATC hierarchy files.
        *   Scripts to parse and load AMT and ATC concepts and relationships into the graph database.
        *   Leverage official AMT to SNOMED CT-AU mappings from NCTS if available.
    2.  **PBS Data Processing:**
        *   Scripts to download and parse the latest PBS XML data (including handling of ZIP archives).
        *   Extraction of key PBS item details (drug name, form, strength, manufacturer, ATC/AMT codes, restrictions, pricing, effective dates, etc.).
        *   Transformation of PBS data into a graph model.
        *   Loading PBS data into the graph database, including temporal properties.
    3.  **Linking PBS Drugs to Conditions & Ontologies:**
        *   NLP applied to PBS restriction text to identify drug indications (conditions).
        *   Mapping of these conditions to SNOMED CT-AU concepts.
        *   Linking `Drug` nodes to `ATCConcept` and `AMTConcept` nodes.
    4.  **Establishing MBS-PBS Links:**
        *   Ability to query and traverse relationships between MBS items and PBS items/drugs via shared `SNOMEDConcept` (condition) nodes.
    5.  **Enhanced Querying & Validation:** More complex queries spanning MBS, PBS, and linked ontologies.

## Phase 3: Advanced NLP, Temporal Analysis, and Policy Insights

*   **Objective:** Refine NLP capabilities, enhance the graph model for sophisticated temporal analysis, and begin addressing complex policy-relevant questions.
*   **Key Deliverables:**
    1.  **Advanced NLP Implementation:**
        *   Fine-tuning NER models for improved accuracy on domain-specific terminology.
        *   Exploration of relation extraction techniques to capture more nuanced information from text.
    2.  **Sophisticated Temporal Querying:**
        *   Development of Cypher queries and potentially graph algorithms to analyze trends, changes over time, and sequences of events based on `effectiveFrom`/`effectiveTo` dates.
    3.  **Ontology Mapping Refinement:**
        *   Implementation of more advanced mapping techniques (e.g., semantic similarity, embedding-based approaches) for challenging text-to-concept links.
        *   Establishment of a review/curation process for mappings.
    4.  **Policy Question Analysis:**
        *   Formulation and execution of queries designed to answer the types of policy-relevant questions identified during project scoping (e.g., service co-dependencies, impact of restrictions, variations in care).
    5.  **Performance Optimization & Scalability:**
        *   Review graph model and query performance.
        *   If necessary, adapt components for Spark processing for improved scalability (if not already done).
    6.  **Documentation and Maintenance Framework:**
        *   Comprehensive documentation of the graph schema, ETL pipelines, NLP models, and maintenance procedures for ongoing data updates.

## Future Considerations (Post Phase 3 / Ongoing)

*   Integration of other relevant ontologies (e.g., ORDO/HPO for rare diseases, LOINC for lab tests) based on evolving analytical needs.
*   Development of a user interface or API for easier access to the knowledge graph.
*   Integration with external datasets for richer contextual analysis.
*   Advanced graph analytics and machine learning applications (e.g., pathway prediction, anomaly detection).
*   Development of visualization tools to explore graph data.
```
