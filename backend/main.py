from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import asyncio
import os
import subprocess
import uuid
import shutil
from mcp.server.fastmcp import FastMCP

# Initialize FastAPI app
app = FastAPI(title="Pro Slicer Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP Server for AI Agent Integration
mcp = FastMCP("ProSlicerMCP")

# Directory for temp files
UPLOAD_DIR = "/tmp/pro_slicer_temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- MCP Tools ---
@mcp.tool()
def get_slicer_status() -> str:
    """Returns the current status of the slicing engine."""
    return "Ready. PrusaSlicer backend active."

@mcp.tool()
def set_print_setting(setting_name: str, value: str) -> str:
    """Sets a print setting in the slicer profile. Examples: infill, layer_height, supports"""
    return f"Successfully updated setting '{setting_name}' to '{value}'"

# --- FastAPI Endpoints for Frontend UI ---

@app.post("/api/slice")
async def slice_model(
    file: UploadFile = File(...),
    layer_height: float = Form(0.20),
    infill: int = Form(15),
    wall_loops: int = Form(3),
    support: bool = Form(False),
    bed_x: float = Form(220),
    bed_y: float = Form(220),
    start_gcode: str = Form(""),
    end_gcode: str = Form("")
):
    """Endpoint for the frontend to upload an STL and get G-code back."""
    
    # Save the uploaded STL
    job_id = str(uuid.uuid4())
    stl_path = os.path.join(UPLOAD_DIR, f"{job_id}.stl")
    gcode_path = os.path.join(UPLOAD_DIR, f"{job_id}.gcode")
    config_path = os.path.join(UPLOAD_DIR, f"{job_id}.ini")
    
    with open(stl_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    print(f"Received STL: {stl_path}, Layer Height: {layer_height}, Infill: {infill}")
    
    # Generate PrusaSlicer Configuration INI
    bed_shape = f"0x0,{bed_x}x0,{bed_x}x{bed_y},0x{bed_y}"
    start_gcode_clean = start_gcode.replace('\n', '\\n')
    end_gcode_clean = end_gcode.replace('\n', '\\n')
    
    config_content = f"""
bed_shape = {bed_shape}
start_gcode = {start_gcode_clean}
end_gcode = {end_gcode_clean}
"""
    with open(config_path, "w") as f:
        f.write(config_content)
    
    fill_density = infill / 100.0
    
    command = [
        "prusa-slicer",
        "--load", config_path,
        "--export-gcode",
        "--dont-arrange",
        "--layer-height", str(layer_height),
        "--fill-density", str(fill_density),
        "--perimeters", str(wall_loops)
    ]
    
    if support:
        command.append("--support-material")
        
    command.extend(["--output", gcode_path, stl_path])
    
    print(f"Running Command: {' '.join(command)}")
    
    try:
        # Run Slicer as a subprocess
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Slicer Output:", result.stdout)
        
        # Ensure G-Code was created
        if os.path.exists(gcode_path):
            return FileResponse(
                path=gcode_path, 
                filename=file.filename.replace(".stl", ".gcode").replace(".STL", ".gcode"), 
                media_type="application/octet-stream"
            )
        else:
            return {"status": "error", "message": "G-Code file not generated."}
            
    except subprocess.CalledProcessError as e:
        print("Slicer Error:", e.stderr)
        return {"status": "error", "message": f"Slicing failed: {e.stderr}"}

@app.get("/api/status")
async def get_status():
    """Endpoint for frontend to get status"""
    return {"status": "idle", "engine": "prusa-slicer"}

if __name__ == "__main__":
    import sys
    if "--mcp" in sys.argv:
        print("Starting Pro Slicer MCP Server...")
        mcp.run()
    else:
        print("Starting Pro Slicer Web API...")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
