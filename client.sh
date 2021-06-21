#!/usr/bin/env bash
set -ue

function _check_deps {
    tor -h >/dev/null || _err_exit "Couldnt' detect tor" _burn
    python3 --version > /dev/null || _err_exit "Python3 not found" _burn
}


function _boostrap {
    _log_cmd mkdir -p "$APP_FOLDER"
    _burn "$CLIENT_FOLDER"
    _log_cmd mkdir -p "$CLIENT_FOLDER"
}

function _print_key {
    local key
    key=$(cat "$CLIENT_FOLDER/$1.pub") || _err_exit "Something went wrong no public key" _burn
    printf "Content of your Public Key File\n\n%s\n\n"\
           "Give this Key (over a secure channel) to your Server\n"\
           "and wait for onion service address." "$key"
}

function _connect {
    # TODO what about tails
    ssh -i "$CLIENT_FOLDER/$1" -F "$CLIENT_FOLDER/config" -o IdentitiesOnly=yes \
        -o "ProxyCommand nc -X 5 -x 127.0.0.1:9050 %h %p" "$2" -vvv \
        || _err_exit "ssh connection failed" _burn
}

function _ask_connect {
    echo "Do you want to connect to the server?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) _connect "$1" "$2" && break;;
            No ) _err_exit "User cancel" _burn;;
        esac
    done
}

function _ask_onion {
    # TODO regex onion address
    local address
    while true; do
        read -rp "Enter onion service address:" address
        break;
    done
    echo "$address"
}

source ./util.sh

_check_deps
_boostrap
key=$(_create_keys "$CLIENT_FOLDER")
_print_key "$key"
 _ask_connect
address=$(_ask_onion)
_connect "$key" "$address"

