## Demo Video
https://www.youtube.com/watch?v=YKcMhl4a-5I

## Objective
Create a microservice to sync data between two databases using Kafka Connect.

## Design Approach
The Publish/ Subscriber design patern is implemented using Kafka Connect to sync data between two databases. The source database is Postgres and the target database is also Postgres. The source database is the original database and the target database is the replica of the source database. The data is synced between the two databases using Kafka Connect. The data is synced in real-time and all the changes from postgres are reflected in the target database (test-db).

**io.debezium.connector.postgresql.PostgresConnector** is used to connect the source database with the Kafka topics. The connector is configured to connect to the source database and listen to the changes in the database. The connector listens to the changes in the database and publishes the changes to the Kafka topics. The connector is configured to publish the changes to the Kafka topic named **subscription**.

**io.confluent.connect.jdbc.JdbcSinkConnector** is used to connect the Kafka topics with the target database. The connector is configured to connect to the Kafka topic named **subscription** and listen to the changes in the topic. The connector listens to the changes in the Kafka topic and syncs the changes to the target database (test-db).

The solution is implemented using Docker containers. The following containers are used in the solution:
1. Zookeeper
2. Kafka
3. postgres (DB1 - orignal db which should be replicated to DB2)
4. test-db (DB2 - replica of DB1)
5. Connect (Kafka connector to connect the DB's with the kafka topics)

## Scalability and Maintainability
The solution is scalable and maintainable. The solution is implemented using Docker containers. The containers are lightweight and can be easily scaled up or down based on the requirements. The containers can be easily deployed on any cloud platform or on-premises infrastructure. The solution is easy to maintain as the containers are isolated and can be easily updated or replaced without affecting the other containers.
Failure Recovery and Fault Tolerance are implemented using the zookeeper and Kafka. Zookeeper ensures that if kafka broker does down, a new broker is elected as the leader and the data is replicated to the new broker. The solution is fault-tolerant as the data is replicated to multiple brokers and the data is not lost even if one broker goes down.

## Code Structure
1. **docker-compose.yml** - The docker-compose file is used to define the services and the containers used in the solution. The file defines the services for Zookeeper, Kafka, Postgres, test-db, and Connect.
2. **connector.json** - The connector.json file is used to define the configuration for the source connector. The file defines the configuration for the Postgres connector to connect to the source database and publish the changes to the Kafka topic.
3. **test-sink.json** - The test-sink.json file is used to define the configuration for the sink connector. The file defines the configuration for the JDBC sink connector to connect to the Kafka topic and sync the changes to the target database.
4. **clear.sh** - The clear.sh file is used to remove all running docker instances.
5. **Dockerfile** - The Dockerfile is used to build the custom image for the Connect service. The Dockerfile installs the required dependencies and copies the connector jars to the image.

## Time estimation
- Understanding Kafka (connector, debezium, etc) - 5 hours
- Setting up the environment (Docker, Kafka, Postgres) - 2 hours
- Implementing the solution - 3 hours
- Testing and debugging - 2 hours
- Documentation - 1 hour
- Total - 13 hours

## Challenges
The main challenge faced during the implementation was setting up the environment and configuring the connectors. The configuration of the connectors required understanding the Kafka Connect framework and the configuration parameters. The configuration parameters for the connectors needed to be set correctly to connect the source database with the Kafka topics and the Kafka topics with the target database. The configuration parameters for the connectors were not well documented and required some trial and error to get the connectors working correctly. The other challenge faced was setting up the environment with Docker containers. The Docker containers needed to be configured correctly to connect the services and the containers needed to be linked correctly to communicate with each other.

JDBC connector was needed to write changes to postgres and does not come pre-installed with the confluent image. The connector had to be installed manually and the connector jar had to be copied to the image.

## Alternatives Considered
- RabbitMQ instead of Kafka: RabbitMQ is another message broker that could be used to implement the Publish/Subscriber design pattern. RabbitMQ is lightweight and easy to use. However, Kafka was chosen as it is more scalable and fault-tolerant compared to RabbitMQ. Kafka is designed for high-throughput and low-latency messaging and is more suitable for real-time data processing.

## Steps to verify the solution

Start the docker containers using the following command:
```
docker-compose up -d
```

Once the containers are up and running, you can check the status of the containers using the following command:
```
docker ps -a
```

Run the following command to verify the db are empty:
```
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select * from subscription"'
```
```
docker-compose exec test-db bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select * from subscription"'
```

The above commands should result in an error as the tables are empty.

Now run the following command create a db in postgres (db1):
```
docker-compose exec postgres bash -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -c 'CREATE TABLE subscription (email VARCHAR(255) PRIMARY KEY, status VARCHAR(50));'"
```
update the db1 with some data:
```
docker-compose exec postgres bash -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -c \"INSERT INTO subscription (email, status) VALUES 
('example1@example.com', 'active'),
('example2@example.com', 'inactive'),
('example3@example.com', 'active'),
('example4@example.com', 'inactive'),
('example5@example.com', 'active'),
('example6@example.com', 'inactive'),
('example7@example.com', 'active'),
('example8@example.com', 'inactive'),
('example9@example.com', 'active'),
('example10@example.com', 'inactive'),
('example11@example.com', 'active'),
('example12@example.com', 'inactive'),
('example13@example.com', 'active'),
('example14@example.com', 'inactive'),
('example15@example.com', 'active'),
('example16@example.com', 'inactive');\""

```

Verify again using the following commands to check contents of both db's:
```
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select * from subscription"'
docker-compose exec test-db bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select * from subscription"'
```

Start the source and sink connectors to link the db's with kafka topics:
```
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ --data "@connector.json"
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @test-sink.json
```

Verify the connectors using this command:
```
curl -H "Accept:application/json" localhost:8083/connectors/
```

Feel free to use test-db data verification command after each curd operation on postgres db to verify the data replication.

Update the subscription status in postgres db using the following command:
```
docker-compose exec postgres bash -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -c \"UPDATE subscription SET status = 'active' WHERE email = 'example2@example.com';\""
```

Create a new record row in the db1:
```
docker-compose exec postgres bash -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -c \"INSERT INTO subscription (email, status) VALUES ('neuroai@x.com', 'active');\""
```
delete a record from db1:
```
docker-compose exec postgres bash -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -c \"DELETE FROM subscription WHERE email = 'neuroai@x.com';\""
```



## References:
1. https://debezium.io/blog/2017/09/25/streaming-to-another-database/
2. https://medium.com/geekculture/listen-to-database-changes-with-apache-kafka-35440a3344f0
