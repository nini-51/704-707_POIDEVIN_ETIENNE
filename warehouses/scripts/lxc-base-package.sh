#!/usr/bin/bash

name='base-package'
codename='bullseye'
arch='amd64'

packages_path='src/package'

if [[ -d "/var/lib/lxc/$name" ]]; then
	echo "/var/lib/lxc/$name already exists!"
	exit 0
fi

# Create lxc container
lxc-create -t download -n $name -- -d debian -r $codename -a $arch

# DNS config
sed -i 's/#DNS=.*/DNS=9.9.9.9/' /var/lib/lxc/$name/rootfs/etc/systemd/resolved.conf

# Start container
lxc-start -n $name

# Wait container is up
lxc-wait -n $name -s RUNNING
# Wait systemd-resolved.service is up
lxc-attach -n $name -- /usr/bin/bash -c 'while ! ping -c 1 -n -w 1 gentoo.org &> /dev/null ; do sleep 1; done'

# Update packages
lxc-attach -n $name -- /usr/bin/bash << EOF
/usr/bin/apt-get update -q=2
/usr/bin/apt-get upgrade -q=2
EOF

# Services for 802.11 client and sleeping features
lxc-attach -n $name -- /usr/bin/bash << EOF
apt-get -q=2 install wpasupplicant cron
EOF

# Python
lxc-attach -n $name -- /usr/bin/bash << EOF
apt-get -q=2 install python3 python3-pip
EOF

# Setup app in /srv folder of lxc container
rsync -av $packages_path/ /var/lib/lxc/$name/rootfs/srv/
lxc-attach -n $name -- /usr/bin/bash << EOF
pip3 install --no-cache-dir --upgrade -r /srv/requirements.txt
EOF

# Reset DNS config
sed -i 's/DNS=.*/#DNS=/' /var/lib/lxc/$name/rootfs/etc/systemd/resolved.conf

# Create wireless nic config
cat << EOF > /var/lib/lxc/$name/rootfs/etc/systemd/network/wlan0.network
[Match]
Name=wlan0

[Network]
IPv6AcceptRA=true

[IPv6AcceptRA]
UseDNS=yes
EOF

# Create wpa_supplicant config
cat << EOF > /var/lib/lxc/$name/rootfs/etc/wpa_supplicant/wpa_supplicant.conf
# AP scanning
# ap_scan=1

# ISO/IEC alpha2 country code in which the device is operating
country=FR

# network section generated by wpa_passphrase
network={
	ssid="MYSSID"
	key_mgmt=WPA-PSK
	psk="Password"
}
EOF

# Create wake up script
mkdir /var/lib/lxc/$name/rootfs/srv/scripts
cat << 'EOF' > /var/lib/lxc/$name/rootfs/srv/scripts/wake-up.sh
#!/usr/bin/bash
function main()
{
	/usr/bin/systemctl restart wpa_supplicant@wlan0
	sleep 15
	if [[ $(ip -6 -o a | grep fd) ]]
	then
		update-dns
		/usr/bin/python3 /srv/app/main.py packageid update
	fi
	/usr/bin/systemctl stop wpa_supplicant@wlan0
}

function update-dns()
{
	DNS=$(/usr/bin/resolvectl dns wlan0 | grep -o 'fd.*')
	echo "nameserver $DNS" > /etc/resolv.conf
	sleep 5
}

main
EOF
chmod u+x /var/lib/lxc/$name/rootfs/srv/scripts/wake-up.sh

# Create crontab task
cat << EOF > /var/lib/lxc/$name/rootfs/var/spool/cron/crontabs/root
# m h  dom mon dow   command
*/5 * * * * /srv/scripts/wake-up.sh
EOF
chown root:crontab /var/lib/lxc/$name/rootfs/var/spool/cron/crontabs/root
chmod 600 /var/lib/lxc/$name/rootfs/var/spool/cron/crontabs/root

# Stop container
lxc-stop -n $name

# Delete nic info
sed -i "s/lxc.net.*//" /var/lib/lxc/$name/config