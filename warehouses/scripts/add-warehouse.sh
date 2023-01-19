#!/usr/bin/bash

function usage() {
  echo "
Usage :
  `basename $0` [-e <FILE>] [-h]

Options :
  -e      Define the env file to use.
          Defaults to 'env/warehouse-demo'
  -h      Prints this help and exit
"
}

function parse_options()
{
  ENV_FILE=env/warehouse-demo

  while getopts ":he:" option; do
        case $option in
            e)
                ENV_FILE=$OPTARG
                ;;
            h)
                usage
                exit 0
                ;;
            :)
                usage
                exit 1
                ;;
            \?)
                usage
                exit 1
                ;;
        esac
    done
}

function main()
{
    parse_options "$@"

    WAREHOUSE_ID=$(echo $ENV_FILE | cut -d/ -f2)
    SSID=DEMO
    NIC=wlan0

    if [[ -d "/var/lib/lxc/$WAREHOUSE_ID" ]]; then
      echo "/var/lib/lxc/$WAREHOUSE_ID already exists!"
      exit 0
    fi

    source $ENV_FILE

    # Create new warehouse based on warehouse-base
    lxc-copy -n base-warehouse -N $WAREHOUSE_ID

    # Configure radvd
    sed -i "s/interface wlan0/interface $NIC/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/radvd.conf
    sed -i "s/2001:db8:1:0::/$LAN/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/radvd.conf
    sed -i "s/2001:db8::/$LAN/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/radvd.conf

    # Configure hostapd
    sed -i "s/interface=.*/interface=$NIC/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/hostapd/hostapd.conf
    sed -i "s/YourWiFiName/$SSID/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/hostapd/hostapd.conf
    sed -i "s/Somepassphrase/$WIFI_PWD/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/hostapd/hostapd.conf

    # Configure bind9
    sed -i "s/2001:db8:1:0::/$LAN/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/bind/named.conf.options
    sed -i "s/2001:db8:1:0::/$LAN/g" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/bind/warehouse.local.db

    # Configure wireless nic
    sed -i "s/Name=.*/Name=$NIC/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/systemd/network/wlan0.network
    sed -i "s/2001:db8:1:0::/$LAN/" /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/systemd/network/wlan0.network
    mv /var/lib/lxc/$WAREHOUSE_ID/rootfs/etc/systemd/network/{wlan0,$NIC}.network

    # Start container
    lxc-start -n $WAREHOUSE_ID
    lxc-wait -n $WAREHOUSE_ID -s RUNNING

    # Move nic into lxc container
    PHYS=$(iw dev | grep -B1  $NIC | head -n1 | sed 's/#//')
    PID=$(lxc-info -n $WAREHOUSE_ID | grep PID | grep -Po '[0-9]+$')
    iw phy $PHYS set netns $PID

    exit 0
}

main "$@"
