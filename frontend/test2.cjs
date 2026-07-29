const THREE = require('three');
const { GCodeLoader } = require('three-stdlib');
const loader = new GCodeLoader();
const gcode = `G1 X110 Y110 Z10 E1`;
const object = loader.parse(gcode);
console.log('Object rotation:', object.rotation);
console.log('Object position:', object.position);
