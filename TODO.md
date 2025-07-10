# TODO List: aus-health-knowledge-graph

This list tracks current and pending tasks. It will be updated as the project progresses.

## Phase 1: Core MBS Data Ingestion and Initial Graph Foundation

### Environment & Setup
- [ ] Finalize choice of repository name (current: `aus-health-knowledge-graph`) and create GitHub repository.
- [ ] Set up local Python development environment (e.g., using `venv` or `conda`).
    - [ ] Install Python 3.x.
    - [ ] Initialize `requirements.txt`.
- [ ] Install core Python libraries:
    - [ ] `pip install lxml pandas python-dotenv neo4j` (add others as identified).
- [ ] Set up a local Neo4j instance (e.g., Neo4j Desktop or Docker container).
    - [ ] Confirm connection from Python using the `neo4j` driver.
- [ ] Create initial project directory structure as outlined in `README.md`.
- [ ] Create initial documentation files (`README.md`, `AGENTS.MD`, `ROADMAP.MD`, `TODO.md`, `CHANGELOG.MD`, `session_log.md`) and commit to repository. (Partially done by AI, user to commit)

### Ontology Acquisition & Processing (SNOMED CT-AU)
- [ ] Register and gain access to the National Clinical Terminology Service (NCTS) portal (`healthterminologies.gov.au`).
- [ ] **Task 1.1:** Develop a script (`scripts/ontology_processing/download_snomed.py`) to:
    - [ ] Securely handle NCTS credentials (e.g., using environment variables or a config file, not hardcoded).
    - [ ] Download the latest SNOMED CT-AU RF2 release ZIP file.
    - [ ] Unzip the downloaded file into `data/raw/snomed_ct_au/`.
- [ ] **Task 1.2:** Develop a script (`scripts/ontology_processing/parse_snomed_rf2.py`) to:
    - [ ] Identify and parse key SNOMED CT-AU RF2 files (e.g., `sct2_Concept_Snapshot_AUxxxxxx.txt`, `sct2_Description_Snapshot-en-AU_AUxxxxxx.txt`, `sct2_Relationship_Snapshot_AUxxxxxx.txt`).
    - [ ] Focus initially on concepts relevant to MBS (procedures, clinical findings, body structures, qualifier values).
    - [ ] Transform data into a format suitable for Neo4j import (e.g., CSVs for nodes and relationships, or direct loading).
- [ ] **Task 1.3:** Develop a script (`scripts/loading/load_snomed_to_neo4j.py`) to:
    - [ ] Load processed SNOMED CT-AU concepts, preferred terms, and `IS_A` relationships into Neo4j.
    - [ ] Create appropriate indexes on `SNOMEDConcept` nodes (e.g., on `conceptId`).
- [ ] Validate SNOMED CT-AU data loading in Neo4j with sample queries.

### MBS Data Processing
- [ ] **Task 1.4:** Develop a script (`scripts/parsing/download_mbs.py`) to:
    - [ ] Download the latest MBS XML file from the URL specified in `README.md`.
    - [ ] Save it to `data/raw/mbs/`.
- [ ] **Task 1.5:** Develop a script (`scripts/parsing/parse_mbs_xml.py`) to:
    - [ ] Use `lxml` for iterative parsing of the MBS XML.
    - [ ] Extract core MBS item details: Item Number, Description, Category, Group, Sub-Group, Schedule Fees (all types with their effective dates if available), Explanatory Notes (ID, text), Restriction Text (if separate), Effective Dates, Cessation Dates.
    - [ ] Handle nested structures (e.g., multiple fee entries for an item).
    - [ ] Output structured data (e.g., Pandas DataFrames, list of dictionaries) for MBS items, fees, notes.
- [ ] **Task 1.6:** Develop a script (`scripts/loading/load_mbs_to_neo4j.py`) to:
    - [ ] Define Neo4j graph model for MBS data (`MBSItem`, `Fee`, `ExplanatoryNote` nodes; `HAS_FEE`, `HAS_NOTE` relationships).
    - [ ] Transform parsed MBS data and load it into Neo4j, ensuring temporal properties (`effectiveFrom`, `effectiveTo`) are populated.
    - [ ] Create indexes on `MBSItem` nodes (e.g., on `itemId`).
- [ ] Validate MBS data loading with sample queries.

### Initial MBS-SNOMED CT-AU Linking
- [ ] **Task 1.7:** Develop an initial NLP script (`scripts/nlp/link_mbs_snomed.py`):
    - [ ] Use `spaCy` with `scispaCy` (e.g., `en_core_sci_sm` or larger models).
    - [ ] Process MBS item descriptions and potentially key sections of `ExplanatoryNote` text.
    - [ ] Perform Named Entity Recognition (NER) to identify potential medical conditions, procedures.
    - [ ] Implement basic term matching (exact, normalized) against loaded SNOMED CT-AU descriptions.
    - [ ] Create `MBSItem -[:MAPS_TO_CONCEPT]-> SNOMEDConcept` relationships for initial links. Store mapping method/confidence if possible.
- [ ] Review and validate a sample of these initial links.

## Phase 2: PBS Data Ingestion and Integration with MBS
- [ ] (Tasks to be detailed once Phase 1 is substantially underway)

## Phase 3: Advanced NLP, Temporal Analysis, and Policy Insights
- [ ] (Tasks to be detailed after Phase 2)

## Backlog / Future Ideas
- [ ] Explore more sophisticated ontology mapping techniques (e.g., semantic similarity with embeddings).
- [ ] Develop a strategy for handling updates to MBS/PBS data and ontologies (versioning, diffing).
- [ ] Research and integrate other relevant ontologies (ORDO, HPO, LOINC) if deemed beneficial.
- [ ] Investigate Spark integration for performance if data scales demand it.
```
