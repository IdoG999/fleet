"""
AI-Powered Business Document Intelligence Platform
A comprehensive solution demonstrating advanced AI integration, automation, and workflow management.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

from services.document_processor import DocumentProcessor
from services.ai_analyzer import AIAnalyzer
from services.workflow_engine import WorkflowEngine
from services.api_integrations import APIIntegrations
from models.document_models import DocumentAnalysis, WorkflowResult

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Document Intelligence Platform",
    description="Advanced AI-powered document analysis and workflow automation",
    version="1.0.0"
)

# Initialize services
document_processor = DocumentProcessor()
ai_analyzer = AIAnalyzer()
workflow_engine = WorkflowEngine()
api_integrations = APIIntegrations()

# Create necessary directories
Path("uploads").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)
Path("static").mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class DocumentUploadRequest(BaseModel):
    document_type: str
    business_context: str
    workflow_type: str = "standard"

class WorkflowRequest(BaseModel):
    document_id: str
    workflow_config: Dict[str, Any]

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Document Intelligence Platform</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .header h1 { font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 40px; }
            .feature-card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
            .feature-card h3 { color: #ffd700; margin-bottom: 15px; }
            .upload-area { background: rgba(255,255,255,0.1); padding: 40px; border-radius: 15px; text-align: center; border: 2px dashed rgba(255,255,255,0.3); margin-bottom: 30px; }
            .upload-btn { background: #4CAF50; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin: 10px; }
            .upload-btn:hover { background: #45a049; }
            .status { margin-top: 20px; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Document Intelligence Platform</h1>
                <p>Advanced AI-powered document analysis and workflow automation</p>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🧠 Smart Analysis</h3>
                    <p>Advanced AI models analyze documents with context-aware understanding, extracting key insights and patterns.</p>
                </div>
                <div class="feature-card">
                    <h3>⚡ Workflow Automation</h3>
                    <p>Automated business processes that adapt based on document content and business rules.</p>
                </div>
                <div class="feature-card">
                    <h3>🔗 API Integration</h3>
                    <p>Seamless integration with multiple services and platforms for comprehensive data processing.</p>
                </div>
                <div class="feature-card">
                    <h3>📊 Real-time Insights</h3>
                    <p>Live dashboards and analytics showing document processing status and business metrics.</p>
                </div>
            </div>
            
            <div class="upload-area">
                <h2>Upload Document for AI Analysis</h2>
                <p>Support for PDF, DOCX, TXT, and image files</p>
                <input type="file" id="fileInput" accept=".pdf,.docx,.txt,.png,.jpg,.jpeg" style="display: none;">
                <button class="upload-btn" onclick="document.getElementById('fileInput').click()">Choose File</button>
                <button class="upload-btn" onclick="uploadDocument()">Analyze with AI</button>
                <div id="status" class="status" style="display: none;"></div>
            </div>
        </div>
        
        <script>
            let selectedFile = null;
            document.getElementById('fileInput').addEventListener('change', function(e) {
                selectedFile = e.target.files[0];
                if (selectedFile) {
                    document.getElementById('status').innerHTML = `Selected: ${selectedFile.name}`;
                    document.getElementById('status').style.display = 'block';
                }
            });
            
            async function uploadDocument() {
                if (!selectedFile) {
                    alert('Please select a file first');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', selectedFile);
                formData.append('document_type', 'business_document');
                formData.append('business_context', 'general_analysis');
                
                document.getElementById('status').innerHTML = 'Processing document with AI...';
                document.getElementById('status').style.display = 'block';
                
                try {
                    const response = await fetch('/analyze-document', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('status').innerHTML = `
                            <h3>Analysis Complete! 🎉</h3>
                            <p><strong>Document Type:</strong> ${result.document_type}</p>
                            <p><strong>Key Insights:</strong> ${result.key_insights}</p>
                            <p><strong>Confidence Score:</strong> ${result.confidence_score}%</p>
                            <p><strong>Recommended Actions:</strong> ${result.recommended_actions}</p>
                        `;
                    } else {
                        document.getElementById('status').innerHTML = `Error: ${result.detail}`;
                    }
                } catch (error) {
                    document.getElementById('status').innerHTML = `Error: ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/analyze-document")
async def analyze_document(
    file: UploadFile = File(...),
    document_type: str = "business_document",
    business_context: str = "general_analysis"
):
    """Analyze uploaded document using AI"""
    try:
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document
        processed_doc = await document_processor.process_document(file_path, file.filename)
        
        # Analyze with AI
        analysis = await ai_analyzer.analyze_document(
            processed_doc, 
            document_type, 
            business_context
        )
        
        # Generate workflow recommendations
        workflow_result = await workflow_engine.generate_workflow(analysis)
        
        return {
            "document_id": analysis.document_id,
            "document_type": analysis.document_type,
            "key_insights": analysis.key_insights,
            "confidence_score": analysis.confidence_score,
            "recommended_actions": analysis.recommended_actions,
            "workflow_suggestions": workflow_result.suggested_workflows,
            "processing_time": analysis.processing_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/execute-workflow")
async def execute_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Execute a specific workflow on a document"""
    try:
        # Add workflow execution to background tasks
        background_tasks.add_task(
            workflow_engine.execute_workflow,
            request.document_id,
            request.workflow_config
        )
        
        return {"message": "Workflow execution started", "workflow_id": f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing workflow: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "document_processor": "active",
            "ai_analyzer": "active",
            "workflow_engine": "active",
            "api_integrations": "active"
        }
    }

@app.get("/api/analytics")
async def get_analytics():
    """Get processing analytics and insights"""
    try:
        analytics = await ai_analyzer.get_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analytics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)