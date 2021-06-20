#!/usr/bin/env bash

function _check_deps {
    tor -h >/dev/null || _err_exit "Couldnt' detect tor" _burn
    sshd --help 2>&1 | grep -qs OpenSSH || _err_exit "Couldn't detect OpenSSH daemon" _burn
    python3 --version > /dev/null || _err_exit "Python3 not found" _burn
}

function _boostrap {
    _log_cmd mkdir -p "$APP_FOLDER"
    _burn "$SERVER_FOLDER"
    _log_cmd mkdir -p "$SERVER_FOLDER"
}

function start_sshd {
    echo 1
}

source ./util.sh

_check_deps
_boostrap
key=$(_create_keys "$SERVER_FOLDER")

