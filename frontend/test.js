const THREE = require('three');
const { GCodeLoader } = require('three-stdlib');
const loader = new GCodeLoader();
const gcode = `
G1 X110 Y110 Z0 E1
G1 X120 Y120 Z10 E2
`;
const object = loader.parse(gcode);
console.log('Object type:', object.type);
console.log('Children count:', object.children.length);
if (object.children.length > 0) {
  const geom = object.children[0].geometry;
  geom.computeBoundingBox();
  console.log('Bounding Box:', geom.boundingBox);
}
