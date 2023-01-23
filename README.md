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

# ...
...
```

Source : [https://docs.docker.com/engine/install/debian/]()

### TODO

- [ ] ...

## Warehouses section

```bash
# Install make tool
apt install -y make

# Ensure that scripts are executable
chmod u+x warehouses/scripts/*

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
# Ensure that scripts are executable
chmod u+x delivery/new-delivery.sh

# Launch new deliveryman
cd delivery
./new-delivery.sh -i john -w deliv1 -s amqp-broker.yousk.fr
```

- [https://www.rabbitmq.com/getstarted.html]()
- [https://graphhopper.com/maps/?profile=small_truck&layer=OpenStreetMap]()

### TODO

- [ ] Auth backend (in rabbitmq)
- [ ] TLS connection
- [ ] Reliability (ack)
