const { JSDOM } = require("jsdom");
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const engineJs = fs.readFileSync('engine.js', 'utf8');

const dom = new JSDOM(html, { runScripts: "outside-only" });
const window = dom.window;

// Mock canvas API
window.HTMLCanvasElement.prototype.getContext = function () {
  return {
    createImageData: (w, h) => ({ data: new Uint8Array(w * h * 4) }),
    getImageData: (x, y, w, h) => {
      // Mock an image that has some pixels
      const data = new Uint8Array(w * h * 4);
      for(let i=0; i<w*h*4; i+=4) {
        // Draw a white circle in the middle
        const px = (i/4) % w;
        const py = Math.floor((i/4) / w);
        const dist = Math.hypot(px - w/2, py - h/2);
        if (dist < w/3) {
          data[i] = 255; data[i+1] = 255; data[i+2] = 255; data[i+3] = 255;
        } else {
          data[i] = 0; data[i+1] = 0; data[i+2] = 0; data[i+3] = 255;
        }
      }
      return { data };
    },
    putImageData: (imgData) => {
      // Check if it's all black
      let allBlack = true;
      for(let i=0; i<imgData.data.length; i+=4) {
        if(imgData.data[i] !== 0) { allBlack = false; break; }
      }
      console.log("putImageData: allBlack = " + allBlack + ", width = " + imgData.width);
    },
    drawImage: () => {},
    clearRect: () => {},
    createRadialGradient: () => ({ addColorStop: () => {} }),
    fillRect: () => {},
    save: () => {},
    restore: () => {}
  };
};

window.eval(engineJs);
window.eval(`
  document.getElementById('threshold').value = '128';
  document.getElementById('invert-toggle').checked = false;
  document.getElementById('box-w').value = '120';
  document.getElementById('box-h').value = '120';
  document.getElementById('box-d').value = '80';
  document.getElementById('led-x').value = '0';
  document.getElementById('led-y').value = '0';
  document.getElementById('wall-d').value = '300';
  
  // SET SCALE TO 3.0 TO MAKE IT HIT THE SIDES!
  document.getElementById('img-scale').value = '3.0';
  document.getElementById('panel-t').value = '2.5';
  
  window.State = { img: { width: 100, height: 100 } }; // Fix State access
  try {
    processSourceImage();
  } catch (e) {
    console.log("ERROR: ", e.message);
  }
`);
