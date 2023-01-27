#!/usr/bin/bash

name='base-warehouse'
codename='bullseye'
arch='amd64'

src_path='src/warehouse'
dns_resolver='195.221.20.53'

if [[ -d "/var/lib/lxc/$name" ]]; then
	echo "/var/lib/lxc/$name already exists!"
	exit 0
fi

# Create lxc container
lxc-create -t download -n $name -- -d debian -r $codename -a $arch

# Config lxc container for Docker
cat << EOF >> /var/lib/lxc/$name/config

lxc.apparmor.profile = generated
lxc.apparmor.allow_nesting = 1
EOF

# DNS config
sed -i 's/#DNS=.*/DNS=9.9.9.9/' /var/lib/lxc/$name/rootfs/etc/systemd/resolved.conf

# Start container
lxc-start -n $name

# Wait container is up
lxc-wait -n $name -s RUNNING
# Wait dns is up
lxc-attach -n $name -- /usr/bin/bash -c 'while ! ping -c 1 -n -w 1 deb.debian.org &> /dev/null ; do sleep 3; done'

# Update packages
lxc-attach -n $name -- /usr/bin/bash << EOF
/usr/bin/apt-get update -q=2
/usr/bin/apt-get upgrade -q=2
EOF

# Docker
lxc-attach -n $name -- /usr/bin/bash << EOF
apt-get install -q=2 ca-certificates curl gnupg
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$arch signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $codename stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -q=2
apt-get -q=2 install docker-ce docker-ce-cli containerd.io docker-compose-plugin
EOF

# Services for DNS resolving and 802.11 AP features
lxc-attach -n $name -- /usr/bin/bash << EOF
apt-get -q=2 install hostapd radvd bind9
EOF

# Create wireless nic config
cat << EOF > /var/lib/lxc/$name/rootfs/etc/systemd/network/wlan0.network
[Match]
Name=wlan0

[Network]
IPv6AcceptRA=false
Address=2001:db8:1:0::1/64
EOF

# Create hostapd config
cat << EOF > /var/lib/lxc/$name/rootfs/etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
country_code=FR
ssid=YourWiFiName
channel=0
hw_mode=b
wpa=3
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
wpa_passphrase=Somepassphrase
auth_algs=3
beacon_int=100
EOF

# Create radvd config
cat << EOF > /var/lib/lxc/$name/rootfs/etc/radvd.conf
interface wlan0
{
	AdvSendAdvert on;
	MinRtrAdvInterval 30;
	MaxRtrAdvInterval 100;
	AdvHomeAgentFlag off;

	prefix 2001:db8:1:0::/64
	{
		AdvOnLink on;
		AdvAutonomous on;
		AdvRouterAddr off;
	};

  RDNSS 2001:db8::1
  {
    AdvRDNSSLifetime 100;
  };

  DNSSL warehouse.local
  {
    AdvDNSSLLifetime 100;
  };
};
EOF

# Create bind9 config
cat << EOF > /var/lib/lxc/$name/rootfs/etc/bind/named.conf.options
options {
	directory "/var/cache/bind";

	forward only;
	forwarders {
	 	$dns_resolver;
	};

	//========================================================================
	// If BIND logs error messages about the root key being expired,
	// you will need to update your keys.  See https://www.isc.org/bind-keys
	//========================================================================
	dnssec-validation auto;

        listen-on-v6 { ::1; 2001:db8:1:0::1; };
        listen-on { none; };

};
EOF

cat << EOF >> /var/lib/lxc/$name/rootfs/etc/bind/named.conf.local
zone "warehouse.local" {
	type primary;
	file "/etc/bind/warehouse.local.db";
};
EOF

cat << 'EOF' > /var/lib/lxc/$name/rootfs/etc/bind/warehouse.local.db
; base zone file for warehouse.local
$TTL 3h
$ORIGIN warehouse.local.
@         IN      SOA   ns1.warehouse.local. hostmaster.warehouse.local. (
                                2023011800 ; serial number
                                12h        ; refresh
                                6h        ; update retry
                                1w         ; expiry
                                3h         ; minimum
                                )

           IN      NS      ns1.warehouse.local.

ns1        IN      AAAA    2001:db8:1:0::1
mqtt       IN      AAAA    2001:db8:1:0::1
EOF

lxc-attach -n $name -- /usr/bin/bash << EOF
systemctl stop systemd-resolved
systemctl disable systemd-resolved

systemctl unmask hostapd.service
EOF

rm /var/lib/lxc/$name/rootfs/etc/resolv.conf
cat << EOF > /var/lib/lxc/$name/rootfs/etc/resolv.conf
nameserver ::1
nameserver $dns_resolver
EOF

# Setup app in /srv folder
rsync -av $src_path/ /var/lib/lxc/$name/rootfs/srv/

# Stop container
lxc-stop -n $name
