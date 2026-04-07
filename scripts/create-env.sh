#!/usr/bin/env bash

set -euo pipefail

workspace_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
template_path="$workspace_root/.env.example"
target_path="$workspace_root/.env"

frontend_port="${FRONTEND_PORT:-3000}"
backend_port="${BACKEND_PORT:-3001}"

if [[ -n "${CODESPACE_NAME:-}" && -n "${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-}" ]]; then
  frontend_url="https://${CODESPACE_NAME}-${frontend_port}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
  backend_url="https://${CODESPACE_NAME}-${backend_port}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
else
  frontend_url="http://localhost:${frontend_port}"
  backend_url="http://localhost:${backend_port}"
fi

if [[ ! -f "$target_path" ]]; then
  cp "$template_path" "$target_path"
fi

upsert_env_value() {
  local key="$1"
  local value="$2"

  if grep -q "^${key}=" "$target_path"; then
    sed -i "s|^${key}=.*$|${key}=${value}|" "$target_path"
  else
    printf '%s=%s\n' "$key" "$value" >> "$target_path"
  fi
}

upsert_env_value "BACKEND_URL" "$backend_url"
upsert_env_value "FRONTEND_URL" "$frontend_url"
upsert_env_value "CORS_ORIGINS" "$frontend_url"
upsert_env_value "REACT_APP_FRONTEND_URL" "$frontend_url"
upsert_env_value "REACT_APP_BACKEND_URL" "$backend_url"
upsert_env_value "REACT_APP_API_URL" "${backend_url}/api"