"""
성능 최적화 및 캐싱 모듈
"""
import streamlit as st
import hashlib
import time
from functools import wraps
from typing import Dict, Any, Optional
import concurrent.futures
import threading

class PerformanceOptimizer:
    """성능 최적화 클래스"""
    
    def __init__(self):
        self._cache = {}
        self._cache_lock = threading.Lock()
        self._max_cache_size = 100
        self._cache_ttl = 3600  # 1시간
    
    def cache_result(self, ttl: int = 3600):
        """결과 캐싱 데코레이터"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 캐시 키 생성
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)
                
                # 캐시에서 결과 확인
                with self._cache_lock:
                    if cache_key in self._cache:
                        cached_result, timestamp = self._cache[cache_key]
                        if time.time() - timestamp < ttl:
                            return cached_result
                
                # 캐시에 없으면 실행
                result = func(*args, **kwargs)
                
                # 결과 캐싱
                with self._cache_lock:
                    self._cache[cache_key] = (result, time.time())
                    self._cleanup_cache()
                
                return result
            return wrapper
        return decorator
    
    def _generate_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """캐시 키 생성"""
        key_data = f"{func_name}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _cleanup_cache(self):
        """캐시 정리"""
        if len(self._cache) > self._max_cache_size:
            # 오래된 항목 제거
            sorted_items = sorted(
                self._cache.items(), 
                key=lambda x: x[1][1]
            )
            items_to_remove = len(sorted_items) - self._max_cache_size
            for i in range(items_to_remove):
                del self._cache[sorted_items[i][0]]
    
    def clear_cache(self):
        """캐시 초기화"""
        with self._cache_lock:
            self._cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """캐시 통계 반환"""
        with self._cache_lock:
            return {
                'cache_size': len(self._cache),
                'max_size': self._max_cache_size,
                'ttl': self._cache_ttl
            }

# 전역 성능 최적화 인스턴스
performance_optimizer = PerformanceOptimizer()

def optimize_azure_calls():
    """Azure API 호출 최적화"""
    @performance_optimizer.cache_result(ttl=1800)  # 30분 캐시
    def cached_openai_call(messages, model="gpt-4.1", temperature=0.7):
        """캐시된 OpenAI 호출"""
        from azure_services import AzureServices
        azure_services = AzureServices()
        return azure_services.call_openai(messages, model, temperature)
    
    return cached_openai_call

def parallel_analysis_executor(analyses: list, max_workers: int = 4):
    """병렬 분석 실행기"""
    def execute_parallel():
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 모든 분석을 병렬로 실행
            future_to_analysis = {
                executor.submit(analysis['func'], *analysis['args'], **analysis['kwargs']): analysis['name']
                for analysis in analyses
            }
            
            results = {}
            for future in concurrent.futures.as_completed(future_to_analysis):
                analysis_name = future_to_analysis[future]
                try:
                    results[analysis_name] = future.result()
                except Exception as e:
                    results[analysis_name] = f"분석 오류: {str(e)}"
            
            return results
    
    return execute_parallel()

def memory_optimized_file_processing(file_data: bytes, chunk_size: int = 8192):
    """메모리 최적화된 파일 처리"""
    def process_in_chunks():
        for i in range(0, len(file_data), chunk_size):
            chunk = file_data[i:i + chunk_size]
            yield chunk
    
    return process_in_chunks()

def session_state_optimizer():
    """세션 상태 최적화"""
    # 불필요한 세션 상태 정리
    keys_to_remove = []
    for key in st.session_state.keys():
        if key.startswith('temp_') or key.startswith('cache_'):
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]

def get_performance_metrics() -> Dict[str, Any]:
    """성능 메트릭 반환"""
    cache_stats = performance_optimizer.get_cache_stats()
    
    return {
        'cache_stats': cache_stats,
        'session_state_size': len(st.session_state),
        'memory_usage': 'N/A',  # Streamlit에서 직접 메모리 측정 어려움
        'optimization_status': 'Active'
    }
