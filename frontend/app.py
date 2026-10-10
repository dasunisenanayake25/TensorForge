import json
import os

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="TensorForge | Support Routing",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)


api_base_url = os.getenv("TENSORFORGE_API_BASE_URL", "http://localhost:8000").strip().rstrip("/")
api_key = os.getenv("TENSORFORGE_API_KEY", "")
config = json.dumps({"apiBaseUrl": api_base_url, "apiKey": api_key}).replace("</", "<\\/")

components.html(
    f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  color-scheme: light;
  --navy: #0b1220; --blue: #2563eb; --cyan: #22d3ee; --violet: #8b5cf6;
  --ink: #172033; --muted: #64748b; --line: rgba(148,163,184,.28);
  --glass: rgba(255,255,255,.78); --panel: rgba(248,250,252,.86);
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; min-height: 100%; }}
body {{
  min-height: 720px; padding: 18px; overflow-x: hidden;
  color: var(--ink); font-family: Inter, system-ui, sans-serif;
  background: radial-gradient(circle at 8% 5%, #dbeafe 0, transparent 34%),
    radial-gradient(circle at 94% 20%, #ede9fe 0, transparent 30%),
    linear-gradient(135deg, #f8fafc, #eef4ff 55%, #f8fafc);
}}
button, input, textarea {{ font: inherit; }}
button {{ cursor: pointer; }}
.outer-window {{
  max-width: 1380px; min-height: 680px; margin: auto; padding: 8px;
  border: 1px solid rgba(100,116,139,.36); border-radius: 22px;
  background: rgba(255,255,255,.54); box-shadow: 0 30px 90px rgba(15,23,42,.18);
  backdrop-filter: blur(20px);
}}
.chrome {{
  display: flex; align-items: center; gap: 7px; height: 35px; padding: 0 10px;
  color: var(--muted); font: 700 11px "Space Grotesk", sans-serif; letter-spacing: .12em;
  text-transform: uppercase;
}}
.traffic {{ width: 10px; height: 10px; border-radius: 50%; }}
.traffic.red {{ background: #fb7185; }} .traffic.yellow {{ background: #fbbf24; }}
.traffic.green {{ background: #34d399; }} .chrome-title {{ margin-left: 5px; }}
.inner-window {{
  position: relative; min-height: 625px; padding: 76px 18px 18px;
  border: 1px solid var(--line); border-radius: 16px; background: var(--glass);
  box-shadow: inset 0 1px rgba(255,255,255,.9); overflow: hidden;
}}
.inner-window::before {{
  content: "TENSORFORGE  /  SUPPORT WORKSPACE";
  position: absolute; inset: 0 0 auto; height: 47px; padding: 0 16px;
  border-bottom: 1px solid var(--line); color: var(--muted);
  background: linear-gradient(#f8fafc, #e2e8f0); line-height: 47px;
  font: 700 11px/47px "Space Grotesk", sans-serif; letter-spacing: .12em;
  white-space: pre;
}}
.hero {{
  position: relative; overflow: hidden; padding: 25px 30px; border-radius: 17px;
  color: white; background: linear-gradient(110deg, #0b1220, #172554 48%, #2563eb);
  box-shadow: 0 20px 45px rgba(23,37,84,.22);
}}
.hero::before {{ content: ""; position: absolute; inset: 0; opacity: .14;
  background-image: linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);
  background-size: 27px 27px; }}
.hero > * {{ position: relative; }}
.kicker {{ color: #a5f3fc; font: 700 11px "Space Grotesk", sans-serif; letter-spacing: .14em; text-transform: uppercase; }}
h1, h2, h3 {{ font-family: "Space Grotesk", sans-serif; }}
h1 {{ margin: 8px 0 8px; font-size: clamp(27px, 4vw, 46px); letter-spacing: -.045em; }}
.hero p {{ margin: 0; color: #dbeafe; }}
.live {{ display: inline-block; width: 8px; height: 8px; margin-right: 8px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 0 5px rgba(34,211,238,.15); }}
.tabs {{ display: flex; gap: 7px; margin: 18px 0 12px; padding: 6px; border: 1px solid var(--line); border-radius: 14px; background: rgba(226,232,240,.7); }}
.tab {{ flex: 1; padding: 10px 12px; border: 0; border-radius: 10px; color: var(--muted); background: transparent; font-weight: 700; }}
.tab:hover {{ color: var(--blue); background: white; }} .tab.active {{ color: white; background: linear-gradient(110deg,var(--blue),var(--violet)); }}
.panel-window {{ display: none; padding: 22px; border: 1px solid var(--line); border-radius: 15px; background: var(--panel); box-shadow: 0 12px 35px rgba(15,23,42,.08); }}
.panel-window.active {{ display: block; }}
.panel-window.floating {{ position:absolute; width:calc(100% - 44px); z-index:10; }}
.panel-head {{ display:flex; align-items:flex-start; justify-content:space-between; gap:16px; margin-bottom: 16px; cursor:grab; user-select:none; }}
.panel-head:active {{ cursor:grabbing; }}
.panel-head h2 {{ margin: 0 0 5px; font-size: 24px; }} .panel-head p {{ margin: 0; color: var(--muted); }}
.window-actions {{ display: flex; gap: 5px; }} .window-actions button {{ width: 28px; height: 28px; padding: 0; border: 1px solid var(--line); border-radius: 8px; color: var(--muted); background: white; }}
.window-actions button:hover {{ color: var(--blue); border-color: var(--blue); }}
.form-card {{ padding: 17px; border: 1px solid var(--line); border-radius: 13px; background: rgba(255,255,255,.7); }}
label {{ display:block; margin: 0 0 6px; color: var(--muted); font-size: 13px; font-weight: 700; }}
input, textarea {{ width:100%; padding:11px 12px; border:1px solid rgba(148,163,184,.5); border-radius:9px; color:var(--ink); background:white; outline:0; }}
input:focus, textarea:focus {{ border-color:var(--blue); box-shadow:0 0 0 3px rgba(37,99,235,.14); }}
textarea {{ min-height: 115px; resize: vertical; }} .field {{ margin-bottom: 14px; }}
.primary {{ position:relative; overflow:hidden; padding:11px 16px; border:0; border-radius:9px; color:white; background:linear-gradient(110deg,var(--blue),var(--cyan)); box-shadow:0 8px 18px rgba(37,99,235,.22); font-weight:700; }}
.primary:hover {{ transform:translateY(-1px); box-shadow:0 11px 24px rgba(37,99,235,.34); }} .primary:active {{ transform:scale(.98); }}
.secondary {{ padding:10px 14px; border:1px solid var(--line); border-radius:9px; color:var(--ink); background:white; font-weight:700; }}
.result, .alert {{ margin-top: 15px; padding: 13px; border-radius: 10px; white-space: pre-wrap; }}
.result {{ border:1px solid #a5f3fc; background:#ecfeff; }} .alert {{ border:1px solid #fda4af; background:#fff1f2; color:#9f1239; }}
.metrics {{ display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin-top:15px; }}
.metric {{ padding:15px; border-left:4px solid var(--cyan); border-radius:11px; background:white; box-shadow:0 8px 20px rgba(15,23,42,.07); }}
.metric small {{ display:block; color:var(--muted); font-weight:700; }} .metric strong {{ display:block; margin-top:4px; font-size:19px; }}
.drop {{ padding:24px; border:2px dashed #93c5fd; border-radius:12px; text-align:center; background:#eff6ff; }}
.drop input {{ margin-top:10px; border:0; background:transparent; }} .muted {{ color:var(--muted); font-size:13px; }}
pre {{ overflow:auto; margin:0; padding:13px; border-radius:9px; color:#dbeafe; background:#0f172a; font-size:12px; }}
.minimized .panel-body {{ display:none; }} .minimized {{ min-height:0; }}
@media (max-width: 700px) {{
  body {{ padding: 7px; }} .outer-window {{ min-height: 100vh; }} .inner-window {{ padding: 68px 9px 9px; }}
  .hero {{ padding: 22px 18px; }} .tabs {{ overflow:auto; }} .tab {{ min-width:130px; }}
  .panel-window {{ padding:15px; }} .metrics {{ grid-template-columns:1fr; }}
}}
@media (prefers-reduced-motion: no-preference) {{
  .hero {{ animation: gradient 12s ease-in-out infinite alternate; }}
  .panel-window.active {{ animation: rise .35s ease-out both; }}
  @keyframes gradient {{ from {{ background-position:0 50%; }} to {{ background-position:100% 50%; }} }}
  @keyframes rise {{ from {{ opacity:0; transform:translateY(7px); }} to {{ opacity:1; transform:none; }} }}
}}
</style>
</head>
<body>
<main class="outer-window">
  <div class="chrome"><span class="traffic red"></span><span class="traffic yellow"></span><span class="traffic green"></span><span class="chrome-title">TensorForge command center</span></div>
  <section class="inner-window">
    <header class="hero"><div class="kicker"> TensorForge workspace</div><h1>Support routing, intelligently delivered.</h1><p><span class="live"></span>Classify customer tickets and route them to the right support team.</p></header>
    <nav class="tabs" aria-label="Workflows">
      <button class="tab active" data-panel="single">Single ticket</button><button class="tab" data-panel="batch">Batch predictions</button><button class="tab" data-panel="async">Async jobs</button><button class="tab" data-panel="health">Health</button>
    </nav>
    <section id="single" class="panel-window active">
      <div class="panel-head"><div><h2>Classify a single ticket</h2><p>Get an immediate category and routing team.</p></div><div class="window-actions"><button title="Minimize">−</button></div></div>
      <div class="panel-body form-card"><div class="field"><label for="ticket-id">Ticket ID</label><input id="ticket-id" value="TICK-1001"></div><div class="field"><label for="ticket-text">Ticket description</label><textarea id="ticket-text">I was charged twice for my subscription payment on checkout.</textarea></div><button class="primary" id="classify">Classify ticket</button><div id="single-result"></div></div>
    </section>
    <section id="batch" class="panel-window">
      <div class="panel-head"><div><h2>Process a batch of tickets</h2><p>Upload a CSV with <b>id</b> and <b>text</b> columns. Up to 100 tickets.</p></div><div class="window-actions"><button title="Minimize">−</button></div></div>
      <div class="panel-body form-card"><div class="drop"><b>Choose a CSV file</b><div class="muted">Example: id,text</div><input id="sync-csv" type="file" accept=".csv"></div><div id="batch-preview"></div><button class="primary" id="run-batch" disabled>Run batch prediction</button><div id="batch-result"></div></div>
    </section>
    <section id="async" class="panel-window">
      <div class="panel-head"><div><h2>Run a large dataset in the background</h2><p>Submit large datasets as background jobs.</p></div><div class="window-actions"><button title="Minimize">−</button></div></div>
      <div class="panel-body form-card"><div class="drop"><b>Choose an evaluation CSV</b><div class="muted">Required columns: id,text</div><input id="async-csv" type="file" accept=".csv"></div><div id="async-preview"></div><button class="primary" id="submit-async" disabled>Submit async job</button><div id="async-result"></div><hr><h3>Check an existing job</h3><div class="field"><label for="job-id">Job ID</label><input id="job-id" placeholder="Paste a job ID here"></div><button class="secondary" id="check-job">Check job status</button><div id="job-result"></div></div>
    </section>
    <section id="health" class="panel-window">
      <div class="panel-head"><div><h2>Backend health</h2><p>Check whether the TensorForge API is reachable.</p></div><div class="window-actions"><button title="Minimize">−</button></div></div>
      <div class="panel-body form-card"><button class="primary" id="check-health">Check connection</button><div id="health-result"></div></div>
    </section>
  </section>
</main>
<script>
const config = __CONFIG__;
const api = config.apiBaseUrl;
const authHeaders = {{"X-API-Key": config.apiKey, "Content-Type": "application/json"}};
const $ = (id) => document.getElementById(id);
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[char]));
function show(target, text, kind="result") {{ $(target).innerHTML = `<div class="${{kind}}">${{escapeHtml(text)}}</div>`; }}
function showJson(target, value) {{ $(target).innerHTML = `<div class="result"><pre>${{escapeHtml(JSON.stringify(value, null, 2))}}</pre></div>`; }}
async function request(path, options={{}}) {{
  const response = await fetch(api + path, options);
  let data; try {{ data = await response.json(); }} catch {{ data = await response.text(); }}
  if (!response.ok) throw new Error(`${{options.action || "Request"}} failed (HTTP ${{response.status}}). ${{data?.detail || data || ""}}`);
  return data;
}}
function parseCsv(text) {{
  const rows = []; let row = [], cell = "", quoted = false;
  for (let i=0; i<text.length; i++) {{ const c=text[i], next=text[i+1];
    if (c === '"' && quoted && next === '"') {{ cell += '"'; i++; }}
    else if (c === '"') quoted = !quoted;
    else if (c === "," && !quoted) {{ row.push(cell); cell=""; }}
    else if ((c === "\\n" || c === "\\r") && !quoted) {{ if (c === "\\r" && next === "\\n") i++; row.push(cell); if (row.some(v=>v.trim())) rows.push(row); row=[]; cell=""; }}
    else cell += c;
  }} if (cell || row.length) {{ row.push(cell); rows.push(row); }}
  if (!rows.length) throw new Error("The CSV does not contain any tickets.");
  const headers = rows.shift().map(v=>v.trim()); const id = headers.indexOf("id"), textCol = headers.indexOf("text");
  if (id < 0 || textCol < 0) throw new Error("The CSV must contain these columns: id and text.");
  const tickets = rows.map(r=>({{id:(r[id]||"").trim(), text:(r[textCol]||"").trim()}}));
  if (!tickets.length || tickets.some(t=>!t.id || !t.text)) throw new Error("Every ticket must have both an id and text value.");
  return tickets;
}}
function bindFile(input, preview, button) {{ $(input).addEventListener("change", async (event) => {{ const file=event.target.files[0]; if (!file) return; try {{ const tickets=parseCsv(await file.text()); event.target.dataset.tickets=JSON.stringify(tickets); $(preview).innerHTML=`<div class="result">${{tickets.length.toLocaleString()}} ticket(s) ready.</div>`; $(button).disabled=false; }} catch(error) {{ $(preview).innerHTML=`<div class="alert">${{escapeHtml(error.message)}}</div>`; $(button).disabled=true; }} }}); }}
bindFile("sync-csv", "batch-preview", "run-batch"); bindFile("async-csv", "async-preview", "submit-async");
$("classify").onclick = async () => {{ const id=$("ticket-id").value.trim(), text=$("ticket-text").value.trim(); if(!id) return show("single-result","Please enter a ticket ID.","alert"); if(!text) return show("single-result","Please enter a ticket description.","alert"); try {{ const data=await request("/predict",{{method:"POST",headers:authHeaders,body:JSON.stringify({{id,text}}),action:"Ticket classification"}}); $("single-result").innerHTML=`<div class="result">Ticket classified successfully.</div><div class="metrics"><div class="metric"><small>Predicted category</small><strong>${{escapeHtml(data.category || "N/A")}}</strong></div><div class="metric"><small>Routed team</small><strong>${{escapeHtml(data.team || "N/A")}}</strong></div></div>`; }} catch(error) {{ show("single-result",error.message,"alert"); }} }};
$("run-batch").onclick = async () => {{ try {{ const tickets=JSON.parse($("sync-csv").dataset.tickets); const data=await request("/predict/batch",{{method:"POST",headers:authHeaders,body:JSON.stringify({{tickets}}),action:"Batch prediction"}}); showJson("batch-result",data); }} catch(error) {{ show("batch-result",error.message,"alert"); }} }};
$("submit-async").onclick = async () => {{ try {{ const tickets=JSON.parse($("async-csv").dataset.tickets); const data=await request("/batch/jobs",{{method:"POST",headers:authHeaders,body:JSON.stringify({{tickets}}),action:"Async job submission"}}); showJson("async-result",data); }} catch(error) {{ show("async-result",error.message,"alert"); }} }};
$("check-job").onclick = async () => {{ const id=$("job-id").value.trim(); if(!id) return show("job-result","Please enter a job ID.","alert"); try {{ showJson("job-result",await request("/batch/jobs/"+encodeURIComponent(id),{{headers:authHeaders,action:"Job status request"}})); }} catch(error) {{ show("job-result",error.message,"alert"); }} }};
$("check-health").onclick = async () => {{ try {{ showJson("health-result",await request("/health",{{action:"Health check"}})); }} catch(error) {{ show("health-result",error.message,"alert"); }} }};
document.querySelectorAll(".tab").forEach(tab => tab.onclick = () => {{ document.querySelectorAll(".tab").forEach(t=>t.classList.remove("active")); document.querySelectorAll(".panel-window").forEach(p=>p.classList.remove("active")); tab.classList.add("active"); $(tab.dataset.panel).classList.add("active"); }});
document.querySelectorAll(".window-actions button").forEach(button => button.onclick = () => button.closest(".panel-window").classList.toggle("minimized"));
document.querySelectorAll(".panel-window").forEach(panel => {{
  const handle = panel.querySelector(".panel-head");
  handle.addEventListener("pointerdown", (event) => {{
    if (event.target.closest("button")) return;
    const workspace = panel.closest(".inner-window");
    const workspaceBox = workspace.getBoundingClientRect();
    const panelBox = panel.getBoundingClientRect();
    const offsetX = event.clientX - panelBox.left;
    const offsetY = event.clientY - panelBox.top;
    panel.classList.add("floating");
    panel.style.left = `${{Math.max(10, panelBox.left - workspaceBox.left)}}px`;
    panel.style.top = `${{Math.max(58, panelBox.top - workspaceBox.top)}}px`;
    panel.setPointerCapture(event.pointerId);
    const move = (moveEvent) => {{
      const nextLeft = moveEvent.clientX - workspaceBox.left - offsetX;
      const nextTop = moveEvent.clientY - workspaceBox.top - offsetY;
      const maxLeft = workspace.clientWidth - panel.offsetWidth - 10;
      const maxTop = workspace.clientHeight - panel.offsetHeight - 10;
      panel.style.left = `${{Math.min(Math.max(10, nextLeft), Math.max(10, maxLeft))}}px`;
      panel.style.top = `${{Math.min(Math.max(58, nextTop), Math.max(58, maxTop))}}px`;
    }};
    const stop = () => {{
      panel.releasePointerCapture(event.pointerId);
      panel.removeEventListener("pointermove", move);
      panel.removeEventListener("pointerup", stop);
      panel.removeEventListener("pointercancel", stop);
    }};
    panel.addEventListener("pointermove", move);
    panel.addEventListener("pointerup", stop);
    panel.addEventListener("pointercancel", stop);
  }});
}});
</script>
</body>
</html>
""".replace("__CONFIG__", config),
    height=760,
    scrolling=False,
)
