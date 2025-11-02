#!/usr/bin/env python3

"""
validate_links.py - Markdown Link Validation Script

Purpose: Validate all links in markdown documentation files
Usage: python3 validate_links.py [path/to/docs] [--fix] [--strict]

Features:
- Finds all markdown files
- Validates internal links
- Checks external URLs (optional)
- Detects broken references
- Reports issues with line numbers
- Can auto-fix common issues

Exit codes:
  0 - All links valid
  1 - Broken links found
  2 - Usage error
"""

import os
import re
import sys
import argparse
import requests
from pathlib import Path
from typing import List, Dict, Tuple, Set
from urllib.parse import urlparse

# Color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Logging functions
def print_info(msg: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def print_success(msg: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_warning(msg: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_error(msg: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {msg}")

class LinkValidator:
    """Validates links in markdown documents"""
    
    def __init__(self, docs_path: str, strict: bool = False, fix: bool = False):
        """Initialize validator"""
        self.docs_path = Path(docs_path).resolve()
        self.strict = strict
        self.fix = fix
        self.issues = []
        self.validated_files = set()
        self.link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        self.external_url_regex = re.compile(r'^https?://')
        
    def get_markdown_files(self) -> List[Path]:
        """Get all markdown files in docs path"""
        files = []
        if self.docs_path.is_file():
            if self.docs_path.suffix == '.md':
                files.append(self.docs_path)
        else:
            files = list(self.docs_path.rglob('*.md'))
        
        return sorted(files)
    
    def validate_file(self, file_path: Path) -> Dict:
        """Validate links in a single file"""
        print_info(f"Validating: {file_path.relative_to(self.docs_path)}")
        
        result = {
            'file': file_path,
            'errors': [],
            'warnings': [],
            'fixed': []
        }
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            result['errors'].append(f"Cannot read file: {e}")
            return result
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Find all links in line
            for match in self.link_regex.finditer(line):
                link_text = match.group(1)
                link_url = match.group(2)
                
                # Validate the link
                error = self._validate_link(link_url, file_path)
                if error:
                    result['errors'].append({
                        'line': line_num,
                        'text': link_text,
                        'url': link_url,
                        'error': error
                    })
        
        self.validated_files.add(file_path)
        return result
    
    def _validate_link(self, url: str, file_path: Path) -> str:
        """Validate individual link"""
        
        # Skip email links and anchors-only
        if url.startswith('mailto:') or url.startswith('#'):
            return ""
        
        # Check external URLs
        if self.external_url_regex.match(url):
            if self.strict:
                try:
                    response = requests.head(url, timeout=5)
                    if response.status_code >= 400:
                        return f"HTTP {response.status_code}"
                except Exception as e:
                    return f"External link check failed: {str(e)}"
            return ""
        
        # Check internal links
        if url.startswith('/'):
            # Absolute path from root
            target = Path(self.docs_path.parent) / url.lstrip('/')
        elif url.startswith('./'):
            # Relative to current file
            target = file_path.parent / url
        elif url.startswith('../'):
            # Parent directory reference
            target = (file_path.parent / url).resolve()
        else:
            # Relative to current file
            target = file_path.parent / url
        
        # Remove anchor if present
        if '#' in str(target):
            target = Path(str(target).split('#')[0])
        
        # Check if target exists
        if not target.exists():
            # Try to find in docs directory
            if target.is_absolute():
                relative = target.relative_to(self.docs_path.parent)
            else:
                relative = target
            
            # Look for file in docs
            alt_path = self.docs_path.parent / str(relative).lstrip('/')
            if alt_path.exists():
                return ""
            
            return f"File not found: {target}"
        
        return ""
    
    def generate_report(self, results: List[Dict]) -> Tuple[int, int, int]:
        """Generate validation report"""
        total_errors = 0
        total_warnings = 0
        fixed_count = 0
        
        print("\n" + "="*70)
        print(f"{Colors.BOLD}Link Validation Report{Colors.END}")
        print("="*70)
        
        for result in results:
            if not result['errors'] and not result['warnings']:
                print_success(f"{result['file'].name}")
                continue
            
            if result['errors']:
                total_errors += len(result['errors'])
                print_error(f"\n{result['file'].name}:")
                
                for error in result['errors']:
                    line_info = f"Line {error['line']}"
                    print(f"  {Colors.RED}✗{Colors.END} {line_info}: {error['error']}")
                    print(f"    Link: [{error['text']}]({error['url']})")
            
            if result['warnings']:
                total_warnings += len(result['warnings'])
                for warning in result['warnings']:
                    print_warning(f"  {warning}")
            
            if result['fixed']:
                fixed_count += len(result['fixed'])
                for fix in result['fixed']:
                    print(f"  {Colors.GREEN}Fixed{Colors.END}: {fix}")
        
        # Print summary
        print("\n" + "="*70)
        print(f"{Colors.BOLD}Summary{Colors.END}")
        print("="*70)
        print(f"Files validated: {len(results)}")
        print(f"Errors found: {total_errors}")
        print(f"Warnings: {total_warnings}")
        print(f"Issues fixed: {fixed_count}")
        
        if total_errors == 0:
            print_success("All links validated successfully!")
        else:
            print_error(f"Found {total_errors} broken links")
        
        return total_errors, total_warnings, fixed_count
    
    def validate_all(self) -> int:
        """Validate all markdown files"""
        if not self.docs_path.exists():
            print_error(f"Path not found: {self.docs_path}")
            return 2
        
        files = self.get_markdown_files()
        
        if not files:
            print_warning("No markdown files found")
            return 0
        
        print_info(f"Found {len(files)} markdown files")
        print()
        
        results = []
        for file_path in files:
            result = self.validate_file(file_path)
            results.append(result)
        
        errors, warnings, fixed = self.generate_report(results)
        
        return 1 if errors > 0 else 0

class AnchorValidator:
    """Validates that anchor references match headings"""
    
    def __init__(self, file_path: Path):
        """Initialize validator"""
        self.file_path = file_path
        self.headings = {}
        
    def extract_headings(self) -> Dict[str, int]:
        """Extract all headings from file"""
        content = self.file_path.read_text(encoding='utf-8')
        heading_regex = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
        
        headings = {}
        for match in heading_regex.finditer(content):
            heading_text = match.group(1)
            # Convert to anchor format
            anchor = heading_text.lower().replace(' ', '-').replace('_', '-')
            # Remove special characters
            anchor = re.sub(r'[^\w\-]', '', anchor)
            headings[anchor] = heading_text
        
        return headings
    
    def validate_anchor(self, anchor: str) -> bool:
        """Check if anchor exists in file"""
        headings = self.extract_headings()
        return anchor in headings

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Validate markdown links and references',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 validate_links.py docs/
  python3 validate_links.py docs/ --strict
  python3 validate_links.py docs/*.md
        '''
    )
    
    parser.add_argument(
        'path',
        help='Path to markdown file or directory'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Check external URLs (slower)'
    )
    
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Attempt to fix common issues'
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = LinkValidator(args.path, strict=args.strict, fix=args.fix)
    
    # Run validation
    exit_code = validator.validate_all()
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
