// app.js

document.addEventListener('DOMContentLoaded', () => {
  // Init
  loadDemoImage('probharath');
  
  // Theme from localStorage
  const savedTheme = localStorage.getItem('shadowTheme') || 'dark';
  setTheme(savedTheme);
});

function switchTab(tab) {
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('btn-' + tab).classList.add('active');
  
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
  
  if (tab === 'preview') {
    drawPreviewRoom();
  }
}

function setTheme(theme) {
  document.body.className = 'theme-' + theme;
  localStorage.setItem('shadowTheme', theme);
}

function updateParam(id, valId, val) {
  if (valId) {
    const el = document.getElementById(valId);
    if (el) el.innerText = val;
  }
  if (State.img) {
    rebuildProjection();
  }
}

function updateDual(baseId, val) {
  const slider = document.getElementById(baseId + '-slider');
  const num = document.getElementById(baseId);
  if (slider && slider.value !== val) slider.value = val;
  if (num && num.value !== val) num.value = val;
  if (State.img) {
    rebuildProjection();
  }
}

function updateThreshold(val) {
  document.getElementById('threshold-val').innerText = val;
  if (State.img) {
    processSourceImage();
  }
}

function setStatus(text) {
  document.getElementById('status-text').innerText = text;
}

function handleFileUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  
  setStatus("Loading image: " + file.name);
  
  const reader = new FileReader();
  reader.onload = (event) => {
    const img = new Image();
    img.onload = () => {
      State.img = img;
      processSourceImage();
      setStatus("Image loaded. Geometry updated.");
    };
    img.src = event.target.result;
  };
  reader.readAsDataURL(file);
}

function loadDemoImage(key) {
  setStatus("Loading demo: " + key);
  
  if (['einstein', 'shiva', 'car', 'rocket', 'samurai', 'lotus', 'cityscape', 'wolf', 'probharath'].includes(key)) {
    const img = new Image();
    img.onload = () => {
      State.img = img;
      processSourceImage();
      setStatus("Demo loaded. Ready to export.");
    };
    img.src = 'img/' + key + '.jpg?v=' + new Date().getTime();
    return;
  }
  
  const svgStr = getDemoImage(key);
  const blob = new Blob([svgStr], {type: 'image/svg+xml;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  
  const img = new Image();
  img.onload = () => {
    State.img = img;
    processSourceImage();
    URL.revokeObjectURL(url);
    setStatus("Demo loaded. Ready to export.");
  };
  img.src = url;
}

let isLightOn = true;
function toggleLight() {
  isLightOn = !isLightOn;
  
  const btn = document.getElementById('toggle-light-btn');
  if (btn) {
    btn.innerHTML = isLightOn ? '💡 Light is ON' : '🌑 Light is OFF';
    if (isLightOn) btn.classList.add('active');
    else btn.classList.remove('active');
  }
  
  const led = document.getElementById('lamp-led');
  if (isLightOn) {
    led.style.boxShadow = '0 0 20px 8px rgba(255,240,200,0.9)';
    led.style.background = '#fff';
    led.style.animation = 'glow-pulse 1.5s infinite';
  } else {
    led.style.boxShadow = 'none';
    led.style.background = '#333';
    led.style.animation = 'none';
  }
  
  drawPreviewRoom();
}

function drawPreviewRoom() {
  const canvas = document.getElementById('canvas-wall-preview');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  if (!isLightOn) return;
  
  if (!State.img) return;
  
  // To draw the preview, we just draw the processed silhouette canvas,
  // scaled and colored with a bright yellow/white glow.
  
  const silCanvas = document.getElementById('canvas-sil');
  
  ctx.save();
  // Draw glow background
  const grad = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 0, canvas.width/2, canvas.height/2, 300);
  grad.addColorStop(0, 'rgba(255, 230, 150, 0.15)');
  grad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0,0,canvas.width, canvas.height);
  
  // We want to tint the silhouette image to yellow glow.
  // We can use globalCompositeOperation
  
  // Calculate size on wall
  const params = getParams();
  const baseSize = 3 * params.boxW * (params.wallD / params.boxD); 
  const physicalW = baseSize * params.scale;
  const physicalH = (State.imgH / State.imgW) * physicalW;
  
  // Map physical mm to preview pixels (let's say preview height is 1000mm)
  const scaleToPreview = canvas.height / 1000;
  
  const w = physicalW * scaleToPreview;
  const h = physicalH * scaleToPreview;
  
  const x = canvas.width/2 - w/2; // centered
  const y = canvas.height/2 - h/2;
  
  // Draw tint
  ctx.globalAlpha = 0.8;
  ctx.drawImage(silCanvas, x, y, w, h);
  
  // Apply color tint (Source-Atop)
  ctx.globalCompositeOperation = 'source-atop';
  ctx.fillStyle = '#ffe680';
  ctx.fillRect(x, y, w, h);
  
  // Reset
  ctx.globalCompositeOperation = 'source-over';
  
  // Add some blur/bloom
  ctx.filter = 'blur(4px)';
  ctx.globalAlpha = 0.5;
  ctx.drawImage(silCanvas, x, y, w, h);
  ctx.globalCompositeOperation = 'source-atop';
  ctx.fillStyle = '#ffaa00';
  ctx.fillRect(x, y, w, h);
  
  ctx.restore();
}
