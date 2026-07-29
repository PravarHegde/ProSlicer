import React, { useState, useRef, Suspense, useEffect } from 'react';
import * as THREE from 'three';
import { Canvas, useLoader } from '@react-three/fiber';
import { OrbitControls, TransformControls, Grid, Center, Environment } from '@react-three/drei';
import { STLLoader, GCodeLoader, STLExporter } from 'three-stdlib';
import axios from 'axios';
import { 
  Menu, FolderOpen, Save, Maximize, RotateCcw, Move, Layers, ChevronDown, ChevronRight, Bot, Send, Settings, X
} from 'lucide-react';
import './index.css';

// --- CURA DYNAMIC SETTINGS ENGINE ---
const CURA_SETTINGS = [
  {
    category: "Quality",
    settings: [
      { id: 'layer_height', label: 'Layer Height', min: 0.05, max: 0.40, unit: 'mm', default: 0.20 },
      { id: 'initial_layer_height', label: 'Initial Layer Height', min: 0.05, max: 0.40, unit: 'mm', default: 0.20 },
      { id: 'line_width', label: 'Line Width', min: 0.20, max: 0.80, unit: 'mm', default: 0.40 },
    ]
  },
  {
    category: "Strength",
    settings: [
      { id: 'wall_thickness', label: 'Wall Thickness', min: 0.4, max: 3.0, unit: 'mm', default: 1.2 },
      { id: 'wall_line_count', label: 'Wall Line Count', min: 1, max: 10, unit: '', default: 3 },
      { id: 'top_thickness', label: 'Top Thickness', min: 0.4, max: 3.0, unit: 'mm', default: 0.8 },
      { id: 'bottom_thickness', label: 'Bottom Thickness', min: 0.4, max: 3.0, unit: 'mm', default: 0.8 },
      { id: 'infill_density', label: 'Infill Density', min: 0, max: 100, unit: '%', default: 25 },
    ]
  },
  {
    category: "Material",
    settings: [
      { id: 'printing_temperature', label: 'Printing Temperature', min: 180, max: 300, unit: '°C', default: 200 },
      { id: 'build_plate_temperature', label: 'Build Plate Temp', min: 0, max: 120, unit: '°C', default: 60 },
      { id: 'flow', label: 'Flow', min: 50, max: 150, unit: '%', default: 100 },
      { id: 'retraction_distance', label: 'Retraction Distance', min: 0, max: 10, unit: 'mm', default: 5 },
      { id: 'retraction_speed', label: 'Retraction Speed', min: 10, max: 100, unit: 'mm/s', default: 45 },
    ]
  },
  {
    category: "Speed",
    settings: [
      { id: 'print_speed', label: 'Print Speed', min: 20, max: 300, unit: 'mm/s', default: 60 },
      { id: 'infill_speed', label: 'Infill Speed', min: 20, max: 300, unit: 'mm/s', default: 60 },
      { id: 'wall_speed', label: 'Wall Speed', min: 10, max: 150, unit: 'mm/s', default: 30 },
      { id: 'travel_speed', label: 'Travel Speed', min: 50, max: 500, unit: 'mm/s', default: 120 },
      { id: 'initial_layer_speed', label: 'Initial Layer Speed', min: 10, max: 100, unit: 'mm/s', default: 20 },
    ]
  },
  {
    category: "Cooling",
    settings: [
      { id: 'enable_cooling', label: 'Enable Cooling', type: 'toggle', default: true },
      { id: 'fan_speed', label: 'Fan Speed', min: 0, max: 100, unit: '%', default: 100 },
      { id: 'initial_fan_speed', label: 'Initial Fan Speed', min: 0, max: 100, unit: '%', default: 0 },
    ]
  },
  {
    category: "Support",
    settings: [
      { id: 'generate_support', label: 'Generate Support', type: 'toggle', default: false },
      { id: 'support_overhang_angle', label: 'Overhang Angle', min: 10, max: 90, unit: '°', default: 50 },
      { id: 'support_density', label: 'Support Density', min: 0, max: 100, unit: '%', default: 15 },
    ]
  },
  {
    category: "Adhesion",
    settings: [
      { id: 'enable_adhesion', label: 'Enable Adhesion', type: 'toggle', default: true },
      { id: 'skirt_lines', label: 'Skirt Lines', min: 1, max: 10, unit: '', default: 3 },
    ]
  }
];

// --- 3D Components ---

function BuildPlate({ bedX, bedY }) {
  return (
    <group>
      {/* Dynamic 3D Grid */}
      <Grid 
        infiniteGrid={false}
        args={[bedX, bedY]}
        fadeDistance={Math.max(bedX, bedY) * 3} 
        sectionSize={20} 
        cellSize={5} 
        sectionColor="rgba(255, 255, 255, 0.2)" 
        cellColor="rgba(255, 255, 255, 0.08)" 
        position={[0, 0.01, 0]} 
      />
      {/* Physical Build Plate */}
      <mesh receiveShadow position={[0, -2, 0]}>
        <boxGeometry args={[bedX, 4, bedY]} />
        <meshStandardMaterial color="#111216" roughness={0.7} metalness={0.2} />
      </mesh>
      
      {/* Origin Indicator - Bottom Left */}
      <group position={[-bedX/2, 0.5, bedY/2]}>
        <mesh position={[5, 0, 0]}><boxGeometry args={[10, 1, 1]} /><meshBasicMaterial color="#FF3366"/></mesh>
        <mesh position={[0, 0, -5]}><boxGeometry args={[1, 1, 10]} /><meshBasicMaterial color="#00E5FF"/></mesh>
        <mesh position={[0, 5, 0]}><boxGeometry args={[1, 10, 1]} /><meshBasicMaterial color="#8A4BFA"/></mesh>
      </group>
    </group>
  );
}

function UploadedModel({ url, meshRef }) {
  const geom = useLoader(STLLoader, url);
  // Center the model along X and Y, but make the bottom rest exactly on the bed (Z=0)
  geom.center();
  geom.computeBoundingBox();
  geom.translate(0, 0, -geom.boundingBox.min.z);
  
  return (
    <mesh ref={meshRef} geometry={geom} castShadow receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
      <meshStandardMaterial 
        color="#00FF88" 
        transparent 
        opacity={0.8} 
        roughness={0.2} 
        metalness={0.4} 
      />
    </mesh>
  );
}

function DemoModel({ meshRef }) {
  return (
    <mesh ref={meshRef} castShadow receiveShadow position={[0, 30, 0]}>
      <boxGeometry args={[40, 60, 40]} />
      <meshStandardMaterial 
        color="#00FF88" 
        transparent 
        opacity={0.8} 
        roughness={0.2} 
        metalness={0.4} 
      />
    </mesh>
  );
}

// --- UI Controls ---

const CustomSlider = ({ label, value, min, max, unit, onChange }) => {
  const percentage = ((value - min) / (max - min)) * 100;
  
  return (
    <div className="slider-container">
      <div className="slider-header">
        <span className="text-label">{label}</span>
        <span className="text-value">{value}{unit}</span>
      </div>
      <div className="custom-slider-track">
        <div className="custom-slider-fill" style={{ width: `${Math.max(0, Math.min(100, percentage))}%` }}></div>
        <div className="custom-slider-thumb" style={{ left: `${Math.max(0, Math.min(100, percentage))}%` }}></div>
        <input 
          type="range" 
          min={min} 
          max={max} 
          step={unit === 'mm' ? '0.01' : '1'}
          value={value} 
          onChange={(e) => onChange(parseFloat(e.target.value))}
          style={{ opacity: 0, position: 'absolute', width: '100%', height: '100%', top: 0, left: 0, cursor: 'pointer' }}
        />
      </div>
    </div>
  );
};

const CustomToggle = ({ label, checked, onChange }) => {
  return (
    <div className="toggle-container">
      <span className="text-label">{label}</span>
      <div className={`custom-toggle ${checked ? 'active' : ''}`} onClick={() => onChange(!checked)}>
        <div className="custom-toggle-thumb"></div>
      </div>
    </div>
  );
};

const Accordion = ({ title, defaultOpen = false, children }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  return (
    <div className="accordion-group">
      <div className="accordion-header" onClick={() => setIsOpen(!isOpen)}>
        <span className="text-label" style={{ color: isOpen ? 'var(--text-main)' : 'var(--text-muted)' }}>{title}</span>
        {isOpen ? <ChevronDown size={14} color="var(--text-main)" /> : <ChevronRight size={14} color="var(--text-muted)" />}
      </div>
      {isOpen && (
        <div className="accordion-content">
          {children}
        </div>
      )}
    </div>
  );
};

// --- Modals ---
const MachineSettingsModal = ({ onClose, machineSettings, setMachineSettings }) => {
  const [localSettings, setLocalSettings] = useState({ ...machineSettings });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setLocalSettings(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    setMachineSettings({
      ...localSettings,
      bedX: parseFloat(localSettings.bedX) || 220,
      bedY: parseFloat(localSettings.bedY) || 220,
      bedZ: parseFloat(localSettings.bedZ) || 250,
    });
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <span className="panel-title" style={{ fontSize: '14px' }}>MACHINE SETTINGS</span>
          <X size={18} color="var(--text-muted)" style={{ cursor: 'pointer' }} onClick={onClose} />
        </div>
        <div className="modal-body" style={{ flexDirection: 'row' }}>
          
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <span className="text-label" style={{ color: 'var(--text-main)' }}>PRINTER GEOMETRY</span>
            <div style={{ display: 'flex', gap: '10px' }}>
              <div className="input-group">
                <span className="text-label">X (Width) mm</span>
                <input type="number" name="bedX" value={localSettings.bedX} onChange={handleChange} className="custom-input" />
              </div>
              <div className="input-group">
                <span className="text-label">Y (Depth) mm</span>
                <input type="number" name="bedY" value={localSettings.bedY} onChange={handleChange} className="custom-input" />
              </div>
              <div className="input-group">
                <span className="text-label">Z (Height) mm</span>
                <input type="number" name="bedZ" value={localSettings.bedZ} onChange={handleChange} className="custom-input" />
              </div>
            </div>
            
            <span className="text-label" style={{ color: 'var(--text-main)', marginTop: '10px' }}>EXTRUDER SETTINGS</span>
            <div style={{ display: 'flex', gap: '10px' }}>
              <div className="input-group">
                <span className="text-label">Nozzle Size (mm)</span>
                <input type="number" name="nozzleSize" value={localSettings.nozzleSize} onChange={handleChange} className="custom-input" />
              </div>
              <div className="input-group">
                <span className="text-label">Material Dia. (mm)</span>
                <input type="number" name="materialDiameter" value={localSettings.materialDiameter} onChange={handleChange} className="custom-input" />
              </div>
            </div>
          </div>

          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div className="input-group">
              <span className="text-label" style={{ color: 'var(--text-main)' }}>START G-CODE</span>
              <textarea name="startGcode" value={localSettings.startGcode} onChange={handleChange} className="custom-input custom-textarea" />
            </div>
            <div className="input-group">
              <span className="text-label" style={{ color: 'var(--text-main)' }}>END G-CODE</span>
              <textarea name="endGcode" value={localSettings.endGcode} onChange={handleChange} className="custom-input custom-textarea" />
            </div>
          </div>

        </div>
        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleSave}>Save Configuration</button>
        </div>
      </div>
    </div>
  );
};

export default function App() {
  // Navigation
  const [activeNav, setActiveNav] = useState('PREPARE');
  const [activeTool, setActiveTool] = useState('Move');
  const [rightTab, setRightTab] = useState('DATA');

  // File & Models
  const [stlFile, setStlFile] = useState(null);
  const [stlUrl, setStlUrl] = useState(null);
  const fileInputRef = useRef(null);
  const meshRef = useRef(null);
  
  // GCode Preview State
  const [gcodeModel, setGcodeModel] = useState(null);
  const [gcodeBlob, setGcodeBlob] = useState(null);

  // Machine Settings State
  const [showMachineModal, setShowMachineModal] = useState(false);
  const [printer, setPrinter] = useState('Stratasys F120');
  const [machineSettings, setMachineSettings] = useState({
    bedX: 254, bedY: 254, bedZ: 254,
    nozzleSize: 0.4, materialDiameter: 1.75,
    startGcode: "G28 ; home all axes\nG1 Z5 F5000 ; lift nozzle",
    endGcode: "M104 S0 ; turn off temperature\nM140 S0 ; turn off bed\nG28 X0  ; home X axis\nM84     ; disable motors"
  });
  
  const [material, setMaterial] = useState('PLA (Cyan)');

  // Change default bed size when dropdown changes
  useEffect(() => {
    if (printer === 'Stratasys F120') setMachineSettings(prev => ({...prev, bedX: 254, bedY: 254, bedZ: 254}));
    if (printer === 'ProBharath CoreXY') setMachineSettings(prev => ({...prev, bedX: 300, bedY: 300, bedZ: 300}));
    if (printer === 'Custom FDM Printer') setMachineSettings(prev => ({...prev, bedX: 220, bedY: 220, bedZ: 250}));
  }, [printer]);

  // Dynamic Engine State
  const [settings, setSettings] = useState(() => {
    const initialState = {};
    CURA_SETTINGS.forEach(cat => {
      cat.settings.forEach(s => {
        initialState[s.id] = s.default;
      });
    });
    return initialState;
  });

  const updateSetting = (id, val) => {
    setSettings(prev => ({...prev, [id]: val}));
  };

  // 3D Controls
  const [orbitEnabled, setOrbitEnabled] = useState(true);

  // AI Chat State
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'ai', text: 'Hello! I am your AI Slicing Assistant. Looking at your model, I can recommend optimal settings. Need help?' }
  ]);

  const [isSlicing, setIsSlicing] = useState(false);

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;
    setMessages(prev => [...prev, { role: 'user', text: chatInput }]);
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        text: `Based on your request, I recommend increasing Wall Line Count to 4 for better strength.` 
      }]);
    }, 1000);
    setChatInput('');
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file && (file.name.toLowerCase().endsWith('.stl'))) {
      setStlFile(file);
      const objectUrl = URL.createObjectURL(file);
      setStlUrl(objectUrl);
      setGcodeModel(null); // Clear preview if new model loaded
      setGcodeBlob(null);
    }
  };

  const handleSlice = async () => {
    if (!stlFile) {
      alert("Please open an STL file first using the Open tool.");
      return;
    }
    
    setIsSlicing(true);
    setGcodeModel(null);
    
    const formData = new FormData();
    
    // EXPORT TRANSFORMED MESH ONLY (Exclude Gizmos)
    if (meshRef.current) {
      const clone = meshRef.current.clone();
      const tempGroup = new THREE.Group();
      
      // Map Three.js centered coordinates (Y-up) to PrusaSlicer front-left coordinates (Z-up)
      tempGroup.position.set(machineSettings.bedX / 2, machineSettings.bedY / 2, 0);
      tempGroup.rotation.x = Math.PI / 2;
      
      tempGroup.add(clone);
      tempGroup.updateMatrixWorld(true);
      
      const exporter = new STLExporter();
      const stlString = exporter.parse(tempGroup);
      
      const blob = new Blob([stlString], { type: 'text/plain' });
      formData.append("file", blob, "model.stl");
    } else {
      formData.append("file", stlFile);
    }

    formData.append("layer_height", settings['layer_height']);
    formData.append("infill", settings['infill_density']);
    formData.append("wall_loops", settings['wall_line_count']);
    formData.append("support", settings['generate_support']);
    
    // CUSTOM MACHINE SETTINGS
    formData.append("bed_x", machineSettings.bedX);
    formData.append("bed_y", machineSettings.bedY);
    formData.append("start_gcode", machineSettings.startGcode);
    formData.append("end_gcode", machineSettings.endGcode);

    try {
      const backendUrl = `http://${window.location.hostname}:8000/api/slice`;
      const response = await axios.post(backendUrl, formData, {
        responseType: 'blob'
      });
      
      const blob = new Blob([response.data], { type: 'application/octet-stream' });
      setGcodeBlob(blob);
      
      // PARSE GCODE FOR PERFECT PREVIEW
      const gcodeText = await blob.text();
      const loader = new GCodeLoader();
      const object = loader.parse(gcodeText);
      // GCode origin is 0,0,0 (Front-Left in PrusaSlicer)
      object.position.set(0, 0, 0); 
      setGcodeModel(object);
      
      // Auto-switch to preview tab like Cura
      setActiveNav('PREVIEW');

    } catch (error) {
      console.error("Slicing failed", error);
      alert(`Failed to slice: ${error.message || error}`);
    } finally {
      setIsSlicing(false);
    }
  };

  const handleSaveDisk = async () => {
    if (!gcodeBlob) return;
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: `${stlFile.name.replace('.stl', '')}_sliced.gcode`,
        types: [{
          description: 'G-Code File',
          accept: {'application/octet-stream': ['.gcode']},
        }],
      });
      const writable = await handle.createWritable();
      await writable.write(gcodeBlob);
      await writable.close();
    } catch (err) {
      if (err.name !== 'AbortError') {
        const url = URL.createObjectURL(gcodeBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${stlFile.name.replace('.stl', '')}_sliced.gcode`;
        a.click();
      }
    }
  }

  const getTransformMode = () => {
    if (activeTool === 'Move') return 'translate';
    if (activeTool === 'Rotate') return 'rotate';
    if (activeTool === 'Scale') return 'scale';
    return null;
  };
  const transformMode = getTransformMode();

  return (
    <div className="app-container">
      {showMachineModal && (
        <MachineSettingsModal 
          machineSettings={machineSettings} 
          setMachineSettings={setMachineSettings} 
          onClose={() => setShowMachineModal(false)} 
        />
      )}
      
      {/* 3D CANVAS LAYER */}
      <div className="viewport-container">
        <Canvas shadows camera={{ position: [0, 150, 200], fov: 45 }}>
          <ambientLight intensity={0.2} />
          <directionalLight position={[50, 100, 50]} intensity={1.5} castShadow color="#FFFFFF" />
          <pointLight position={[-50, 50, -50]} intensity={2} color="#00E5FF" />
          <pointLight position={[50, 20, 50]} intensity={1} color="#8A4BFA" />
          <Environment preset="city" />
          
          <BuildPlate bedX={machineSettings.bedX} bedY={machineSettings.bedY} />
          
          <Suspense fallback={null}>
            {activeNav === 'PREVIEW' ? (
              gcodeModel ? (
                // Preview Mode: Align front-left of PrusaSlicer (0,0) to front-left of ThreeJS bed (-bedX/2, bedY/2)
                <group position={[-machineSettings.bedX / 2, 0, machineSettings.bedY / 2]}>
                  <primitive object={gcodeModel} />
                </group>
              ) : null
            ) : transformMode ? (
              <TransformControls mode={transformMode} onDraggingChanged={(e) => setOrbitEnabled(!e.value)}>
                {stlUrl ? <UploadedModel url={stlUrl} meshRef={meshRef} /> : <DemoModel meshRef={meshRef} />}
              </TransformControls>
            ) : (
              stlUrl ? <UploadedModel url={stlUrl} meshRef={meshRef} /> : <DemoModel meshRef={meshRef} />
            )}
          </Suspense>
          
          <OrbitControls makeDefault enabled={orbitEnabled} maxPolarAngle={Math.PI/2 - 0.05} />
        </Canvas>
      </div>

      {/* OVERLAY UI LAYER */}
      <div className="overlay-layer">
        
        {/* Top Navigation */}
        <nav className="top-nav">
          <div className="brand">
            <div className="brand-icon">P</div>
            <span className="brand-text">PRO SLICER</span>
          </div>
          <div className="nav-links">
            {['PREPARE', 'PREVIEW', 'MONITOR'].map(link => (
              <div 
                key={link} 
                className={`nav-link ${activeNav === link ? 'active' : ''}`}
                onClick={() => setActiveNav(link)}
              >
                {link}
              </div>
            ))}
          </div>
          <div className="menu-btn">
            <Menu size={16} color="var(--text-main)" />
          </div>
        </nav>

        {/* Toolbar */}
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <div className="toolbar">
            <input 
              type="file" 
              accept=".stl" 
              ref={fileInputRef} 
              style={{ display: 'none' }} 
              onChange={handleFileUpload} 
            />
            {[
              { name: 'Open', icon: FolderOpen, action: () => fileInputRef.current?.click() },
              { name: 'Save', icon: Save },
              { name: 'Scale', icon: Maximize },
              { name: 'Rotate', icon: RotateCcw },
              { name: 'Move', icon: Move },
              { name: 'Supports', icon: Layers }
            ].map(tool => (
              <div 
                key={tool.name} 
                className={`tool-item ${activeTool === tool.name ? 'active' : ''}`}
                onClick={() => { setActiveTool(tool.name); if(tool.action) tool.action(); }}
              >
                <tool.icon size={18} />
                <span>{tool.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Main Panels */}
        <div className="main-workspace">
          
          {/* LEFT PANEL - DYNAMIC SETTINGS */}
          <div className="glass-panel left-panel">
            <div className="panel-header">
              <span className="panel-title">PARAMETERS</span>
            </div>
            
            {/* Machine & Filament Selection */}
            <div style={{ padding: '16px 20px', borderBottom: '1px solid rgba(255, 255, 255, 0.03)' }}>
              <div style={{ marginBottom: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span className="text-label">PRINTER</span>
                  <div 
                    onClick={() => setShowMachineModal(true)} 
                    style={{ display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer', color: 'var(--accent-cyan)' }}
                  >
                    <Settings size={12} /> <span style={{ fontSize: '10px', fontWeight: 'bold' }}>EDIT</span>
                  </div>
                </div>
                <select className="custom-select" value={printer} onChange={(e) => setPrinter(e.target.value)}>
                  <option>Stratasys F120</option>
                  <option>ProBharath CoreXY</option>
                  <option>Custom FDM Printer</option>
                </select>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <div style={{ flex: 2 }}>
                  <span className="text-label" style={{ display: 'block', marginBottom: '8px' }}>MATERIAL</span>
                  <select className="custom-select" value={material} onChange={(e) => setMaterial(e.target.value)}>
                    <option>PLA (Cyan)</option>
                    <option>PETG (Clear)</option>
                    <option>ABS (Black)</option>
                  </select>
                </div>
                <div style={{ flex: 1 }}>
                  <span className="text-label" style={{ display: 'block', marginBottom: '8px' }}>NOZZLE</span>
                  <input 
                    readOnly
                    className="custom-input" 
                    style={{ width: '100%', padding: '8px' }} 
                    value={`${machineSettings.nozzleSize}mm`} 
                  />
                </div>
              </div>
            </div>

            <div style={{ flex: 1, paddingBottom: '20px' }}>
              {CURA_SETTINGS.map((category, idx) => (
                <Accordion key={category.category} title={category.category.toUpperCase()} defaultOpen={idx === 0}>
                  {category.settings.map(setting => {
                    if (setting.type === 'toggle') {
                      return (
                        <CustomToggle 
                          key={setting.id}
                          label={setting.label.toUpperCase()} 
                          checked={settings[setting.id]} 
                          onChange={(val) => updateSetting(setting.id, val)} 
                        />
                      );
                    } else {
                      return (
                        <CustomSlider 
                          key={setting.id}
                          label={setting.label.toUpperCase()} 
                          value={settings[setting.id]} 
                          min={setting.min} 
                          max={setting.max} 
                          unit={setting.unit} 
                          onChange={(val) => updateSetting(setting.id, val)} 
                        />
                      );
                    }
                  })}
                </Accordion>
              ))}
            </div>
          </div>

          {/* RIGHT PANEL - MULTI-TAB */}
          <div className="glass-panel right-panel">
            <div className="panel-tabs">
              <div className={`panel-tab ${rightTab === 'DATA' ? 'active' : ''}`} onClick={() => setRightTab('DATA')}>SLICING DATA</div>
              <div className={`panel-tab ${rightTab === 'AI' ? 'active' : ''}`} onClick={() => setRightTab('AI')}>AI ASSISTANT</div>
            </div>

            {rightTab === 'DATA' && (
              <div className="tab-content" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                <div className="dropdown-item">
                  <span className="text-label">SLICE SETTINGS</span>
                  <ChevronDown size={14} color="var(--text-muted)" />
                </div>
                <div className="dropdown-item">
                  <span className="text-label">3D MODEL PREVIEW</span>
                  <span className="text-value" style={{ color: gcodeModel ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>
                    {gcodeModel ? 'G-CODE PATH' : 'SOLID STL'}
                  </span>
                </div>
                
                <div className="layer-view-section">
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span className="text-label">LAYER VIEW</span>
                    <span className="text-label" style={{ color: gcodeModel ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>
                      {gcodeModel ? 'Active Preview' : 'Inactive'}
                    </span>
                  </div>
                  
                  <div className="layer-preview-box" style={{ borderColor: gcodeModel ? 'var(--accent-cyan)' : 'rgba(255,255,255,0.05)' }}>
                    <Layers size={40} color={gcodeModel ? 'var(--accent-cyan)' : 'var(--text-muted)'} style={{ opacity: gcodeModel ? 1 : 0.3 }} />
                  </div>
                  
                  <div className="custom-slider-track" style={{ margin: '16px 0 8px' }}>
                    <div className="custom-slider-fill" style={{ width: gcodeModel ? '100%' : '0%' }}></div>
                    <div className="custom-slider-thumb" style={{ left: gcodeModel ? '100%' : '0%', width: '10px', height: '10px' }}></div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <span className="text-muted" style={{ fontSize: '10px' }}>Layer --/--</span>
                  </div>
                </div>
                
                <div className="data-table">
                  <div className="data-row">
                    <span className="text-label">ESTIMATED TIME</span>
                    <span className="text-value">3h 14m</span>
                  </div>
                  <div className="data-row">
                    <span className="text-label">MATERIAL</span>
                    <span className="text-value">{material}</span>
                  </div>
                  <div className="data-row">
                    <span className="text-label">PRINTER</span>
                    <span className="text-value">{printer}</span>
                  </div>
                  
                  {gcodeBlob && (
                    <div style={{ marginTop: '20px' }}>
                      <button className="btn-secondary" style={{ width: '100%', borderColor: 'var(--accent-cyan)', color: 'var(--accent-cyan)' }} onClick={handleSaveDisk}>
                        <Save size={14} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
                        SAVE G-CODE TO DISK
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}

            {rightTab === 'AI' && (
              <div className="tab-content ai-tab" style={{ display: 'flex', flexDirection: 'column', height: '100%', padding: '16px' }}>
                <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px', paddingBottom: '16px' }}>
                  {messages.map((msg, idx) => (
                    <div key={idx} className={`ai-message ${msg.role}`}>
                      {msg.role === 'ai' && <Bot size={14} style={{ marginRight: '6px', marginBottom: '-2px' }} />}
                      {msg.text}
                    </div>
                  ))}
                </div>
                <div className="ai-input-wrapper">
                  <input 
                    type="text" 
                    placeholder="Ask about settings..." 
                    value={chatInput}
                    onChange={e => setChatInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
                  />
                  <button onClick={handleSendMessage}><Send size={14} /></button>
                </div>
              </div>
            )}
          </div>
          
        </div>
        
        {/* SLICE BUTTON & WARNINGS */}
        <div className="slice-footer-area">
          {activeNav === 'PREVIEW' && !gcodeModel && !isSlicing && (
            <div className="cura-warning">
              <div className="warning-icon">!</div>
              <div className="warning-text">
                <strong style={{display: 'block', fontSize: '13px', marginBottom: '2px'}}>No layers to show</strong>
                <span style={{fontSize: '11px', color: 'rgba(255,255,255,0.7)'}}>Nothing is shown because you need to slice first.</span>
              </div>
              <div className="warning-close"><X size={16} color="rgba(255,255,255,0.5)"/></div>
            </div>
          )}
          
          <div className="slice-button-container">
            <button className="slice-btn" onClick={handleSlice} disabled={isSlicing}>
              <span className="slice-title">{isSlicing ? "SLICING..." : "SLICE MODEL"}</span>
              <span className="slice-subtitle">{isSlicing ? "PLEASE WAIT" : "READY TO SLICE"}</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
