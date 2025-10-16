"""
Advanced AI Analysis Service
Uses sophisticated prompt engineering and multiple AI models for document analysis
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
import openai
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.analysis_cache = {}
        self.analytics_data = {
            'total_documents': 0,
            'analysis_types': {},
            'average_confidence': 0,
            'processing_times': []
        }
    
    async def analyze_document(self, document_data: Dict[str, Any], document_type: str, business_context: str) -> Dict[str, Any]:
        """Perform comprehensive AI analysis on document"""
        try:
            start_time = datetime.now()
            
            # Create analysis prompts based on document type and context
            analysis_prompts = self._create_analysis_prompts(document_data, document_type, business_context)
            
            # Perform multiple types of analysis
            analyses = {}
            
            # Basic content analysis
            analyses['content_analysis'] = await self._analyze_content(document_data['content'], analysis_prompts['content'])
            
            # Business intelligence analysis
            analyses['business_intelligence'] = await self._analyze_business_intelligence(
                document_data['content'], 
                analysis_prompts['business_intelligence']
            )
            
            # Risk and opportunity analysis
            analyses['risk_opportunity'] = await self._analyze_risks_opportunities(
                document_data['content'],
                analysis_prompts['risk_opportunity']
            )
            
            # Action items extraction
            analyses['action_items'] = await self._extract_action_items(
                document_data['content'],
                analysis_prompts['action_items']
            )
            
            # Generate comprehensive summary
            summary = await self._generate_summary(analyses, document_type, business_context)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create final analysis result
            analysis_result = {
                'document_id': document_data['document_id'],
                'document_type': self._classify_document_type(document_data['content']),
                'key_insights': summary['key_insights'],
                'confidence_score': summary['confidence_score'],
                'recommended_actions': summary['recommended_actions'],
                'business_impact': analyses['business_intelligence'].get('impact_assessment', 'Medium'),
                'risk_level': analyses['risk_opportunity'].get('risk_level', 'Low'),
                'opportunities': analyses['risk_opportunity'].get('opportunities', []),
                'action_items': analyses['action_items'].get('items', []),
                'processing_time': processing_time,
                'analysis_timestamp': datetime.now().isoformat(),
                'detailed_analysis': analyses
            }
            
            # Update analytics
            self._update_analytics(analysis_result, processing_time)
            
            # Cache result
            self.analysis_cache[document_data['document_id']] = analysis_result
            
            return analysis_result
            
        except Exception as e:
            raise Exception(f"Error analyzing document: {str(e)}")
    
    def _create_analysis_prompts(self, document_data: Dict[str, Any], document_type: str, business_context: str) -> Dict[str, str]:
        """Create sophisticated prompts for different analysis types"""
        
        base_context = f"""
        Document Type: {document_type}
        Business Context: {business_context}
        Document Structure: {json.dumps(document_data.get('structure', {}), indent=2)}
        """
        
        prompts = {
            'content': f"""
            Analyze the following document content and provide a comprehensive content analysis.
            {base_context}
            
            Focus on:
            1. Main topics and themes
            2. Key information and data points
            3. Document structure and organization
            4. Writing quality and clarity
            5. Completeness of information
            
            Document Content:
            {document_data['content'][:4000]}  # Limit content for API efficiency
            
            Provide your analysis in JSON format with the following structure:
            {{
                "main_topics": ["topic1", "topic2", "topic3"],
                "key_information": ["info1", "info2", "info3"],
                "structure_quality": "excellent|good|fair|poor",
                "clarity_score": 1-10,
                "completeness_score": 1-10,
                "summary": "Brief summary of the document"
            }}
            """,
            
            'business_intelligence': f"""
            Perform business intelligence analysis on this document.
            {base_context}
            
            Analyze:
            1. Business value and relevance
            2. Financial implications
            3. Strategic importance
            4. Stakeholder impact
            5. Market implications
            
            Document Content:
            {document_data['content'][:4000]}
            
            Provide analysis in JSON format:
            {{
                "business_value": "high|medium|low",
                "financial_impact": "positive|neutral|negative",
                "strategic_importance": "critical|important|moderate|low",
                "stakeholder_impact": ["stakeholder1", "stakeholder2"],
                "market_implications": "description",
                "recommendations": ["rec1", "rec2", "rec3"]
            }}
            """,
            
            'risk_opportunity': f"""
            Analyze risks and opportunities in this document.
            {base_context}
            
            Identify:
            1. Potential risks and their severity
            2. Business opportunities
            3. Compliance issues
            4. Operational challenges
            5. Growth potential
            
            Document Content:
            {document_data['content'][:4000]}
            
            Provide analysis in JSON format:
            {{
                "risk_level": "high|medium|low",
                "risks": [{{"type": "risk_type", "severity": "high|medium|low", "description": "description"}}],
                "opportunities": [{{"type": "opportunity_type", "potential": "high|medium|low", "description": "description"}}],
                "compliance_issues": ["issue1", "issue2"],
                "mitigation_strategies": ["strategy1", "strategy2"]
            }}
            """,
            
            'action_items': f"""
            Extract actionable items from this document.
            {base_context}
            
            Find:
            1. Specific tasks and assignments
            2. Deadlines and timelines
            3. Responsible parties
            4. Dependencies
            5. Success criteria
            
            Document Content:
            {document_data['content'][:4000]}
            
            Provide in JSON format:
            {{
                "items": [
                    {{
                        "task": "task description",
                        "assignee": "responsible party",
                        "deadline": "deadline if mentioned",
                        "priority": "high|medium|low",
                        "dependencies": ["dep1", "dep2"]
                    }}
                ],
                "timeline": "overall timeline if available",
                "success_metrics": ["metric1", "metric2"]
            }}
            """
        }
        
        return prompts
    
    async def _analyze_content(self, content: str, prompt: str) -> Dict[str, Any]:
        """Analyze document content using AI"""
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert document analyst. Provide accurate, structured analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            return {"error": f"Content analysis failed: {str(e)}"}
    
    async def _analyze_business_intelligence(self, content: str, prompt: str) -> Dict[str, Any]:
        """Perform business intelligence analysis"""
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a business intelligence expert. Analyze documents for business value and strategic implications."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            return {"error": f"Business intelligence analysis failed: {str(e)}"}
    
    async def _analyze_risks_opportunities(self, content: str, prompt: str) -> Dict[str, Any]:
        """Analyze risks and opportunities"""
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a risk management and opportunity assessment expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            return {"error": f"Risk/opportunity analysis failed: {str(e)}"}
    
    async def _extract_action_items(self, content: str, prompt: str) -> Dict[str, Any]:
        """Extract actionable items from document"""
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a project management expert. Extract clear, actionable items from documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=600
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            return {"error": f"Action items extraction failed: {str(e)}"}
    
    async def _generate_summary(self, analyses: Dict[str, Any], document_type: str, business_context: str) -> Dict[str, Any]:
        """Generate comprehensive summary from all analyses"""
        try:
            summary_prompt = f"""
            Create a comprehensive summary of the document analysis.
            
            Document Type: {document_type}
            Business Context: {business_context}
            
            Analysis Results:
            {json.dumps(analyses, indent=2)}
            
            Provide a summary in JSON format:
            {{
                "key_insights": ["insight1", "insight2", "insight3"],
                "confidence_score": 85,
                "recommended_actions": ["action1", "action2", "action3"],
                "executive_summary": "Brief executive summary",
                "next_steps": ["step1", "step2"]
            }}
            """
            
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an executive assistant creating comprehensive document summaries."},
                    {"role": "user", "content": summary_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            return {
                "key_insights": ["Analysis completed with some limitations"],
                "confidence_score": 70,
                "recommended_actions": ["Review document manually for complete analysis"],
                "executive_summary": "Document analysis completed with AI assistance",
                "next_steps": ["Manual review recommended"]
            }
    
    def _classify_document_type(self, content: str) -> str:
        """Classify document type based on content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['contract', 'agreement', 'terms', 'conditions']):
            return 'contract'
        elif any(word in content_lower for word in ['invoice', 'bill', 'payment', 'amount', 'total']):
            return 'financial_document'
        elif any(word in content_lower for word in ['report', 'analysis', 'findings', 'conclusions']):
            return 'report'
        elif any(word in content_lower for word in ['proposal', 'suggestion', 'recommendation']):
            return 'proposal'
        elif any(word in content_lower for word in ['meeting', 'minutes', 'agenda', 'discussion']):
            return 'meeting_notes'
        else:
            return 'general_document'
    
    def _update_analytics(self, analysis_result: Dict[str, Any], processing_time: float):
        """Update analytics data"""
        self.analytics_data['total_documents'] += 1
        self.analytics_data['processing_times'].append(processing_time)
        
        doc_type = analysis_result['document_type']
        if doc_type not in self.analytics_data['analysis_types']:
            self.analytics_data['analysis_types'][doc_type] = 0
        self.analytics_data['analysis_types'][doc_type] += 1
        
        # Update average confidence
        total_docs = self.analytics_data['total_documents']
        current_avg = self.analytics_data['average_confidence']
        new_confidence = analysis_result['confidence_score']
        self.analytics_data['average_confidence'] = ((current_avg * (total_docs - 1)) + new_confidence) / total_docs
    
    async def get_analytics(self) -> Dict[str, Any]:
        """Get processing analytics"""
        avg_processing_time = sum(self.analytics_data['processing_times']) / len(self.analytics_data['processing_times']) if self.analytics_data['processing_times'] else 0
        
        return {
            'total_documents_processed': self.analytics_data['total_documents'],
            'average_processing_time': round(avg_processing_time, 2),
            'average_confidence_score': round(self.analytics_data['average_confidence'], 1),
            'document_types_analyzed': self.analytics_data['analysis_types'],
            'performance_metrics': {
                'fastest_processing': min(self.analytics_data['processing_times']) if self.analytics_data['processing_times'] else 0,
                'slowest_processing': max(self.analytics_data['processing_times']) if self.analytics_data['processing_times'] else 0
            }
        }