const fs = require('fs');
let text = fs.readFileSync('engine.js', 'utf8');
text = text.replace(/panelType\.substring\(0,3\)/g, "shortName");
fs.writeFileSync('engine.js', text);
