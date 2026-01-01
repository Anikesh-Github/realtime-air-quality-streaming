# Introduction

This project implements an end-to-end real-time data engineering pipeline designed to monitor global air pollution levels.
Live Air Quality Index (AQI) readings are fetched from the World Air Quality Index (WAQI) Public API, after which the data passes through multiple stages of ingestion, processing, storage, and analytics.

The raw AQI events are first orchestrated using Apache Airflow, which schedules and manages the ingestion workflow and stores the initial readings in a PostgreSQL database.

To enable real-time data movement, PostgreSQL events are streamed into Apache Kafka, coordinated by Apache Zookeeper.
For governance and manageability of Kafka topics and schemas, Control Center and Schema Registry are incorporated to monitor traffic and enforce schema evolution.

Next, Apache Spark performs distributed processing on live AQI streams to classify pollution levels based on health risk categories (e.g., Good, Moderate, Unhealthy, Hazardous).
The refined results are persisted in a Cassandra database to support scalable, high-throughput storage and fast analytical querying.

The complete pipeline — including Airflow, Kafka, Spark, PostgreSQL, Cassandra, and supporting services — runs inside Docker containers, providing portability and ease of deployment across environments.
## System Architecture ![System Architecture](https://github.com/NitinDatta8/realtime-data-streaming/blob/main/Data%20engineering%20architecture.png)


# 🌍 Real-Time Air Quality Monitoring & Streaming Pipeline

An end-to-end **real-time data engineering project** that ingests live Air Quality Index (AQI) data, streams it through a distributed pipeline, processes it in parallel, and stores it for fast historical analytics.

This project showcases a **production-style streaming architecture** using modern big-data tools.

---

## 📌 Project Overview

Air quality data is continuously changing and needs to be processed in real time for monitoring, analytics, and alerting.  
This project builds a **scalable and fault-tolerant pipeline** that:

- Fetches live AQI data from a public API
- Streams data reliably using Kafka
- Processes data in real time using Spark
- Stores processed data as time-series in Cassandra

---

## 🧠 Architecture

WAQI API
↓
Apache Airflow (Scheduling & Orchestration)
↓
PostgreSQL (Raw / Staging Storage)
↓
Apache Kafka (Streaming Layer)
↓
Apache Spark (Real-Time Processing)
↓
Apache Cassandra (Time-Series Analytics Storage)

---
Final Visualization in Power Bi in Clustered Bar Charts different Categories:
<img width="1908" height="982" alt="Screenshot 2026-01-01 214542" src="https://github.com/user-attachments/assets/9446eac3-28c1-4f98-8793-66507cfdf080" />

## 🛠️ Tech Stack

- **Language:** Python  
- **Workflow Orchestration:** Apache Airflow  
- **Streaming Platform:** Apache Kafka, Zookeeper  
- **Processing Engine:** Apache Spark (Structured Streaming)  
- **Databases:**
  - PostgreSQL (raw / staging data)
  - Cassandra (processed time-series data)
- **Containerization:** Docker, Docker Compose  

---

## 🔄 Data Flow

1. **Ingestion**
   - Airflow schedules periodic jobs to fetch live AQI data.
   - Raw data is stored in PostgreSQL to ensure durability and auditability.

2. **Streaming**
   - Data is published to Kafka topics.
   - Kafka acts as a buffer and decouples ingestion from processing.

3. **Processing**
   - Spark reads Kafka data as a **consumer group**.
   - Kafka partitions are processed in parallel by Spark executors.
   - AQI values are classified (Good, Moderate, Poor, Hazardous).

4. **Storage**
   - Processed AQI data is written to Cassandra.
   - Cassandra stores data efficiently as time-series for fast reads.

---

## ⚙️ Why These Technologies?

### PostgreSQL
- Used as a **staging layer** for raw AQI data
- Provides structured storage and easy integration with Airflow

### Kafka
- Enables real-time streaming and fault tolerance
- Supports parallel consumption using consumer groups

### Spark
- Provides distributed and parallel data processing
- Handles streaming data using micro-batching
- Supports fault tolerance via checkpointing

### Cassandra
- Optimized for **time-series data**
- High write throughput and horizontal scalability
- Ideal for long-term AQI analytics

---
Key Features
--Real-time AQI data ingestion
---Parallel processing using Spark executors
--Fault tolerance with Kafka offsets and Spark checkpointing
--Scalable time-series storage
--Fully dockerized environment



🎯 Learning Outcomes
--End-to-end real-time data pipeline design
--Kafka consumer groups and partition-based parallelism
--Spark Structured Streaming concepts
--Time-series data modeling in Cassandra
--Production-style data engineering architecture

🔮 Future Enhancements
--Window-based AQI analytics (hourly / daily trends)
--Alerting system for hazardous AQI levels
--Dashboard integration (Grafana / Power BI
--Schema registry and Avro serialization

🧾 Conclusion

This repository demonstrates a real-world real-time data engineering pipeline, showcasing how streaming systems are built using modern distributed technologies.
