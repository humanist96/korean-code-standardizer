"""
Batch Code Transformer
Transform multiple files at once using the terminology dictionary
"""

import os
import glob
from typing import List, Dict, Tuple
from datetime import datetime
import json

from variable_name_standardizer import CodeReviewer


class BatchTransformer:
    """Handle batch transformation of multiple code files"""
    
    def __init__(self, csv_path: str = "용어사전.csv"):
        self.reviewer = CodeReviewer(csv_path)
        self.results = []
    
    def transform_directory(self, directory: str, pattern: str = "*.py", 
                          recursive: bool = True, output_dir: str = None) -> Dict:
        """Transform all Python files in a directory"""
        # Find all files
        if recursive:
            files = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
        else:
            files = glob.glob(os.path.join(directory, pattern))
        
        # Set output directory
        if output_dir is None:
            output_dir = os.path.join(directory, "transformed")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Transform each file
        results = {
            'total_files': len(files),
            'transformed_files': 0,
            'total_changes': 0,
            'failed_files': [],
            'file_results': []
        }
        
        for file_path in files:
            try:
                file_result = self.transform_file(file_path, output_dir)
                results['file_results'].append(file_result)
                
                if file_result['changes'] > 0:
                    results['transformed_files'] += 1
                    results['total_changes'] += file_result['changes']
                    
            except Exception as e:
                results['failed_files'].append({
                    'file': file_path,
                    'error': str(e)
                })
        
        return results
    
    def transform_file(self, file_path: str, output_dir: str = None) -> Dict:
        """Transform a single file"""
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        
        # Analyze code
        analysis_results = self.reviewer.review_code(original_code)
        
        # Transform code
        transformed_code = self.apply_transformations(original_code, analysis_results)
        
        # Determine output path
        if output_dir:
            filename = os.path.basename(file_path)
            output_path = os.path.join(output_dir, filename)
        else:
            base, ext = os.path.splitext(file_path)
            output_path = f"{base}_transformed{ext}"
        
        # Write transformed file
        if analysis_results:  # Only write if there were changes
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transformed_code)
        
        # Return result
        return {
            'original_file': file_path,
            'output_file': output_path if analysis_results else None,
            'changes': len(analysis_results),
            'lines': len(original_code.strip().split('\n')),
            'transformations': [
                {
                    'original': r.original_name,
                    'suggested': r.suggested_name,
                    'reason': r.reason
                }
                for r in analysis_results
            ]
        }
    
    def apply_transformations(self, code: str, results: List) -> str:
        """Apply all transformations to code"""
        if not results:
            return code
        
        transformed = code
        
        # Sort by position in reverse order to avoid position shifts
        sorted_results = sorted(results, key=lambda r: code.rfind(r.original_name), reverse=True)
        
        for result in sorted_results:
            # Use word boundary regex for more accurate replacement
            import re
            pattern = r'\b' + re.escape(result.original_name) + r'\b'
            transformed = re.sub(pattern, result.suggested_name, transformed)
        
        return transformed
    
    def generate_report(self, results: Dict, output_file: str = None) -> str:
        """Generate a transformation report"""
        report = []
        report.append("=" * 60)
        report.append("변수명 표준화 변환 리포트")
        report.append("=" * 60)
        report.append(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("## 요약")
        report.append(f"- 총 파일 수: {results['total_files']}")
        report.append(f"- 변환된 파일 수: {results['transformed_files']}")
        report.append(f"- 총 변경사항: {results['total_changes']}")
        report.append(f"- 실패한 파일: {len(results['failed_files'])}")
        report.append("")
        
        # File details
        if results['file_results']:
            report.append("## 파일별 상세 내역")
            report.append("")
            
            for file_result in results['file_results']:
                if file_result['changes'] > 0:
                    report.append(f"### {file_result['original_file']}")
                    report.append(f"- 변경사항: {file_result['changes']}개")
                    report.append(f"- 코드 라인: {file_result['lines']}줄")
                    report.append(f"- 출력 파일: {file_result['output_file']}")
                    report.append("")
                    
                    report.append("변환 내역:")
                    for trans in file_result['transformations']:
                        report.append(f"  - {trans['original']} → {trans['suggested']} ({trans['reason']})")
                    report.append("")
        
        # Failed files
        if results['failed_files']:
            report.append("## 실패한 파일")
            report.append("")
            
            for failed in results['failed_files']:
                report.append(f"- {failed['file']}: {failed['error']}")
            report.append("")
        
        report_text = '\n'.join(report)
        
        # Save report if output file specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
        
        return report_text


def main():
    """Example usage"""
    transformer = BatchTransformer()
    
    # Transform current directory
    results = transformer.transform_directory(
        directory=".",
        pattern="*.py",
        recursive=False,
        output_dir="./transformed"
    )
    
    # Generate report
    report = transformer.generate_report(results, "transformation_report.txt")
    print(report)


if __name__ == "__main__":
    main()