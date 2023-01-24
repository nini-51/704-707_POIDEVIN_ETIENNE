#!/usr/bin/bash

function usage() {
  echo "
Usage :
  `basename $0` [-e <FILE>] [-h]

Options :
  -i      Define the id of the deliveryman.
          Defaults to 'demo'
  -w      Define the warehouse from which the deliveryman leaves.
          Defaults to 'demo'
  -s      Define the AMQP server to use. Don't use 'localhost' or '127.0.0.1' address.
          Defaults to 'amqp-broker.datacenter.local'
  -h      Prints this help and exit
"
}

function parse_options()
{
  DELIVERY_ID=demo
  WAREHOUSE=demo
  AMQP_SERVER=amqp-broker.datacenter.local

  while getopts ":hi:w:s:" option; do
        case $option in
            i)
                DELIVERY_ID=$OPTARG
                ;;
            w)
                WAREHOUSE=$OPTARG
                ;;
            s)
                AMQP_SERVER=$OPTARG
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

# List packages in the seleted warehouse
function fetch-packages() {
  list=()
  for package in $(lxc-ls | grep -o 'package-.*'); do
    if [[ $(grep -P "ssid=.${WAREHOUSE^^}." /var/lib/lxc/$package/rootfs/etc/wpa_supplicant/wpa_supplicant-*.conf) ]]; then
      list+=($package)
    fi
  done
  echo ${list[@]}
}

# Delete package's container
function prepare-packages() {
  prepared=()
  while read line; do
    for package in $line; do
      package_id=$(echo $package | cut -d'-' -f2)
      # lxc-stop -n $package
      # lxc-destroy -n $package
      prepared+=(${package_id^^})
    done
  done < /dev/stdin
  echo ${prepared[@]}
}

# Select random track
function select-track() {
  tracks=(`ls app/tracks/`)
  index=$(($RANDOM % ${#tracks[@]}))
  echo ${tracks[$index]}
}

# Create new deliveryman
function launch-delivery() {
  docker container run --rm --env AMQP_SERVER=$AMQP_SERVER --env DELIVERY_ID=${DELIVERY_ID^^} --env TRACK=$(select-track) deliveryman $(fetch-packages | prepare-packages)
}

function main()
{
  parse_options "$@"

  # check if the docker image already exists
  if ! [[ $(docker image list -q deliveryman) ]]; then
    docker image build -t deliveryman:latest .
  fi

  # launch deliveryman container
  launch-delivery

  exit 0
}

main "$@"
