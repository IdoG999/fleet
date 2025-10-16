#!/usr/bin/env python3
"""
Demo script for AI Document Intelligence Platform
Demonstrates the platform's capabilities with sample documents
"""

import asyncio
import json
import os
from pathlib import Path
from services.document_processor import DocumentProcessor
from services.ai_analyzer import AIAnalyzer
from services.workflow_engine import WorkflowEngine
from services.api_integrations import APIIntegrations

async def create_sample_documents():
    """Create sample documents for demonstration"""
    
    # Create sample contract document
    contract_content = """
    SOFTWARE LICENSE AGREEMENT
    
    This Software License Agreement ("Agreement") is entered into on January 15, 2024, between:
    
    Licensor: TechCorp Solutions Inc.
    Address: 123 Technology Drive, Silicon Valley, CA 94000
    
    Licensee: AI Innovations Ltd.
    Address: 456 Innovation Street, Tel Aviv, Israel 67890
    
    TERMS AND CONDITIONS:
    
    1. GRANT OF LICENSE
    Subject to the terms and conditions of this Agreement, Licensor hereby grants to Licensee a non-exclusive, non-transferable license to use the Software.
    
    2. LICENSE FEE
    Licensee agrees to pay Licensor a one-time license fee of $50,000 within 30 days of execution of this Agreement.
    
    3. TERM
    This Agreement shall commence on the Effective Date and continue for a period of three (3) years.
    
    4. INTELLECTUAL PROPERTY
    All rights, title, and interest in and to the Software remain with Licensor.
    
    5. CONFIDENTIALITY
    Both parties agree to maintain the confidentiality of all proprietary information.
    
    6. TERMINATION
    Either party may terminate this Agreement with 30 days written notice.
    
    IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.
    
    TechCorp Solutions Inc.          AI Innovations Ltd.
    _________________               _________________
    John Smith, CEO                 Sarah Cohen, CTO
    """
    
    # Create sample financial document
    financial_content = """
    INVOICE
    
    Invoice Number: INV-2024-001
    Date: January 15, 2024
    Due Date: February 14, 2024
    
    BILL TO:
    AI Innovations Ltd.
    456 Innovation Street
    Tel Aviv, Israel 67890
    
    FROM:
    CloudTech Services
    789 Cloud Avenue
    San Francisco, CA 94105
    
    DESCRIPTION OF SERVICES:
    
    Item 1: AI Model Training Services
    Quantity: 100 hours
    Rate: $150.00/hour
    Amount: $15,000.00
    
    Item 2: Data Processing Services
    Quantity: 50 hours
    Rate: $100.00/hour
    Amount: $5,000.00
    
    Item 3: Cloud Infrastructure
    Quantity: 1 month
    Rate: $2,500.00/month
    Amount: $2,500.00
    
    SUBTOTAL: $22,500.00
    TAX (8.5%): $1,912.50
    TOTAL: $24,412.50
    
    Payment Terms: Net 30
    Payment Method: Bank Transfer
    
    Thank you for your business!
    """
    
    # Create sample business report
    report_content = """
    QUARTERLY BUSINESS REPORT
    Q4 2023 - AI Solutions Division
    
    EXECUTIVE SUMMARY:
    The AI Solutions Division has shown remarkable growth in Q4 2023, with a 35% increase in revenue and successful deployment of three major AI projects.
    
    KEY ACHIEVEMENTS:
    1. Launched AI Document Processing Platform
    2. Secured 5 new enterprise clients
    3. Reduced processing time by 60%
    4. Achieved 99.5% accuracy in document analysis
    
    FINANCIAL PERFORMANCE:
    - Revenue: $2.5M (35% increase from Q3)
    - Profit Margin: 28% (up from 22% in Q3)
    - Customer Acquisition Cost: $15,000 (down 25%)
    - Customer Lifetime Value: $180,000 (up 40%)
    
    MARKET ANALYSIS:
    The AI document processing market is growing at 45% CAGR. Our competitive advantages include:
    - Advanced prompt engineering
    - Multi-format support
    - Real-time processing
    - Enterprise-grade security
    
    CHALLENGES AND OPPORTUNITIES:
    Challenges:
    - Talent acquisition in competitive market
    - Scaling infrastructure for growth
    - Regulatory compliance requirements
    
    Opportunities:
    - International expansion
    - New vertical markets
    - Strategic partnerships
    - Product line extensions
    
    RECOMMENDATIONS:
    1. Invest in talent acquisition and retention
    2. Expand infrastructure capacity
    3. Develop compliance automation tools
    4. Explore European and Asian markets
    5. Consider acquisition opportunities
    
    NEXT QUARTER PRIORITIES:
    1. Launch mobile application
    2. Implement advanced analytics
    3. Expand integration capabilities
    4. Strengthen security measures
    5. Prepare for Series B funding
    """
    
    # Save sample documents
    os.makedirs("sample_documents", exist_ok=True)
    
    with open("sample_documents/contract.txt", "w") as f:
        f.write(contract_content)
    
    with open("sample_documents/invoice.txt", "w") as f:
        f.write(financial_content)
    
    with open("sample_documents/quarterly_report.txt", "w") as f:
        f.write(report_content)
    
    print("✅ Sample documents created successfully!")

async def demonstrate_platform():
    """Demonstrate platform capabilities"""
    
    print("🚀 AI Document Intelligence Platform Demo")
    print("=" * 50)
    
    # Initialize services
    document_processor = DocumentProcessor()
    ai_analyzer = AIAnalyzer()
    workflow_engine = WorkflowEngine()
    api_integrations = APIIntegrations()
    
    # Create sample documents
    await create_sample_documents()
    
    # Process each sample document
    sample_files = [
        ("sample_documents/contract.txt", "contract", "legal_review"),
        ("sample_documents/invoice.txt", "financial_document", "financial_processing"),
        ("sample_documents/quarterly_report.txt", "report", "business_analysis")
    ]
    
    results = []
    
    for file_path, doc_type, business_context in sample_files:
        print(f"\n📄 Processing: {file_path}")
        print("-" * 30)
        
        try:
            # Process document
            processed_doc = await document_processor.process_document(file_path, os.path.basename(file_path))
            print(f"✅ Document processed: {processed_doc['document_id']}")
            
            # Analyze with AI (simulated for demo)
            print("🤖 Running AI analysis...")
            analysis = {
                'document_id': processed_doc['document_id'],
                'document_type': doc_type,
                'key_insights': [
                    f"Document type: {doc_type}",
                    f"Word count: {processed_doc['metadata']['word_count']}",
                    f"Business context: {business_context}"
                ],
                'confidence_score': 85,
                'recommended_actions': [
                    "Review document for accuracy",
                    "Process through appropriate workflow",
                    "Notify relevant stakeholders"
                ],
                'business_impact': 'high' if doc_type == 'contract' else 'medium',
                'risk_level': 'high' if doc_type == 'contract' else 'low',
                'processing_time': 2.5
            }
            
            print(f"📊 Analysis complete - Confidence: {analysis['confidence_score']}%")
            print(f"🎯 Key insights: {len(analysis['key_insights'])} identified")
            
            # Generate workflow recommendations
            workflow_result = await workflow_engine.generate_workflow(analysis)
            print(f"⚡ Workflow suggestions: {len(workflow_result.get('suggested_workflows', []))} generated")
            
            results.append({
                'file': file_path,
                'analysis': analysis,
                'workflow': workflow_result
            })
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")
    
    # Display summary
    print("\n" + "=" * 50)
    print("📈 DEMO SUMMARY")
    print("=" * 50)
    
    print(f"📄 Documents processed: {len(results)}")
    print(f"🤖 AI analyses completed: {len([r for r in results if 'analysis' in r])}")
    print(f"⚡ Workflows generated: {sum(len(r.get('workflow', {}).get('suggested_workflows', [])) for r in results)}")
    
    # Show integration status
    print(f"\n🔗 Integration Status:")
    integration_status = api_integrations.get_integration_status()
    for name, status in integration_status.items():
        status_icon = "✅" if status['enabled'] else "❌"
        print(f"  {status_icon} {name.title()}: {'Enabled' if status['enabled'] else 'Disabled'}")
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"🌐 Access the web interface at: http://localhost:8000")
    print(f"📚 API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    asyncio.run(demonstrate_platform())