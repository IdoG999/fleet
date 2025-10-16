"""
Pydantic models for document processing and analysis
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum

class DocumentType(str, Enum):
    CONTRACT = "contract"
    FINANCIAL_DOCUMENT = "financial_document"
    REPORT = "report"
    PROPOSAL = "proposal"
    MEETING_NOTES = "meeting_notes"
    GENERAL_DOCUMENT = "general_document"

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class DocumentMetadata(BaseModel):
    file_size: int
    processed_at: str
    word_count: int
    character_count: int
    file_type: str
    encoding: Optional[str] = None

class DocumentStructure(BaseModel):
    total_lines: int
    headers: List[str] = Field(default_factory=list)
    list_items: List[str] = Field(default_factory=list)
    table_rows: List[str] = Field(default_factory=list)
    has_numbers: bool = False
    has_emails: bool = False
    has_urls: bool = False
    has_dates: bool = False

class ContentAnalysis(BaseModel):
    main_topics: List[str] = Field(default_factory=list)
    key_information: List[str] = Field(default_factory=list)
    structure_quality: str = "good"
    clarity_score: int = Field(ge=1, le=10, default=5)
    completeness_score: int = Field(ge=1, le=10, default=5)
    summary: str = ""

class BusinessIntelligence(BaseModel):
    business_value: str = "medium"  # high, medium, low
    financial_impact: str = "neutral"  # positive, neutral, negative
    strategic_importance: str = "moderate"  # critical, important, moderate, low
    stakeholder_impact: List[str] = Field(default_factory=list)
    market_implications: str = ""
    recommendations: List[str] = Field(default_factory=list)

class RiskOpportunity(BaseModel):
    risk_level: str = "low"  # high, medium, low
    risks: List[Dict[str, str]] = Field(default_factory=list)
    opportunities: List[Dict[str, str]] = Field(default_factory=list)
    compliance_issues: List[str] = Field(default_factory=list)
    mitigation_strategies: List[str] = Field(default_factory=list)

class ActionItem(BaseModel):
    task: str
    assignee: str
    deadline: Optional[str] = None
    priority: str = "medium"  # high, medium, low
    dependencies: List[str] = Field(default_factory=list)

class ActionItems(BaseModel):
    items: List[ActionItem] = Field(default_factory=list)
    timeline: Optional[str] = None
    success_metrics: List[str] = Field(default_factory=list)

class DocumentAnalysis(BaseModel):
    document_id: str
    document_type: DocumentType
    key_insights: List[str] = Field(default_factory=list)
    confidence_score: int = Field(ge=0, le=100, default=0)
    recommended_actions: List[str] = Field(default_factory=list)
    business_impact: str = "medium"
    risk_level: str = "low"
    opportunities: List[str] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)
    processing_time: float = 0.0
    analysis_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Detailed analysis components
    content_analysis: Optional[ContentAnalysis] = None
    business_intelligence: Optional[BusinessIntelligence] = None
    risk_opportunity: Optional[RiskOpportunity] = None
    action_items_analysis: Optional[ActionItems] = None
    
    # Document metadata
    filename: Optional[str] = None
    file_path: Optional[str] = None
    metadata: Optional[DocumentMetadata] = None
    structure: Optional[DocumentStructure] = None

class WorkflowStep(BaseModel):
    id: str
    name: str
    type: str  # ai_analysis, compliance_validation, notification, approval, etc.
    config: Dict[str, Any] = Field(default_factory=dict)
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None

class WorkflowResult(BaseModel):
    workflow_id: str
    document_id: str
    status: WorkflowStatus
    started_at: str
    completed_at: Optional[str] = None
    steps: List[WorkflowStep] = Field(default_factory=list)
    current_step: int = 0
    results: Dict[str, Any] = Field(default_factory=dict)
    errors: List[Dict[str, str]] = Field(default_factory=list)
    suggested_workflows: List[Dict[str, Any]] = Field(default_factory=list)
    workflow_recommendations: List[str] = Field(default_factory=list)
    estimated_completion_time: Optional[str] = None
    required_approvals: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)

class NotificationRequest(BaseModel):
    message: str
    channels: List[str] = Field(default_factory=list)
    priority: str = "normal"  # low, normal, high, urgent
    recipients: Optional[List[str]] = None

class IntegrationRequest(BaseModel):
    integration_type: str  # slack, email, teams, webhook, etc.
    action: str  # send_message, upload_file, create_webhook, etc.
    data: Dict[str, Any] = Field(default_factory=dict)
    config: Optional[Dict[str, Any]] = None

class AnalyticsData(BaseModel):
    total_documents_processed: int = 0
    average_processing_time: float = 0.0
    average_confidence_score: float = 0.0
    document_types_analyzed: Dict[str, int] = Field(default_factory=dict)
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)
    workflow_statistics: Dict[str, Any] = Field(default_factory=dict)
    integration_usage: Dict[str, int] = Field(default_factory=dict)

class DocumentUploadResponse(BaseModel):
    document_id: str
    status: str
    message: str
    processing_time: Optional[float] = None
    analysis_result: Optional[DocumentAnalysis] = None

class WorkflowExecutionRequest(BaseModel):
    document_id: str
    workflow_template: str
    custom_config: Optional[Dict[str, Any]] = None
    priority: str = "normal"

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]
    version: str = "1.0.0"
    uptime: Optional[float] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    request_id: Optional[str] = None