#!/usr/bin/env bash
# Copy pogoscan to the Raspberry Pi. Usage: ./deploy.sh [pi@host]
set -euo pipefail
TARGET="${1:-pi@10.16.226.244}"
cd "$(dirname "$0")"
rsync -a --delete --exclude data --exclude __pycache__ --exclude .pytest_cache --exclude '*.pyc' ./ "$TARGET:~/pogoscan/"
echo "deployed to $TARGET:~/pogoscan"
if [ "${2:-}" = "--service" ]; then
  # first-time install of the systemd unit; afterwards a plain deploy + restart is enough
  ssh -t "$TARGET" 'sudo install -m 644 ~/pogoscan/pogoscan.service /etc/systemd/system/pogoscan.service && sudo systemctl daemon-reload && sudo systemctl enable --now pogoscan'
else
  ssh "$TARGET" 'systemctl is-enabled pogoscan >/dev/null 2>&1 && sudo -n systemctl restart pogoscan 2>/dev/null && echo "service restarted" || true'
fi
echo "check wiring : ssh $TARGET 'cd ~/pogoscan && sudo systemctl stop pogoscan && python3 -m pogoscan.check; sudo systemctl start pogoscan'"
echo "service      : ssh $TARGET 'systemctl status pogoscan'   (logs: journalctl -u pogoscan -f)"
echo "simulate     : ssh $TARGET 'cd ~/pogoscan && sudo systemctl stop pogoscan && python3 -m pogoscan.server --simulate'"
echo "then open    : http://${TARGET#*@}:8080/"
