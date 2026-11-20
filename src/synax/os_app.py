"""SYNAX-OS Sovereign Desktop Window Manager Application Server.

Serves an interactive multi-window OS desktop with:
- Window 1: Task Manager & Process Monitor (/proc/agents)
- Window 2: Interactive Terminal Shell (synax-sh)
- Window 3: 3D Pixar Agent Office Viewport
- Window 4: Super-LLM Canvas Workbench (KaTeX + PubMed)
- Window 5: Virtual Agent File System Explorer (VAFS)
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from synax.kernel.kernel import SynaxOSKernel
from synax.shell import SynaxShell


def get_desktop_html() -> str:
    """Generate the complete SYNAX-OS Desktop Window Manager HTML5 application."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SYNAX-OS Sovereign Agentic Operating System v6.1</title>
<style>
  :root {
    --bg-desktop: #0a0e17;
    --window-bg: rgba(16, 22, 36, 0.88);
    --window-border: rgba(99, 102, 241, 0.35);
    --accent: #6366f1;
    --accent-glow: rgba(99, 102, 241, 0.5);
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
    --dock-bg: rgba(15, 23, 42, 0.75);
    --font-mono: 'JetBrains Mono', 'Fira Code', Menlo, monospace;
    --font-ui: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background: var(--bg-desktop);
    background-image: 
      radial-gradient(circle at 15% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
      radial-gradient(circle at 85% 80%, rgba(168, 85, 247, 0.15) 0%, transparent 40%);
    color: var(--text-primary);
    font-family: var(--font-ui);
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  /* Top Menu Bar */
  #topbar {
    height: 32px;
    background: rgba(10, 14, 23, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    font-size: 13px;
    z-index: 1000;
  }
  .top-left { display: flex; align-items: center; gap: 16px; font-weight: 600; }
  .logo-badge { color: #818cf8; display: flex; align-items: center; gap: 6px; }
  .top-menu-item { color: var(--text-muted); cursor: pointer; transition: color 0.2s; }
  .top-menu-item:hover { color: #fff; }
  .top-right { display: flex; align-items: center; gap: 16px; color: var(--text-muted); font-size: 12px; font-family: var(--font-mono); }

  /* Desktop Workspace */
  #desktop {
    flex: 1;
    position: relative;
    overflow: hidden;
  }

  /* Draggable Windows */
  .window {
    position: absolute;
    background: var(--window-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--window-border);
    border-radius: 12px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5), 0 0 20px rgba(99, 102, 241, 0.15);
    display: flex;
    flex-direction: column;
    min-width: 320px;
    min-height: 220px;
    overflow: hidden;
    z-index: 10;
  }
  .window-header {
    height: 38px;
    background: rgba(255, 255, 255, 0.04);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    cursor: grab;
  }
  .window-title { font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
  .window-controls { display: flex; gap: 6px; }
  .win-btn {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    cursor: pointer;
  }
  .btn-close { background: #ef4444; }
  .btn-min { background: #f59e0b; }
  .btn-max { background: #10b981; }
  .window-body {
    flex: 1;
    overflow-y: auto;
    padding: 14px;
    font-size: 13px;
  }

  /* Terminal Window */
  .terminal-output {
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.5;
    color: #38bdf8;
    white-space: pre-wrap;
    height: calc(100% - 36px);
    overflow-y: auto;
  }
  .terminal-input-row {
    display: flex;
    align-items: center;
    gap: 8px;
    height: 32px;
    font-family: var(--font-mono);
  }
  .prompt-symbol { color: #a855f7; font-weight: bold; }
  .terminal-input {
    flex: 1;
    background: transparent;
    border: none;
    color: #fff;
    font-family: var(--font-mono);
    font-size: 13px;
    outline: none;
  }

  /* Process Table */
  table.ps-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    font-family: var(--font-mono);
  }
  table.ps-table th {
    text-align: left;
    padding: 6px 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-muted);
  }
  table.ps-table td {
    padding: 6px 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  }
  .badge-state {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
  }
  .state-READY { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
  .state-RUNNING { background: rgba(16, 185, 129, 0.2); color: #34d399; }
  .state-TERMINATED { background: rgba(239, 68, 68, 0.2); color: #f87171; }

  /* Bottom Dock */
  #dock {
    height: 56px;
    margin: 0 auto 12px auto;
    background: var(--dock-bg);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 16px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    z-index: 1000;
  }
  .dock-app {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 20px;
    transition: transform 0.2s, background 0.2s;
  }
  .dock-app:hover {
    transform: translateY(-6px) scale(1.1);
    background: rgba(99, 102, 241, 0.3);
  }
</style>
</head>
<body>

<div id="topbar">
  <div class="top-left">
    <div class="logo-badge">⚡ SYNAX-OS</div>
    <div class="top-menu-item" onclick="openWindow('win-ps')">Tasks</div>
    <div class="top-menu-item" onclick="openWindow('win-term')">Terminal</div>
    <div class="top-menu-item" onclick="openWindow('win-canvas')">Super-LLM</div>
    <div class="top-menu-item" onclick="openWindow('win-vafs')">VAFS Files</div>
    <div class="top-menu-item" onclick="openWindow('win-3d')">3D Office</div>
  </div>
  <div class="top-right">
    <span id="os-status">STATUS: SOVEREIGN RUNNING</span>
    <span id="os-clock">00:00:00</span>
  </div>
</div>

<div id="desktop">
  <!-- Window 1: Task Manager -->
  <div class="window" id="win-ps" style="top: 30px; left: 40px; width: 620px; height: 380px;">
    <div class="window-header" onmousedown="dragWindow(event, 'win-ps')">
      <div class="window-title">📊 Task Manager — Agent Process Table (/proc/agents)</div>
      <div class="window-controls">
        <div class="win-btn btn-min" onclick="toggleWin('win-ps')"></div>
        <div class="win-btn btn-max"></div>
        <div class="win-btn btn-close" onclick="closeWin('win-ps')"></div>
      </div>
    </div>
    <div class="window-body">
      <table class="ps-table">
        <thead>
          <tr><th>PID</th><th>Agent Name</th><th>Role</th><th>State</th><th>Cycles</th><th>Tokens</th></tr>
        </thead>
        <tbody id="ps-tbody">
          <tr><td colspan="6">Loading processes...</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Window 2: Interactive Terminal -->
  <div class="window" id="win-term" style="top: 70px; left: 690px; width: 560px; height: 380px;">
    <div class="window-header" onmousedown="dragWindow(event, 'win-term')">
      <div class="window-title">💻 Terminal — synax-sh (Sovereign CLI)</div>
      <div class="window-controls">
        <div class="win-btn btn-min" onclick="toggleWin('win-term')"></div>
        <div class="win-btn btn-max"></div>
        <div class="win-btn btn-close" onclick="closeWin('win-term')"></div>
      </div>
    </div>
    <div class="window-body" style="background: rgba(5, 8, 15, 0.95); padding: 10px;">
      <div class="terminal-output" id="term-out">SYNAX-OS Kernel v6.1.0-SovereignOS Booted.
Type 'help' for built-in syscall commands (ps, top, spawn, kill, cat, tools, exec)...
</div>
      <div class="terminal-input-row">
        <span class="prompt-symbol">synax-os&gt;</span>
        <input type="text" class="terminal-input" id="term-input" autofocus onkeydown="handleTermKey(event)">
      </div>
    </div>
  </div>

  <!-- Window 3: Super-LLM Canvas -->
  <div class="window" id="win-canvas" style="top: 430px; left: 40px; width: 620px; height: 340px;">
    <div class="window-header" onmousedown="dragWindow(event, 'win-canvas')">
      <div class="window-title">✨ Super-LLM Canvas & Code Interpreter</div>
      <div class="window-controls">
        <div class="win-btn btn-min" onclick="toggleWin('win-canvas')"></div>
        <div class="win-btn btn-max"></div>
        <div class="win-btn btn-close" onclick="closeWin('win-canvas')"></div>
      </div>
    </div>
    <div class="window-body">
      <div style="display:flex; gap:8px; margin-bottom:10px;">
        <input type="text" id="llm-prompt" placeholder="Ask Super-LLM, query live PubMed, or solve math..." style="flex:1; padding:8px 12px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
        <button onclick="askLLM()" style="padding:8px 16px; background:#6366f1; border:none; border-radius:6px; color:#fff; font-weight:600; cursor:pointer;">Synthesize</button>
      </div>
      <div id="llm-output" style="font-family:var(--font-mono); font-size:12px; color:#a5b4fc; background:rgba(0,0,0,0.3); padding:12px; border-radius:6px; height:220px; overflow-y:auto; white-space:pre-wrap;">Ready for reasoning queries...</div>
    </div>
  </div>

  <!-- Window 4: Virtual Agent File System -->
  <div class="window" id="win-vafs" style="top: 430px; left: 690px; width: 560px; height: 340px;">
    <div class="window-header" onmousedown="dragWindow(event, 'win-vafs')">
      <div class="window-title">📂 VAFS Explorer (/proc, /dev/tools, /sys)</div>
      <div class="window-controls">
        <div class="win-btn btn-min" onclick="toggleWin('win-vafs')"></div>
        <div class="win-btn btn-max"></div>
        <div class="win-btn btn-close" onclick="closeWin('win-vafs')"></div>
      </div>
    </div>
    <div class="window-body">
      <div style="display:flex; gap:6px; margin-bottom:10px;">
        <button onclick="loadVAFS('/sys/metrics')" style="padding:4px 8px; background:rgba(255,255,255,0.08); border:none; color:#fff; border-radius:4px; cursor:pointer;">/sys/metrics</button>
        <button onclick="loadVAFS('/sys/uptime')" style="padding:4px 8px; background:rgba(255,255,255,0.08); border:none; color:#fff; border-radius:4px; cursor:pointer;">/sys/uptime</button>
        <button onclick="loadVAFS('/proc/agents/2/status')" style="padding:4px 8px; background:rgba(255,255,255,0.08); border:none; color:#fff; border-radius:4px; cursor:pointer;">/proc/agents/2</button>
        <button onclick="loadVAFS('/dev/tools')" style="padding:4px 8px; background:rgba(255,255,255,0.08); border:none; color:#fff; border-radius:4px; cursor:pointer;">/dev/tools</button>
      </div>
      <pre id="vafs-content" style="font-family:var(--font-mono); font-size:12px; color:#34d399; background:rgba(0,0,0,0.3); padding:10px; border-radius:6px; height:220px; overflow-y:auto;">Click a path above to inspect virtual filesystem...</pre>
    </div>
  </div>
</div>

<!-- Dock -->
<div id="dock">
  <div class="dock-app" title="Tasks" onclick="openWindow('win-ps')">📊</div>
  <div class="dock-app" title="Terminal" onclick="openWindow('win-term')">💻</div>
  <div class="dock-app" title="Super-LLM" onclick="openWindow('win-canvas')">✨</div>
  <div class="dock-app" title="VAFS Files" onclick="openWindow('win-vafs')">📂</div>
  <div class="dock-app" title="3D Office Web" onclick="window.open('/office.html', '_blank')">🏢</div>
  <div class="dock-app" title="GitHub Repo" onclick="window.open('https://github.com/ofaemd-creator/synax-agent-office', '_blank')">🐙</div>
</div>

<script>
  // Clock
  setInterval(() => {
    document.getElementById('os-clock').textContent = new Date().toLocaleTimeString();
  }, 1000);

  // Window Management
  let highestZ = 10;
  function bringToFront(el) {
    highestZ++;
    el.style.zIndex = highestZ;
  }
  function openWindow(id) {
    const el = document.getElementById(id);
    if (el) { el.style.display = 'flex'; bringToFront(el); }
  }
  function closeWin(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  }
  function toggleWin(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = el.style.display === 'none' ? 'flex' : 'none';
  }

  // Draggable logic
  function dragWindow(e, id) {
    const win = document.getElementById(id);
    bringToFront(win);
    let shiftX = e.clientX - win.getBoundingClientRect().left;
    let shiftY = e.clientY - win.getBoundingClientRect().top;
    function moveAt(pageX, pageY) {
      win.style.left = (pageX - shiftX) + 'px';
      win.style.top = Math.max(32, (pageY - shiftY)) + 'px';
    }
    function onMouseMove(event) { moveAt(event.pageX, event.pageY); }
    document.addEventListener('mousemove', onMouseMove);
    document.onmouseup = function() {
      document.removeEventListener('mousemove', onMouseMove);
      document.onmouseup = null;
    };
  }

  // Fetch Processes
  async function refreshProcesses() {
    try {
      const res = await fetch('/api/os/ps');
      const data = await res.json();
      const tbody = document.getElementById('ps-tbody');
      tbody.innerHTML = data.map(p => `
        <tr>
          <td><strong>${p.pid}</strong></td>
          <td>${p.name}</td>
          <td style="color:#94a3b8; font-size:11px;">${p.role}</td>
          <td><span class="badge-state state-${p.state}">${p.state}</span></td>
          <td>${p.cpu_cycles_used}</td>
          <td>${p.tokens_consumed}</td>
        </tr>
      `).join('');
    } catch(e) {}
  }
  setInterval(refreshProcesses, 3000);
  refreshProcesses();

  // Terminal Handler
  async function handleTermKey(e) {
    if (e.key === 'Enter') {
      const input = document.getElementById('term-input');
      const cmd = input.value.trim();
      input.value = '';
      const out = document.getElementById('term-out');
      out.textContent += '\\nsynax-os> ' + cmd + '\\n';
      try {
        const res = await fetch('/api/os/exec', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({cmd})
        });
        const data = await res.json();
        out.textContent += data.output + '\\n';
      } catch(err) {
        out.textContent += 'Error: ' + err.message + '\\n';
      }
      out.scrollTop = out.scrollHeight;
      refreshProcesses();
    }
  }

  // Super-LLM Query
  async function askLLM() {
    const prompt = document.getElementById('llm-prompt').value.trim();
    if (!prompt) return;
    const out = document.getElementById('llm-output');
    out.textContent = 'Executing ReAct reasoning loop with live NCBI PubMed search...\\n';
    try {
      const res = await fetch('/api/os/exec', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({cmd: 'exec pubmed ' + prompt})
      });
      const data = await res.json();
      out.textContent = '✓ Synthesized Result from Specialist Agents:\\n' + data.output;
    } catch(e) {
      out.textContent = 'Error: ' + e.message;
    }
  }

  // VAFS Inspector
  async function loadVAFS(path) {
    const el = document.getElementById('vafs-content');
    el.textContent = 'Reading ' + path + '...';
    try {
      const res = await fetch('/api/os/vafs?path=' + encodeURIComponent(path));
      const data = await res.json();
      el.textContent = typeof data.content === 'object' ? JSON.stringify(data.content, null, 2) : data.content;
    } catch(e) {
      el.textContent = 'Error: ' + e.message;
    }
  }
</script>
</body>
</html>
"""


class SynaxOSRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for SYNAX-OS Desktop Window Manager."""

    kernel: SynaxOSKernel = None  # Class-level kernel instance
    shell: SynaxShell = None

    def do_GET(self) -> None:
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/os", "/desktop"):
            html = get_desktop_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return

        elif path == "/api/os/ps":
            data = json.dumps(self.kernel.sys_ps()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        elif path == "/api/os/vafs":
            qs = parse_qs(parsed.query)
            target_path = qs.get("path", ["/sys/version"])[0]
            try:
                content = self.kernel.vafs.read_file(target_path)
                try:
                    parsed_json = json.loads(content)
                    resp = json.dumps({"path": target_path, "content": parsed_json}).encode("utf-8")
                except Exception:
                    resp = json.dumps({"path": target_path, "content": content}).encode("utf-8")
                status = 200
            except Exception as e:
                resp = json.dumps({"error": str(e)}).encode("utf-8")
                status = 404

            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self) -> None:
        """Handle POST requests."""
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if parsed.path == "/api/os/exec":
            cmd = payload.get("cmd", "help")
            output = self.shell.execute_command(cmd)
            resp = json.dumps({"cmd": cmd, "output": output}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        else:
            self.send_response(404)
            self.end_headers()


def run_os_server(port: int = 8796) -> None:
    """Start the SYNAX-OS HTTP Server."""
    kernel = SynaxOSKernel()
    kernel.boot()
    shell = SynaxShell(kernel=kernel)

    SynaxOSRequestHandler.kernel = kernel
    SynaxOSRequestHandler.shell = shell

    server = ThreadingHTTPServer(("0.0.0.0", port), SynaxOSRequestHandler)
    print(f"⚡ SYNAX-OS Sovereign Agentic Operating System running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SYNAX-OS Sovereign Desktop Runner")
    parser.add_argument("--port", type=int, default=8796, help="Port to listen on (default: 8796)")
    args = parser.parse_args()
    run_os_server(port=args.port)
