# Projet RT0704 / RT0707 : Suivi de livraison

Ce projet vise à fournir un suivi multi-niveau pour les livraisons d'un vendeur en ligne.

Le premier niveau sera suivi grâce à un objet connecté embarqué dans chaque colis, tandis que le second niveau utilisera une application mobile pour suivre la livraison par le livreur.

Les données seront collectées via des signaux de présence, des mises à jour régulières de la position et seront archivées à la livraison.

Les clients pourront suivre leur colis à l'aide d'une application WEB.

## Datacenter section

Soon

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

Source : [https://docs.docker.com/engine/install/debian/]()

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
# launch datacenter services
cd datacenter
docker compose up -d
```

### TODO

- [ ] Error handling on beaver when rabbitmq is unavailable (no crash)
- [ ] Managing http return codes in amqp-bridge
- [ ] Added management of lost packages
- [ ] Clean code and comment it

## Warehouses section

Soon

```bash
# Install make tool
apt install -y make

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

- [The Paho Python Client](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [mac80211_hwsim - software simulator of 802.11 radio(s) for mac80211](https://www.kernel.org/doc/html/latest/networking/mac80211_hwsim/mac80211_hwsim.html)

### TODO

- [ ] Error handling on mqtt-bridge when API is unavailable (no crash)
- [ ] Clean code and comment it

## Delivery section

Soon

NB : La partie `delivery` doit au moins être sur le même hôte que la partie `warehouses` afin de pouvoir accéder aux colis.

```bash
# Install docker (cf. datacenter section)
apt-get install -y docker-ce docker-ce-cli containerd.io

# Add a new deliveryman on rabbitmq
docker exec datacenter-rabbit-1 rabbitmqctl add_user 'john' 'secret'
docker exec datacenter-rabbit-1 rabbitmqctl set_permissions -p '/' 'john' '' '^(amq\.gen.*|amq\.default)$' ''

# Copy rabbitmq ca certificate from datacenter
mkdir -p /etc/ssl/rabbitmq
vim /etc/ssl/rabbitmq/ca.crt

# Launch new deliveryman
#  -u      Define the username of the deliveryman.
#  -p      Define the password of the deliveryman.
#  -w      Define the warehouse from which the deliveryman leaves.
#  -s      Define the AMQP server to use. (datacenter section)
cd delivery
./new-delivery.sh -u john -p secret -w deliv1 -s amqp-broker.yousk.fr
```

- [Pika is a pure-Python implementation of the AMQP 0-9-1 protocol](https://pika.readthedocs.io/en/stable/)
- [The GraphHopper Directions API](https://graphhopper.com/maps/?profile=small_truck&layer=OpenStreetMap)

### TODO

- [ ] Reliability check (ack) in case of loss of connection
