
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


#
# Create kafka topics

$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181  --topic mInput --replication-factor 1 --partitions 2
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181  --topic mOutput --replication-factor 1 --partitions 2
