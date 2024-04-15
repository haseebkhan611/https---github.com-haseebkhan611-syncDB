Start the docker containers using the following command:
```
docker-compose up -d
```

The above command should start the following containers:
1. Zookeeper
2. Kafka
3. postgres (DB1 - orignal db which should be replicated to DB2)
4. test-db (DB2 - replica of DB1)
5. Connect (Kafka connector to connect the DB's with the kafka topics)

Once the containers are up and running, you can check the status of the containers using the following command:
```
docker ps -a
```

Run the following command to verify the db are empty:
```
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select * from subscription"'
docker-compose exec test-db bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select * from subscription"'
```

Now run the following command to populate the db in postgres (db1):
```
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -c \
CREATE TABLE subscription (email VARCHAR(255) PRIMARY KEY, status VARCHAR(50)); \
INSERT INTO subscription (email, status) VALUES \
 ('example1@example.com', 'active'), \
    ('example2@example.com', 'inactive'),\
    ('example3@example.com', 'active'),\
    ('example4@example.com', 'inactive'),\
    ('example5@example.com', 'active'),\
    ('example6@example.com', 'inactive'),\
    ('example7@example.com', 'active'),\
    ('example8@example.com', 'inactive'),\
    ('example9@example.com', 'active'),\
    ('example10@example.com', 'inactive'),\
    ('example11@example.com', 'active'),\
    ('example12@example.com', 'inactive'),\
    ('example13@example.com', 'active'),\
    ('example14@example.com', 'inactive'),\
    ('example15@example.com', 'active'),\
    ('example16@example.com', 'inactive'),\
    ('example17@example.com', 'active'),\
    ('example18@example.com', 'inactive'),\
    ('example19@example.com', 'active'),\
    ('example20@example.com', 'inactive');
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

Feel free to use test-db data verification command after each curd operation on postgres db to verify the data replication.

Update the subscription status in postgres db using the following command:
```
docker-compose exec postgres bash -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -c \"UPDATE subscription SET status = 'active' WHERE email = 'example2@example.com';\""
```

Create a new record row in the db1:
```
docker-compose exec postgres bash -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -c \"INSERT INTO subscription (email, status) VALUES ('neuroai@x.com', 'active'); UPDATE subscription SET status = 'active' WHERE email = 'example2@example.com';\""
```
delete a record from db1:
```
docker-compose exec postgres bash -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -c \"DELETE FROM subscription WHERE email = 'example5@example.com';\""
```
