// stl.js

function generateBinarySTL(grid, wPx, hPx, wMm, hMm, thickness, transform = null, flipWinding = false) {
  const dx = wMm / wPx;
  const dy = hMm / hPx;
  const th = thickness;
  
  const triangles = [];
  
  function addQuad(p1, p2, p3, p4, n) {
    if (transform) {
      p1 = transform(p1);
      p2 = transform(p2);
      p3 = transform(p3);
      p4 = transform(p4);
      // Transform normal (simplified: assume orthogonal transformations without scaling)
      const origin = transform([0,0,0]);
      const nt = transform(n);
      n = [nt[0]-origin[0], nt[1]-origin[1], nt[2]-origin[2]];
    }
    
    if (flipWinding) {
      triangles.push({n:n, v1:p1, v2:p4, v3:p3});
      triangles.push({n:n, v1:p1, v2:p3, v3:p2});
    } else {
      triangles.push({n:n, v1:p1, v2:p2, v3:p3});
      triangles.push({n:n, v1:p1, v2:p3, v3:p4});
    }
  }
  
  function getGrid(u, v) {
    if (u < 0 || u >= wPx || v < 0 || v >= hPx) return 0; // treat outside as empty space
    return grid[v * wPx + u];
  }
  
  // We want to generate a frame around the panel so it holds together even if cutouts touch the edges.
  // Actually, let's treat pixels outside the boundary as solid if they are meant to be a frame.
  // But for now, just mesh the grid.
  
  for (let v = 0; v < hPx; v++) {
    for (let u = 0; u < wPx; u++) {
      if (getGrid(u, v) === 1) { // Solid
        const x0 = u * dx;
        const x1 = (u + 1) * dx;
        const y0 = v * dy;
        const y1 = (v + 1) * dy;
        
        // p1: (x0, y0, 0), p2: (x1, y0, 0), p3: (x1, y1, 0), p4: (x0, y1, 0)
        // bottom face (Z=0)
        addQuad(
          [x0, y1, 0], [x1, y1, 0], [x1, y0, 0], [x0, y0, 0],
          [0, 0, -1]
        );
        
        // top face (Z=th)
        addQuad(
          [x0, y0, th], [x1, y0, th], [x1, y1, th], [x0, y1, th],
          [0, 0, 1]
        );
        
        // Left face (if neighbor is empty)
        if (getGrid(u - 1, v) === 0) {
          addQuad(
            [x0, y1, 0], [x0, y0, 0], [x0, y0, th], [x0, y1, th],
            [-1, 0, 0]
          );
        }
        // Right face
        if (getGrid(u + 1, v) === 0) {
          addQuad(
            [x1, y0, 0], [x1, y1, 0], [x1, y1, th], [x1, y0, th],
            [1, 0, 0]
          );
        }
        // Front face (v-1)
        if (getGrid(u, v - 1) === 0) {
          addQuad(
            [x0, y0, 0], [x1, y0, 0], [x1, y0, th], [x0, y0, th],
            [0, -1, 0]
          );
        }
        // Back face (v+1)
        if (getGrid(u, v + 1) === 0) {
          addQuad(
            [x1, y1, 0], [x0, y1, 0], [x0, y1, th], [x1, y1, th],
            [0, 1, 0]
          );
        }
      }
    }
  }
  
  // Write to binary STL
  const buffer = new ArrayBuffer(80 + 4 + triangles.length * 50);
  const view = new DataView(buffer);
  
  // 80 byte header
  for (let i = 0; i < 80; i++) {
    view.setUint8(i, 0); 
  }
  
  // Number of triangles
  view.setUint32(80, triangles.length, true); // little-endian
  
  let offset = 84;
  for (const tri of triangles) {
    // normal
    view.setFloat32(offset, tri.n[0], true); offset += 4;
    view.setFloat32(offset, tri.n[1], true); offset += 4;
    view.setFloat32(offset, tri.n[2], true); offset += 4;
    
    // v1
    view.setFloat32(offset, tri.v1[0], true); offset += 4;
    view.setFloat32(offset, tri.v1[1], true); offset += 4;
    view.setFloat32(offset, tri.v1[2], true); offset += 4;
    
    // v2
    view.setFloat32(offset, tri.v2[0], true); offset += 4;
    view.setFloat32(offset, tri.v2[1], true); offset += 4;
    view.setFloat32(offset, tri.v2[2], true); offset += 4;
    
    // v3
    view.setFloat32(offset, tri.v3[0], true); offset += 4;
    view.setFloat32(offset, tri.v3[1], true); offset += 4;
    view.setFloat32(offset, tri.v3[2], true); offset += 4;
    
    // attribute byte count
    view.setUint16(offset, 0, true); offset += 2;
  }
  
  return { triangles: triangles, buffer: buffer };
}

function saveSTL(buffer, filename) {
  const blob = new Blob([buffer], { type: 'application/octet-stream' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function downloadSTL(panelType) {
  if (!State.panels[panelType].grid) {
    alert("Please load an image first.");
    return;
  }
  
  const panel = State.panels[panelType];
  const thickness = parseFloat(document.getElementById('panel-t').value);
  
  const result = generateBinarySTL(panel.grid, panel.wPx, panel.hPx, panel.wMm, panel.hMm, thickness);
  saveSTL(result.buffer, `shadow_lamp_${panelType}.stl`);
}

function exportAllSTL() {
  if (!State.panels.top.grid) {
    alert("Please load an image first.");
    return;
  }
  
  const thickness = parseFloat(document.getElementById('panel-t').value);
  const zip = new JSZip();
  
  ['top', 'bottom', 'left', 'right'].forEach(panelType => {
    const panel = State.panels[panelType];
    const result = generateBinarySTL(panel.grid, panel.wPx, panel.hPx, panel.wMm, panel.hMm, thickness);
    zip.file(`shadow_lamp_${panelType}.stl`, result.buffer);
  });
  
  zip.generateAsync({type:"blob"}).then(function(content) {
    const url = URL.createObjectURL(content);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'shadow_lamp_panels.zip';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  });
}

function exportAssembledBox() {
  if (!State.panels.top.grid) {
    alert("Please load an image first.");
    return;
  }
  const thickness = parseFloat(document.getElementById('panel-t').value);
  const params = getParams();
  
  const transforms = {
    'top': {
      fn: p => [p[0], params.boxH - thickness + p[2], p[1]],
      flip: true
    },
    'bottom': {
      fn: p => [p[0], thickness - p[2], p[1]],
      flip: false
    },
    'left': {
      fn: p => [thickness - p[2], p[1], p[0]],
      flip: false
    },
    'right': {
      fn: p => [params.boxW - thickness + p[2], p[1], p[0]],
      flip: true
    }
  };
  
  let allTriangles = [];
  ['top', 'bottom', 'left', 'right'].forEach(panelType => {
    const panel = State.panels[panelType];
    const t = transforms[panelType];
    const result = generateBinarySTL(panel.grid, panel.wPx, panel.hPx, panel.wMm, panel.hMm, thickness, t.fn, t.flip);
    allTriangles = allTriangles.concat(result.triangles);
  });
  
  // Create binary STL from allTriangles
  const buffer = new ArrayBuffer(80 + 4 + allTriangles.length * 50);
  const view = new DataView(buffer);
  
  // Header
  for (let i = 0; i < 80; i++) view.setUint8(i, 0);
  view.setUint32(80, allTriangles.length, true);
  
  let offset = 84;
  for (const tri of allTriangles) {
    view.setFloat32(offset, tri.n[0], true); offset += 4;
    view.setFloat32(offset, tri.n[1], true); offset += 4;
    view.setFloat32(offset, tri.n[2], true); offset += 4;
    view.setFloat32(offset, tri.v1[0], true); offset += 4;
    view.setFloat32(offset, tri.v1[1], true); offset += 4;
    view.setFloat32(offset, tri.v1[2], true); offset += 4;
    view.setFloat32(offset, tri.v2[0], true); offset += 4;
    view.setFloat32(offset, tri.v2[1], true); offset += 4;
    view.setFloat32(offset, tri.v2[2], true); offset += 4;
    view.setFloat32(offset, tri.v3[0], true); offset += 4;
    view.setFloat32(offset, tri.v3[1], true); offset += 4;
    view.setFloat32(offset, tri.v3[2], true); offset += 4;
    view.setUint16(offset, 0, true); offset += 2;
  }
  
  saveSTL(buffer, 'shadow_lamp_assembled.stl');
}
