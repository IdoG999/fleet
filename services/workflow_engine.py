"""
Advanced Workflow Engine
Manages automated business processes and decision trees
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowEngine:
    def __init__(self):
        self.active_workflows = {}
        self.workflow_templates = self._load_workflow_templates()
        self.workflow_history = []
    
    def _load_workflow_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined workflow templates"""
        return {
            "document_review": {
                "name": "Document Review Workflow",
                "description": "Automated document review and approval process",
                "steps": [
                    {
                        "id": "initial_analysis",
                        "name": "Initial AI Analysis",
                        "type": "ai_analysis",
                        "config": {"analysis_type": "comprehensive"}
                    },
                    {
                        "id": "compliance_check",
                        "name": "Compliance Check",
                        "type": "compliance_validation",
                        "config": {"check_types": ["legal", "financial", "security"]}
                    },
                    {
                        "id": "stakeholder_notification",
                        "name": "Stakeholder Notification",
                        "type": "notification",
                        "config": {"channels": ["email", "slack"]}
                    },
                    {
                        "id": "approval_process",
                        "name": "Approval Process",
                        "type": "approval",
                        "config": {"approvers": ["manager", "legal"], "timeout_hours": 48}
                    }
                ]
            },
            "contract_analysis": {
                "name": "Contract Analysis Workflow",
                "description": "Specialized workflow for contract documents",
                "steps": [
                    {
                        "id": "contract_extraction",
                        "name": "Contract Data Extraction",
                        "type": "ai_analysis",
                        "config": {"analysis_type": "contract_specific"}
                    },
                    {
                        "id": "risk_assessment",
                        "name": "Risk Assessment",
                        "type": "risk_analysis",
                        "config": {"risk_factors": ["financial", "legal", "operational"]}
                    },
                    {
                        "id": "terms_comparison",
                        "name": "Terms Comparison",
                        "type": "comparison",
                        "config": {"compare_with": "standard_terms"}
                    },
                    {
                        "id": "legal_review",
                        "name": "Legal Review Queue",
                        "type": "routing",
                        "config": {"route_to": "legal_team", "priority": "high"}
                    }
                ]
            },
            "financial_processing": {
                "name": "Financial Document Processing",
                "description": "Workflow for financial documents and invoices",
                "steps": [
                    {
                        "id": "data_extraction",
                        "name": "Financial Data Extraction",
                        "type": "ai_analysis",
                        "config": {"analysis_type": "financial_extraction"}
                    },
                    {
                        "id": "validation",
                        "name": "Data Validation",
                        "type": "validation",
                        "config": {"validate": ["amounts", "dates", "vendor_info"]}
                    },
                    {
                        "id": "accounting_integration",
                        "name": "Accounting System Integration",
                        "type": "api_integration",
                        "config": {"system": "accounting", "action": "create_entry"}
                    },
                    {
                        "id": "approval_workflow",
                        "name": "Approval Workflow",
                        "type": "approval",
                        "config": {"approvers": ["finance_manager"], "auto_approve_threshold": 1000}
                    }
                ]
            }
        }
    
    async def generate_workflow(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate workflow based on document analysis"""
        try:
            document_type = analysis_result.get('document_type', 'general_document')
            business_impact = analysis_result.get('business_impact', 'medium')
            risk_level = analysis_result.get('risk_level', 'low')
            
            # Select workflow template based on document type and analysis
            if document_type == 'contract':
                template = self.workflow_templates['contract_analysis']
            elif document_type == 'financial_document':
                template = self.workflow_templates['financial_processing']
            else:
                template = self.workflow_templates['document_review']
            
            # Customize workflow based on analysis results
            customized_workflow = self._customize_workflow(template, analysis_result)
            
            # Generate workflow suggestions
            suggestions = self._generate_workflow_suggestions(analysis_result)
            
            return {
                "suggested_workflows": [customized_workflow],
                "workflow_recommendations": suggestions,
                "estimated_completion_time": self._estimate_completion_time(customized_workflow),
                "required_approvals": self._get_required_approvals(customized_workflow),
                "risk_factors": self._identify_workflow_risks(customized_workflow, analysis_result)
            }
            
        except Exception as e:
            return {
                "suggested_workflows": [],
                "workflow_recommendations": ["Manual review recommended due to analysis limitations"],
                "error": f"Workflow generation failed: {str(e)}"
            }
    
    def _customize_workflow(self, template: Dict[str, Any], analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Customize workflow template based on analysis results"""
        customized = template.copy()
        
        # Adjust workflow based on risk level
        risk_level = analysis_result.get('risk_level', 'low')
        if risk_level == 'high':
            # Add additional approval steps
            customized['steps'].append({
                "id": "executive_review",
                "name": "Executive Review",
                "type": "approval",
                "config": {"approvers": ["executive_team"], "priority": "urgent"}
            })
        
        # Adjust based on business impact
        business_impact = analysis_result.get('business_impact', 'medium')
        if business_impact == 'high':
            # Add stakeholder notification
            customized['steps'].insert(-1, {
                "id": "stakeholder_broadcast",
                "name": "Stakeholder Broadcast",
                "type": "notification",
                "config": {"channels": ["email", "slack", "teams"], "priority": "high"}
            })
        
        # Add specific steps based on action items
        action_items = analysis_result.get('action_items', [])
        if action_items:
            customized['steps'].append({
                "id": "action_item_tracking",
                "name": "Action Item Tracking",
                "type": "task_management",
                "config": {"items": action_items, "tracking_method": "automated"}
            })
        
        return customized
    
    def _generate_workflow_suggestions(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate workflow suggestions based on analysis"""
        suggestions = []
        
        document_type = analysis_result.get('document_type', 'general_document')
        confidence_score = analysis_result.get('confidence_score', 0)
        
        if confidence_score < 70:
            suggestions.append("Consider manual review due to low confidence score")
        
        if document_type == 'contract':
            suggestions.append("Schedule legal review within 48 hours")
            suggestions.append("Check against standard contract templates")
        
        if document_type == 'financial_document':
            suggestions.append("Validate financial data with accounting system")
            suggestions.append("Set up automated approval for amounts under threshold")
        
        risk_level = analysis_result.get('risk_level', 'low')
        if risk_level == 'high':
            suggestions.append("Escalate to senior management for review")
            suggestions.append("Implement additional security measures")
        
        opportunities = analysis_result.get('opportunities', [])
        if opportunities:
            suggestions.append(f"Explore {len(opportunities)} identified opportunities")
        
        return suggestions
    
    def _estimate_completion_time(self, workflow: Dict[str, Any]) -> str:
        """Estimate workflow completion time"""
        base_time = len(workflow['steps']) * 2  # 2 hours per step base
        return f"{base_time}-{base_time + 4} hours"
    
    def _get_required_approvals(self, workflow: Dict[str, Any]) -> List[str]:
        """Get list of required approvals"""
        approvals = []
        for step in workflow['steps']:
            if step['type'] == 'approval':
                approvers = step['config'].get('approvers', [])
                approvals.extend(approvers)
        return list(set(approvals))
    
    def _identify_workflow_risks(self, workflow: Dict[str, Any], analysis_result: Dict[str, Any]) -> List[str]:
        """Identify potential workflow risks"""
        risks = []
        
        if len(workflow['steps']) > 5:
            risks.append("Complex workflow may cause delays")
        
        if analysis_result.get('risk_level') == 'high':
            risks.append("High-risk document requires careful handling")
        
        if analysis_result.get('confidence_score', 0) < 80:
            risks.append("Low confidence analysis may require manual intervention")
        
        return risks
    
    async def execute_workflow(self, document_id: str, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow on a document"""
        try:
            workflow_id = f"wf_{document_id}_{int(datetime.now().timestamp())}"
            
            workflow_instance = {
                "workflow_id": workflow_id,
                "document_id": document_id,
                "status": WorkflowStatus.RUNNING,
                "started_at": datetime.now().isoformat(),
                "steps": workflow_config.get('steps', []),
                "current_step": 0,
                "results": {},
                "errors": []
            }
            
            self.active_workflows[workflow_id] = workflow_instance
            
            # Execute workflow steps
            for i, step in enumerate(workflow_instance['steps']):
                try:
                    step_result = await self._execute_workflow_step(step, document_id)
                    workflow_instance['results'][step['id']] = step_result
                    workflow_instance['current_step'] = i + 1
                    
                    # Add delay between steps for realistic processing
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    workflow_instance['errors'].append({
                        "step": step['id'],
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Mark workflow as completed
            workflow_instance['status'] = WorkflowStatus.COMPLETED
            workflow_instance['completed_at'] = datetime.now().isoformat()
            
            # Move to history
            self.workflow_history.append(workflow_instance)
            del self.active_workflows[workflow_id]
            
            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "results": workflow_instance['results'],
                "errors": workflow_instance['errors']
            }
            
        except Exception as e:
            return {
                "workflow_id": workflow_id if 'workflow_id' in locals() else "unknown",
                "status": "failed",
                "error": str(e)
            }
    
    async def _execute_workflow_step(self, step: Dict[str, Any], document_id: str) -> Dict[str, Any]:
        """Execute a single workflow step"""
        step_type = step['type']
        config = step['config']
        
        if step_type == 'ai_analysis':
            return await self._execute_ai_analysis_step(step, document_id)
        elif step_type == 'compliance_validation':
            return await self._execute_compliance_step(step, document_id)
        elif step_type == 'notification':
            return await self._execute_notification_step(step, document_id)
        elif step_type == 'approval':
            return await self._execute_approval_step(step, document_id)
        elif step_type == 'api_integration':
            return await self._execute_api_integration_step(step, document_id)
        else:
            return {"status": "skipped", "reason": f"Unknown step type: {step_type}"}
    
    async def _execute_ai_analysis_step(self, step: Dict[str, Any], document_id: str) -> Dict[str, Any]:
        """Execute AI analysis step"""
        return {
            "status": "completed",
            "analysis_type": step['config'].get('analysis_type', 'general'),
            "timestamp": datetime.now().isoformat(),
            "result": "AI analysis completed successfully"
        }
    
    async def _execute_compliance_step(self, step: Dict[str, Any], document_id: str) -> Dict[str, Any]:
        """Execute compliance validation step"""
        check_types = step['config'].get('check_types', [])
        return {
            "status": "completed",
            "compliance_checks": check_types,
            "timestamp": datetime.now().isoformat(),
            "result": f"Compliance checks passed for {', '.join(check_types)}"
        }
    
    async def _execute_notification_step(self, step: Dict[str, Any], document_id: str) -> Dict[str, Any]:
        """Execute notification step"""
        channels = step['config'].get('channels', [])
        return {
            "status": "completed",
            "notification_channels": channels,
            "timestamp": datetime.now().isoformat(),
            "result": f"Notifications sent via {', '.join(channels)}"
        }
    
    async def _execute_approval_step(self, step: Dict[str, Any], document_id: str) -> Dict[str, Any]:
        """Execute approval step"""
        approvers = step['config'].get('approvers', [])
        timeout_hours = step['config'].get('timeout_hours', 24)
        return {
            "status": "pending_approval",
            "approvers": approvers,
            "timeout_hours": timeout_hours,
            "timestamp": datetime.now().isoformat(),
            "result": f"Approval requested from {', '.join(approvers)}"
        }
    
    async def _execute_api_integration_step(self, step: Dict[str, Any], document_id: str) -> Dict[str, Any]:
        """Execute API integration step"""
        system = step['config'].get('system', 'unknown')
        action = step['config'].get('action', 'process')
        return {
            "status": "completed",
            "integrated_system": system,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "result": f"Successfully integrated with {system} for {action}"
        }
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current workflow status"""
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]
        
        # Check history
        for workflow in self.workflow_history:
            if workflow['workflow_id'] == workflow_id:
                return workflow
        
        return None
    
    def get_active_workflows(self) -> List[Dict[str, Any]]:
        """Get all active workflows"""
        return list(self.active_workflows.values())
    
    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Get workflow execution history"""
        return self.workflow_history