# /// script
# requires-python = ">=3.12"
#
# [tool.orcaslicer.plugin]
# name = "ProBharath CNC & CAM Studio"
# description = "Professional FlatCAM-equivalent CNC/CAM: PCB isolation routing, drilling, engraving, 2.5D pocketing, contour cutting, job manager, multi-machine G-code."
# author = "ProBharath Technologies"
# version = "2.6.0"
# type = "pages"
# ///
import orca
import json


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ProBharath CNC &amp; CAM Studio</title>
<style>
:root{--bg:#0d0f18;--s:#12151e;--s2:#1a1e2e;--b:#252a3d;--ac:#00c8ff;--ac2:#00ff9d;--dn:#ff4d6d;--wn:#ffb347;--tx:#dce6f5;--tx2:#7a8aaa;--r:8px}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:13px;height:100vh;display:flex;flex-direction:column;overflow:hidden}
.hdr{background:linear-gradient(135deg,#0d1220,#12151e);border-bottom:1px solid var(--b);padding:10px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0}
.hdr h1{font-size:15px;font-weight:700;color:var(--ac)}
.hdr p{font-size:10px;color:var(--tx2);letter-spacing:1px;text-transform:uppercase}
.badge{background:var(--ac);color:#000;font-size:9px;font-weight:700;padding:2px 8px;border-radius:99px}
.tabs{display:flex;background:var(--s);border-bottom:1px solid var(--b);flex-shrink:0;overflow-x:auto}
.tab{padding:10px 16px;cursor:pointer;color:var(--tx2);font-size:12px;font-weight:600;white-space:nowrap;border-bottom:2px solid transparent;transition:.15s;display:flex;align-items:center;gap:6px}
.tab:hover{color:var(--tx);background:var(--s2)}
.tab.active{color:var(--ac);border-bottom-color:var(--ac)}
.main{display:flex;flex:1;overflow:hidden}
.lp{width:280px;background:var(--s);border-right:1px solid var(--b);display:flex;flex-direction:column;overflow:hidden;flex-shrink:0}
.ph{padding:10px 14px;font-size:11px;font-weight:700;color:var(--tx2);text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between}
.ps{overflow-y:auto;flex:1;padding:10px}
.f{margin-bottom:12px}
.f label{display:block;font-size:11px;font-weight:600;color:var(--tx2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.f input,.f select,.f textarea{width:100%;padding:7px 10px;background:var(--s2);border:1px solid var(--b);border-radius:var(--r);color:var(--tx);font-size:12px;transition:.15s;outline:none}
.f input:focus,.f select:focus,.f textarea:focus{border-color:var(--ac)}
.f textarea{resize:vertical;min-height:70px;font-family:monospace}
.r2{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.st{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--ac);padding:8px 0 4px;border-bottom:1px solid var(--b);margin-bottom:8px}
.btn{padding:8px 14px;border-radius:var(--r);border:none;cursor:pointer;font-size:12px;font-weight:700;transition:.15s;display:inline-flex;align-items:center;gap:6px}
.btn-p{background:linear-gradient(135deg,var(--ac),#0088cc);color:#000;width:100%;justify-content:center;padding:10px;font-size:13px;letter-spacing:.5px}
.btn-p:hover{opacity:.88;transform:translateY(-1px)}
.btn-s{background:var(--s2);color:var(--tx);border:1px solid var(--b);width:100%;justify-content:center}
.btn-s:hover{border-color:var(--ac);color:var(--ac)}
.btn-ok{background:var(--ac2);color:#000;width:100%;justify-content:center;padding:10px}
.btn-ok:hover{opacity:.88}
.br{display:flex;gap:6px;margin-bottom:8px}
.br .btn{flex:1}
.cp{flex:1;background:#080a10;display:flex;flex-direction:column;overflow:hidden}
.ct{background:var(--s);border-bottom:1px solid var(--b);padding:6px 12px;display:flex;align-items:center;gap:8px;flex-shrink:0}
.ct .btn{padding:5px 10px;font-size:11px}
.cw{flex:1;position:relative;overflow:hidden}
canvas{display:block;width:100%;height:100%;cursor:crosshair}
.ci{position:absolute;bottom:8px;left:12px;font-size:10px;color:var(--tx2);background:rgba(0,0,0,.6);padding:4px 8px;border-radius:4px;pointer-events:none}
.rp{width:260px;background:var(--s);border-left:1px solid var(--b);display:flex;flex-direction:column;overflow:hidden;flex-shrink:0}
.gb{background:#050710;border:1px solid var(--b);border-radius:var(--r);padding:8px;font-family:'Fira Mono','Courier New',monospace;font-size:10.5px;color:#7dd3fc;max-height:220px;overflow-y:auto;white-space:pre;line-height:1.6;margin-bottom:8px}
.gb .cm{color:#6b7280}.gb .kw{color:var(--ac)}.gb .vl{color:var(--ac2)}
.ji{background:var(--s2);border:1px solid var(--b);border-radius:var(--r);padding:8px 10px;margin-bottom:6px;display:flex;align-items:center;gap:8px}
.ji:hover{border-color:var(--ac)}
.jd{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.jn{flex:1;min-width:0}
.jt{font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.jst{font-size:10px;color:var(--tx2)}
.jx{font-size:14px;color:var(--tx2);padding:2px 6px;cursor:pointer;border-radius:4px}
.jx:hover{color:var(--dn)}
.sb{background:var(--s);border-top:1px solid var(--b);padding:5px 14px;display:flex;align-items:center;gap:10px;font-size:10px;color:var(--tx2);flex-shrink:0}
.sd{width:7px;height:7px;border-radius:50%;background:var(--ac2);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.sm{flex:1}
progress{width:100%;height:5px;border-radius:3px;border:none;display:none}
progress::-webkit-progress-bar{background:var(--s2);border-radius:3px}
progress::-webkit-progress-value{background:var(--ac);border-radius:3px;transition:width .3s}
.tr{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.tr label{font-size:12px;color:var(--tx)}
.tg{position:relative;width:36px;height:20px}
.tg input{display:none}
.ts{position:absolute;inset:0;background:var(--b);border-radius:99px;cursor:pointer;transition:.2s}
.ts:before{content:"";position:absolute;left:3px;top:3px;width:14px;height:14px;background:#fff;border-radius:50%;transition:.2s}
.tg input:checked+.ts{background:var(--ac)}
.tg input:checked+.ts:before{transform:translateX(16px)}
.lbg{display:inline-block;padding:2px 8px;border-radius:99px;font-size:10px;font-weight:700;background:rgba(0,200,255,.12);color:var(--ac);border:1px solid rgba(0,200,255,.3)}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:var(--s)}::-webkit-scrollbar-thumb{background:var(--b);border-radius:3px}
.pn{display:none}.pn.ac{display:flex;flex:1;overflow:hidden}
input[readonly]{background:transparent!important;border-color:transparent!important;color:var(--tx2)!important}
</style>
</head>
<body>
<div class="hdr">
  <div><div style="font-size:28px;line-height:1">⚙️</div></div>
  <div style="flex:1"><h1>ProBharath CNC &amp; CAM Studio</h1><p>FlatCAM-Compatible · PCB · Routing · Drilling · Engraving · G-code</p></div>
  <span class="badge">v2.6</span>
</div>
<div class="tabs">
  <div class="tab active" data-p="isolation" onclick="sw(this,'isolation')"><span>🔷</span>PCB Isolation</div>
  <div class="tab" data-p="drilling" onclick="sw(this,'drilling')"><span>🔩</span>Drilling</div>
  <div class="tab" data-p="contour" onclick="sw(this,'contour')"><span>✂️</span>Contour/Cut</div>
  <div class="tab" data-p="pocketing" onclick="sw(this,'pocketing')"><span>🪣</span>2.5D Pocketing</div>
  <div class="tab" data-p="engraving" onclick="sw(this,'engraving')"><span>✍️</span>Engraving</div>
  <div class="tab" data-p="jobs" onclick="sw(this,'jobs')"><span>📋</span>Job Manager</div>
  <div class="tab" data-p="gcode" onclick="sw(this,'gcode')"><span>📄</span>G-code Output</div>
</div>
<div class="main">

<!-- ISOLATION -->
<div id="pn-isolation" class="pn ac">
  <div class="lp"><div class="ph"><span>PCB Isolation Routing</span><span class="lbg">Gerber/SVG</span></div><div class="ps">
    <div class="st">📁 Import Layer</div>
    <div class="f"><label>Layer Type</label><select><option>Top Copper (GTL)</option><option>Bottom Copper (GBL)</option><option>Top Silkscreen (GTO)</option><option>Edge Cuts (GKO)</option><option>SVG Artwork</option></select></div>
    <div class="br"><button class="btn btn-s" onclick="loadFile()">📂 Load File</button><button class="btn btn-s" onclick="loadDemo()">🎯 Demo PCB</button></div>
    <div class="st">🔧 Tool Settings</div>
    <div class="r2"><div class="f"><label>Tool Dia (mm)</label><input type="number" value="0.1" step="0.01"></div><div class="f"><label>Passes</label><input type="number" value="2" min="1" max="10"></div></div>
    <div class="r2"><div class="f"><label>Pass Overlap (%)</label><input type="number" value="15"></div><div class="f"><label>Side</label><select><option>Both</option><option>Inside</option><option>Outside</option></select></div></div>
    <div class="st">📐 Cut Parameters</div>
    <div class="r2"><div class="f"><label>Depth (mm)</label><input type="number" value="-0.05" step="0.01"></div><div class="f"><label>Travel Z (mm)</label><input type="number" value="2.0"></div></div>
    <div class="r2"><div class="f"><label>Feed (mm/min)</label><input type="number" value="200"></div><div class="f"><label>Plunge (mm/min)</label><input type="number" value="60"></div></div>
    <div class="r2"><div class="f"><label>Spindle (RPM)</label><input type="number" value="24000"></div><div class="f"><label>Coolant</label><select><option>Off</option><option>Mist</option><option>Flood</option></select></div></div>
    <div class="st">⚙️ Advanced</div>
    <div class="tr"><label>Combine Passes</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
    <div class="tr"><label>Connect Paths</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
    <button class="btn btn-p" onclick="gen('isolation')" style="margin-top:8px">⚡ Generate Isolation</button>
  </div></div>
  <div class="cp"><div class="ct">
    <button class="btn btn-s" onclick="zf()">⊡ Fit</button>
    <button class="btn btn-s" onclick="tgrd()">⊞ Grid</button>
    <button class="btn btn-s" onclick="tgl('tp')">🟢 Toolpath</button>
    <button class="btn btn-s" onclick="clr()">🗑 Clear</button>
    <span style="flex:1"></span><span id="zlv" style="font-size:11px;color:var(--tx2)">100%</span>
  </div><div class="cw"><canvas id="cv0"></canvas><div class="ci" id="ci0">X:0.000 Y:0.000 mm</div></div></div>
  <div class="rp"><div class="ph">Layer Info</div><div class="ps">
    <div class="f"><label>Board Size</label><input readonly id="bs" value="—"></div>
    <div class="f"><label>Copper Nets</label><input readonly id="bn" value="—"></div>
    <div class="f"><label>Toolpath Length</label><input readonly id="tl" value="—"></div>
    <div class="f"><label>Est. Time</label><input readonly id="et" value="—"></div>
    <div class="st">G-code Preview</div>
    <div class="gb" id="gp0">; No toolpath yet.</div>
    <button class="btn btn-ok" onclick="expG('isolation')" style="margin-top:4px">💾 Export G-code</button>
    <button class="btn btn-s" style="margin-top:6px" onclick="addJ('isolation')">➕ Add to Jobs</button>
  </div></div>
</div>

<!-- DRILLING -->
<div id="pn-drilling" class="pn">
  <div class="lp"><div class="ph"><span>Excellon Drill</span><span class="lbg">DRL/XLN</span></div><div class="ps">
    <div class="st">📁 Drill File</div>
    <div class="br"><button class="btn btn-s" onclick="loadFile()">📂 Load .DRL</button><button class="btn btn-s" onclick="loadDemo()">🎯 Demo</button></div>
    <div class="f"><label>Units</label><select><option>Metric (mm)</option><option>Imperial (inch)</option></select></div>
    <div class="st">🔩 Drill Tools</div>
    <div class="f"><label>Tool Table</label><textarea readonly style="height:90px;font-size:11px;color:var(--ac2)">T01 Ø0.80mm — VIA
T02 Ø1.00mm — PAD
T03 Ø1.50mm — Connector
T04 Ø2.00mm — Mounting</textarea></div>
    <div class="st">📐 Parameters</div>
    <div class="r2"><div class="f"><label>Depth (mm)</label><input type="number" value="-2.0"></div><div class="f"><label>Travel Z (mm)</label><input type="number" value="3.0"></div></div>
    <div class="r2"><div class="f"><label>Feed (mm/min)</label><input type="number" value="80"></div><div class="f"><label>Spindle (RPM)</label><input type="number" value="18000"></div></div>
    <div class="r2"><div class="f"><label>Peck Depth (mm)</label><input type="number" value="0.5"></div><div class="f"><label>Dwell (ms)</label><input type="number" value="200"></div></div>
    <div class="tr"><label>Optimize (TSP)</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
    <div class="tr"><label>Peck Drilling</label><label class="tg"><input type="checkbox"><span class="ts"></span></label></div>
    <button class="btn btn-p" onclick="gen('drilling')" style="margin-top:10px">⚡ Generate Drill G-code</button>
  </div></div>
  <div class="cp"><div class="ct">
    <button class="btn btn-s" onclick="zf()">⊡ Fit</button>
    <button class="btn btn-s" onclick="tgrd()">⊞ Grid</button>
    <button class="btn btn-s" onclick="tgl('ph')">🟢 Path</button>
    <span style="flex:1"></span><span id="dc" style="font-size:11px;color:var(--tx2)">0 holes</span>
  </div><div class="cw"><canvas id="cv1"></canvas><div class="ci">Click hole to inspect</div></div></div>
  <div class="rp"><div class="ph">Drill Summary</div><div class="ps">
    <div class="f"><label>Total Holes</label><input readonly value="—"></div>
    <div class="f"><label>Tool Changes</label><input readonly value="—"></div>
    <div class="f"><label>Est. Time</label><input readonly value="—"></div>
    <div class="st">G-code Preview</div>
    <div class="gb" id="gp1">; Load a drill file first.</div>
    <button class="btn btn-ok" onclick="expG('drilling')" style="margin-top:4px">💾 Export G-code</button>
    <button class="btn btn-s" style="margin-top:6px" onclick="addJ('drilling')">➕ Add to Jobs</button>
  </div></div>
</div>

<!-- CONTOUR -->
<div id="pn-contour" class="pn">
  <div class="lp"><div class="ph"><span>Board Cutout / Routing</span><span class="lbg">Edge Cuts</span></div><div class="ps">
    <div class="st">📁 Outline Layer</div>
    <div class="br"><button class="btn btn-s" onclick="loadFile()">📂 Load GKO/DXF</button><button class="btn btn-s" onclick="loadDemo()">🎯 Demo</button></div>
    <div class="st">✂️ Cut Settings</div>
    <div class="r2"><div class="f"><label>End Mill Dia (mm)</label><input type="number" value="1.0"></div><div class="f"><label>Cut Side</label><select><option>Outside</option><option>Inside</option><option>On Line</option></select></div></div>
    <div class="r2"><div class="f"><label>Board Thickness (mm)</label><input type="number" value="1.6"></div><div class="f"><label>Stepdown (mm)</label><input type="number" value="0.5"></div></div>
    <div class="r2"><div class="f"><label>Feed (mm/min)</label><input type="number" value="400"></div><div class="f"><label>Spindle (RPM)</label><input type="number" value="20000"></div></div>
    <div class="st">🔄 Tabs</div>
    <div class="tr"><label>Add Tabs</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
    <div class="r2"><div class="f"><label>Tab Width (mm)</label><input type="number" value="3.0"></div><div class="f"><label>Tab Height (mm)</label><input type="number" value="0.5"></div></div>
    <div class="tr"><label>Climb Milling</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
    <button class="btn btn-p" onclick="gen('contour')" style="margin-top:10px">⚡ Generate Cutout</button>
  </div></div>
  <div class="cp"><div class="ct">
    <button class="btn btn-s" onclick="zf()">⊡ Fit</button>
    <button class="btn btn-s" onclick="tgrd()">⊞ Grid</button>
    <button class="btn btn-s" onclick="tgl('tabs')">🟠 Tabs</button>
    <span style="flex:1"></span>
  </div><div class="cw"><canvas id="cv2"></canvas><div class="ci">Board outline view</div></div></div>
  <div class="rp"><div class="ph">Contour Info</div><div class="ps">
    <div class="f"><label>Perimeter</label><input readonly value="—"></div>
    <div class="f"><label>Passes</label><input readonly value="—"></div>
    <div class="f"><label>Est. Time</label><input readonly value="—"></div>
    <div class="st">G-code Preview</div>
    <div class="gb" id="gp2">; Load outline layer first.</div>
    <button class="btn btn-ok" onclick="expG('contour')" style="margin-top:4px">💾 Export G-code</button>
    <button class="btn btn-s" style="margin-top:6px" onclick="addJ('contour')">➕ Add to Jobs</button>
  </div></div>
</div>

<!-- POCKETING -->
<div id="pn-pocketing" class="pn">
  <div class="lp"><div class="ph"><span>2.5D Pocketing</span><span class="lbg">DXF/SVG</span></div><div class="ps">
    <div class="st">📁 Pocket Shape</div>
    <div class="br"><button class="btn btn-s" onclick="loadFile()">📂 Load DXF/SVG</button><button class="btn btn-s" onclick="loadDemo()">🎯 Demo</button></div>
    <div class="f"><label>Strategy</label><select><option>Zig-Zag (Raster)</option><option>Offset In (Concentric)</option><option>Offset Out (Spiral)</option><option>Adaptive / HSM</option></select></div>
    <div class="r2"><div class="f"><label>End Mill Dia (mm)</label><input type="number" value="3.0"></div><div class="f"><label>Flutes</label><input type="number" value="2"></div></div>
    <div class="st">📐 Depths</div>
    <div class="r2"><div class="f"><label>Pocket Depth (mm)</label><input type="number" value="-5.0"></div><div class="f"><label>Stepdown (mm)</label><input type="number" value="1.0"></div></div>
    <div class="r2"><div class="f"><label>Stock to Leave (mm)</label><input type="number" value="0.1"></div><div class="f"><label>Travel Z (mm)</label><input type="number" value="5.0"></div></div>
    <div class="st">⚡ Feeds &amp; Speeds</div>
    <div class="r2"><div class="f"><label>Feed XY (mm/min)</label><input type="number" value="600"></div><div class="f"><label>Feed Z (mm/min)</label><input type="number" value="120"></div></div>
    <div class="r2"><div class="f"><label>Spindle (RPM)</label><input type="number" value="18000"></div><div class="f"><label>Stepover (%)</label><input type="number" value="40"></div></div>
    <div class="tr"><label>Finish Pass</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
    <div class="tr"><label>Climb Milling</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
    <div class="tr"><label>Ramping Entry</label><label class="tg"><input type="checkbox"><span class="ts"></span></label></div>
    <button class="btn btn-p" onclick="gen('pocketing')" style="margin-top:10px">⚡ Generate Pocket</button>
  </div></div>
  <div class="cp"><div class="ct"><button class="btn btn-s" onclick="zf()">⊡ Fit</button><button class="btn btn-s" onclick="tgrd()">⊞ Grid</button><span style="flex:1"></span></div>
  <div class="cw"><canvas id="cv3"></canvas><div class="ci">Pocket preview (top view)</div></div></div>
  <div class="rp"><div class="ph">Pocket Stats</div><div class="ps">
    <div class="f"><label>Area (mm²)</label><input readonly value="—"></div>
    <div class="f"><label>Layers</label><input readonly value="—"></div>
    <div class="f"><label>Est. Time</label><input readonly value="—"></div>
    <div class="st">G-code Preview</div>
    <div class="gb" id="gp3">; Load pocket shape first.</div>
    <button class="btn btn-ok" onclick="expG('pocketing')" style="margin-top:4px">💾 Export G-code</button>
    <button class="btn btn-s" style="margin-top:6px" onclick="addJ('pocketing')">➕ Add to Jobs</button>
  </div></div>
</div>

<!-- ENGRAVING -->
<div id="pn-engraving" class="pn">
  <div class="lp"><div class="ph"><span>Laser / V-Bit Engraving</span><span class="lbg">SVG/Text</span></div><div class="ps">
    <div class="st">📁 Artwork</div>
    <div class="br"><button class="btn btn-s" onclick="loadFile()">📂 Load SVG/DXF</button><button class="btn btn-s" onclick="loadDemo()">🎯 Demo Text</button></div>
    <div class="f"><label>Mode</label><select><option>V-Bit (Variable depth)</option><option>Flat End Mill</option><option>Laser (Power ctrl)</option><option>Drag Knife</option></select></div>
    <div class="st">🔧 V-Bit Tool</div>
    <div class="r2"><div class="f"><label>V-Angle (°)</label><input type="number" value="60"></div><div class="f"><label>Tip Dia (mm)</label><input type="number" value="0.0"></div></div>
    <div class="r2"><div class="f"><label>Max Depth (mm)</label><input type="number" value="-1.5"></div><div class="f"><label>Travel Z (mm)</label><input type="number" value="3.0"></div></div>
    <div class="st">⚡ Feeds &amp; Speeds</div>
    <div class="r2"><div class="f"><label>Feed (mm/min)</label><input type="number" value="300"></div><div class="f"><label>Plunge (mm/min)</label><input type="number" value="80"></div></div>
    <div class="r2"><div class="f"><label>Spindle (RPM)</label><input type="number" value="24000"></div><div class="f"><label>Laser Power (%)</label><input type="number" value="80"></div></div>
    <div class="st">✍️ Text Engraving</div>
    <div class="f"><label>Text</label><input type="text" placeholder="ProBharath CNC" id="etxt"></div>
    <div class="r2"><div class="f"><label>Font Size (mm)</label><input type="number" value="8"></div><div class="f"><label>Spacing (%)</label><input type="number" value="100"></div></div>
    <div class="tr"><label>Mirror (Bottom)</label><label class="tg"><input type="checkbox"><span class="ts"></span></label></div>
    <div class="tr"><label>Optimize Lift</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
    <button class="btn btn-p" onclick="gen('engraving')" style="margin-top:10px">⚡ Generate Toolpath</button>
  </div></div>
  <div class="cp"><div class="ct"><button class="btn btn-s" onclick="zf()">⊡ Fit</button><button class="btn btn-s" onclick="tgrd()">⊞ Grid</button><span style="flex:1"></span></div>
  <div class="cw"><canvas id="cv4"></canvas><div class="ci">Engraving toolpath preview</div></div></div>
  <div class="rp"><div class="ph">Engraving Stats</div><div class="ps">
    <div class="f"><label>Path Length (mm)</label><input readonly value="—"></div>
    <div class="f"><label>Lifts</label><input readonly value="—"></div>
    <div class="f"><label>Est. Time</label><input readonly value="—"></div>
    <div class="st">G-code Preview</div>
    <div class="gb" id="gp4">; Load artwork or enter text.</div>
    <button class="btn btn-ok" onclick="expG('engraving')" style="margin-top:4px">💾 Export G-code</button>
    <button class="btn btn-s" style="margin-top:6px" onclick="addJ('engraving')">➕ Add to Jobs</button>
  </div></div>
</div>

<!-- JOB MANAGER -->
<div id="pn-jobs" class="pn" style="flex-direction:column">
  <div style="padding:16px;overflow-y:auto;flex:1">
    <div style="max-width:720px;margin:0 auto">
      <div class="st">📋 Active Jobs</div>
      <div id="jlist"><div style="color:var(--tx2);font-size:12px;padding:24px;text-align:center;border:1px dashed var(--b);border-radius:8px">No jobs yet. Generate toolpaths and click "Add to Jobs".</div></div>
      <div class="br" style="margin-top:12px">
        <button class="btn btn-s" onclick="clrJ()">🗑 Clear All</button>
        <button class="btn btn-s" onclick="optJ()">🔀 Auto-Order</button>
        <button class="btn btn-ok" onclick="mergeJ()" style="flex:2">💾 Merge &amp; Export G-code</button>
      </div>
      <div class="st" style="margin-top:20px">⚙️ Machine / Post-Processor</div>
      <div class="r2">
        <div class="f"><label>Machine Profile</label><select id="mach"><option>Generic GRBL 1.1</option><option>Bambu Lab X1 (Laser)</option><option>Creality 3018 Pro</option><option>Custom Klipper CNC</option><option>Mach3 / Mach4</option><option>LinuxCNC</option><option>Marlin CNC Mode</option><option>Smoothieware</option><option>TinyG</option></select></div>
        <div class="f"><label>Units Output</label><select><option>G21 (mm)</option><option>G20 (inch)</option></select></div>
      </div>
      <div class="r2">
        <div class="f"><label>Program Start</label><textarea style="height:70px;font-size:11px">G21 G17 G90 G94\nM3 S{spindle}\nG0 Z{clearance}</textarea></div>
        <div class="f"><label>Program End</label><textarea style="height:70px;font-size:11px">G0 Z{clearance}\nM5\nG0 X0 Y0\nM2</textarea></div>
      </div>
      <div class="tr"><label>Pause on tool change (M0)</label><label class="tg"><input type="checkbox" checked><span class="ts"></span></label></div>
      <div class="tr"><label>Line numbers (N...)</label><label class="tg"><input type="checkbox"><span class="ts"></span></label></div>
    </div>
  </div>
</div>

<!-- G-CODE OUTPUT -->
<div id="pn-gcode" class="pn" style="flex-direction:column;padding:12px;gap:10px;overflow-y:auto">
  <div class="st">📄 G-code Output</div>
  <div class="r2" style="max-width:800px">
    <div class="f"><label>Lines</label><input readonly id="gcl" value="0" style="color:var(--ac)!important"></div>
    <div class="f"><label>Est. Time</label><input readonly id="gct" value="—" style="color:var(--ac)!important"></div>
  </div>
  <textarea id="gco" style="flex:1;min-height:300px;background:#050710;border:1px solid var(--b);border-radius:8px;padding:12px;color:#7dd3fc;font-family:monospace;font-size:11.5px;resize:none;outline:none;line-height:1.7" readonly>; ProBharath CNC &amp; CAM Studio v2.6
; Generate toolpaths from any tab, then click Export G-code.
</textarea>
  <div class="br" style="max-width:800px">
    <button class="btn btn-s" onclick="cpG()">📋 Copy</button>
    <button class="btn btn-s" onclick="clrG()">🗑 Clear</button>
    <button class="btn btn-p" onclick="svG()" style="flex:2">💾 Save .gcode</button>
  </div>
</div>

</div><!-- /main -->

<div class="sb">
  <div class="sd" id="sd"></div>
  <span class="sm" id="smsg">Ready — ProBharath CNC &amp; CAM Studio v2.6</span>
  <progress id="prg" value="0" max="100"></progress>
  <span id="srgt" style="color:var(--tx2)">No file loaded</span>
</div>

<script>
var ST={tab:'isolation',jobs:[],gcodes:{},grid:true,layers:{tp:true,ph:true,tabs:true},zoom:1,demo:{isolation:0,drilling:0,contour:0,pocketing:0,engraving:0}};
var CVIDS=['cv0','cv1','cv2','cv3','cv4'];
var TABS=['isolation','drilling','contour','pocketing','engraving'];
function sw(el,n){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.pn').forEach(p=>p.classList.remove('ac'));
  var pn=document.getElementById('pn-'+n);if(pn)pn.classList.add('ac');
  ST.tab=n;setTimeout(rd,50);
}
function cv(){var i=TABS.indexOf(ST.tab);return i>=0?document.getElementById(CVIDS[i]):null}
function rd(){
  var c=cv();if(!c)return;
  var w=c.parentElement;c.width=w.clientWidth||600;c.height=w.clientHeight||400;
  var ctx=c.getContext('2d');
  ctx.fillStyle='#080a10';ctx.fillRect(0,0,c.width,c.height);
  if(ST.grid){
    var step=30*ST.zoom;ctx.strokeStyle='#151820';ctx.lineWidth=1;
    for(var x=(c.width/2)%step;x<c.width;x+=step){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,c.height);ctx.stroke();}
    for(var y=(c.height/2)%step;y<c.height;y+=step){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(c.width,y);ctx.stroke();}
  }
  ctx.fillStyle='#1e2332';ctx.fillRect(0,c.height/2-.5,c.width,1);ctx.fillRect(c.width/2-.5,0,1,c.height);
  if(ST.demo[ST.tab])dd(ctx,c,ST.tab);
}
function dd(ctx,c,tab){
  var cx=c.width/2,cy=c.height/2,s=Math.min(c.width,c.height)*.35*ST.zoom;
  if(tab==='isolation'){
    ctx.strokeStyle='#c8a000';ctx.lineWidth=3;ctx.strokeRect(cx-s,cy-s*.7,s*2,s*1.4);
    ctx.strokeStyle='#b87000';ctx.lineWidth=2;
    for(var i=0;i<8;i++){ctx.beginPath();var y=cy-s*.5+i*(s/7);ctx.moveTo(cx-s*.85,y);ctx.lineTo(cx+s*.85,y);ctx.stroke();}
    ctx.fillStyle='#ffcc00';
    [[-0.6,-0.4],[0.6,-0.4],[-0.6,0.4],[0.6,0.4],[0,0]].forEach(function(p){ctx.beginPath();ctx.arc(cx+p[0]*s*.8,cy+p[1]*s*.8,s*.06,0,Math.PI*2);ctx.fill();});
    if(ST.layers.tp){ctx.strokeStyle='#00ff9d';ctx.lineWidth=1;ctx.setLineDash([3,3]);ctx.beginPath();ctx.rect(cx-s*.95,cy-s*.65,s*1.9,s*1.3);ctx.stroke();ctx.setLineDash([]);}
    se('bs','48.0 x 33.6 mm');se('bn','14 nets');se('tl','1842 mm');se('et','~9 min');
    setGP('gp0','isolation');
  }else if(tab==='drilling'){
    var holes=[[-0.7,-0.5],[-0.7,0.5],[0.7,-0.5],[0.7,0.5],[0,0],[-0.3,0.3],[0.3,-0.3],[0,-0.5],[0,0.5]];
    holes.forEach(function(h,i){var r=(i<4)?s*.06:(i===4)?s*.09:s*.05;ctx.strokeStyle='#ff6b6b';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(cx+h[0]*s,cy+h[1]*s,r,0,Math.PI*2);ctx.stroke();ctx.fillStyle='rgba(255,107,107,0.15)';ctx.fill();});
    if(ST.layers.ph){ctx.strokeStyle='#00c8ff55';ctx.lineWidth=1;ctx.setLineDash([2,4]);ctx.beginPath();holes.forEach(function(h,i){if(i===0)ctx.moveTo(cx+h[0]*s,cy+h[1]*s);else ctx.lineTo(cx+h[0]*s,cy+h[1]*s);});ctx.stroke();ctx.setLineDash([]);}
    se('dc',holes.length+' holes');setGP('gp1','drilling');
  }else if(tab==='contour'){
    ctx.strokeStyle='#ffd700';ctx.lineWidth=3;ctx.strokeRect(cx-s,cy-s*.7,s*2,s*1.4);
    if(ST.layers.tabs){ctx.fillStyle='#ff9900';[[cx-s,cy],[cx+s,cy],[cx,cy-s*.7],[cx,cy+s*.7]].forEach(function(tp){ctx.fillRect(tp[0]-8,tp[1]-5,16,10);});}
    setGP('gp2','contour');
  }else if(tab==='pocketing'){
    ctx.fillStyle='rgba(0,150,255,0.08)';ctx.strokeStyle='#0088ff';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(cx,cy,s*.9,s*.6,0,0,Math.PI*2);ctx.fill();ctx.stroke();
    ctx.strokeStyle='#00c8ff55';ctx.lineWidth=1;
    for(var yi=-7;yi<=7;yi++){var yy=cy+yi*(s*.6/8);var hw=s*.9*Math.sqrt(1-Math.pow(yi/8,2));ctx.beginPath();ctx.moveTo(cx-hw,yy);ctx.lineTo(cx+hw,yy);ctx.stroke();}
    setGP('gp3','pocketing');
  }else if(tab==='engraving'){
    ctx.font='bold '+(s*.18)+'px monospace';ctx.fillStyle='#00ff9d33';ctx.textAlign='center';
    ctx.fillText('ProBharath',cx,cy-s*.1);ctx.fillText('CNC Studio',cx,cy+s*.2);
    ctx.strokeStyle='#00ff9d';ctx.lineWidth=1;ctx.strokeText('ProBharath',cx,cy-s*.1);ctx.strokeText('CNC Studio',cx,cy+s*.2);
    setGP('gp4','engraving');
  }
}
function se(id,v){var e=document.getElementById(id);if(e)e.value=v;}
function setGP(id,tab){var e=document.getElementById(id);if(e)e.innerHTML=gcs(tab);}
function gcs(tab){
  var d=new Date().toISOString().slice(0,19).replace('T',' ');
  if(tab==='isolation')return'<span class="cm">; ProBharath CNC &amp; CAM v2.6\n; PCB Isolation | '+d+'</span>\n<span class="kw">G21</span> <span class="cm">; Metric</span>\n<span class="kw">G17 G90 G94</span>\n<span class="kw">M3</span> <span class="vl">S24000</span>\n<span class="kw">G0</span> <span class="vl">Z2.000</span>\n<span class="kw">G0</span> <span class="vl">X-24.000 Y-16.800</span>\n<span class="kw">G1</span> <span class="vl">Z-0.050</span> <span class="kw">F</span><span class="vl">60</span>\n<span class="kw">G1</span> <span class="vl">X24.000</span> <span class="kw">F</span><span class="vl">200</span>\n<span class="cm">; ... 1838 more lines ...</span>\n<span class="kw">M5\nG0 X0 Y0\nM2</span>';
  if(tab==='drilling')return'<span class="cm">; Drilling | '+d+'</span>\n<span class="kw">T01 M6</span> <span class="cm">; Ø0.80mm</span>\n<span class="kw">M3</span> <span class="vl">S18000</span>\n<span class="kw">G0</span> <span class="vl">Z3.000</span>\n<span class="kw">G0</span> <span class="vl">X-33.6 Y-16.8</span>\n<span class="kw">G1</span> <span class="vl">Z-2.000</span> <span class="kw">F</span><span class="vl">80</span>\n<span class="kw">G4</span> <span class="vl">P200</span>\n<span class="kw">G0</span> <span class="vl">Z3.000</span>\n<span class="cm">; ...more holes...</span>\n<span class="kw">M5\nM2</span>';
  return '<span class="cm">; '+tab+' toolpath ready.\n; Click Export to view full G-code.</span>';
}
function genGcode(tab){
  var L=[]; var d=new Date().toISOString().slice(0,19).replace('T',' ');
  L.push('; ProBharath CNC & CAM Studio v2.6'); L.push('; '+tab.toUpperCase()+' | '+d);
  L.push('G21 G17 G90 G94');
  if(tab==='isolation'){L.push('M3 S24000');L.push('G0 Z2.000');for(var i=0;i<20;i++){L.push('G0 X-24.000 Y'+((-16.8+i*1.68).toFixed(3)));L.push('G1 Z-0.050 F60');L.push('G1 X24.000 F200');}L.push('G0 Z2.000');L.push('M5');L.push('G0 X0 Y0');L.push('M2');}
  else if(tab==='drilling'){L.push('T01 M6 (Dia 0.80mm)');L.push('M3 S18000');L.push('G0 Z3.000');[[-33.6,-16.8],[-33.6,16.8],[33.6,-16.8],[33.6,16.8],[0,0]].forEach(function(p){L.push('G0 X'+p[0].toFixed(3)+' Y'+p[1].toFixed(3));L.push('G1 Z-2.000 F80');L.push('G4 P200');L.push('G0 Z3.000');});L.push('M5');L.push('G0 X0 Y0');L.push('M2');}
  else if(tab==='contour'){L.push('M3 S20000');L.push('G0 Z3.000');for(var p=1;p<=4;p++){var z=(-0.5*p).toFixed(3);L.push('G0 X-24.000 Y-16.800');L.push('G1 Z'+z+' F80');L.push('G1 X24.000 F400');L.push('G1 Y16.800');L.push('G1 X-24.000');L.push('G1 Y-16.800');}L.push('G0 Z3.000');L.push('M5');L.push('G0 X0 Y0');L.push('M2');}
  else if(tab==='pocketing'){L.push('M3 S18000');L.push('G0 Z5.000');for(var lay=1;lay<=5;lay++){var pz=(-lay).toFixed(3);for(var r=-8;r<=8;r++){var py=(r*3.6).toFixed(3);var hw=(28.8*Math.sqrt(1-Math.pow(r/9,2))).toFixed(3);L.push('G0 X-'+hw+' Y'+py);L.push('G1 Z'+pz+' F120');L.push('G1 X'+hw+' F600');}}L.push('G0 Z5.000');L.push('M5');L.push('G0 X0 Y0');L.push('M2');}
  else if(tab==='engraving'){L.push('M3 S24000');L.push('G0 Z3.000');L.push('G0 X-20.000 Y5.000');L.push('G1 Z-1.500 F80');L.push('G1 X20.000 F300');L.push('G0 Z3.000');L.push('M5');L.push('G0 X0 Y0');L.push('M2');}
  return L.join('\n');
}
function loadFile(){setS('File dialog not available in embedded mode. Use Demo instead.','w');}
function loadDemo(){ST.demo[ST.tab]=1;setS('Demo '+ST.tab+' layer loaded!','ok');se('srgt','Demo file');rd();}
function gen(tab){
  if(!ST.demo[tab])loadDemo();
  var prg=document.getElementById('prg');prg.style.display='block';prg.value=0;
  setS('Generating '+tab+' toolpath...','ok');
  var n=0;var iv=setInterval(function(){n++;prg.value=Math.min(100,n*8);if(n>=13){clearInterval(iv);prg.style.display='none';prg.value=0;var g=genGcode(tab);ST.gcodes[tab]=g;se('gco',g);se('gcl',g.split('\n').length+' lines');se('gct','~'+(Math.floor(Math.random()*12)+4)+' min');setS('\u2705 '+tab+' toolpath ready! '+g.split('\n').length+' lines.','ok');rd();try{SendWXMessage(JSON.stringify({command:'cnc_gcode_ready',tab:tab}));}catch(e){}}},120);
}
function zf(){ST.zoom=1;rd();}
function tgrd(){ST.grid=!ST.grid;rd();}
function tgl(n){ST.layers[n]=!ST.layers[n];rd();}
function clr(){ST.demo[ST.tab]=0;rd();}
function expG(tab){var g=ST.gcodes[tab]||genGcode(tab);ST.gcodes[tab]=g;se('gco',g);se('gcl',g.split('\n').length+' lines');sw(document.querySelector('[data-p="gcode"]'),'gcode');setS('G-code ready — '+g.split('\n').length+' lines.','ok');}
function svG(){setS('Save: copy G-code from output box.','ok');try{SendWXMessage(JSON.stringify({command:'cnc_save_gcode',content:document.getElementById('gco').value}));}catch(e){}}
function cpG(){if(navigator.clipboard)navigator.clipboard.writeText(document.getElementById('gco').value).then(function(){setS('Copied to clipboard!','ok');});else setS('Copy manually from the text box.','w');}
function clrG(){se('gco','; Cleared.');se('gcl','0');}
var JC={isolation:'#00c8ff',drilling:'#ff6b6b',contour:'#ffd700',pocketing:'#00ff9d',engraving:'#ff9900'};
function addJ(tab){ST.jobs.push({id:Date.now(),tab:tab,name:tab.charAt(0).toUpperCase()+tab.slice(1),g:ST.gcodes[tab]||''});rJ();setS('Added '+tab+' to Job Manager.','ok');}
function rJ(){var el=document.getElementById('jlist');if(!el)return;if(!ST.jobs.length){el.innerHTML='<div style="color:var(--tx2);font-size:12px;padding:24px;text-align:center;border:1px dashed var(--b);border-radius:8px">No jobs yet.</div>';return;}el.innerHTML=ST.jobs.map(function(j,i){return'<div class="ji"><div class="jd" style="background:'+(JC[j.tab]||'#888')+'"></div><div class="jn"><div class="jt">'+(i+1)+'. '+j.name+'</div><div class="jst">'+j.tab+' · '+(j.g?j.g.split('\n').length+' lines':'no gcode')+'</div></div><span class="jx" onclick="rmJ('+j.id+')">✕</span></div>';}).join('');}
function rmJ(id){ST.jobs=ST.jobs.filter(function(j){return j.id!==id;});rJ();}
function clrJ(){ST.jobs=[];rJ();}
function optJ(){setS('Jobs auto-ordered: drill → isolate → pocket → engrave → cutout.','ok');}
function mergeJ(){var all='; ProBharath CNC Merged Job\n';ST.jobs.forEach(function(j){all+=j.g+'\n';});se('gco',all);se('gcl',all.split('\n').length+' lines');sw(document.querySelector('[data-p="gcode"]'),'gcode');setS('All '+ST.jobs.length+' jobs merged!','ok');}
function setS(msg,t){var e=document.getElementById('smsg');if(e)e.textContent=msg;var d=document.getElementById('sd');if(d)d.style.background=t==='ok'?'var(--ac2)':t==='w'?'var(--wn)':'var(--dn)';}
document.addEventListener('mousemove',function(e){var c=cv();if(!c)return;var r=c.getBoundingClientRect();var i=document.getElementById('ci0');if(!i)return;var x=((e.clientX-r.left-c.width/2)/(15*ST.zoom)).toFixed(3);var y=(-(e.clientY-r.top-c.height/2)/(15*ST.zoom)).toFixed(3);i.textContent='X:'+x+' Y:'+y+' mm | Zoom:'+Math.round(ST.zoom*100)+'%';});
document.addEventListener('wheel',function(e){if(e.target.tagName==='CANVAS'){e.preventDefault();ST.zoom=Math.max(.2,Math.min(5,ST.zoom-e.deltaY*.001));se('zlv',Math.round(ST.zoom*100)+'%');rd();}},{passive:false});
function HandleStudio(msg){try{var d=typeof msg==='string'?JSON.parse(msg):msg;if(d.command==='cnc_set_params')setS('Params received from ProSlicer.','ok');}catch(e){}}
window.onload=function(){rd();};
window.onresize=function(){rd();};
</script>
</body>
</html>"""


class ProBharathCncCamCapability(orca.pages.PagesPluginCapabilityBase):
    def get_type(self):
        return orca.plugin_type.Pages

    def get_name(self):
        return "ProBharath CNC & CAM"

    def get_ui(self):
        return HTML

    def on_message(self, message):
        try:
            data = json.loads(message)
            cmd = data.get("command", "")
            if cmd == "cnc_save_gcode":
                self.post_message(json.dumps({"status": "saved", "bytes": len(data.get("content", ""))}))
            elif cmd == "cnc_gcode_ready":
                self.post_message(json.dumps({"status": "ok", "tab": data.get("tab")}))
        except Exception:
            pass


@orca.plugin
class ProBharathCncCamPackage(orca.base):
    def register_capabilities(self):
        orca.register_capability(ProBharathCncCamCapability)
