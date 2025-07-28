"""
Terminology Manager with persistent storage
Handles adding, deleting, and managing terminology dictionary
"""

import json
import os
import csv
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import pandas as pd


@dataclass
class Term:
    """Represents a single term entry"""
    korean_name: str
    english_name: str
    abbreviation: str
    standard_variable: str
    description: str
    related_terms: List[str]
    added_date: str
    modified_date: str
    source: str  # 'csv' or 'manual'


class TerminologyManager:
    """Manages terminology with persistent storage"""
    
    def __init__(self, csv_path: str = "용어사전.csv", 
                 custom_terms_file: str = "custom_terms.json"):
        self.csv_path = csv_path
        self.custom_terms_file = custom_terms_file
        self.terms: Dict[str, Term] = {}
        self.csv_terms: Set[str] = set()  # Track which terms came from CSV
        
        # Load terms from CSV first
        self._load_csv_terms()
        
        # Then load custom terms (may override CSV terms)
        self._load_custom_terms()
    
    def _load_csv_terms(self):
        """Load terms from CSV file with multiple encoding support"""
        encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr']
        loaded_count = 0
        
        for encoding in encodings:
            try:
                # Try pandas for better CSV handling
                df = pd.read_csv(self.csv_path, encoding=encoding, header=None)
                
                for index, row in df.iterrows():
                    if len(row) >= 3:
                        korean_name = str(row[0]).strip() if pd.notna(row[0]) else ""
                        english_name = str(row[1]).strip() if pd.notna(row[1]) else ""
                        abbreviation = str(row[2]).strip() if pd.notna(row[2]) else ""
                        
                        # Skip empty rows or header rows
                        if not korean_name and not english_name:
                            continue
                        
                        # Skip if it looks like a header
                        if korean_name in ['한글명', 'Korean', 'KOR'] or english_name in ['영문명', 'English', 'ENG']:
                            continue
                        
                        # Create standard variable name
                        if abbreviation and len(abbreviation) >= 2 and abbreviation.replace('_', '').replace('-', '').isalnum():
                            standard_var = abbreviation.lower().replace('-', '_')
                        elif english_name and len(english_name) > 2:
                            # Convert english name to snake_case
                            import re
                            standard_var = english_name.lower()
                            standard_var = re.sub(r'[^\w\s]', '', standard_var)
                            standard_var = standard_var.replace(' ', '_')
                            standard_var = re.sub(r'_+', '_', standard_var).strip('_')
                        else:
                            continue
                        
                        if standard_var and len(standard_var) > 1:
                            # Create term
                            term = Term(
                                korean_name=korean_name,
                                english_name=english_name,
                                abbreviation=abbreviation,
                                standard_variable=standard_var,
                                description=f"{korean_name} ({english_name})" if korean_name else english_name,
                                related_terms=self._generate_related_terms(english_name, abbreviation, standard_var),
                                added_date=datetime.now().isoformat(),
                                modified_date=datetime.now().isoformat(),
                                source='csv'
                            )
                            
                            # Add to dictionary with multiple keys for lookup
                            self._add_term_to_index(term)
                            self.csv_terms.add(standard_var)
                            loaded_count += 1
                
                if loaded_count > 0:
                    print(f"[INFO] Loaded {loaded_count} terms from CSV using {encoding} encoding")
                    return loaded_count
                    
            except Exception as e:
                continue
        
        print(f"[WARNING] Could not load CSV file properly. Loaded {loaded_count} terms.")
        return loaded_count
    
    def _generate_related_terms(self, english_name: str, abbreviation: str, standard_var: str) -> List[str]:
        """Generate related terms for a given term"""
        related = []
        
        if abbreviation and abbreviation.lower() != standard_var:
            related.append(abbreviation.lower())
        
        if english_name:
            # Add variations of english name
            import re
            eng_lower = english_name.lower()
            variations = [
                eng_lower.replace(' ', '_'),
                eng_lower.replace(' ', ''),
                eng_lower.replace(' ', '-'),
                re.sub(r'[^\w]', '', eng_lower)
            ]
            
            for var in variations:
                if var != standard_var and len(var) > 2:
                    related.append(var)
        
        # Remove duplicates
        return list(set(related))
    
    def _add_term_to_index(self, term: Term):
        """Add term to index with multiple lookup keys"""
        # Standard variable name
        self.terms[term.standard_variable] = term
        
        # Korean name
        if term.korean_name:
            self.terms[term.korean_name.lower()] = term
        
        # English name
        if term.english_name:
            self.terms[term.english_name.lower()] = term
        
        # Abbreviation
        if term.abbreviation and term.abbreviation.lower() != term.standard_variable:
            self.terms[term.abbreviation.lower()] = term
        
        # Related terms
        for related in term.related_terms:
            if related not in self.terms:
                self.terms[related] = term
    
    def _load_custom_terms(self):
        """Load custom terms from JSON file"""
        if os.path.exists(self.custom_terms_file):
            try:
                with open(self.custom_terms_file, 'r', encoding='utf-8') as f:
                    custom_data = json.load(f)
                
                for term_data in custom_data.get('terms', []):
                    term = Term(**term_data)
                    self._add_term_to_index(term)
                
                print(f"[INFO] Loaded {len(custom_data.get('terms', []))} custom terms")
            except Exception as e:
                print(f"[ERROR] Failed to load custom terms: {e}")
    
    def save_custom_terms(self):
        """Save custom terms to JSON file"""
        custom_terms = []
        
        for key, term in self.terms.items():
            # Only save each term once (by standard variable)
            if key == term.standard_variable and term.source == 'manual':
                custom_terms.append(asdict(term))
        
        data = {
            'version': '1.0',
            'last_modified': datetime.now().isoformat(),
            'terms': custom_terms
        }
        
        try:
            with open(self.custom_terms_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save custom terms: {e}")
            return False
    
    def add_term(self, korean_name: str, english_name: str, abbreviation: str,
                 description: str = "", related_terms: List[str] = None) -> bool:
        """Add a new term"""
        # Validate inputs
        if not english_name or len(english_name) < 2:
            return False
        
        # Create standard variable name
        if abbreviation and len(abbreviation) >= 2:
            standard_var = abbreviation.lower().replace('-', '_')
        else:
            import re
            standard_var = english_name.lower()
            standard_var = re.sub(r'[^\w\s]', '', standard_var)
            standard_var = standard_var.replace(' ', '_')
            standard_var = re.sub(r'_+', '_', standard_var).strip('_')
        
        if not standard_var or len(standard_var) < 2:
            return False
        
        # Create term
        term = Term(
            korean_name=korean_name or "",
            english_name=english_name,
            abbreviation=abbreviation or "",
            standard_variable=standard_var,
            description=description or f"{korean_name} ({english_name})" if korean_name else english_name,
            related_terms=related_terms or self._generate_related_terms(english_name, abbreviation, standard_var),
            added_date=datetime.now().isoformat(),
            modified_date=datetime.now().isoformat(),
            source='manual'
        )
        
        # Add to index
        self._add_term_to_index(term)
        
        # Save immediately
        self.save_custom_terms()
        
        return True
    
    def delete_term(self, term_key: str) -> bool:
        """Delete a term (only custom terms can be deleted)"""
        term_key = term_key.lower()
        
        if term_key not in self.terms:
            return False
        
        term = self.terms[term_key]
        
        # Don't allow deleting CSV terms
        if term.source == 'csv':
            return False
        
        # Remove all references to this term
        keys_to_remove = []
        for key, t in self.terms.items():
            if t.standard_variable == term.standard_variable:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.terms[key]
        
        # Save immediately
        self.save_custom_terms()
        
        return True
    
    def update_term(self, term_key: str, korean_name: str = None, 
                    english_name: str = None, abbreviation: str = None,
                    description: str = None, related_terms: List[str] = None) -> bool:
        """Update an existing term (only custom terms can be updated)"""
        term_key = term_key.lower()
        
        if term_key not in self.terms:
            return False
        
        term = self.terms[term_key]
        
        # Don't allow updating CSV terms
        if term.source == 'csv':
            return False
        
        # Update fields
        if korean_name is not None:
            term.korean_name = korean_name
        if english_name is not None:
            term.english_name = english_name
        if abbreviation is not None:
            term.abbreviation = abbreviation
        if description is not None:
            term.description = description
        if related_terms is not None:
            term.related_terms = related_terms
        
        term.modified_date = datetime.now().isoformat()
        
        # Re-index the term
        # First remove old references
        keys_to_remove = []
        for key, t in self.terms.items():
            if t.standard_variable == term.standard_variable:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.terms[key]
        
        # Then add back with new keys
        self._add_term_to_index(term)
        
        # Save immediately
        self.save_custom_terms()
        
        return True
    
    def get_all_terms(self) -> List[Term]:
        """Get all unique terms"""
        unique_terms = {}
        for term in self.terms.values():
            if term.standard_variable not in unique_terms:
                unique_terms[term.standard_variable] = term
        
        return list(unique_terms.values())
    
    def get_term(self, key: str) -> Optional[Term]:
        """Get a specific term"""
        return self.terms.get(key.lower())
    
    def search_terms(self, query: str) -> List[Term]:
        """Search for terms matching a query"""
        query = query.lower()
        results = []
        seen = set()
        
        for term in self.terms.values():
            if term.standard_variable in seen:
                continue
            
            if (query in term.korean_name.lower() or
                query in term.english_name.lower() or
                query in term.abbreviation.lower() or
                query in term.standard_variable or
                any(query in related.lower() for related in term.related_terms)):
                results.append(term)
                seen.add(term.standard_variable)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get statistics about the terminology"""
        unique_terms = self.get_all_terms()
        
        return {
            'total_terms': len(unique_terms),
            'csv_terms': sum(1 for t in unique_terms if t.source == 'csv'),
            'custom_terms': sum(1 for t in unique_terms if t.source == 'manual'),
            'total_lookups': len(self.terms),
            'korean_terms': sum(1 for t in unique_terms if t.korean_name),
            'abbreviations': sum(1 for t in unique_terms if t.abbreviation)
        }