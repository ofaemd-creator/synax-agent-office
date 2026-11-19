#!/usr/bin/env bash
set -euo pipefail
echo "=================================================================="
echo "  SYNAX-OMNI v6.0 & 3D Pixar-Tycoon Agent Office — Desktop Setup"
echo "  (ReAct + NCBI PubMed + Groq LPU + Claude Artifacts Desktop App)"
echo "=================================================================="
INSTALL_DIR="$HOME/.synax-desktop"
rm -rf "$INSTALL_DIR"
git clone --depth 1 https://github.com/ofaemd-creator/synax-agent-office.git "$INSTALL_DIR"

if [ "$(uname -s)" = "Darwin" ]; then
  if [ -f "$INSTALL_DIR/SYNAX-Desktop-macOS-v4.0.0.zip" ]; then
    unzip -qo "$INSTALL_DIR/SYNAX-Desktop-macOS-v4.0.0.zip" -d /Applications/ 2>/dev/null || true
    unzip -qo "$INSTALL_DIR/SYNAX-Desktop-macOS-v4.0.0.zip" -d "$HOME/Desktop/" 2>/dev/null || true
    echo "✓ SYNAX Studio.app /Applications ve Masaüstünüze eklendi!"
  fi
fi

python3 "$INSTALL_DIR/src/synax/office_mcp_server.py" --install-integrations 2>/dev/null || true
lsof -ti :8795 | xargs kill -9 2>/dev/null || true
nohup python3 "$INSTALL_DIR/src/synax/agent_office.py" --serve --port 8795 >/tmp/synax_desktop.log 2>&1 &
sleep 2
open "http://127.0.0.1:8795" 2>/dev/null || xdg-open "http://127.0.0.1:8795" 2>/dev/null || true
echo "🎉 SYNAX-OMNI v6.0 bilgisayarınızda çalışıyor: http://127.0.0.1:8795 !"
