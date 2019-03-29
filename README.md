# ECS781PMiniProject
# Cloud Computing Coursework
===============================

### Core functions of application:

- Find a player in the FUT Database by name.

- Find a specific page of players from the FUT API and simplify the data to only see relevant data.

- Find a specific set of players based on their rarity value.

- Find a specific player based on his rarity value

## Supported platforms
- Windows 8.x
- Linux

## Sample Usage

[Deployment](https://github.com/ec18339/ECS781PMiniProject#player-by-rarity-search)

[Player Search](https://github.com/ec18339/ECS781PMiniProject#player-search)

[Page Search](https://github.com/ec18339/ECS781PMiniProject#page-search)

[Rarity Search](https://github.com/ec18339/ECS781PMiniProject#rarity-search)

[Player by Rarity Search](https://github.com/ec18339/ECS781PMiniProject#player-by-rarity-search)



### Deployment

To deploy the app:

Set the project ID:
~~~
gcloud config set project MY_PROJECT_ID
~~~
Set the timezone and export the project ID to a variable for convenience.
~~~
gcloud config set compute/zone europe-west2-b
export PROJECT_ID="$(gcloud config get-value project -q)"
~~~

Firstly, you must pull the latest docker image:
~~~
docker pull cassandra:latest
~~~
Then run an instance of the Cassandra in the docker:
~~~
docker run --name cassandra-test -d cassandra:latest
~~~
Then create a 3 node cluster called 'cassandra'. Note that the Google container API must be enabled. 
This can be done within the console settings or by running:
~~~
gcloud services enable container.googleapis.com
gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"
~~~
Then the cassandra services must be downloaded:
~~~
wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy
wget -O cassandra-service.yml http://tinyurl.com/y65czz8e
wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8
~~~

And then run the downloaded services to form the ring.
~~~
kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml
~~~

Once the container is working, the nodes can be scaled up.
~~~
kubectl scale rc cassandra --replicas=3
~~~

Then create the requirements.txt file and the Dockerfile if it does not exist already.
The Dockerfile will look like this:
~~~
FROM python:3.7-alpine
WORKDIR /[working directory]
COPY /[working directory]
RUN pip install -U -r requirements.txt
EXPOSE 8080
CMD ["python", "MiniProject.py"]
~~~
And the requirements.txt file will look like this:
~~~
pip
Flask
requests
requests_cache
cassandra-driver
~~~

It may be required to create the Keyspace on the Cassandra node first. 
If so, the following lines of SQL are used inside CQLSH.

This command is to run CQLSH in a cassandra node.
~~~
kubectl exec -it cassandra-[node] cqlsh
~~~
And this is to create the Keyspace and the table.
~~~
DROP KEYSPACE IF EXISTS futplayers;
CREATE KEYSPACE futplayers WITH REPLICATION =
{'class' : 'SimpleStrategy', 'replication_factor' : 1}; 

CREATE TABLE IF NOT EXISTS futplayers.players
         (id INT PRIMARY KEY,
         firstName TEXT,
         lastName TEXT,
         commonName TEXT,
         pace INT,
         shooting INT,
         passing INT,
         dribbling INT,
         defence INT,
         physical INT,
         rarity INT);
~~~

The database can be tested with the [playersdb.csv](https://github.com/ec18339/ECS781PMiniProject/blob/master/playersdb.csv) file provided.
The following lines will copy the csv to the node, and will copy the contents into the table.
~~~
kubectl cp playersdb.csv cassandra-[node]:/playersdb.csv
COPY futplayers.players(id,firstName,lastName,commonName,pace,shooting,passing,dribbling,defence,physical,rarity) FROM '/playersdb.csv'
WITH DELIMITER=',' AND HEADER=TRUE;
~~~

Next, build the image and push it to the Google repository.
~~~
docker build -t gcr.io/${PROJECT_ID}/miniproject-app:v1 .
docker push gcr.io/${PROJECT_ID}/miniproject-app:v1
~~~


Then run the service and expose it to receive an external IP address.
~~~
kubectl run miniproject-app --image=gcr.io/${PROJECT_ID}/miniproject-app:v1 --port 8080
kubectl expose deployment miniproject-app --type=LoadBalancer --port 80 --target-port 8080
~~~

### Player Search

Search by passing the name through the url.

Example: /name/neymar

### Page Search

Search by passing a page number between 1 and 800 through the url.

Example: /page/1

### Rarity Search

Search by passing the name through the url.

Example: /rarity/1

### Player by Rarity Search

Search by passing the name through the url.

Example: /name/neymar/rarity/3

### Cleaning up:
~~~
kubectl delete --all replicationcontroller

kubectl delete --all services
kubectl delete deployment miniproject-app

gcloud container clusters delete cassandra
~~~


