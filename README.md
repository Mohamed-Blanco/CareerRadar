
![ChatGPT Image Sep 26, 2025, 03_33_29 PM](https://github.com/user-attachments/assets/b105191e-bf4f-4a5a-b135-d60d1a136559)



# Intelligent Web Scraper for Job Data

<div align="center">

![Job Scraper](https://img.shields.io/badge/JobScraper-DataCollection-blue?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Database](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge\&logo=postgresql)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=for-the-badge)

**An intelligent, automated system for collecting and standardizing job listings across multiple platforms.**

*Dynamic scraping, anti-bot resilience, and clean data pipelines for job recommendation engines.*

</div>

## Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [Architecture](#architecture)
* [Installation](#installation)
* [Getting Started](#getting-started)
* [Modules](#modules)
* [Challenges & Solutions](#challenges--solutions)
* [Performance](#performance)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

Collecting job data is both critical and complex. Most job boards (LinkedIn, Indeed, DreamJobMaroc) lack public APIs, making manual collection impossible at scale.

This project implements an **intelligent web scraping agent** that:

* Automates data extraction from multiple platforms.
* Cleans and standardizes job listings into JSON.
* Feeds reliable data into downstream recommendation systems.

**What This Project Is:**

* Automated job listing collector.
* Designed to bypass anti-bot protections (rotating agents, adaptive timing).
* Optimized for PostgreSQL storage with batch management.
* Scalable and extensible.

**What This Project Is Not:**

* A full job portal.
* A public API for external clients.
* A guaranteed bypass for all scraping protections (e.g., advanced CAPTCHAs).

---

## Key Features

| Feature              | Description                                                                           |
| -------------------- | ------------------------------------------------------------------------------------- |
| **Auth Manager**     | Handles login simulation, cookie/session management, and retries.                     |
| **ID Extractor**     | Captures unique job IDs from dynamic listings (scrolling/pagination).                 |
| **Batch Management** | Uses PostgreSQL temporary tables to filter duplicates and optimize inserts.           |
| **Data Extractor**   | Collects job details (title, company, location, date, description, applicants, etc.). |
| **Text Processing**  | Cleans job descriptions with regex and NLTK for standardization.                      |
| **JSON Output**      | Produces structured, consistent datasets ready for analysis.                          |
| **Error Handling**   | Implements exponential backoff and detailed logging.                                  |
| **Cross-Platform**   | Runs on Linux, macOS, and Windows.                                                    |

---

## Architecture

```
┌───────────────────────┐
│ Authentication Manager │  ← Login, cookies, sessions
├───────────────────────┤
│ ID Extractor           │  ← Collects unique job IDs
├───────────────────────┤
│ Batch Manager          │  ← Temp tables & duplicate filtering
├───────────────────────┤
│ Data Extractor         │  ← Detailed scraping (Selenium + BS4)
├───────────────────────┤
│ Text Processor         │  ← Cleaning + NLTK normalization
├───────────────────────┤
│ Storage Layer          │  ← PostgreSQL persistence
└───────────────────────┘
```

---

## Installation

### Prerequisites

* **Python 3.10+**
* **PostgreSQL 15+**
* **pip / venv** for dependencies

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/job-scraper.git
cd job-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Configure database in .env
DATABASE_URL=postgresql://user:password@localhost:5432/jobs
```

---

## Getting Started

```bash
In Order to start this project is very simple :
```bash
    #Step 1 : build containers via docker compose 
    docker compose up --build

    #Step 2 : using terminal or any api platform :

          via postman : http://localhost:5099/api/pipelines/full/20
          via terminal : curl -X POST http://flask:5099/api/pipelines/full/8000
    thats it !!!
    Now you can check this file to see the results , when the scrapper finishs :
        opp_seeker/data_warehouse/raw/jobs_data.json
       
```

# Example output
[
  {
        "title": "Analyste KYC - Remote Maroc",
        "entreprise": "Yapla",
        "location": "Casablanca Metropolitan Area",
        "nomberofapplicants": "32",
        "time": null,
        "description": "📢 Nous Recrutons un(e) Analyste KYC !🤝 Notre mission chez Yapla ?Accompagner les associations pour faciliter...",
        "Niveau hiérarchique": "Entry level",
        "Type d’emploi": "Full-time",
        "Fonction": "Finance and Sales",
        "Secteurs": "Non-profit Organizations",
        "joblink": "https://www.linkedin.com/jobs/view/4238238418/?alternateChannel=search&refId=AFYeJOMJHPAGzw3EjH59FQ%3D%3D&trackingId=FcBdDTjfIr%2FJomXXdyVFoA%3D%3D",
        "found_by_keyword": "Programme de stage",
        "logo_url": "https://media.licdn.com/dms/image/v2/D4D0BAQEKi6-J2mBEzQ/company-logo_100_100/company-logo_100_100/0/1712662452867/yaplacommunity_logo?e=2147483647&v=beta&t=YD8UR1KNvg3Y20Hy9R9J9Mas_K4JxA7IFEPlAomEn3w"
    },
]
```

---

## Modules

* **Auth Manager** – Simulates login & manages sessions.
* **ID Extractor** – Pulls unique IDs from job lists.
* **Batch Manager** – Temporary table staging for IDs.
* **Data Extractor** – Extracts full job details.
* **Text Processor** – Regex + NLTK cleaning.
* **Database Layer** – PostgreSQL storage.

---

## Challenges & Solutions

| Challenge                     | Solution                                              |
| ----------------------------- | ----------------------------------------------------- |
| **Dynamic content rendering** | Selenium to handle JavaScript-driven pages.           |
| **Anti-bot protections**      | User-agent rotation + adaptive timing + retry logic.  |
| **CAPTCHAs**                  | Logged & skipped gracefully (proxy rotation planned). |
| **Frequent DOM changes**      | Modularized agents for easier updates.                |

---

## Performance

* **High throughput** – Scrapes thousands of listings/hour.
* **Data uniqueness** – Ensured with batch + temp tables.
* **Low error rates** – Exponential backoff reduces login failures.
* **JSON export** – Standardized for downstream ML/AI pipelines.

---

## Troubleshooting

| Issue               | Cause                                | Solution                               |
| ------------------- | ------------------------------------ | -------------------------------------- |
| `login failed`      | Wrong credentials or blocked session | Check Auth Manager config, retry       |
| `duplicate entries` | ID extractor mismatch                | Verify batch manager is active         |
| `site blocked`      | Anti-bot detection                   | Enable proxy rotation (future release) |

---

## Contributing

```bash
# Fork & clone
git clone https://github.com/yourusername/job-scraper.git

# Create branch
git checkout -b feature/my-feature

# Commit & push
git commit -m "Add new scraping feature"
git push origin feature/my-feature
```

Areas for contribution:

* Proxy rotation system
* New platform agents
* CAPTCHAs bypass improvements
* Advanced NLP preprocessing
* Dashboard for monitoring scrapers

---

## License

MIT License – See [LICENSE](LICENSE) file for details.

---

**if you have any question or you want to contribute , you can contact me here : labiadmo920@gmail.com**

*If this project helped you, give it a ⭐*


