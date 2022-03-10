#/bin/bash

_RED="$(tput -T xterm setaf 1)"
_GREEN="$(tput -T xterm setaf 2)"
_NORMAL="$(tput -T xterm sgr0)"

function info {
    echo "${_GREEN}${*}${_NORMAL}"
}

function error {
    echo "${_RED}${*}${_NORMAL}"
}

function fail {
    error "$1"
    exit 1
}

WEBSITE_DIR="${WEBSITE_DIR:=$(dirname $0)}"
DJANGO_LOGGING_ROOT="${DJANGO_LOGGING_ROOT:=${WEBSITE_DIR}}"
export DJANGO_LOGGING_ROOT

info "Working under directory $WEBSITE_DIR"
cd "$WEBSITE_DIR" || fail "Could not open working directory."

npm rebuild node-sass
npm run build
npm install
python3 manage.py collectstatic
python3 manage.py runserver 8080 &

trap "kill $(jobs -p)" EXIT

/docker-entrypoint.sh
nginx -g "daemon off;"

wait
