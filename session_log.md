# Session Log: aus-health-knowledge-graph Project Inception

This document logs key discussions, decisions, and resources shared during the initial planning of the `aus-health-knowledge-graph` project.

## Initial Project Goal & Scope (Summary)

*   **Objective:** Build a knowledge graph from Australian Medicare Benefits Schedule (MBS) and Pharmaceutical Benefits Scheme (PBS) XML files.
*   **Enrichment:** Integrate medical ontologies (SNOMED CT, ATC, AMT) and use NLP/NER for textual data (notes, restrictions).
*   **Purpose:** Enable complex queries and deeper analysis for healthcare policy and research.
*   **Key Tasks Discussed:** XML parsing, graph database selection (Neo4j favored), schema design, ontology integration strategies, NLP/NER pipeline, handling data with/without Apache Spark.

## Key Decisions & Discussions:

1.  **Repository Name:** Discussed several options. `aus-health-knowledge-graph` or `mbs-pbs-kg` recommended. (User to finalize)
2.  **Core Ontologies:**
    *   **SNOMED CT-AU:** Primary clinical terminology. Source: NCTS/ADHA.
    *   **AMT (Australian Medicines Terminology):** For specific Australian medicine products from PBS. Source: NCTS/ADHA.
    *   **ATC (Anatomical Therapeutic Chemical Classification):** For drug classification from PBS. Source: WHOCC/other.
    *   **ICD-10-AM:** Considered for contextual condition classification.
3.  **Incremental Approach:** Decided to start with processing the MBS file and integrating SNOMED CT-AU first (Phase 1), then incorporate PBS, AMT, and ATC (Phase 2).
4.  **Linking MBS and PBS:** Primarily through shared `Condition` nodes (mapped from text to SNOMED CT/ICD-10-AM). Other potential links via specialties or co-occurrence discussed.
5.  **Linking Medicines to Conditions (PBS):**
    *   Primary method: NLP on PBS restriction text to extract conditions, then map to SNOMED CT.
    *   Secondary methods: Leveraging AMT product information, external drug databases (e.g., DrugBank), text mining (advanced).
6.  **Data Temporality:** Recognized MBS/PBS data is dynamic. Graph model and processing must handle `effectiveFrom`/`effectiveTo` dates for items and relationships.
7.  **Spark Usage:** Design for flexibility. Initial development to focus on Python scripts adaptable to Spark if data volume/complexity requires. Agent confirmed it does not know the user's specific Spark environment availability.
8.  **AI Agent Role:** The AI (Jules) will guide implementation by providing plans, code snippets, and content for documentation. The user (or a developer) will execute the implementation and manage the repository. AI cannot directly save conversational logs to the user's repo but can create file content in a sandbox.
9.  **Foundational Documents:** Agreed to create `README.md`, `AGENTS.MD`, `ROADMAP.MD`, `TODO.md`, `CHANGELOG.md`, and this `session_log.md`.

## Key Resources Provided by User:

*   **MBS XML File Link:** `https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/650f3eec0dfb990fca25692100069854/0b61e1e80b332754ca258c9e0000c7d8/$FILE/MBS-XML-20250701%20Version%203.XML`
*   **PBS XML File Link (ZIP):** `https://m.pbs.gov.au/downloads/2025/07/2025-07-01-xml-V3.zip`
*   **NCTS/ADHA Link (for SNOMED CT-AU, AMT):** `https://www.healthterminologies.gov.au/`

## Initial High-Level Plan Outline:

*   **Phase 1:** Core MBS Data Ingestion and Initial Graph (SNOMED CT-AU integration).
*   **Phase 2:** PBS Data Ingestion and Integration with MBS (AMT, ATC integration, linking via conditions).
*   **Phase 3:** Advanced NLP, Temporal Analysis, and Policy Question Exploration.

*(This log should be updated by the user with summaries of significant future interactions and decisions.)*
```
