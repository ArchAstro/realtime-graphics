#!/usr/bin/env bash
# One entrypoint: rebuild prompt pages, then serve the site.
#   npm run dev
#   npm run dev -- 3000
#   npm run dev -- --no-open

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PORT="${PORT:-8000}"
OPEN_BROWSER=1

for arg in "$@"; do
  case "$arg" in
    --no-open) OPEN_BROWSER=0 ;;
    --help|-h)
      cat <<'EOF'
Usage: npm run dev [-- port] [-- --no-open]

  1. Rebuilds prompts/*/index.html from markdown
  2. Serves the repo at http://127.0.0.1:<port>/
  3. Opens the browser (unless --no-open)

Examples:
  npm run dev
  npm run dev -- 3000
  npm run dev -- --no-open
  PORT=9000 npm run dev
EOF
      exit 0
      ;;
    *)
      if [[ "$arg" =~ ^[0-9]+$ ]]; then
        PORT="$arg"
      else
        echo "Unknown argument: $arg (try --help)" >&2
        exit 1
      fi
      ;;
  esac
done

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "error: python3 is required" >&2
  exit 1
fi

echo "→ building prompt pages…"
"$PY" "$ROOT/scripts/build-prompt-pages.py"

# Free the port if something stale is listening (only our prior servers)
if command -v lsof >/dev/null 2>&1; then
  if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "→ port $PORT busy; trying $((PORT + 1))"
    PORT=$((PORT + 1))
  fi
fi

URL="http://127.0.0.1:${PORT}/"

echo
echo "Realtime Graphics Prompts"
echo "  url     $URL"
echo "  demos   ${URL}techniques/demos/"
echo "  prompts ${URL}prompts/"
echo "  stop    Ctrl+C"
echo

open_url() {
  [[ "$OPEN_BROWSER" == "1" ]] || return 0
  if command -v open >/dev/null 2>&1; then
    open "$1" >/dev/null 2>&1 || true
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$1" >/dev/null 2>&1 || true
  fi
}

( sleep 0.4; open_url "$URL" ) &

exec "$PY" -m http.server "$PORT" --bind 127.0.0.1
