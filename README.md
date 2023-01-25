# Projet RT0704 / RT0707 : Suivi de livraison

Soon

## Datacenter section

```bash
# Install docker
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

```bash
# Generate pki (for AMQP broker)
apt-get install -y openssl
mkdir /etc/ssl/rabbitmq
cd /etc/ssl/rabbitmq

# Creating CA
openssl genrsa -out ca.key 2048
openssl req -x509 -sha256 -new -nodes -days 3650 \
  -key ca.key \
  -out ca.crt

# Creating server certificate
openssl genrsa -out server.key 2048
chmod 644 /etc/ssl/rabbitmq/server.key
openssl req -newkey rsa:2048 -nodes -days 3650 \
   -keyout server.key \
   -out server.csr
openssl x509 -req -days 3650 -set_serial 01 \
   -in server.csr \
   -out server.crt \
   -CA ca.crt \
   -CAkey ca.key
```

```bash
# ...
...
```

Source : [https://docs.docker.com/engine/install/debian/]()

- [https://sqlite-utils.datasette.io/en/stable/python-api.html]()

### TODO

- [ ] ...

## Warehouses section

```bash
# Install make tool
apt install -y make

# Ensure that scripts are executable
chmod u+x warehouses/scripts/*

# Change the API_SERVER variable to the FQDN of the API server (datacenter section)
vim warehouses/src/warehouse/docker-compose.yml

# Build warehouses infra
cd warehouses
make -j3 build-infra

# Create the packages two by two (-j2)
make -j2 init-packages

# Clear instance
make mrproper
```

### TODO

- [ ] Clean msg send by pacakges to mqtt broker
- [ ] Define warehouse id in its app via docker env var in docker-compose.yml
- [ ] Define fqdn of REST API in warehouse app (require to finish dc infra)
- [ ] QoS management (package - broker - bridge)
- [ ] Delete unnecessary files (.old files)
- [ ] Clean code and comment it
- [ ] Improve README and docs

## Delivery section

```bash
# Add a new deliveryman on rabbitmq
docker exec -ti datacenter-rabbit-1 rabbitmqctl add_user 'john' 'secret'
docker exec -ti datacenter-rabbit-1 rabbitmqctl set_permissions -p '/' 'john' '' '^(amq\.gen.*|amq\.default)$' ''

# Ensure that scripts are executable
chmod u+x delivery/new-delivery.sh

# Launch new deliveryman
#  -i      Define the id of the deliveryman.
#  -p      Define the password of the deliveryman.
#  -w      Define the warehouse from which the deliveryman leaves.
#  -s      Define the AMQP server to use. (datacenter section)
cd delivery
./new-delivery.sh -i john -p secret -w deliv1 -s amqp-broker.yousk.fr
```

- [https://www.rabbitmq.com/getstarted.html]()
- [https://graphhopper.com/maps/?profile=small_truck&layer=OpenStreetMap]()

### TODO

- [x] Auth backend (in rabbitmq)
- [x] TLS connection
- [ ] Reliability (ack) > verif on connection lost
- [ ] Improve README and docs
