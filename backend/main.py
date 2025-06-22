# backend/main.py

import os
import io
import json
import base64

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Attempt to import matplotlib and numpy for plotting; if missing, endpoints using plotting will error or skip
try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Determine possible static and templates directories
# In Docker, we expect built frontend at /app/frontend/dist, templates at /app/backend/templates
DOCKER_FRONTEND_DIST = "/app/frontend/dist"
DOCKER_TEMPLATES = "/app/backend/templates"

# For local development, fallback to relative paths:
HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL_FRONTEND_DIST = os.path.normpath(os.path.join(HERE, "../../frontend/dist"))
LOCAL_TEMPLATES = os.path.normpath(os.path.join(HERE, "templates"))

# Choose actual directories if they exist
if os.path.isdir(DOCKER_FRONTEND_DIST):
    FRONTEND_STATIC_DIR = DOCKER_FRONTEND_DIST
elif os.path.isdir(LOCAL_FRONTEND_DIST):
    FRONTEND_STATIC_DIR = LOCAL_FRONTEND_DIST
else:
    FRONTEND_STATIC_DIR = None

if os.path.isdir(DOCKER_TEMPLATES):
    TEMPLATES_DIR = DOCKER_TEMPLATES
elif os.path.isdir(LOCAL_TEMPLATES):
    TEMPLATES_DIR = LOCAL_TEMPLATES
else:
    TEMPLATES_DIR = None

app = FastAPI(
    title="GRC Nexus API",
    description="Backend API for the GRC Nexus platform.",
    version="0.0.1",
)

# Mount static files only if the directory exists
if FRONTEND_STATIC_DIR:
    app.mount("/static", StaticFiles(directory=FRONTEND_STATIC_DIR), name="static")
else:
    print(
        f"Warning: frontend static directory not found. "
        f"Skipping StaticFiles mount. Checked: {DOCKER_FRONTEND_DIST}, {LOCAL_FRONTEND_DIST}"
    )

# Initialize templates if available
if TEMPLATES_DIR:
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
else:
    templates = None
    print(
        f"Warning: templates directory not found. "
        f"Skipping Jinja2Templates init. Checked: {DOCKER_TEMPLATES}, {LOCAL_TEMPLATES}"
    )

# In-memory storage for prototype
class ControlStatus(BaseModel):
    id: str
    status: str  # "Implemented", "Not Implemented", "Partially Implemented"

class Asset(BaseModel):
    name: str
    impact: int
    likelihood: int

controls_data: list[dict] = []
current_control_statuses: dict[str, str] = {}
current_assets: list[dict] = []

@app.on_event("startup")
async def load_controls():
    global controls_data
    controls_file_path = os.path.join(HERE, "controls.json")
    try:
        with open(controls_file_path, "r") as f:
            controls_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: controls.json not found at {controls_file_path}. Using empty controls list.")
        controls_data = []

@app.get("/api/controls", response_model=list[dict])
async def get_controls():
    return controls_data

@app.post("/api/assess-compliance")
async def assess_compliance(statuses: list[ControlStatus]):
    global current_control_statuses
    current_control_statuses = {s.id: s.status for s in statuses}
    return {"message": "Compliance statuses updated successfully."}

@app.get("/api/compliance-results")
async def get_compliance_results():
    total_controls = len(controls_data)
    if total_controls == 0:
        return {
            "total_controls": 0,
            "compliant_count": 0,
            "non_compliant_count": 0,
            "partially_compliant_count": 0,
            "compliance_percentage": 0,
            "results": [],
            "recommendations": []
        }

    compliant_count = non_compliant_count = partially_compliant_count = 0
    results = []
    recommendations: list[dict] = []

    for control in controls_data:
        status = current_control_statuses.get(control.get("id", ""), "Not Assessed")
        is_compliant = False
        if status == "Implemented":
            compliant_count += 1
            is_compliant = True
        elif status == "Not Implemented":
            non_compliant_count += 1
            recommendations.append({
                "type": "Control Remediation",
                "area": control.get("category", ""),
                "item": control.get("name", ""),
                "suggestion": control.get("remediation_suggestion", "")
            })
        elif status == "Partially Implemented":
            partially_compliant_count += 1
            recommendations.append({
                "type": "Control Improvement",
                "area": control.get("category", ""),
                "item": control.get("name", ""),
                "suggestion": f"Further action needed: {control.get('remediation_suggestion', '')}"
            })
        results.append({
            "id": control.get("id", ""),
            "name": control.get("name", ""),
            "status": status,
            "is_compliant": is_compliant,
            "description": control.get("description", ""),
            "remediation_suggestion": control.get("remediation_suggestion", "N/A")
        })

    compliance_percentage = (compliant_count / total_controls) * 100 if total_controls > 0 else 0

    return {
        "total_controls": total_controls,
        "compliant_count": compliant_count,
        "non_compliant_count": non_compliant_count,
        "partially_compliant_count": partially_compliant_count,
        "compliance_percentage": round(compliance_percentage, 2),
        "results": results,
        "recommendations": recommendations
    }

@app.post("/api/add-asset")
async def add_asset(asset: Asset):
    if not (1 <= asset.impact <= 5 and 1 <= asset.likelihood <= 5):
        raise HTTPException(status_code=400, detail="impact and likelihood must be between 1 and 5")
    current_assets.append(asset.dict())
    return {"message": "Asset added successfully."}

@app.get("/api/assets")
async def get_assets():
    return current_assets

@app.get("/api/risk-assessment")
async def get_risk_assessment():
    risk_data: list[dict] = []
    recommendations: list[dict] = []
    risk_matrix = None
    if current_assets:
        # 5x5 matrix for counts
        risk_matrix = [[0]*5 for _ in range(5)]

    for asset in current_assets:
        impact = asset.get("impact", 0)
        likelihood = asset.get("likelihood", 0)
        risk_score = impact * likelihood
        if risk_score > 15:
            risk_level = "High"
        elif 7 <= risk_score <= 15:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        risk_data.append({
            "name": asset.get("name", ""),
            "impact": impact,
            "likelihood": likelihood,
            "score": risk_score,
            "level": risk_level
        })

        if risk_matrix is not None and 1 <= impact <= 5 and 1 <= likelihood <= 5:
            risk_matrix[impact-1][likelihood-1] += 1

        if risk_level in ["Medium", "High"]:
            treatment = "Mitigate (Urgent)" if risk_level == "High" else "Mitigate / Monitor"
            recommendations.append({
                "type": "Risk Treatment",
                "area": "Asset Risk",
                "item": asset.get("name", ""),
                "suggestion": f"Risk Level: {risk_level}. Recommended Treatment: {treatment}. Consider extra controls or risk transfer."
            })

    # Generate heatmap if possible
    risk_heatmap_base64 = None
    if MATPLOTLIB_AVAILABLE and risk_matrix:
        arr = np.array(risk_matrix)
        fig, ax = plt.subplots(figsize=(6,5))
        cax = ax.imshow(arr[::-1], cmap='hot_r', origin='lower', extent=[0.5, 5.5, 0.5, 5.5])
        ax.set_xlabel("Likelihood (1-5)")
        ax.set_ylabel("Impact (1-5)")
        ax.set_title("Risk Matrix Heatmap")
        ax.set_xticks(np.arange(1,6))
        ax.set_yticks(np.arange(1,6))
        # annotate counts
        for i in range(5):
            for j in range(5):
                count = arr[4-i][j]
                if count > 0:
                    ax.text(j+1, i+1, str(count), ha='center', va='center', color='black', fontsize=10)
        fig.colorbar(cax, label='Number of Assets')
        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="png")
        buf.seek(0)
        risk_heatmap_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)

    return {
        "risk_data": risk_data,
        "recommendations": recommendations,
        "risk_heatmap": risk_heatmap_base64
    }

@app.get("/api/all-recommendations")
async def get_all_recommendations():
    comp = await get_compliance_results()
    risk = await get_risk_assessment()
    combined = comp.get("recommendations", []) + risk.get("recommendations", [])
    return combined

@app.get("/report", response_class=HTMLResponse)
async def generate_report(request: Request):
    if not templates:
        raise HTTPException(status_code=500, detail="Templates directory not configured")
    compliance_results = await get_compliance_results()
    risk_assessment_results = await get_risk_assessment()
    all_recommendations = await get_all_recommendations()
    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "compliance_results": compliance_results,
            "risk_assessment_results": risk_assessment_results,
            "all_recommendations": all_recommendations
        }
    )

# Serve frontend SPA only if built static is present
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str, request: Request):
    if full_path.startswith("api"):
        raise HTTPException(status_code=404, detail="API Not Found")
    if FRONTEND_STATIC_DIR:
        index_path = os.path.join(FRONTEND_STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            raise HTTPException(status_code=404, detail="Frontend built but index.html missing")
    # No built frontend available
    raise HTTPException(status_code=404, detail="Frontend not built; use Vite dev server in development")

@app.get("/")
async def root_redirect():
    if FRONTEND_STATIC_DIR:
        index_path = os.path.join(FRONTEND_STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
    return {"message": "Backend is running. Frontend not built; run Vite dev server separately."}
