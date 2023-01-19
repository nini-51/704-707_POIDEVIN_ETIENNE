#!/usr/bin/bash

function usage() {
  echo "
Usage :
  `basename $0` [-e <FILE>] [-h]

Options :
  -e      Define the env file to use.
          Defaults to 'env/package-demo'
  -h      Prints this help and exit
"
}

function parse_options()
{
  ENV_FILE=env/package-demo

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

    PACKAGE_ID=$(echo $ENV_FILE | cut -d/ -f2)
    NIC=wlan0
    SSID=DEMO
    WIFI_PWD=Password

    if [[ -d "/var/lib/lxc/$PACKAGE_ID" ]]; then
      echo "/var/lib/lxc/$PACKAGE_ID already exists!"
      exit 0
    fi

    source $ENV_FILE

    # Create new package based on package-base
    lxc-copy -n base-package -N $PACKAGE_ID

    # Configure wireless nic
    sed -i "s/Name=.*/Name=$NIC/" /var/lib/lxc/$PACKAGE_ID/rootfs/etc/systemd/network/wlan0.network
    mv /var/lib/lxc/$PACKAGE_ID/rootfs/etc/systemd/network/{wlan0,$NIC}.network

    # Configure wpa supplicant
    sed -i "s/MYSSID/$SSID/" /var/lib/lxc/$PACKAGE_ID/rootfs/etc/wpa_supplicant/wpa_supplicant.conf
    sed -i "s/Password/$WIFI_PWD/" /var/lib/lxc/$PACKAGE_ID/rootfs/etc/wpa_supplicant/wpa_supplicant.conf
    mv /var/lib/lxc/$PACKAGE_ID/rootfs/etc/wpa_supplicant/{wpa_supplicant,wpa_supplicant-$NIC}.conf

    # Configure cron tasks
    sed -i "s/wlan0/$NIC/g" /var/lib/lxc/$PACKAGE_ID/rootfs/srv/scripts/wake-up.sh
    sed -i "s/packageid/$PACKAGE_ID/g" /var/lib/lxc/$PACKAGE_ID/rootfs/srv/scripts/wake-up.sh

    # Start container
    lxc-start -n $PACKAGE_ID
    lxc-wait -n $PACKAGE_ID -s RUNNING

    # Move nic info container
    PHYS=$(iw dev | grep -B1  $NIC | head -n1 | sed 's/#//')
    PID=$(lxc-info -n $PACKAGE_ID | grep PID | grep -Po '[0-9]+$')
    iw phy $PHYS set netns $PID

    sleep 3

    lxc-attach -n $PACKAGE_ID -- /usr/bin/bash <<- EOF
    systemctl enable wpa_supplicant@$NIC.service
    systemctl restart systemd-networkd.service
    systemctl restart wpa_supplicant@$NIC.service
EOF

    sleep 10

    DNS=$(lxc-attach -n $PACKAGE_ID -- /usr/bin/resolvectl dns | grep -o 'fd.*')
    mv /var/lib/lxc/$PACKAGE_ID/rootfs/etc/resolv.{conf,conf.old}
    echo "nameserver $DNS" | tee /var/lib/lxc/$PACKAGE_ID/rootfs/etc/resolv.conf

    lxc-attach -n $PACKAGE_ID -- /usr/bin/python3 /srv/app/main.py $PACKAGE_ID init

    exit 0
}

main "$@"
