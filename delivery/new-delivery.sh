#!/usr/bin/bash

function usage() {
  echo "
Usage :
  `basename $0` [-u <username>] [-p <password>] [-w <warehouse>] [-s <amqp_server>] [-h]

Options :
  -u      Define the username of the deliveryman.
          Defaults to 'demo'
  -p      Define the password of the deliveryman.
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
  DELIVER_ID=demo
  DELIVER_PWD=demo
  WAREHOUSE=demo
  AMQP_SERVER=amqp-broker.datacenter.local

  while getopts ":hu:p:w:s:" option; do
        case $option in
            u)
                DELIVER_ID=$OPTARG
                ;;
            p)
                DELIVER_PWD=$OPTARG
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
  for package in $(lxc-ls -1 | grep 'package-.*'); do
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
      lxc-stop -n $package
      lxc-destroy -n $package
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
  CA_CERT='/etc/ssl/rabbitmq/ca.crt'

  docker container run \
    --rm \
    --volume $CA_CERT:/etc/ssl/certs/ca.crt:ro \
    --env AMQP_SERVER=$AMQP_SERVER \
    --env DELIVER_ID=$DELIVER_ID \
    --env DELIVER_PWD=$DELIVER_PWD \
    --env TRACK=$(select-track) \
    deliveryman $(fetch-packages | prepare-packages)
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
