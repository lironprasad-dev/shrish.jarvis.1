"""
JARVIS-LOQ Backend Server
Run this file first, then open JARVIS-LOQ.html in Chrome.
Requires Python 3 (already on most Windows PCs).
Install dependency once: pip install flask flask-cors
"""

import subprocess
import os
import sys

# Auto-install dependencies if missing
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])
    from flask import Flask, request, jsonify
    from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow browser to talk to this server

# ── App definitions ──────────────────────────────────────────────
APPS = {
    "chrome":        {"open": "start chrome",                   "exe": "chrome.exe"},
    "firefox":       {"open": "start firefox",                  "exe": "firefox.exe"},
    "notepad":       {"open": "start notepad",                  "exe": "notepad.exe"},
    "vscode":        {"open": "start code",                     "exe": "Code.exe"},
    "vs code":       {"open": "start code",                     "exe": "Code.exe"},
    "explorer":      {"open": "start explorer",                 "exe": "explorer.exe"},
    "file explorer": {"open": "start explorer",                 "exe": "explorer.exe"},
    "taskmgr":       {"open": "start taskmgr",                  "exe": "Taskmgr.exe"},
    "task manager":  {"open": "start taskmgr",                  "exe": "Taskmgr.exe"},
    "spotify":       {"open": "start spotify",                  "exe": "Spotify.exe"},
    "discord":       {"open": "start discord",                  "exe": "Discord.exe"},
    "calculator":    {"open": "start calc",                     "exe": "CalculatorApp.exe"},
    "calc":          {"open": "start calc",                     "exe": "CalculatorApp.exe"},
    "vlc":           {"open": "start vlc",                      "exe": "vlc.exe"},
    "paint":         {"open": "start mspaint",                  "exe": "mspaint.exe"},
    "word":          {"open": "start winword",                  "exe": "WINWORD.EXE"},
    "excel":         {"open": "start excel",                    "exe": "EXCEL.EXE"},
    "powerpoint":    {"open": "start powerpnt",                 "exe": "POWERPNT.EXE"},
    "steam":         {"open": "start steam",                    "exe": "Steam.exe"},
    "whatsapp":      {"open": "start whatsapp",                 "exe": "WhatsApp.exe"},
    "zoom":          {"open": "start zoom",                     "exe": "Zoom.exe"},
    "brave":         {"open": "start brave",                    "exe": "brave.exe"},
    "obs":           {"open": "start obs64",                    "exe": "obs64.exe"},
    "notepad++":     {"open": "start notepadplusplus",          "exe": "notepad++.exe"},
    "snipping tool": {"open": "start snippingtool",             "exe": "SnippingTool.exe"},
    "cmd":           {"open": "start cmd",                      "exe": "cmd.exe"},
    "powershell":    {"open": "start powershell",               "exe": "powershell.exe"},
}

# ── Routes ───────────────────────────────────────────────────────

@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "message": "JARVIS-LOQ server is running!"})

@app.route("/open", methods=["POST"])
def open_app():
    data = request.json
    name = data.get("app", "").lower().strip()
    app_info = APPS.get(name)
    if not app_info:
        return jsonify({"success": False, "message": f"I don't know the app '{name}'. Try adding it to the server!"})
    try:
        subprocess.Popen(app_info["open"], shell=True)
        return jsonify({"success": True, "message": f"Opened {name.title()} successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/close", methods=["POST"])
def close_app():
    data = request.json
    name = data.get("app", "").lower().strip()
    app_info = APPS.get(name)
    if not app_info:
        return jsonify({"success": False, "message": f"I don't know '{name}'."})
    try:
        subprocess.run(f'taskkill /F /IM "{app_info["exe"]}" /T', shell=True, capture_output=True)
        return jsonify({"success": True, "message": f"Closed {name.title()}!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/system", methods=["POST"])
def system_cmd():
    data = request.json
    cmd = data.get("cmd", "").lower().strip()

    commands = {
        "shutdown":      ("shutdown /s /t 30", "Shutting down in 30 seconds!"),
        "restart":       ("shutdown /r /t 30", "Restarting in 30 seconds!"),
        "sleep":         ("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", "Going to sleep!"),
        "lock":          ("rundll32.exe user32.dll,LockWorkStation", "Screen locked!"),
        "volume_up":     ("nircmd.exe changesysvolume 5000", "Volume up!"),
        "volume_down":   ("nircmd.exe changesysvolume -5000", "Volume down!"),
        "mute":          ("nircmd.exe mutesysvolume 2", "Mute toggled!"),
        "cancel_shutdown": ("shutdown /a", "Shutdown cancelled!"),
        "flush_dns":     ("ipconfig /flushdns", "DNS flushed!"),
        "clear_temp":    ("del /q/f/s %TEMP%\\*", "Temp files cleared!"),
        "recycle_bin":   ('powershell -Command "Clear-RecycleBin -Force"', "Recycle bin emptied!"),
    }

    if cmd == "screenshot":
        path = os.path.join(os.path.expanduser("~"), "Desktop", "screenshot.png")
        ps = f'Add-Type -AssemblyName System.Windows.Forms; $img=[System.Drawing.Bitmap]::new([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width,[System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); $g=[System.Drawing.Graphics]::FromImage($img); $g.CopyFromScreen(0,0,0,0,$img.Size); $img.Save("{path}")'
        subprocess.Popen(["powershell", "-Command", ps])
        return jsonify({"success": True, "message": f"Screenshot saved to Desktop!"})

    if cmd == "battery":
        result = subprocess.run('powershell -Command "Get-WmiObject Win32_Battery | Select-Object EstimatedChargeRemaining"', shell=True, capture_output=True, text=True)
        out = result.stdout.strip()
        return jsonify({"success": True, "message": f"Battery info: {out}"})

    if cmd == "ip":
        result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True)
        lines = [l for l in result.stdout.splitlines() if "IPv4" in l]
        ip = lines[0].split(":")[-1].strip() if lines else "Not found"
        return jsonify({"success": True, "message": f"Your IP: {ip}"})

    if cmd in commands:
        shell_cmd, msg = commands[cmd]
        subprocess.Popen(shell_cmd, shell=True)
        return jsonify({"success": True, "message": msg})

    return jsonify({"success": False, "message": f"Unknown system command: {cmd}"})

@app.route("/type", methods=["POST"])
def type_text():
    """Type text anywhere using PowerShell"""
    data = request.json
    text = data.get("text", "")
    ps = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{text}")'
    subprocess.Popen(["powershell", "-Command", ps])
    return jsonify({"success": True, "message": f"Typed: {text}"})

# ── Start ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  JARVIS-LOQ Backend Server")
    print("  Lenovo LOQ · RTX 5050 · i7")
    print("=" * 50)
    print("\n✅ Server starting on http://localhost:5050")
    print("📂 Now open JARVIS-LOQ-v2.html in Chrome")
    print("🔴 Keep this window open while using JARVIS")
    print("   Press Ctrl+C to stop the server\n")
    app.run(host="127.0.0.1", port=5050, debug=False)
