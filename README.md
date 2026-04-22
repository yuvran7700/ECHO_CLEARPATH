# ClearPath Microservices API — Backend

> **Event-driven intelligence platform for Sydney train disruption forecasting.**
> Live site -> [clearpath.vercel.app](https://echo-clearpath-frontend-2a3qp1r82-yuvran7700s-projects.vercel.app/)
> Frontend repo -> [clearpath-frontend](https://github.com/yuvran7700/ECHO_CLEARPATH_FRONTEND)

**Tools used:** AWS (Lambda, DynamoDB, S3, API Gateway, SAM) · GitHub Actions · Python (scikit-learn, pandas, boto3) · Twitter.io API · Google Weather API

## Key Technical Highlights
- **5-day AI-powered disruption forecasting** — correlates historical weather/disruption patterns against live weather data to generate forward-looking risk scores
- **Machine learning classification** — trained a TF-IDF + Logistic Regression model to classify train disruption status.
- **Event-driven microservices architecture** — three independently deployed AWS microservices communicate entirely via event triggers (S3 uploads, DynamoDB Streams, scheduled Lambdas), exposing results through a shared REST API Gateway
- **DevOps & CI/CD pipeline** — two-tier staging/production cloud deployment via AWS SAM; per-microservice CI pipelines enforce linting, TDD-based unit and integration testing on every PR. Automated deployment to staging and/or production via GitHub Environments.
- **Cloud-native infrastructure** — fully serverless on AWS (Lambda, DynamoDB, S3, API Gateway, SSM), defined entirely as Infrastructure as Code via SAM and versioned through the SDLC alongside application code

---

## What is ClearPath?

Sydney Trains carries around 1 million passengers a day — and when disruptions hit, commuters find out too late. Transport NSW only publishes live alerts reactively, leaving passengers stranded on platforms with no warning.

ClearPath solves this with a **dual-layer intelligence platform**:

- **5-day disruption forecasting** — predicts the likelihood of disruption on a given train line for each of the next 5 days, along with the probable cause and suggested alternative routes.
- **Historical analytics** — lets users explore how a train line has performed over time, broken down by day of week, month, season, and weather severity.

This repository contains the backend: three event-driven microservices deployed on AWS, exposing a REST API consumed by the frontend.

---

## Architecture Overview

ClearPath is built on an **event-driven, serverless architecture** using AWS Lambda, DynamoDB, S3, and API Gateway. Each microservice is independently deployed via AWS SAM with its own CI/CD pipeline.

```
┌─────────────────────────────────────────────────┐
│                  React Frontend                  │
│              (Vite · Vercel · TypeScript)         │
└────────────────────┬────────────────────────────┘
                     │ REST API (API Gateway)
        ┌────────────┼────────────┐
        ▼            ▼            ▼
  [MS1 Weather] [MS2 Alerts] [MS3 Analytics]
        │            │            │
        ▼            ▼            ▼
     S3 + DynamoDB  DynamoDB   DynamoDB (Joined)
```

### Microservice 1 — Weather

Collects raw BOM weather data (CSV), uploads it to S3, which triggers a Lambda to parse and structure the readings. A second Lambda applies weather severity labels (e.g. *mild*, *moderate*, *severe*) and stores the result in DynamoDB.

**Endpoints:**
- `GET /weather/data?date={date}` — Returns cleaned weather readings for a given date (ADAGE-compliant JSON)
- `GET /weather/severity?date={date}` — Returns weather severity label and the metrics used to calculate it

### Microservice 2 — Alerts
A scheduled `TwitterCollectionLambda` scrapes each Sydney train line's Twitter/X page, normalises the data, and writes it to `clearpath-alert-data` DynamoDB table. A DynamoDB Stream triggers a `ClassificationLambda` which runs each tweet through a trained **TF-IDF + Logistic Regression** model (`alert-microservice/src/ml/model/tweet_classifier.pkl`) to classify it as `cancelled`, `delayed`, or `unknown`, writing the result back to the table.

**Endpoints:**
- `GET /alerts?line={line}&date={date}` — Returns historical disruption alerts for a given train line and date

### Microservice 3 — Analytics (Transport)

A `JoinLambda` merges weather severity and alert data from the upstream DynamoDB tables. A `CorrelationLambda` then performs statistical analysis on the joined dataset — correlating weather conditions with disruption frequency — and stores results in a dedicated analytics table.

**Endpoints:**
- `GET /transport/disruption-forecast` — Returns a 5-day forward-looking risk score per day, incorporating upcoming weather forecasts (sourced via Google Weather API)
- `GET /transport/disruption-analytics` — Returns historical disruption statistics broken down by day of week, month, trend over time, and weather severity (supports optional `year` filter)

All endpoints return **ADAGE-compliant JSON**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Compute | AWS Lambda (Python 3.11) |
| Storage | AWS DynamoDB, AWS S3 |
| API | AWS API Gateway (REST) |
| IaC / Deploy | AWS SAM (`template.yaml` + `samconfig.toml`) |
| CI/CD | GitHub Actions |
| Secret Management | AWS SSM Parameter Store |
| Data Sources | BOM (weather), Twitter.io (alerts), Google Weather API (forecast) |
| ML Classification | TF-IDF + Logistic Regression (`scikit-learn`) |
| Data Format | ADAGE-compliant JSON |

---

## Repository Structure

```
.
├── weather-microservice/    # MS1: BOM ingestion, severity labelling
├── alert-microservice/      # MS2: Twitter scraping, disruption classification
├── transport-microservice/  # MS3: Join, correlation, forecasting & analytics endpoints
├── testing-microservice/       # Cross-service smoke, contract & componen
└── .github/workflows/       # CI/CD pipelines (per-service + prod-cd)
├── util/                    # Pre-commit hooks and setup scripts
├── template.yaml            # Root SAM stack (shared API Gateway, DynamoDB tables)
├── samconfig.toml           # Root SAM config
├── README.md
└── CONTRIBUTING.md
```

---

## Running Locally

### Prerequisites

- Python 3.11
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- AWS CLI configured with appropriate credentials

### Per-microservice

```bash
cd weather-microservice   # or alert-microservice / transport-microservice
pip install -r requirements.txt
sam build
sam local invoke          # invoke a specific function locally
```

### Environment Variables

Each microservice reads config from AWS SSM. For local development, set the following environment variables or mock them in your SAM local config:

| Variable | Description |
|---|---|
| `Environment` | `staging` or `prod` |
| `ApiId` | Shared API Gateway ID (from SSM `/clearpath/{env}/api-id`) |
| `GOOGLE_WEATHER_API_KEY` | Google Weather API key (SecureString in SSM) |

---

## CI/CD

Each microservice has its own GitHub Actions workflow scoped to its directory. Pushes to `main` trigger the unified `prod-cd.yml` which deploys all affected microservices to production.

| Workflow | Trigger |
|---|---|
| `weather-ci.yml` | PR/push to `weather-microservice/**` |
| `alert-ci.yml` | PR/push to `alert-microservice/**` |
| `transport-ci.yml` | PR/push to `transport-microservice/**` |
| `prod-cd.yml` | Push to `main` (all services) |

---

## API Documentation

Full Swagger/OpenAPI documentation is available on the live site under the **API Docs** tab. All endpoints follow the ADAGE data specification.

---

## Related

- **Frontend repo:** [clearpath-frontend](https://github.com/your-org/clearpath-frontend)
- **Live site:** [clearpath.vercel.app](https://clearpath.vercel.app)
