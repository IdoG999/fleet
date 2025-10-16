"""
Advanced Document Processing Service
Handles multiple document formats with intelligent content extraction
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import PyPDF2
from docx import Document
import pandas as pd

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg']
        self.processed_docs = {}
    
    async def process_document(self, file_path: str, filename: str) -> Dict[str, Any]:
        """Process document and extract structured data"""
        try:
            file_extension = Path(filename).suffix.lower()
            
            if file_extension not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            # Generate unique document ID
            doc_id = self._generate_document_id(file_path, filename)
            
            # Extract content based on file type
            if file_extension == '.pdf':
                content = await self._extract_pdf_content(file_path)
            elif file_extension == '.docx':
                content = await self._extract_docx_content(file_path)
            elif file_extension == '.txt':
                content = await self._extract_text_content(file_path)
            else:
                content = await self._extract_image_content(file_path)
            
            # Create document metadata
            document_data = {
                'document_id': doc_id,
                'filename': filename,
                'file_path': file_path,
                'file_type': file_extension,
                'content': content,
                'metadata': {
                    'file_size': os.path.getsize(file_path),
                    'processed_at': datetime.now().isoformat(),
                    'word_count': len(content.split()) if content else 0,
                    'character_count': len(content) if content else 0
                },
                'structure': self._analyze_document_structure(content)
            }
            
            # Store processed document
            self.processed_docs[doc_id] = document_data
            
            return document_data
            
        except Exception as e:
            raise Exception(f"Error processing document {filename}: {str(e)}")
    
    def _generate_document_id(self, file_path: str, filename: str) -> str:
        """Generate unique document ID based on content hash"""
        with open(file_path, 'rb') as f:
            content_hash = hashlib.md5(f.read()).hexdigest()[:12]
        return f"doc_{content_hash}_{int(datetime.now().timestamp())}"
    
    async def _extract_pdf_content(self, file_path: str) -> str:
        """Extract text content from PDF"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting PDF content: {str(e)}")
    
    async def _extract_docx_content(self, file_path: str) -> str:
        """Extract text content from DOCX"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting DOCX content: {str(e)}")
    
    async def _extract_text_content(self, file_path: str) -> str:
        """Extract text content from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            raise Exception(f"Error extracting text content: {str(e)}")
    
    async def _extract_image_content(self, file_path: str) -> str:
        """Placeholder for image content extraction (would use OCR in production)"""
        return f"[Image file: {Path(file_path).name}] - OCR processing would be implemented here"
    
    def _analyze_document_structure(self, content: str) -> Dict[str, Any]:
        """Analyze document structure and extract key elements"""
        if not content:
            return {}
        
        lines = content.split('\n')
        
        # Extract potential headers (lines that are short and might be titles)
        headers = [line.strip() for line in lines if len(line.strip()) < 100 and line.strip().isupper()]
        
        # Extract potential lists
        list_items = [line.strip() for line in lines if line.strip().startswith(('-', '*', '•', '1.', '2.', '3.'))]
        
        # Extract potential data tables (lines with multiple separators)
        table_rows = [line.strip() for line in lines if '|' in line or '\t' in line]
        
        return {
            'total_lines': len(lines),
            'headers': headers[:10],  # Limit to first 10 headers
            'list_items': list_items[:20],  # Limit to first 20 list items
            'table_rows': table_rows[:10],  # Limit to first 10 table rows
            'has_numbers': any(char.isdigit() for char in content),
            'has_emails': '@' in content,
            'has_urls': 'http' in content.lower(),
            'has_dates': any(word in content.lower() for word in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'])
        }
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve processed document by ID"""
        return self.processed_docs.get(document_id)
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all processed documents"""
        return list(self.processed_docs.values())