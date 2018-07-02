
TMP_DIR="/mnt/tmp-m"
S3_DIR="s3://praveenvunnava/code_dir"
KAFKA_HOME="/home/hadoop/kafka"

sudo mkdir -p $TMP_DIR
sudo chown -R hadoop:hadoop $TMP_DIR
sudo chmod -R 777 $TMP_DIR

# Check if master and download code. Install requirements on all nodes in the cluster

IS_MASTER=false
if [ -f /mnt/var/lib/info/instance.json ]
then
	IS_MASTER=`cat /mnt/var/lib/info/instance.json | grep isMaster | awk -F':' '{print $2}'`
fi
if [ "$IS_MASTER" = "false" ]
then
    sudo apt-get install python-pip
    aws s3 cp "$S3_DIR/requirements.txt" "$TMP_DIR/requirements.txt"
    sudo pip install -r "$TMP_DIR/requirements.txt"
    exit 0
fi

aws s3 cp "$S3_DIR/m.tar.gz" "$TMP_DIR/m.tar.gz"
cd $TMP_DIR; gunzip < m.tar.gz | tar xvf -

# Install mongo and restore a sample test db
aws s3 cp "$S3_DIR/mongodb-org-3.6.repo" "$TMP_DIR/mongodb-org-3.6.repo"
sudo cp "$TMP_DIR/mongodb-org-3.6.repo" /etc/yum.repos.d/
sudo yum install -y mongodb-org
aws s3 cp "$S3_DIR/emr-mongo.conf" "$TMP_DIR/mongodb.conf"
sudo cp "/etc/mongod.conf"  "$TMP_DIR/mongod_back.conf"
sudo cp "$TMP_DIR/mongodb.conf" /etc/mongod.conf
sudo mkdir -p /var/lib/mongodb; sudo chown -R mongod:mongod /var/lib/mongodb
sudo mkdir -p /var/log/mongodb/; sudo chown -R mongod:mongodb /var/log/mongodb
sudo service mongod start & # for some reason this command hogs the terminal and doesn't return
sleep 10 # this is to wait till mongo comes up

mongo  admin --eval "db.getSiblingDB('a_db').createUser( { user: 'a_user',pwd: 'a_user123',roles: [ { role: 'readWrite', db: 'a_db' } ]} );"
mongo  admin --eval "db.getSiblingDB('e_db').createUser( { user: 'e_user',pwd: 'e_user123',roles: [ { role: 'readWrite', db: 'e_db' } ]} );"


aws s3 cp "$S3_DIR/test-mongo-a.archive.gz" "$TMP_DIR/test-mongo-a-archive.gz"
aws s3 cp "$S3_DIR/test-mongo-e.archive.gz" "$TMP_DIR/test-mongo-e-archive.gz"

sudo mongorestore --host localhost --port 27017 --drop --gzip --archive=$TMP_DIR/test-mongo-a-archive.gz
sudo mongorestore --host localhost --port 27017 --drop --gzip --archive=$TMP_DIR/test-mongo-e-archive.gz

rm -rf "$TMP_DIR/test-mongo-a-archive.gz"
rm -rf "$TMP_DIR/test-mongo-e-archive.gz"



# Install neo and restore a sample test db

sudo rpm --import http://debian.neo4j.org/neotechnology.gpg.key
aws s3 cp "$S3_DIR/neo4j-repo" "$TMP_DIR/neo4j-repo"
sudo cp "$TMP_DIR/neo4j-repo" /etc/yum.repos.d/neo4j.repo
sudo yum install -y "neo4j-3.3.1"
sudo chown -R neo4j /var/log/neo4j
sudo chown -R neo4j /var/lib/neo4j/
aws s3 cp "$S3_DIR/emr-neo.conf" "$TMP_DIR/neo4j.conf" ; sudo cp "$TMP_DIR/neo4j.conf" /etc/neo4j/neo4j.conf
sudo service neo4j start

# Install redis

cd $TMP_DIR; wget http://download.redis.io/releases/redis-4.0.10.tar.gz;  tar xzf redis-4.0.10.tar.gz; cd redis-4.0.10; make
$TMP_DIR/redis-4.0.10/src/redis-server

#
# Create kafka topics

$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181  --topic mInput --replication-factor 1 --partitions 2
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181  --topic mOutput --replication-factor 1 --partitions 2
