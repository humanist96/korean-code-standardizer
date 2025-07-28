"""
Batch Processing and Real-time Analysis Module
Handles multiple code files and real-time variable name analysis
"""

import os
import glob
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

from variable_name_standardizer import CodeReviewer
from advanced_analyzer import AdvancedCodeReviewer


@dataclass
class BatchResult:
    """Result of batch processing"""
    file_path: str
    total_lines: int
    issues_found: int
    processing_time: float
    results: List[Any]
    error: Optional[str] = None


class BatchProcessor:
    """Handles batch processing of multiple code files"""
    
    def __init__(self, csv_path: str = "용어사전.csv"):
        self.reviewer = CodeReviewer(csv_path)
        self.advanced_reviewer = AdvancedCodeReviewer(csv_path)
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def process_directory(self, directory: str, pattern: str = "*.py", 
                         recursive: bool = True) -> List[BatchResult]:
        """Process all files in a directory"""
        if recursive:
            files = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
        else:
            files = glob.glob(os.path.join(directory, pattern))
        
        return self.process_files(files)
    
    def process_files(self, file_paths: List[str]) -> List[BatchResult]:
        """Process multiple files in parallel"""
        futures = []
        for file_path in file_paths:
            future = self.executor.submit(self._process_single_file, file_path)
            futures.append((file_path, future))
        
        results = []
        for file_path, future in futures:
            try:
                result = future.result(timeout=30)  # 30 second timeout
                results.append(result)
            except Exception as e:
                results.append(BatchResult(
                    file_path=file_path,
                    total_lines=0,
                    issues_found=0,
                    processing_time=0,
                    results=[],
                    error=str(e)
                ))
        
        return results
    
    def _process_single_file(self, file_path: str) -> BatchResult:
        """Process a single file"""
        start_time = datetime.now()
        
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Count lines
            lines = len(code.strip().split('\n'))
            
            # Analyze code
            results = self.reviewer.review_code(code)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return BatchResult(
                file_path=file_path,
                total_lines=lines,
                issues_found=len(results),
                processing_time=processing_time,
                results=results,
                error=None
            )
        
        except Exception as e:
            return BatchResult(
                file_path=file_path,
                total_lines=0,
                issues_found=0,
                processing_time=0,
                results=[],
                error=str(e)
            )
    
    def generate_batch_report(self, results: List[BatchResult]) -> Dict[str, Any]:
        """Generate summary report for batch processing"""
        total_files = len(results)
        successful_files = len([r for r in results if r.error is None])
        failed_files = total_files - successful_files
        
        total_lines = sum(r.total_lines for r in results)
        total_issues = sum(r.issues_found for r in results)
        total_time = sum(r.processing_time for r in results)
        
        # Issue type analysis
        issue_types = {}
        for result in results:
            for issue in result.results:
                issue_types[issue.reason] = issue_types.get(issue.reason, 0) + 1
        
        # Files with most issues
        problematic_files = sorted(
            [(r.file_path, r.issues_found) for r in results if r.issues_found > 0],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            'summary': {
                'total_files': total_files,
                'successful_files': successful_files,
                'failed_files': failed_files,
                'total_lines': total_lines,
                'total_issues': total_issues,
                'total_time': total_time,
                'avg_time_per_file': total_time / total_files if total_files > 0 else 0,
                'avg_issues_per_file': total_issues / successful_files if successful_files > 0 else 0
            },
            'issue_types': issue_types,
            'problematic_files': problematic_files,
            'errors': [(r.file_path, r.error) for r in results if r.error]
        }


class RealTimeAnalyzer:
    """Handles real-time code analysis as user types"""
    
    def __init__(self, csv_path: str = "용어사전.csv"):
        self.reviewer = CodeReviewer(csv_path)
        self.analysis_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.running = False
        self.worker_thread = None
        self._last_analysis_time = datetime.now()
        self._min_interval = 0.5  # Minimum 0.5 seconds between analyses
    
    def start(self):
        """Start the real-time analyzer"""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._worker)
            self.worker_thread.daemon = True
            self.worker_thread.start()
    
    def stop(self):
        """Stop the real-time analyzer"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1)
    
    def analyze(self, code: str, request_id: str):
        """Queue code for analysis"""
        # Throttle requests
        now = datetime.now()
        if (now - self._last_analysis_time).total_seconds() < self._min_interval:
            return
        
        self._last_analysis_time = now
        self.analysis_queue.put((code, request_id))
    
    def get_results(self, timeout: float = 0.1) -> Optional[Dict[str, Any]]:
        """Get analysis results if available"""
        try:
            return self.result_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def _worker(self):
        """Worker thread for processing analysis requests"""
        while self.running:
            try:
                # Get analysis request
                code, request_id = self.analysis_queue.get(timeout=0.1)
                
                # Perform analysis
                start_time = datetime.now()
                results = self.reviewer.review_code(code)
                analysis_time = (datetime.now() - start_time).total_seconds()
                
                # Extract variable names being typed
                lines = code.strip().split('\n')
                current_line = lines[-1] if lines else ""
                
                # Quick variable detection in current line
                import re
                var_pattern = r'\b([a-zA-Z_]\w*)\b'
                current_vars = re.findall(var_pattern, current_line)
                
                # Prepare results
                result = {
                    'request_id': request_id,
                    'timestamp': datetime.now().isoformat(),
                    'total_issues': len(results),
                    'analysis_time': analysis_time,
                    'current_line_vars': current_vars,
                    'issues': [
                        {
                            'original': r.original_name,
                            'suggested': r.suggested_name,
                            'reason': r.reason,
                            'confidence': r.confidence
                        }
                        for r in results
                    ],
                    'suggestions': self._get_quick_suggestions(current_line, results)
                }
                
                # Put result in queue
                self.result_queue.put(result)
                
            except queue.Empty:
                continue
            except Exception as e:
                # Log error but continue running
                print(f"Real-time analysis error: {e}")
    
    def _get_quick_suggestions(self, current_line: str, results) -> List[Dict[str, str]]:
        """Get quick suggestions for the current line"""
        suggestions = []
        
        for result in results:
            if result.original_name in current_line:
                suggestions.append({
                    'original': result.original_name,
                    'suggested': result.suggested_name,
                    'reason': result.reason
                })
        
        return suggestions[:3]  # Return top 3 suggestions


class FileWatcher:
    """Watches files for changes and triggers analysis"""
    
    def __init__(self, callback, csv_path: str = "용어사전.csv"):
        self.callback = callback
        self.reviewer = CodeReviewer(csv_path)
        self.watched_files = {}
        self.running = False
        self.watch_thread = None
    
    def add_file(self, file_path: str):
        """Add a file to watch list"""
        if os.path.exists(file_path):
            self.watched_files[file_path] = os.path.getmtime(file_path)
    
    def remove_file(self, file_path: str):
        """Remove a file from watch list"""
        self.watched_files.pop(file_path, None)
    
    def start(self):
        """Start watching files"""
        if not self.running:
            self.running = True
            self.watch_thread = threading.Thread(target=self._watch_loop)
            self.watch_thread.daemon = True
            self.watch_thread.start()
    
    def stop(self):
        """Stop watching files"""
        self.running = False
        if self.watch_thread:
            self.watch_thread.join(timeout=1)
    
    def _watch_loop(self):
        """Main watch loop"""
        while self.running:
            for file_path in list(self.watched_files.keys()):
                try:
                    if os.path.exists(file_path):
                        current_mtime = os.path.getmtime(file_path)
                        if current_mtime > self.watched_files[file_path]:
                            # File has been modified
                            self.watched_files[file_path] = current_mtime
                            self._analyze_file(file_path)
                except Exception as e:
                    print(f"Error watching file {file_path}: {e}")
            
            # Sleep for a bit
            import time
            time.sleep(1)
    
    def _analyze_file(self, file_path: str):
        """Analyze a modified file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            results = self.reviewer.review_code(code)
            
            # Call the callback with results
            self.callback(file_path, results)
            
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")


# Example usage
if __name__ == "__main__":
    # Test batch processor
    print("=== Batch Processor Test ===")
    processor = BatchProcessor()
    
    # Process current directory Python files
    results = processor.process_directory(".", "*.py", recursive=False)
    
    # Generate report
    report = processor.generate_batch_report(results)
    
    print(f"\nBatch Processing Report:")
    print(f"Total files: {report['summary']['total_files']}")
    print(f"Total issues: {report['summary']['total_issues']}")
    print(f"Average issues per file: {report['summary']['avg_issues_per_file']:.2f}")
    
    print("\nTop issue types:")
    for issue_type, count in sorted(report['issue_types'].items(), 
                                  key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {issue_type}: {count}")
    
    # Test real-time analyzer
    print("\n\n=== Real-Time Analyzer Test ===")
    analyzer = RealTimeAnalyzer()
    analyzer.start()
    
    # Simulate typing
    test_code = """
def process_usr_data(usr_id):
    res = get_user(usr_id)
    err_msg = ""
    return res
"""
    
    analyzer.analyze(test_code, "test_1")
    
    # Wait for results
    import time
    time.sleep(0.5)
    
    result = analyzer.get_results()
    if result:
        print(f"Real-time analysis found {result['total_issues']} issues")
        print(f"Analysis time: {result['analysis_time']:.3f}s")
        for issue in result['issues']:
            print(f"  - {issue['original']} → {issue['suggested']}")
    
    analyzer.stop()