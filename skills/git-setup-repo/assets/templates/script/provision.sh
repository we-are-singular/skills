#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
COMPOSE_FILE="$ROOT_DIR/ops/docker-compose.yml"
COMPOSE_PROJECT="__PROJECT_SLUG__-dev"

compose() {
  docker compose -f "$COMPOSE_FILE" -p "$COMPOSE_PROJECT" "$@"
}

require_cli() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required CLI: $1" >&2
    exit 1
  fi
}

retry() {
  label="$1"
  shift
  attempts=1

  echo "- $label"
  while [ "$attempts" -le 5 ]; do
    if "$@"; then
      return 0
    fi

    if [ "$attempts" -eq 5 ]; then
      break
    fi

    attempts=$((attempts + 1))
    sleep 5
  done

  echo "Failed: $label" >&2
  return 1
}

up() {
  require_cli docker
  require_cli __PACKAGE_MANAGER__
  cd "$ROOT_DIR"

  # TODO(git-setup-repo): remove services the repository does not need.
  compose up -d db db-test redis

  retry "Waiting for development database" compose exec -T db pg_isready -U root -d app
  retry "Waiting for test database" compose exec -T db-test pg_isready -U root -d app_test
  retry "Waiting for Redis" compose exec -T redis redis-cli ping

  # TODO(git-setup-repo): replace env names, ports, and migration scripts with the real contract.
  echo "- Migrating development database"
  env __DATABASE_URL_ENV__=postgres://root:pass@127.0.0.1:__POSTGRES_DEV_PORT__/app __PACKAGE_MANAGER__ run db:migrate
  echo "- Migrating test database"
  env __DATABASE_URL_ENV__=postgres://root:pass@127.0.0.1:__POSTGRES_TEST_PORT__/app_test __PACKAGE_MANAGER__ run db:migrate

  echo ""
  echo "Local services are ready."
  echo "Run '__PACKAGE_MANAGER__ run dev' to start development."
}

down() {
  compose down --remove-orphans
}

case "${1:-up}" in
  up)
    up
    ;;
  down)
    down
    ;;
  *)
    echo "Usage: script/provision.sh [up|down]" >&2
    exit 1
    ;;
esac
