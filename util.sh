#!/usr/bin/env bash
set -ue

APP_FOLDER=~/.onionssh
CLIENT_FOLDER=$APP_FOLDER/client
SERVER_FOLDER=$APP_FOLDER/server


function _create_keys {
    # Generate ED25519 key pair to folder
    # $1 - Path to folder

    #TODO dont safe if folder is not empty
    local name
    name=$(_random_name)
    ssh-keygen -N "" -C "" -t ed25519 -f "$1/$name" >&2
    echo "$name"
}


function _random_name {
    # print 16 - 32bit random string

    # TODO error handling
    local name
    name=$(python -c "import secrets; print(secrets.token_hex(16 + secrets.randbelow(17)))")
    echo "$name"
}

function _burn {
    # Delete key folders if no path is given
    # $1 - Path to folder to be deleted

    #TODO add secure deleting
    if [ "$#" -gt 0 ]; then
        echo "Burning key folder ($1)"
        _log_cmd rm -rf "$1"
    else
        echo "Burning key folders ($CLIENT_FOLDER, $SERVER_FOLDER)"
        _log_cmd rm -rf $CLIENT_FOLDER
        _log_cmd rm -rf $SERVER_FOLDER
    fi
}

function _stderr {
    echo "${*}" 2>&1
}

function _log_cmd {
    _stderr "$ ${*}"
    eval "${*}"
}

function _err {
    _stderr "Error: $*"
}

function _err_exit {

    if [ "$#" -gt 1 ]; then
        _err "$1"
        $2
    fi

    if [ "$#" -eq 1 ]; then
        _err "$1"
    fi

    if [ "$#" -eq 0 ]; then
        _err "Something went wrong."
    fi

    exit 1
}
