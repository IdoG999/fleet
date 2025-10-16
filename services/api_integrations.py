"""
API Integration Service
Handles integrations with external services and platforms
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class APIIntegrations:
    def __init__(self):
        self.integrations = {
            'slack': self._init_slack_integration(),
            'email': self._init_email_integration(),
            'google_drive': self._init_google_drive_integration(),
            'microsoft_teams': self._init_teams_integration(),
            'webhook': self._init_webhook_integration()
        }
        self.integration_status = {}
    
    def _init_slack_integration(self) -> Dict[str, Any]:
        """Initialize Slack integration"""
        return {
            'enabled': bool(os.getenv('SLACK_WEBHOOK_URL')),
            'webhook_url': os.getenv('SLACK_WEBHOOK_URL'),
            'default_channel': '#ai-document-processing',
            'bot_name': 'AI Document Bot'
        }
    
    def _init_email_integration(self) -> Dict[str, Any]:
        """Initialize email integration"""
        return {
            'enabled': bool(os.getenv('SMTP_SERVER')),
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
            'username': os.getenv('SMTP_USERNAME'),
            'password': os.getenv('SMTP_PASSWORD'),
            'from_email': os.getenv('FROM_EMAIL', 'ai-documents@company.com')
        }
    
    def _init_google_drive_integration(self) -> Dict[str, Any]:
        """Initialize Google Drive integration"""
        return {
            'enabled': bool(os.getenv('GOOGLE_DRIVE_CREDENTIALS')),
            'credentials_file': os.getenv('GOOGLE_DRIVE_CREDENTIALS'),
            'folder_id': os.getenv('GOOGLE_DRIVE_FOLDER_ID', 'root')
        }
    
    def _init_teams_integration(self) -> Dict[str, Any]:
        """Initialize Microsoft Teams integration"""
        return {
            'enabled': bool(os.getenv('TEAMS_WEBHOOK_URL')),
            'webhook_url': os.getenv('TEAMS_WEBHOOK_URL'),
            'default_channel': 'AI Document Processing'
        }
    
    def _init_webhook_integration(self) -> Dict[str, Any]:
        """Initialize generic webhook integration"""
        return {
            'enabled': True,  # Always available for custom integrations
            'endpoints': []
        }
    
    async def send_notification(self, message: str, channels: List[str], priority: str = 'normal') -> Dict[str, Any]:
        """Send notification to multiple channels"""
        results = {}
        
        for channel in channels:
            try:
                if channel == 'slack' and self.integrations['slack']['enabled']:
                    results[channel] = await self._send_slack_message(message, priority)
                elif channel == 'email' and self.integrations['email']['enabled']:
                    results[channel] = await self._send_email(message, priority)
                elif channel == 'teams' and self.integrations['microsoft_teams']['enabled']:
                    results[channel] = await self._send_teams_message(message, priority)
                else:
                    results[channel] = {'status': 'skipped', 'reason': f'Channel {channel} not configured'}
            except Exception as e:
                results[channel] = {'status': 'error', 'error': str(e)}
        
        return results
    
    async def _send_slack_message(self, message: str, priority: str) -> Dict[str, Any]:
        """Send message to Slack"""
        try:
            webhook_url = self.integrations['slack']['webhook_url']
            
            # Format message based on priority
            color = 'good' if priority == 'normal' else 'warning' if priority == 'high' else 'danger'
            
            payload = {
                'text': f"🤖 AI Document Processing Update",
                'attachments': [
                    {
                        'color': color,
                        'fields': [
                            {
                                'title': 'Message',
                                'value': message,
                                'short': False
                            },
                            {
                                'title': 'Priority',
                                'value': priority.upper(),
                                'short': True
                            },
                            {
                                'title': 'Timestamp',
                                'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'short': True
                            }
                        ]
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 200:
                        return {'status': 'success', 'response': 'Message sent to Slack'}
                    else:
                        return {'status': 'error', 'error': f'Slack API returned status {response.status}'}
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def _send_email(self, message: str, priority: str) -> Dict[str, Any]:
        """Send email notification"""
        try:
            # In a real implementation, you would use an email library like smtplib
            # For demo purposes, we'll simulate email sending
            subject = f"[{priority.upper()}] AI Document Processing Update"
            
            email_data = {
                'to': 'recipient@company.com',
                'subject': subject,
                'body': message,
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            }
            
            # Simulate email sending
            await asyncio.sleep(0.1)  # Simulate network delay
            
            return {
                'status': 'success',
                'response': f'Email sent to {email_data["to"]}',
                'email_data': email_data
            }
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def _send_teams_message(self, message: str, priority: str) -> Dict[str, Any]:
        """Send message to Microsoft Teams"""
        try:
            webhook_url = self.integrations['microsoft_teams']['webhook_url']
            
            # Format message for Teams
            color = '00ff00' if priority == 'normal' else 'ffaa00' if priority == 'high' else 'ff0000'
            
            payload = {
                '@type': 'MessageCard',
                '@context': 'http://schema.org/extensions',
                'themeColor': color,
                'summary': 'AI Document Processing Update',
                'sections': [
                    {
                        'activityTitle': '🤖 AI Document Processing',
                        'activitySubtitle': f'Priority: {priority.upper()}',
                        'activityImage': 'https://via.placeholder.com/64x64/4CAF50/white?text=AI',
                        'text': message,
                        'facts': [
                            {
                                'name': 'Timestamp',
                                'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                        ]
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 200:
                        return {'status': 'success', 'response': 'Message sent to Teams'}
                    else:
                        return {'status': 'error', 'error': f'Teams API returned status {response.status}'}
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def upload_to_cloud_storage(self, file_path: str, destination: str) -> Dict[str, Any]:
        """Upload file to cloud storage"""
        try:
            if self.integrations['google_drive']['enabled']:
                return await self._upload_to_google_drive(file_path, destination)
            else:
                return {'status': 'skipped', 'reason': 'Cloud storage not configured'}
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def _upload_to_google_drive(self, file_path: str, destination: str) -> Dict[str, Any]:
        """Upload file to Google Drive"""
        try:
            # In a real implementation, you would use the Google Drive API
            # For demo purposes, we'll simulate the upload
            file_name = os.path.basename(file_path)
            
            upload_data = {
                'file_name': file_name,
                'destination': destination,
                'upload_time': datetime.now().isoformat(),
                'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
            
            # Simulate upload process
            await asyncio.sleep(0.5)  # Simulate network delay
            
            return {
                'status': 'success',
                'response': f'File {file_name} uploaded to Google Drive',
                'upload_data': upload_data
            }
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def create_webhook_endpoint(self, url: str, events: List[str]) -> Dict[str, Any]:
        """Create webhook endpoint for external integrations"""
        try:
            webhook_id = f"wh_{int(datetime.now().timestamp())}"
            
            webhook_config = {
                'webhook_id': webhook_id,
                'url': url,
                'events': events,
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            self.integrations['webhook']['endpoints'].append(webhook_config)
            
            return {
                'status': 'success',
                'webhook_id': webhook_id,
                'config': webhook_config
            }
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def trigger_webhook(self, event: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger webhook for specific event"""
        results = {}
        
        for webhook in self.integrations['webhook']['endpoints']:
            if event in webhook['events'] and webhook['status'] == 'active':
                try:
                    payload = {
                        'event': event,
                        'data': data,
                        'timestamp': datetime.now().isoformat(),
                        'webhook_id': webhook['webhook_id']
                    }
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.post(webhook['url'], json=payload) as response:
                            results[webhook['webhook_id']] = {
                                'status': 'success' if response.status == 200 else 'error',
                                'response_code': response.status
                            }
                
                except Exception as e:
                    results[webhook['webhook_id']] = {
                        'status': 'error',
                        'error': str(e)
                    }
        
        return results
    
    async def integrate_with_crm(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate document data with CRM system"""
        try:
            # Simulate CRM integration
            crm_data = {
                'document_id': document_data.get('document_id'),
                'customer_name': self._extract_customer_name(document_data.get('content', '')),
                'document_type': document_data.get('document_type'),
                'created_at': datetime.now().isoformat(),
                'status': 'processed'
            }
            
            # Simulate API call to CRM
            await asyncio.sleep(0.2)
            
            return {
                'status': 'success',
                'crm_record_id': f"crm_{int(datetime.now().timestamp())}",
                'data': crm_data
            }
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _extract_customer_name(self, content: str) -> str:
        """Extract customer name from document content"""
        # Simple extraction logic - in production, use more sophisticated NLP
        lines = content.split('\n')
        for line in lines:
            if 'customer' in line.lower() or 'client' in line.lower():
                return line.strip()
        return 'Unknown Customer'
    
    async def integrate_with_accounting(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate financial data with accounting system"""
        try:
            # Simulate accounting system integration
            accounting_entry = {
                'entry_id': f"acc_{int(datetime.now().timestamp())}",
                'amount': financial_data.get('amount', 0),
                'description': financial_data.get('description', 'Document processing'),
                'account_code': financial_data.get('account_code', '1000'),
                'date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'pending_approval'
            }
            
            # Simulate API call to accounting system
            await asyncio.sleep(0.3)
            
            return {
                'status': 'success',
                'entry_id': accounting_entry['entry_id'],
                'data': accounting_entry
            }
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrations"""
        status = {}
        for name, config in self.integrations.items():
            status[name] = {
                'enabled': config['enabled'],
                'configured': bool(config.get('webhook_url') or config.get('smtp_server') or config.get('credentials_file')),
                'last_check': datetime.now().isoformat()
            }
        return status
    
    async def test_integration(self, integration_name: str) -> Dict[str, Any]:
        """Test specific integration"""
        try:
            if integration_name == 'slack' and self.integrations['slack']['enabled']:
                return await self._send_slack_message("Integration test message", "normal")
            elif integration_name == 'email' and self.integrations['email']['enabled']:
                return await self._send_email("Integration test message", "normal")
            elif integration_name == 'teams' and self.integrations['microsoft_teams']['enabled']:
                return await self._send_teams_message("Integration test message", "normal")
            else:
                return {'status': 'skipped', 'reason': f'Integration {integration_name} not configured'}
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}