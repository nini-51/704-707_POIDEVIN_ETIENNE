# Projet RT0704 / RT0707 : Suivi de livraison

Soon

## Datacenter section

Soon

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

Soon

![https://www.rabbitmq.com/getstarted.html]()

### TODO

- [ ] Auth backend (in rabbitmq)
- [ ] Reliability (ack)
- [ ] Auth backend
- [ ] Auth backend
- [ ] Auth backend
