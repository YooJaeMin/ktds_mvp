import io
import os
from typing import Dict, Any
import PyPDF2
from docx import Document

class DocumentProcessor:
    """문서 처리를 위한 유틸리티 클래스"""
    
    @staticmethod
    def extract_text_from_pdf(content: bytes) -> str:
        """PDF에서 텍스트를 추출합니다."""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF 텍스트 추출 실패: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(content: bytes) -> str:
        """DOCX에서 텍스트를 추출합니다."""
        try:
            doc_file = io.BytesIO(content)
            doc = Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"DOCX 텍스트 추출 실패: {str(e)}")
    
    @staticmethod
    def extract_text_from_file(content: bytes, filename: str) -> str:
        """파일 확장자에 따라 적절한 텍스트 추출 방법을 선택합니다."""
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension == '.pdf':
            return DocumentProcessor.extract_text_from_pdf(content)
        elif file_extension in ['.docx', '.doc']:
            return DocumentProcessor.extract_text_from_docx(content)
        elif file_extension == '.txt':
            return content.decode('utf-8')
        else:
            raise Exception(f"지원하지 않는 파일 형식: {file_extension}")

class TextAnalyzer:
    """텍스트 분석을 위한 유틸리티 클래스"""
    
    @staticmethod
    def calculate_readability_score(text: str) -> float:
        """텍스트의 가독성 점수를 계산합니다."""
        sentences = text.split('.')
        words = text.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        # 간단한 가독성 점수 (실제로는 더 복잡한 알고리즘 사용)
        score = max(0, min(100, 100 - (avg_sentence_length - 15) * 2))
        return round(score, 2)
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 10) -> list:
        """텍스트에서 주요 키워드를 추출합니다."""
        # 간단한 키워드 추출 (실제로는 TF-IDF나 다른 방법 사용)
        words = text.lower().split()
        word_freq = {}
        
        # 불용어 제거 (간단한 버전)
        stop_words = {'의', '이', '가', '을', '를', '에', '와', '과', '으로', '로', '에서', '은', '는'}
        
        for word in words:
            if len(word) > 2 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 빈도수로 정렬
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]