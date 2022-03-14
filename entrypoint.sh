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
DATABASE_ROOT_DIR="${DATABASE_ROOT_DIR:=${WEBSITE_DIR}}"
export DJANGO_LOGGING_ROOT
export DATABASE_ROOT_DIR

info "Working under directory $WEBSITE_DIR"
cd "$WEBSITE_DIR" || fail "Could not open working directory."

# Generate deploy-specific config
SETTINGS_FILE="kmsuj_website/generated_settings.py"

echo "CSRF_COOKIE_SECURE = True" >> "$SETTINGS_FILE" 
echo "DEBUG = False" >> "$SETTINGS_FILE"
echo "SESSION_COOKIE_SECURE = True" >> "$SETTINGS_FILE"
echo "SECURE_SSL_REDIRECTS = True" >> "$SETTINGS_FILE"

echo "Generated config file at $SETTINGS_FILE"
cat "$SETTINGS_FILE"

npm rebuild node-sass
npm install
npm run build

python3 manage.py collectstatic
python3 manage.py migrate

echo "Running some additional configurations..."
python3 manage.py shell -c 'from create_admin import *'

echo "Last checks whether everything looks ok"
python3 manage.py check --deploy

python3 manage.py runserver 8080 &

trap "kill $(jobs -p)" EXIT

/docker-entrypoint.sh
nginx -g "daemon off;"

wait
