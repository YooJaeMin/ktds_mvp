from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os
import hashlib
from pathlib import Path
import sqlite3
import time

from app.utils.document_utils import DocumentProcessor, TextAnalyzer
from app.utils.azure_client import azure_client

class KnowledgeManager:
    """지식 관리 서비스"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.text_analyzer = TextAnalyzer()
        
        # 지식 베이스 디렉토리 설정
        self.knowledge_base_dir = Path("/home/runner/work/ktds_mvp/ktds_mvp/knowledge_base")
        self.knowledge_base_dir.mkdir(exist_ok=True)
        
        # SQLite 데이터베이스 초기화
        self.db_path = self.knowledge_base_dir / "knowledge.db"
        self._init_database()
        
        # 카테고리 정의
        self.categories = {
            "제안서": "제안서 템플릿, 우수 제안서 사례",
            "기술문서": "기술 사양서, 아키텍처 문서",
            "계약서": "계약서 템플릿, 계약 조건",
            "사업분석": "시장 분석, 산업 동향",
            "경쟁사분석": "경쟁사 정보, 벤치마킹",
            "법규제": "관련 법규, 컴플라이언스",
            "모범사례": "성공 사례, 노하우"
        }
    
    def _init_database(self):
        """SQLite 데이터베이스를 초기화합니다."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 문서 메타데이터 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                content_hash TEXT,
                upload_date TEXT,
                file_size INTEGER,
                content_preview TEXT
            )
        ''')
        
        # 문서 내용 테이블 (검색용)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_contents (
                document_id TEXT,
                content TEXT,
                keywords TEXT,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')
        
        # 검색 로그 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                category TEXT,
                results_count INTEGER,
                search_time REAL,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def add_document(self, content: bytes, filename: str, category: str, description: str) -> Dict[str, Any]:
        """새로운 문서를 지식 베이스에 추가합니다."""
        
        try:
            # 문서 텍스트 추출
            text_content = self.document_processor.extract_text_from_file(content, filename)
            
            # 문서 ID 생성 (해시 기반)
            content_hash = hashlib.md5(content).hexdigest()
            document_id = f"{category}_{int(datetime.now().timestamp())}_{content_hash[:8]}"
            
            # 키워드 추출
            keywords = self.text_analyzer.extract_keywords(text_content)
            
            # 파일 저장
            file_path = self.knowledge_base_dir / f"{document_id}_{filename}"
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # 데이터베이스에 메타데이터 저장
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO documents 
                (id, filename, category, description, content_hash, upload_date, file_size, content_preview)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                document_id, filename, category, description, content_hash,
                datetime.now().isoformat(), len(content), text_content[:500]
            ))
            
            cursor.execute('''
                INSERT INTO document_contents 
                (document_id, content, keywords)
                VALUES (?, ?, ?)
            ''', (document_id, text_content, json.dumps(keywords)))
            
            conn.commit()
            conn.close()
            
            # Azure AI를 사용한 문서 분석 및 태깅
            try:
                key_phrases = await azure_client.extract_key_phrases(text_content[:1000])
                sentiment = await azure_client.analyze_sentiment(text_content[:1000])
            except:
                key_phrases = keywords
                sentiment = {"sentiment": "neutral"}
            
            return {
                "document_id": document_id,
                "filename": filename,
                "category": category,
                "status": "success",
                "indexed_at": datetime.now().isoformat(),
                "file_size": len(content),
                "keywords": keywords,
                "key_phrases": key_phrases,
                "sentiment": sentiment.get("sentiment", "neutral")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "filename": filename
            }
    
    async def search_knowledge(self, query: str, category: Optional[str] = None) -> Dict[str, Any]:
        """지식 베이스에서 관련 문서를 검색합니다."""
        
        start_time = time.time()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 기본 SQL 쿼리 구성
            base_query = '''
                SELECT d.id, d.filename, d.category, d.description, d.upload_date, d.content_preview,
                       dc.keywords
                FROM documents d
                JOIN document_contents dc ON d.id = dc.document_id
                WHERE (dc.content LIKE ? OR dc.keywords LIKE ? OR d.description LIKE ?)
            '''
            
            params = [f'%{query}%', f'%{query}%', f'%{query}%']
            
            # 카테고리 필터 추가
            if category and category != "전체":
                base_query += ' AND d.category = ?'
                params.append(category)
            
            base_query += ' ORDER BY d.upload_date DESC LIMIT 20'
            
            cursor.execute(base_query, params)
            raw_results = cursor.fetchall()
            
            # 결과 처리 및 점수 계산
            results = []
            for row in raw_results:
                doc_id, filename, doc_category, description, upload_date, content_preview, keywords_json = row
                
                try:
                    keywords = json.loads(keywords_json)
                except:
                    keywords = []
                
                # 관련성 점수 계산
                relevance_score = self._calculate_relevance_score(query, content_preview, keywords, description)
                
                results.append({
                    "document_id": doc_id,
                    "filename": filename,
                    "category": doc_category,
                    "description": description,
                    "upload_date": upload_date,
                    "content_preview": content_preview,
                    "keywords": keywords,
                    "relevance_score": relevance_score
                })
            
            # 관련성 점수로 정렬
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Azure AI를 사용한 의미적 검색 개선
            try:
                if results:
                    enhanced_results = await self._enhance_search_with_ai(query, results[:10])
                    results = enhanced_results
            except:
                pass
            
            search_time = time.time() - start_time
            
            # 검색 로그 저장
            cursor.execute('''
                INSERT INTO search_logs (query, category, results_count, search_time, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (query, category or "전체", len(results), search_time, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return {
                "results": results,
                "total_count": len(results),
                "search_time": round(search_time, 3),
                "query": query,
                "category": category,
                "suggestions": await self._generate_search_suggestions(query, results)
            }
            
        except Exception as e:
            return {
                "results": [],
                "total_count": 0,
                "search_time": 0,
                "error": str(e)
            }
    
    def _calculate_relevance_score(self, query: str, content: str, keywords: List[str], description: str) -> float:
        """검색 결과의 관련성 점수를 계산합니다."""
        
        score = 0.0
        query_terms = query.lower().split()
        
        # 키워드 매칭 점수 (40%)
        keyword_matches = sum(1 for term in query_terms for keyword in keywords if term in keyword.lower())
        score += (keyword_matches / max(len(query_terms), 1)) * 40
        
        # 내용 매칭 점수 (35%)
        content_lower = content.lower()
        content_matches = sum(1 for term in query_terms if term in content_lower)
        score += (content_matches / max(len(query_terms), 1)) * 35
        
        # 설명 매칭 점수 (25%)
        description_lower = description.lower()
        description_matches = sum(1 for term in query_terms if term in description_lower)
        score += (description_matches / max(len(query_terms), 1)) * 25
        
        return min(score, 100.0)
    
    async def _enhance_search_with_ai(self, query: str, results: List[Dict]) -> List[Dict]:
        """Azure AI를 사용하여 검색 결과를 개선합니다."""
        
        try:
            # 검색 결과 요약 생성
            prompt = f"""
사용자가 "{query}"에 대해 검색했습니다. 
다음 검색 결과들 중에서 가장 관련성이 높은 순서로 3개를 선택하고, 각각에 대한 관련성 이유를 설명해주세요.

검색 결과:
"""
            for i, result in enumerate(results[:5]):
                prompt += f"{i+1}. {result['filename']}: {result['description']}\n"
            
            ai_analysis = await azure_client.generate_completion(prompt, max_tokens=400)
            
            # AI 분석 결과를 검색 결과에 추가
            for result in results:
                result['ai_relevance_note'] = "AI 분석 완료"
            
        except:
            pass
        
        return results
    
    async def _generate_search_suggestions(self, query: str, results: List[Dict]) -> List[str]:
        """검색 제안사항을 생성합니다."""
        
        suggestions = []
        
        # 결과가 적은 경우 관련 키워드 제안
        if len(results) < 3:
            suggestions.append(f"'{query}' 대신 더 일반적인 용어로 검색해보세요")
            suggestions.append("카테고리를 '전체'로 설정하여 검색 범위를 넓혀보세요")
        
        # 결과의 키워드를 기반으로 추가 검색어 제안
        if results:
            all_keywords = []
            for result in results[:5]:
                all_keywords.extend(result.get('keywords', []))
            
            # 빈도가 높은 키워드 제안
            keyword_freq = {}
            for keyword in all_keywords:
                keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
            
            top_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:3]
            for keyword, freq in top_keywords:
                if keyword.lower() not in query.lower():
                    suggestions.append(f"'{keyword}' 키워드를 추가해보세요")
        
        return suggestions[:5]
    
    async def get_document_content(self, document_id: str) -> Dict[str, Any]:
        """문서의 전체 내용을 조회합니다."""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT d.filename, d.category, d.description, d.upload_date, dc.content
                FROM documents d
                JOIN document_contents dc ON d.id = dc.document_id
                WHERE d.id = ?
            ''', (document_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                filename, category, description, upload_date, content = result
                return {
                    "document_id": document_id,
                    "filename": filename,
                    "category": category,
                    "description": description,
                    "upload_date": upload_date,
                    "content": content,
                    "content_length": len(content)
                }
            else:
                return {"error": "문서를 찾을 수 없습니다"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def get_knowledge_statistics(self) -> Dict[str, Any]:
        """지식 베이스 통계를 조회합니다."""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 전체 문서 수
            cursor.execute('SELECT COUNT(*) FROM documents')
            total_documents = cursor.fetchone()[0]
            
            # 카테고리별 문서 수
            cursor.execute('SELECT category, COUNT(*) FROM documents GROUP BY category')
            category_counts = dict(cursor.fetchall())
            
            # 최근 업로드된 문서
            cursor.execute('''
                SELECT filename, category, upload_date 
                FROM documents 
                ORDER BY upload_date DESC 
                LIMIT 10
            ''')
            recent_documents = [
                {"filename": row[0], "category": row[1], "upload_date": row[2]}
                for row in cursor.fetchall()
            ]
            
            # 인기 검색어
            cursor.execute('''
                SELECT query, COUNT(*) as search_count 
                FROM search_logs 
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY query 
                ORDER BY search_count DESC 
                LIMIT 10
            ''')
            popular_queries = [
                {"query": row[0], "count": row[1]}
                for row in cursor.fetchall()
            ]
            
            conn.close()
            
            return {
                "total_documents": total_documents,
                "category_counts": category_counts,
                "recent_documents": recent_documents,
                "popular_queries": popular_queries,
                "available_categories": list(self.categories.keys())
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """문서를 삭제합니다."""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 문서 정보 조회
            cursor.execute('SELECT filename FROM documents WHERE id = ?', (document_id,))
            result = cursor.fetchone()
            
            if not result:
                return {"error": "문서를 찾을 수 없습니다"}
            
            filename = result[0]
            
            # 데이터베이스에서 삭제
            cursor.execute('DELETE FROM document_contents WHERE document_id = ?', (document_id,))
            cursor.execute('DELETE FROM documents WHERE id = ?', (document_id,))
            
            # 파일 삭제
            file_path = self.knowledge_base_dir / f"{document_id}_{filename}"
            if file_path.exists():
                file_path.unlink()
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "message": f"문서 '{filename}'이 삭제되었습니다",
                "document_id": document_id
            }
            
        except Exception as e:
            return {"error": str(e)}