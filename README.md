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


#Technologies:-

*Data Source: World Air Quality Index (WAQI) Public API for live air pollution readings

*Apache Airflow: Orchestrates ingestion workflows and inserts raw readings into PostgreSQL

*PostgreSQL: Stores initial AQI readings

*Apache Kafka & Zookeeper: Streams AQI events from PostgreSQL in real time to the processing layer

*Schema Registry & Control Center: Manage schemas and monitor Kafka streaming pipelines

*Apache Spark: Performs distributed processing and health-risk classification on AQI streams

*Cassandra: Stores processed, analytics-ready AQI insights

*Docker: Containerizes the entire infrastructure for portable deployment

#Things Learned:-

*Building ETL/ELT workflows using Apache Airflow

*Implementing real-time event streaming with Kafka

*Handling distributed coordination with Zookeeper

*Performing scalable transformation and analytics using Apache Spark

*Working with polyglot storage (PostgreSQL for raw data + Cassandra for processed data)

*Deploying complete data engineering ecosystems using Docker containers