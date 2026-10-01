// engine.js

const State = {
  img: null,
  srcData: null, // thresholded source data
  imgW: 0,
  imgH: 0,
  panels: {
    top: { ctx: null, data: null, paths: [] },
    bottom: { ctx: null, data: null, paths: [] },
    left: { ctx: null, data: null, paths: [] },
    right: { ctx: null, data: null, paths: [] },
  }
};

const DPI = 4; // pixels per mm for processing

// Get UI params
function getParams() {
  return {
    boxW: parseFloat(document.getElementById('box-w').value),
    boxH: parseFloat(document.getElementById('box-h').value),
    boxD: parseFloat(document.getElementById('box-d').value),
    ledX: parseFloat(document.getElementById('led-x').value),
    ledY: parseFloat(document.getElementById('led-y').value),
    wallD: parseFloat(document.getElementById('wall-d').value),
    scale: parseFloat(document.getElementById('img-scale').value),
    thresh: parseInt(document.getElementById('threshold').value),
    invert: document.getElementById('invert-toggle').checked
  };
}

function processSourceImage() {
  if (!State.img) return;
  const canvas = document.getElementById('canvas-src');
  const ctx = canvas.getContext('2d');
  
  // Fit image into canvas maintaining aspect ratio
  const maxDim = 280;
  let w = State.img.width || 100;
  let h = State.img.height || 100;
  if (w > h) {
    h = Math.round((h / w) * maxDim);
    w = maxDim;
  } else {
    w = Math.round((w / h) * maxDim);
    h = maxDim;
  }
  
  State.imgW = w;
  State.imgH = h;
  
  canvas.width = w;
  canvas.height = h;
  ctx.drawImage(State.img, 0, 0, w, h);
  
  const imgData = ctx.getImageData(0, 0, w, h);
  const data = imgData.data;
  const { thresh, invert } = getParams();
  
  // Create thresholded silhouette canvas
  const silCanvas = document.getElementById('canvas-sil');
  silCanvas.width = w;
  silCanvas.height = h;
  const silCtx = silCanvas.getContext('2d');
  const silData = silCtx.createImageData(w, h);
  
  const bwData = new Uint8Array(w * h); // 1 for solid (shadow), 0 for cutout (light)
  
  for (let i = 0; i < data.length; i += 4) {
    // grayscale luminance
    const lum = 0.299 * data[i] + 0.587 * data[i+1] + 0.114 * data[i+2];
    
    // Is it light or shadow?
    let isLight = lum > thresh;
    // For alpha, if transparent, treat as shadow or light? Treat as background (light)
    if (data[i+3] < 128) {
      isLight = true;
    }
    
    if (invert) isLight = !isLight;
    
    const val = isLight ? 255 : 0;
    silData.data[i] = val;
    silData.data[i+1] = val;
    silData.data[i+2] = val;
    silData.data[i+3] = 255;
    
    // In our model: 1 = solid panel (shadow), 0 = empty space (cutout/light)
    bwData[i/4] = isLight ? 0 : 1; 
  }
  
  silCtx.putImageData(silData, 0, 0);
  State.srcData = bwData;
  
  rebuildProjection();
}

function rebuildProjection() {
  if (!State.srcData) return;
  const params = getParams();
  
  // Wall size of the image (in mm)
  // Let's base the base scale such that scale=1.0 makes the image fit roughly inside the box projection on the wall
  const baseSize = 3 * params.boxW * (params.wallD / params.boxD);
  const physicalW = baseSize * params.scale;
  const physicalH = (State.imgH / State.imgW) * physicalW;
  
  // Generate each panel
  generatePanel('top', params, physicalW, physicalH);
  generatePanel('bottom', params, physicalW, physicalH);
  generatePanel('left', params, physicalW, physicalH);
  generatePanel('right', params, physicalW, physicalH);
  
  updateStats();
  drawPreviewRoom();
}

// Map from panel UV (in pixels) to 3D world coordinate
function getPanelWorldCoord(panelType, u, v, wPx, hPx, params) {
  let x, y, z;
  const { boxW, boxH, boxD } = params;
  
  // u, v are pixel coordinates [0..wPx), [0..hPx)
  // For top/bottom panels: u maps to X, v maps to Z
  // For left/right panels: u maps to Z, v maps to Y
  
  if (panelType === 'top') {
    x = -boxW/2 + (u / wPx) * boxW;
    z = (v / hPx) * boxD;
    y = boxH/2;
  } else if (panelType === 'bottom') {
    x = -boxW/2 + (u / wPx) * boxW;
    z = (v / hPx) * boxD;
    y = -boxH/2;
  } else if (panelType === 'left') {
    z = (u / wPx) * boxD;
    y = boxH/2 - (v / hPx) * boxH;
    x = -boxW/2;
  } else if (panelType === 'right') {
    z = (u / wPx) * boxD;
    y = boxH/2 - (v / hPx) * boxH;
    x = boxW/2;
  }
  return {x, y, z};
}

function generatePanel(panelType, params, physW, physH) {
  const { boxW, boxH, boxD, ledX, ledY, wallD } = params;
  
  let wMm, hMm;
  if (panelType === 'top' || panelType === 'bottom') {
    wMm = boxW; hMm = boxD;
  } else {
    wMm = boxD; hMm = boxH;
  }
  
  const wPx = Math.ceil(wMm * DPI);
  const hPx = Math.ceil(hMm * DPI);
  
  let shortName = panelType;
  if (panelType === 'bottom') shortName = 'bot';
  if (panelType === 'left') shortName = 'lft';
  if (panelType === 'right') shortName = 'rgt';
  
  const canvas = document.getElementById('canvas-' + shortName);
  canvas.width = wPx;
  canvas.height = hPx;
  const ctx = canvas.getContext('2d');
  const imgData = ctx.createImageData(wPx, hPx);
  
  const grid = new Uint8Array(wPx * hPx);
  
  for (let v = 0; v < hPx; v++) {
    for (let u = 0; u < wPx; u++) {
      const idx = (v * wPx + u);
      const pxIdx = idx * 4;
      
      const {x, y, z} = getPanelWorldCoord(panelType, u, v, wPx, hPx, params);
      
      // Ray from (ledX, ledY, 0) through (x, y, z)
      if (z <= 0.1) {
        // Too close to light, solid
        grid[idx] = 1;
        setPixel(imgData.data, pxIdx, 0,0,0);
        continue;
      }
      
      const t = wallD / z;
      const wallX = ledX + t * (x - ledX);
      const wallY = ledY + t * (y - ledY);
      
      // Map wall intersection to source image coordinates
      const imgU = Math.floor((wallX / physW + 0.5) * State.imgW);
      const imgV = Math.floor((-wallY / physH + 0.5) * State.imgH);
      
      if (imgU >= 0 && imgU < State.imgW && imgV >= 0 && imgV < State.imgH) {
        const srcVal = State.srcData[imgV * State.imgW + imgU];
        grid[idx] = srcVal;
        const col = srcVal === 1 ? 0 : 255;
        setPixel(imgData.data, pxIdx, col, col, col);
      } else {
        // Outside the image is solid shadow
        grid[idx] = 1;
        setPixel(imgData.data, pxIdx, 0, 0, 0);
      }
    }
  }
  
  const bridgeMm = parseFloat(document.getElementById('bridge-w').value) || 1.5;
  const bridgePx = Math.ceil(bridgeMm * DPI);
  
  // Enforce solid border frame so panel holds together
  for (let v = 0; v < hPx; v++) {
    for (let u = 0; u < wPx; u++) {
      if (u < bridgePx || u >= wPx - bridgePx || v < bridgePx || v >= hPx - bridgePx) {
        const idx = (v * wPx + u);
        grid[idx] = 1;
        const pxIdx = idx * 4;
        setPixel(imgData.data, pxIdx, 0, 0, 0);
      }
    }
  }

  ctx.putImageData(imgData, 0, 0);
  
  // Also draw to export canvas
  const expCanvas = document.getElementById('exp-canvas-' + shortName);
  expCanvas.width = wPx;
  expCanvas.height = hPx;
  expCanvas.getContext('2d').putImageData(imgData, 0, 0);
  document.getElementById('exp-' + shortName + '-dim').innerText = `${wMm} × ${hMm} mm`;
  
  // Extract paths using Marching Squares
  State.panels[panelType].paths = extractPaths(grid, wPx, hPx, wMm, hMm);
  State.panels[panelType].grid = grid;
  State.panels[panelType].wPx = wPx;
  State.panels[panelType].hPx = hPx;
  State.panels[panelType].wMm = wMm;
  State.panels[panelType].hMm = hMm;
}

function setPixel(data, i, r, g, b) {
  data[i] = r; data[i+1] = g; data[i+2] = b; data[i+3] = 255;
}

// Very basic Marching Squares implementation to get vector contours from the grid
function extractPaths(grid, wPx, hPx, wMm, hMm) {
  // We'll use a simpler boundary tracing since Marching Squares implementation is lengthy.
  // Instead, since we need STL, we can just generate a voxel/quad mesh directly in stl.js 
  // or return the grid. But returning the grid is easiest and most robust for 3D extrusion.
  return []; 
}

function updateStats() {
  const params = getParams();
  document.getElementById('stat-ratio').innerText = (params.wallD / params.boxD).toFixed(1) + '×';
  
  const baseW = params.boxW * (params.wallD / params.boxD);
  const baseH = params.boxH * (params.wallD / params.boxD);
  
  document.getElementById('stat-sw').innerText = Math.round(baseW) + ' mm';
  document.getElementById('stat-sh').innerText = Math.round(baseH) + ' mm';
}
