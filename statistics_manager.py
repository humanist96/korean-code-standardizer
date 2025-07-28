"""
Statistics Manager for Code Transformation System
Handles persistent storage and analysis of transformation statistics
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np


@dataclass
class TransformationRecord:
    """Record of a single transformation session"""
    timestamp: str
    file_name: str
    file_path: str
    original_code: str
    transformed_code: str
    issues_found: int
    confidence_score: float
    transformation_details: List[Dict[str, Any]]
    
    # Computed properties
    @property
    def code_length(self) -> int:
        return len(self.original_code)
    
    @property
    def lines_of_code(self) -> int:
        return len(self.original_code.splitlines())
    
    @property
    def total_changes(self) -> int:
        return self.issues_found
    
    @property
    def changes_by_type(self) -> Dict[str, int]:
        """Count changes by type from transformation details"""
        type_counts = {}
        for detail in self.transformation_details:
            reason = detail.get('reason', 'Unknown')
            type_counts[reason] = type_counts.get(reason, 0) + 1
        return type_counts
    
    @property
    def variables_transformed(self) -> List[Dict[str, str]]:
        """Get list of variable transformations"""
        return self.transformation_details
    
    @property
    def confidence_scores(self) -> List[float]:
        """Get list of confidence scores"""
        return [self.confidence_score]
    
    @property
    def naming_convention(self) -> str:
        """Detect primary naming convention"""
        return "snake_case"  # Default
    
    @property
    def duration_seconds(self) -> Optional[float]:
        return None
    
    @property
    def applied_changes(self) -> Optional[int]:
        return self.issues_found


class StatisticsManager:
    """Manages statistics collection and persistence"""
    
    def __init__(self, stats_file: str = "transformation_statistics.json"):
        self.stats_file = stats_file
        self.current_session = {
            'start_time': datetime.now().isoformat(),
            'transformations': []
        }
        self._load_statistics()
    
    def _load_statistics(self):
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
            except Exception as e:
                print(f"Error loading statistics: {e}")
                self.stats = self._create_empty_stats()
        else:
            self.stats = self._create_empty_stats()
    
    def _create_empty_stats(self) -> Dict:
        """Create empty statistics structure"""
        return {
            'total_transformations': 0,
            'total_changes': 0,
            'total_lines_processed': 0,
            'total_files': 0,
            'total_lines': 0,
            'daily_stats': {},
            'weekly_stats': {},
            'monthly_stats': {},
            'issue_type_distribution': {},
            'common_transformations': {},
            'average_confidence': 0.0,
            'sessions': []
        }
    
    def save_statistics(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving statistics: {e}")
    
    def record_transformation(self, record: TransformationRecord):
        """Record a transformation session"""
        # Convert to dict
        record_dict = asdict(record)
        
        # Update current session
        self.current_session['transformations'].append(record_dict)
        
        # Also store in sessions for persistence
        if 'sessions' not in self.stats:
            self.stats['sessions'] = []
        
        # Add to the latest session or create new one
        if not self.stats['sessions'] or len(self.stats['sessions'][-1].get('transformations', [])) > 100:
            # Create new session if none exists or current session is too large
            self.stats['sessions'].append({
                'start_time': datetime.now().isoformat(),
                'transformations': []
            })
        
        # Add transformation to the latest session
        self.stats['sessions'][-1]['transformations'].append(record_dict)
        
        # Keep only last 5 sessions to avoid bloat
        if len(self.stats['sessions']) > 5:
            self.stats['sessions'] = self.stats['sessions'][-5:]
        
        # Update global statistics
        self.stats['total_transformations'] += 1
        self.stats['total_changes'] += record.total_changes
        self.stats['total_lines_processed'] += record.lines_of_code
        
        # Also update the alternate field names for compatibility
        self.stats['total_files'] = self.stats.get('total_files', 0) + 1
        self.stats['total_lines'] = self.stats.get('total_lines', 0) + record.lines_of_code
        
        # Update issue type distribution
        for issue_type, count in record.changes_by_type.items():
            if issue_type not in self.stats['issue_type_distribution']:
                self.stats['issue_type_distribution'][issue_type] = 0
            self.stats['issue_type_distribution'][issue_type] += count
        
        # Update common transformations
        for transform in record.variables_transformed:
            # Handle both 'suggested' and 'suggestion' keys for compatibility
            suggested = transform.get('suggested', transform.get('suggestion', ''))
            key = f"{transform['original']} → {suggested}"
            if key not in self.stats['common_transformations']:
                self.stats['common_transformations'][key] = 0
            self.stats['common_transformations'][key] += 1
        
        # Update average confidence
        if record.confidence_scores:
            total_confidence = self.stats['average_confidence'] * (self.stats['total_transformations'] - 1)
            new_avg = (total_confidence + np.mean(record.confidence_scores)) / self.stats['total_transformations']
            self.stats['average_confidence'] = new_avg
        
        # Update daily/weekly/monthly stats
        self._update_time_based_stats(record)
        
        # Save immediately
        self.save_statistics()
    
    def _update_time_based_stats(self, record: TransformationRecord):
        """Update time-based statistics"""
        date = datetime.fromisoformat(record.timestamp)
        
        # Daily stats
        day_key = date.strftime('%Y-%m-%d')
        if day_key not in self.stats['daily_stats']:
            self.stats['daily_stats'][day_key] = {
                'transformations': 0,
                'changes': 0,
                'lines': 0
            }
        self.stats['daily_stats'][day_key]['transformations'] += 1
        self.stats['daily_stats'][day_key]['changes'] += record.total_changes
        self.stats['daily_stats'][day_key]['lines'] += record.lines_of_code
        
        # Weekly stats
        week_key = f"{date.year}-W{date.isocalendar()[1]:02d}"
        if week_key not in self.stats['weekly_stats']:
            self.stats['weekly_stats'][week_key] = {
                'transformations': 0,
                'changes': 0,
                'lines': 0
            }
        self.stats['weekly_stats'][week_key]['transformations'] += 1
        self.stats['weekly_stats'][week_key]['changes'] += record.total_changes
        self.stats['weekly_stats'][week_key]['lines'] += record.lines_of_code
        
        # Monthly stats
        month_key = date.strftime('%Y-%m')
        if month_key not in self.stats['monthly_stats']:
            self.stats['monthly_stats'][month_key] = {
                'transformations': 0,
                'changes': 0,
                'lines': 0
            }
        self.stats['monthly_stats'][month_key]['transformations'] += 1
        self.stats['monthly_stats'][month_key]['changes'] += record.total_changes
        self.stats['monthly_stats'][month_key]['lines'] += record.lines_of_code
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics"""
        return {
            'total_transformations': self.stats['total_transformations'],
            'total_changes': self.stats['total_changes'],
            'total_lines_processed': self.stats['total_lines_processed'],
            'average_changes_per_transformation': (
                self.stats['total_changes'] / self.stats['total_transformations']
                if self.stats['total_transformations'] > 0 else 0
            ),
            'average_confidence': self.stats['average_confidence'],
            'most_common_issue': (
                max(self.stats['issue_type_distribution'].items(), key=lambda x: x[1])[0]
                if self.stats['issue_type_distribution'] else None
            ),
            'most_common_transformation': (
                max(self.stats['common_transformations'].items(), key=lambda x: x[1])[0]
                if self.stats['common_transformations'] else None
            )
        }
    
    def get_time_series_data(self, period: str = 'daily', days: int = 30) -> pd.DataFrame:
        """Get time series data for visualization"""
        if period == 'daily':
            data = self.stats['daily_stats']
        elif period == 'weekly':
            data = self.stats['weekly_stats']
        elif period == 'monthly':
            data = self.stats['monthly_stats']
        else:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        # Filter by days if specified
        if period == 'daily' and days > 0:
            cutoff_date = datetime.now() - timedelta(days=days)
            df = df[df.index >= cutoff_date]
        
        return df
    
    def get_issue_distribution(self) -> Dict[str, int]:
        """Get issue type distribution"""
        return self.stats['issue_type_distribution']
    
    def get_top_transformations(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get most common transformations"""
        sorted_transforms = sorted(
            self.stats['common_transformations'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_transforms[:limit]
    
    def get_productivity_metrics(self) -> Dict:
        """Calculate productivity metrics"""
        daily_data = self.get_time_series_data('daily', 30)
        
        if daily_data.empty:
            return {
                'avg_daily_transformations': 0,
                'avg_daily_changes': 0,
                'avg_daily_lines': 0,
                'peak_day': None,
                'peak_changes': 0
            }
        
        # Calculate metrics
        avg_daily_transformations = daily_data['transformations'].mean()
        avg_daily_changes = daily_data['changes'].mean()
        avg_daily_lines = daily_data['lines'].mean()
        
        # Find peak day
        peak_idx = daily_data['changes'].idxmax()
        peak_day = peak_idx.strftime('%Y-%m-%d') if peak_idx else None
        peak_changes = daily_data['changes'].max()
        
        return {
            'avg_daily_transformations': avg_daily_transformations,
            'avg_daily_changes': avg_daily_changes,
            'avg_daily_lines': avg_daily_lines,
            'peak_day': peak_day,
            'peak_changes': peak_changes
        }
    
    def export_statistics(self, format: str = 'json') -> str:
        """Export statistics in various formats"""
        if format == 'json':
            return json.dumps(self.stats, ensure_ascii=False, indent=2)
        
        elif format == 'csv':
            # Create summary DataFrame
            summary_data = []
            
            # Daily stats
            for date, stats in self.stats['daily_stats'].items():
                summary_data.append({
                    'date': date,
                    'period': 'daily',
                    'transformations': stats['transformations'],
                    'changes': stats['changes'],
                    'lines': stats['lines']
                })
            
            df = pd.DataFrame(summary_data)
            return df.to_csv(index=False)
        
        elif format == 'excel':
            # Create multiple sheets
            with pd.ExcelWriter('transformation_statistics.xlsx', engine='openpyxl') as writer:
                # Summary sheet
                summary_df = pd.DataFrame([self.get_summary_stats()])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Daily stats
                daily_df = self.get_time_series_data('daily', 0)
                daily_df.to_excel(writer, sheet_name='Daily Stats')
                
                # Issue distribution
                issue_df = pd.DataFrame(
                    list(self.stats['issue_type_distribution'].items()),
                    columns=['Issue Type', 'Count']
                )
                issue_df.to_excel(writer, sheet_name='Issue Distribution', index=False)
                
                # Common transformations
                transform_df = pd.DataFrame(
                    self.get_top_transformations(50),
                    columns=['Transformation', 'Count']
                )
                transform_df.to_excel(writer, sheet_name='Common Transformations', index=False)
            
            return "Statistics exported to transformation_statistics.xlsx"
        
        return ""
    
    def reset_statistics(self):
        """Reset all statistics"""
        self.stats = self._create_empty_stats()
        self.save_statistics()
    
    def get_session_summary(self) -> Dict:
        """Get current session summary"""
        return {
            'start_time': self.current_session['start_time'],
            'transformations_count': len(self.current_session['transformations']),
            'total_changes': sum(t['total_changes'] for t in self.current_session['transformations']),
            'total_lines': sum(t['lines_of_code'] for t in self.current_session['transformations'])
        }
    
    def get_today_statistics(self) -> Dict:
        """Get statistics for today"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today in self.stats['daily_stats']:
            daily_data = self.stats['daily_stats'][today]
            return {
                'total_files': daily_data['transformations'],
                'total_changes': daily_data['changes'],
                'total_lines': daily_data['lines']
            }
        
        return {
            'total_files': 0,
            'total_changes': 0,
            'total_lines': 0
        }
    
    def get_all_time_statistics(self) -> Dict:
        """Get all-time statistics"""
        return {
            'total_transformations': self.stats.get('total_transformations', 0),
            'total_issues_found': self.stats.get('total_changes', 0),  # Use total_changes instead
            'total_files_processed': self.stats.get('total_files', 0),
            'average_confidence': self.stats.get('average_confidence', 0),
            'total_lines_processed': self.stats.get('total_lines', 0)
        }
    
    def get_recent_records(self, limit: int = 10) -> List[Dict]:
        """Get recent transformation records"""
        records = []
        
        # First, add all transformations from sessions if stored
        if 'sessions' in self.stats:
            for session in self.stats['sessions']:
                if 'transformations' in session:
                    for trans in session['transformations']:
                        record = {
                            'file_name': trans.get('file_name', 'Unknown'),
                            'timestamp': trans.get('timestamp', ''),
                            'issues_found': trans.get('issues_found', trans.get('total_changes', 0)),
                            'confidence_score': trans.get('confidence_score', 0)
                        }
                        records.append(record)
        
        # Add current session transformations
        for trans in self.current_session['transformations']:
            record = {
                'file_name': trans.get('file_name', 'Unknown'),
                'timestamp': trans.get('timestamp', ''),
                'issues_found': trans.get('issues_found', trans.get('total_changes', 0)),
                'confidence_score': trans.get('confidence_score', 0)
            }
            records.append(record)
        
        # If no individual records, create from daily stats as fallback
        if not records:
            for date_str, daily_data in sorted(self.stats['daily_stats'].items(), reverse=True)[:limit]:
                record = {
                    'file_name': f"{daily_data['transformations']} files",
                    'timestamp': date_str,
                    'issues_found': daily_data['changes'],
                    'confidence_score': self.stats['average_confidence']
                }
                records.append(record)
        
        # Sort by timestamp and return most recent
        records.sort(key=lambda x: x['timestamp'], reverse=True)
        return records[:limit]