import logging
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType


def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS air_quality
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)
    print("Keyspace created successfully!")


def create_table(session):
    session.execute("""
        CREATE TABLE IF NOT EXISTS air_quality.aqi_readings (
            city TEXT,
            aqi FLOAT,
            pm25 FLOAT,
            pm10 FLOAT,
            o3 FLOAT,
            no2 FLOAT,
            so2 FLOAT,
            timestamp TEXT,
            PRIMARY KEY (city, timestamp)
        );
    """)
    print("Table created successfully!")


def create_spark_connection():
    try:
        spark = SparkSession.builder \
            .appName('AirQualityStreaming') \
            .config('spark.jars.packages',
                    "com.datastax.spark:spark-cassandra-connector_2.13:3.4.1,"
                    "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.1") \
            .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")
        print("Spark connection created successfully!")
        return spark

    except Exception as e:
        logging.error(f"Couldn't create Spark session: {e}")
        return None


def connect_to_kafka(spark):
    try:
        df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "aqi_stream") \
            .option("startingOffsets", "earliest") \
            .load()
        print("Kafka dataframe created successfully")
        return df
    except Exception as e:
        logging.error(f"Kafka dataframe could not be created: {e}")
        return None


def create_cassandra_connection():
    try:
        cluster = Cluster(['localhost'])
        return cluster.connect()
    except Exception as e:
        logging.error(f"Could not connect to Cassandra: {e}")
        return None


def create_selection_df_from_kafka(stream_df):
    schema = StructType([
        StructField("city", StringType(), True),
        StructField("aqi", FloatType(), True),
        StructField("pm25", FloatType(), True),
        StructField("pm10", FloatType(), True),
        StructField("o3", FloatType(), True),
        StructField("no2", FloatType(), True),
        StructField("so2", FloatType(), True),
        StructField("timestamp", StringType(), True)
    ])

    parsed = (stream_df
              .selectExpr("CAST(value AS STRING)")
              .select(from_json(col("value"), schema).alias("data"))
              .select("data.*"))
    return parsed


if __name__ == "__main__":
    spark_conn = create_spark_connection()

    if spark_conn:
        kafka_df = connect_to_kafka(spark_conn)
        if kafka_df is not None:
            selection_df = create_selection_df_from_kafka(kafka_df)
            cas_session = create_cassandra_connection()

            if cas_session:
                create_keyspace(cas_session)
                create_table(cas_session)

                print("\n⚡ Streaming started... waiting for live AQI events.\n")

                query = (selection_df.writeStream
                         .format("org.apache.spark.sql.cassandra")
                         .option("checkpointLocation", "/tmp/checkpoint_aqi")
                         .option("keyspace", "air_quality")
                         .option("table", "aqi_readings")
                         .start())

                query.awaitTermination()
