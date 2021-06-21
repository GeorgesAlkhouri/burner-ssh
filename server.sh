#!/usr/bin/env bash

SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")

SSHD=/etc/init.d/ssh

function _check_deps {
    tor -h >/dev/null || _err_exit "Couldnt' detect tor" _burn
    sshd --help 2>&1 | grep -qs OpenSSH || _err_exit "Couldn't detect OpenSSH daemon" _burn
    python3 --version > /dev/null || _err_exit "Python3 not found" _burn
}

function _boostrap {
    _log_cmd mkdir -p "$APP_FOLDER"
    _burn "$SERVER_FOLDER"
    _log_cmd mkdir -p "$SERVER_FOLDER"
    _log_cmd touch "$SERVER_FOLDER\authorized_keys"
}

function start_sshd {
    echo 1
}

source ./util.sh

_check_deps
_boostrap
key=$(_create_keys "$SERVER_FOLDER")

_log_cmd $SSHD stop
_log_cmd $SSHD start "\"-h $SERVER_FOLDER/$key -f $SCRIPT_PATH/sshd_config -o AuthorizedKeysFile=$SERVER_FOLDER\authorized_keys\""
echo $SCRIPT_PATH
