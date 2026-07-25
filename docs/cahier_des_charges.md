<div align="center">

#  GLOBAL PHOSPHATE MARKET ANALYTICS PLATFORM

### Cahier des Charges — Data Engineering & Data Analytics

**Plateforme d'analyse et de prédiction du marché mondial du phosphate**

---

 Juillet 2026 ·  Projet Fil Rouge ·  Deadline : 08/08/2026

*Data Collection · Data Lake · Data Warehouse · Machine Learning · Business Intelligence*

---

</div>

<div align="center">

| | | | |
|:---:|:---:|:---:|:---:|
|  **Python** |  **Snowflake** |  **dbt** |  **Power BI** |
|  **Airflow** |  **MinIO** | **Docker** |  **Scikit-Learn** |

</div>

\pagebreak

##  Sommaire

| # | Section | 
|---|---------|
| 1 | [Page de couverture](#-global-phosphate-market-analytics-platform) |
| 2 | [Présentation du projet](#2-présentation-du-projet) |
| 3 | [Contexte métier](#3-contexte-métier) |
| 4 | [Objectifs](#4-objectifs) |
| 5 | [Périmètre du projet](#5-périmètre-du-projet) |
| 6 | [Architecture globale](#6-architecture-globale) |
| 7 | [Architecture technique détaillée](#7-architecture-technique-détaillée) |
| 8 | [Architecture Medallion](#8-architecture-medallion) |
| 9 | [Technologies utilisées](#9-technologies-utilisées) |
| 10 | [Flux de données](#10-flux-de-données) |
| 11 | [Description des couches](#11-description-de-chaque-couche) |
| 12 | [Modèle dimensionnel](#12-modèle-dimensionnel) |
| 13 | [Pipeline complet](#13-pipeline-complet) |
| 14 | [Machine Learning](#14-machine-learning) |
| 15 | [Dashboard Power BI](#15-dashboard-power-bi) |
| 16 | [Orchestration Airflow](#16-orchestration-airflow) |
| 17 | [Structure des dossiers](#17-structure-des-dossiers) |
| 18 | [Planning du projet](#18-planning-du-projet) |
| 19 | [Analyse des risques](#19-analyse-des-risques) |
| 20 | [Critères de réussite](#20-critères-de-réussite) |
| 21 | [Livrables](#21-livrables) |
| 22 | [Évolutions futures](#22-évolutions-futures) |
| 23 | [Conclusion](#23-conclusion) |

\pagebreak

## 2. Présentation du projet

>  **En une phrase** : Une plateforme end-to-end qui collecte, structure et prédit les dynamiques du marché mondial du phosphate pour éclairer la décision stratégique.

| Élément | Détail |
|---|---|
|  **Nom du projet** | Global Phosphate Market Analytics Platform |
|  **Type** | Projet Fil Rouge — Data Engineering / Data Analytics |
|  **Domaine** | Marché des matières premières — Phosphate |
|  **Nature** | Pipeline ELT + Data Warehouse + ML + BI |
|  **Échéance** | 08/08/2026 |

---

## 3. Contexte métier

Le phosphate est une ressource stratégique pour l'agriculture mondiale (engrais), sous tension géopolitique et économique croissante. Les décideurs (industriels, investisseurs, institutions) manquent d'un outil unifié croisant **prix, production, échanges commerciaux et indicateurs macroéconomiques**.

>  **Callout — Enjeu métier**
> Sans consolidation de ces données dispersées, l'analyse du marché reste fragmentée, réactive, et peu prédictive.

### Sources de données mobilisées

```mermaid
mindmap
  root((Sources de données))
    IndexMundi
      Prix du phosphate
    FAOSTAT
      Production mondiale
    UN Comtrade
      Import / Export
    World Bank
      Inflation
      Population
      PIB
```

---

## 4. Objectifs

|  Objectif | Description |
|---|---|
| **O1 — Centraliser** | Unifier 4 sources hétérogènes dans un Data Lake puis un Data Warehouse |
| **O2 — Fiabiliser** | Garantir qualité, cohérence et traçabilité des données (tests dbt) |
| **O3 — Prédire** | Anticiper l'évolution des prix du phosphate (2024–2026) via Machine Learning |
| **O4 — Visualiser** | Fournir un dashboard exécutif interactif et décisionnel |
| **O5 — Automatiser** | Orchestrer l'ensemble du pipeline sans intervention manuelle (Airflow) |

---

## 5. Périmètre du projet

 **Inclus dans le projet**
- Extraction automatisée (scraping + API) des 4 sources
- Data Lake MinIO + Data Warehouse Snowflake (Bronze/Silver/Gold)
- Transformations dbt avec tests de qualité
- Modèle de prévision des prix (ML)
- Dashboard Power BI exécutif
- Orchestration Airflow bout en bout

 **Hors périmètre**
- Développement d'une application web front-end dédiée
- Trading algorithmique en temps réel
- Couverture de matières premières autres que le phosphate

---

## 6. Architecture globale

```mermaid
flowchart LR
    A[ Sources de données] --> B[ Python<br/>Extraction]
    B --> C[ MinIO<br/>Data Lake]
    C --> D[ Snowflake<br/>Bronze]
    D --> E[ dbt<br/>Silver]
    E --> F[ dbt<br/>Gold]
    F --> G[ Machine Learning]
    F --> H[ Power BI]
    G --> H
    I[ Airflow — Orchestration] -.-> B
    I -.-> C
    I -.-> D
    I -.-> E
    I -.-> F
    I -.-> G
    I -.-> H

    style A fill:#e8f0fe,stroke:#1a73e8
    style C fill:#fff3e0,stroke:#f9a825
    style D fill:#fce4ec,stroke:#c2185b
    style E fill:#e8eaf6,stroke:#3949ab
    style F fill:#e0f2f1,stroke:#00695c
    style G fill:#f3e5f5,stroke:#8e24aa
    style H fill:#fffde7,stroke:#f57f17
    style I fill:#eceff1,stroke:#455a64
```

---

## 7. Architecture technique détaillée

```mermaid
flowchart TD
    subgraph EXT["  EXTRACTION "]
        S1[IndexMundi<br/>Prix]
        S2[FAOSTAT<br/>Production]
        S3[UN Comtrade<br/>Import/Export]
        S4[World Bank<br/>Macro-éco]
    end

    subgraph LAKE["  DATA LAKE — MinIO "]
        RAW[Fichiers bruts<br/>CSV / JSON]
    end

    subgraph DWH["  SNOWFLAKE "]
        BR[Bronze — Raw]
        SI[Silver — Clean]
        GO[Gold — Star Schema]
    end

    subgraph ML[" MACHINE LEARNING "]
        MOD[Prévision des prix<br/>2024-2026]
    end

    subgraph BI[" RESTITUTION "]
        PBI[Power BI<br/>Dashboard Exécutif]
    end

    S1 & S2 & S3 & S4 --> RAW --> BR --> SI --> GO --> MOD --> PBI
    GO --> PBI
```

### Détail des couches techniques

| Couche | Rôle | Outils |
|---|---|---|
| **Extraction** | Scraping & appels API | Python, Requests, BeautifulSoup, Selenium |
| **Stockage brut** | Data Lake objet | MinIO |
| **Entrepôt** | Bronze / Silver / Gold | Snowflake, dbt Core |
| **Prédiction** | Modélisation prix | Scikit-Learn |
| **Restitution** | Dashboards | Power BI |
| **Orchestration** | Automatisation | Apache Airflow, Docker |
| **Versioning** | Code & collaboration | Git, GitHub, VS Code |

---

## 8. Architecture Medallion

```mermaid
flowchart LR
    B[" BRONZE<br/>Données brutes<br/>Aucune transformation"] --> S[" SILVER<br/>Nettoyage · Validation<br/>Dédoublonnage · Normalisation"]
    S --> G[" GOLD<br/>Star Schema<br/>Faits & Dimensions · KPIs"]

    style B fill:#fde9d9,stroke:#b06a1e
    style S fill:#e2e2e2,stroke:#555
    style G fill:#fff4c2,stroke:#b8860b
```

| Couche | Contenu | Traitements |
|---|---|---|
|  **Bronze** | Copie fidèle des sources | Aucun — traçabilité brute |
|  **Silver** | Données propres | Suppression doublons, gestion des valeurs manquantes, normalisation, tests dbt |
|  **Gold** | Modèle analytique | Star Schema, tables de faits, dimensions, KPIs métier |

---

## 9. Technologies utilisées

<div align="center">

| Catégorie | Technologies |
|---|---|
|  **Langage & Extraction** | Python · Pandas · Requests · BeautifulSoup · Selenium |
|  **Stockage** | MinIO |
|  **Entrepôt de données** | Snowflake |
|  **Transformation** | dbt Core |
|  **Conteneurisation** | Docker |
|  **Orchestration** | Apache Airflow |
|  **Machine Learning** | Scikit-Learn |
|  **Visualisation** | Power BI |
|  **Versioning** | Git · GitHub · VS Code |

</div>

---

## 10. Flux de données

```mermaid
sequenceDiagram
    participant Src as Sources (IndexMundi, FAOSTAT, UN Comtrade, World Bank)
    participant Py as Python
    participant Lake as MinIO
    participant Br as Snowflake Bronze
    participant Si as dbt Silver
    participant Go as dbt Gold
    participant ML as Machine Learning
    participant BI as Power BI
    participant Af as Airflow

    Af->>Py: Déclenche extraction
    Py->>Src: Scraping / API
    Src-->>Py: Données brutes
    Py->>Lake: Upload fichiers
    Lake->>Br: Chargement Bronze
    Af->>Si: Exécution dbt run
    Br->>Si: Nettoyage & validation
    Si->>Go: Construction Star Schema
    Af->>ML: Entraînement / prédiction
    Go->>ML: Données historiques
    ML->>BI: Prévisions
    Go->>BI: Rafraîchissement dataset
    Af->>Af: Notification fin de pipeline
```

---

## 11. Description de chaque couche

>  **Bronze** — Ingestion brute depuis MinIO vers Snowflake, sans altération, pour garantir la traçabilité complète des données sources.

>  **Silver** — Application des règles de qualité : suppression des doublons, traitement des valeurs manquantes, normalisation des formats (dates, unités, devises), exécution des tests dbt (`not_null`, `unique`, `relationships`).

>  **Gold** — Construction du modèle dimensionnel orienté analyse : tables de faits (prix, production, échanges) reliées aux dimensions (temps, pays, produit).

---

## 12. Modèle dimensionnel

```mermaid
erDiagram
    FACT_PHOSPHATE_MARKET }o--|| DIM_DATE : "par date"
    FACT_PHOSPHATE_MARKET }o--|| DIM_COUNTRY : "par pays"
    FACT_PHOSPHATE_MARKET }o--|| DIM_INDICATOR : "par indicateur"

    FACT_PHOSPHATE_MARKET {
        int fact_id PK
        int date_id FK
        int country_id FK
        int indicator_id FK
        float price_usd
        float production_tonnes
        float import_volume
        float export_volume
        float forecast_price
    }

    DIM_DATE {
        int date_id PK
        date full_date
        int year
        int month
        string quarter
    }

    DIM_COUNTRY {
        int country_id PK
        string country_name
        string region
        boolean is_major_producer
    }

    DIM_INDICATOR {
        int indicator_id PK
        string indicator_name
        string source
        string unit
    }
```

---

## 13. Pipeline complet

```mermaid
flowchart TD
    A[ Start] --> B[Extraction Python]
    B --> C[Upload MinIO]
    C --> D[Chargement Snowflake Bronze]
    D --> E[dbt run — Silver]
    E --> F{Tests dbt<br/>OK ?}
    F --  Échec --> N1[ Notification erreur]
    F --  OK --> G[dbt run — Gold]
    G --> H[Entraînement / mise à jour ML]
    H --> I[Rafraîchissement Power BI]
    I --> J[ Notification succès]
    J --> K[ End]
```

---

## 14. Machine Learning

| Élément | Détail |
|---|---|
|  **Objectif** | Prévision des prix du phosphate |
|  **Horizon** | 2024 · 2025 · 2026 |
|  **Approche** | Régression / séries temporelles (Scikit-Learn) |
|  **Données d'entrée** | Table de faits Gold (historique prix, production, macro-économie) |
|  **Sortie** | Prix prédit injecté dans le dashboard Power BI |

```mermaid
flowchart LR
    A[Données Gold] --> B[Feature Engineering]
    B --> C[Entraînement du modèle]
    C --> D[Évaluation]
    D --> E{Performance<br/>acceptable ?}
    E -- Non --> B
    E -- Oui --> F[Prédiction 2024-2026]
    F --> G[Export vers Power BI]
```

---

## 15. Dashboard Power BI

>  **Dashboard Exécutif** — vue synthétique et décisionnelle du marché mondial du phosphate.

| Page | Contenu |
|---|---|
|  **Vue d'ensemble** | KPIs clés, tendance globale |
|  **Prix** | Évolution historique et prévisionnelle |
|  **Production** | Analyse par pays et par période |
|  **Import** | Volumes et tendances par pays |
|  **Export** | Volumes et tendances par pays |
|  **Comparaison pays** | Benchmark des principaux producteurs |
|  **Prévisions** | Résultats du modèle ML |
|  **Insights** | Synthèse des enseignements clés |

---

## 16. Orchestration Airflow

```mermaid
flowchart LR
    T1[Extraction] --> T2[Upload MinIO] --> T3[Chargement Snowflake] --> T4[dbt run] --> T5[Tests dbt] --> T6[Gold] --> T7[Machine Learning] --> T8[Refresh Power BI] --> T9[Notification]
```

| Tâche Airflow | Fréquence |
|---|---|
| Extraction & ingestion | Quotidienne / hebdomadaire selon la source |
| Transformation dbt | À chaque nouvelle donnée |
| Entraînement ML | Mensuelle |
| Refresh Power BI | À chaque fin de pipeline |
| Notifications | Succès / échec de chaque run |

---

## 17. Structure des dossiers

```
 global-phosphate-analytics/
├──  extraction/
│   ├── indexmundi_scraper.py
│   ├── faostat_extractor.py
│   ├── comtrade_extractor.py
│   └── worldbank_extractor.py
├──  dbt_project/
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   └── tests/
├──  ml/
│   ├── train_model.py
│   └── predict.py
├──  airflow/
│   └── dags/
│       └── phosphate_pipeline_dag.py
├──  powerbi/
│   └── dashboard.pbix
├──  docker/
│   └── docker-compose.yml
└──  README.md
```

---

## 18. Planning du projet

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title Planning — Global Phosphate Market Analytics Platform
    section Cadrage
    Cahier des charges           :done, 2026-07-20, 3d
    section Extraction
    Scraping & API                :active, 2026-07-23, 5d
    section Data Lake / DWH
    MinIO + Snowflake Bronze      :2026-07-28, 4d
    dbt Silver                    :2026-08-01, 2d
    dbt Gold                      :2026-08-03, 2d
    section ML & BI
    Machine Learning               :2026-08-04, 2d
    Dashboard Power BI             :2026-08-05, 2d
    section Finalisation
    Airflow & tests bout-en-bout   :2026-08-06, 1d
    Livraison finale                :milestone, 2026-08-08, 0d
```

---

## 19. Analyse des risques

|  Risque | Impact | Probabilité | Mitigation |
|---|---|---|---|
| Données 2026 incomplètes chez les sources | Moyen | Élevée | Recours au forecast ML au-delà des données réelles disponibles |
| Instabilité des sites scrapés | Moyen | Moyenne | Scripts robustes + gestion d'erreurs + Selenium en secours |
| Délai serré (deadline 08/08/2026) | Élevé | Moyenne | Planning strict, priorisation des livrables critiques |
| Qualité hétérogène entre sources | Moyen | Élevée | Tests dbt systématiques en couche Silver |
| Complexité de l'orchestration Airflow | Faible | Moyenne | Tests progressifs par tâche avant intégration complète |

---

## 20. Critères de réussite

 Pipeline end-to-end fonctionnel de l'extraction jusqu'au dashboard
 Données Bronze/Silver/Gold cohérentes et testées
 Modèle ML produisant des prévisions exploitables (2024–2026)
 Dashboard Power BI clair, interactif et orienté décision
 Orchestration Airflow autonome et fiable
 Documentation complète et professionnelle du projet

---

## 21. Livrables

| Livrable | Format |
|---|---|
| Scripts d'extraction | Python (.py) |
| Data Lake | MinIO (buckets) |
| Data Warehouse | Snowflake (Bronze/Silver/Gold) |
| Projet dbt | Modèles + tests |
| Modèle ML | Script + artefact de prédiction |
| Dashboard | Power BI (.pbix) |
| Orchestration | DAG Airflow |
| Documentation | Cahier des charges (ce document) + README |

---

## 22. Évolutions futures

-  Ajout de nouvelles matières premières (potasse, azote)
-  API publique d'exposition des données consolidées
-  Modèles ML avancés (deep learning, séries temporelles multivariées)
-  Migration complète vers une orchestration cloud managée

---

## 23. Conclusion

>  **Global Phosphate Market Analytics Platform** structure une chaîne de valeur data complète — de la donnée brute dispersée à l'insight décisionnel — au service d'une meilleure compréhension du marché mondial du phosphate.

<div align="center">

---
*Document réalisé dans le cadre du projet Fil Rouge — Data Engineering & Data Analytics*

</div>