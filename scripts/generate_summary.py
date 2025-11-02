#!/usr/bin/env python3

"""
generate_summary.py - Documentation Summary Generator

Purpose: Generate comprehensive summary and statistics for documentation
Usage: python3 generate_summary.py [path/to/docs] [--output summary.json] [--format json|md|txt]

Features:
- Counts files, lines, sections
- Generates statistics
- Analyzes content
- Creates index
- Exports in multiple formats
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(msg: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def print_success(msg: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_error(msg: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {msg}")

class DocumentationAnalyzer:
    """Analyzes documentation structure and content"""
    
    def __init__(self, docs_path: str):
        """Initialize analyzer"""
        self.docs_path = Path(docs_path).resolve()
        self.stats = {
            'total_files': 0,
            'total_lines': 0,
            'total_words': 0,
            'total_size': 0,
            'files': [],
            'categories': {},
            'sections': [],
            'generated_at': datetime.now().isoformat()
        }
        
    def analyze(self) -> Dict[str, Any]:
        """Analyze documentation"""
        if not self.docs_path.exists():
            print_error(f"Path not found: {self.docs_path}")
            return self.stats
        
        print_info(f"Analyzing: {self.docs_path}")
        
        # Get all markdown files
        md_files = sorted(self.docs_path.rglob('*.md'))
        
        if not md_files:
            print_error("No markdown files found")
            return self.stats
        
        print_info(f"Found {len(md_files)} markdown files")
        
        # Analyze each file
        for file_path in md_files:
            self._analyze_file(file_path)
        
        # Calculate totals
        self._calculate_totals()
        
        print_success("Analysis complete")
        return self.stats
    
    def _analyze_file(self, file_path: Path) -> None:
        """Analyze individual file"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print_error(f"Cannot read {file_path}: {e}")
            return
        
        # Calculate metrics
        lines = content.split('\n')
        words = content.split()
        size = len(content.encode('utf-8'))
        
        # Extract sections
        sections = self._extract_sections(content, file_path)
        
        # Categorize file
        category = self._categorize_file(file_path)
        
        file_info = {
            'name': file_path.name,
            'path': str(file_path.relative_to(self.docs_path.parent)),
            'category': category,
            'lines': len(lines),
            'words': len(words),
            'size': size,
            'sections': len(sections),
            'headings': sections
        }
        
        self.stats['files'].append(file_info)
        
        # Add to category stats
        if category not in self.stats['categories']:
            self.stats['categories'][category] = {
                'count': 0,
                'lines': 0,
                'words': 0,
                'size': 0
            }
        
        self.stats['categories'][category]['count'] += 1
        self.stats['categories'][category]['lines'] += len(lines)
        self.stats['categories'][category]['words'] += len(words)
        self.stats['categories'][category]['size'] += size
        
        # Add sections
        self.stats['sections'].extend(sections)
    
    def _extract_sections(self, content: str, file_path: Path) -> List[Dict]:
        """Extract section headings from content"""
        sections = []
        heading_regex = re.compile(r'^(#+)\s+(.+)$', re.MULTILINE)
        
        for match in heading_regex.finditer(content):
            level = len(match.group(1))
            text = match.group(2)
            
            sections.append({
                'file': file_path.name,
                'level': level,
                'text': text,
                'anchor': self._text_to_anchor(text)
            })
        
        return sections
    
    def _text_to_anchor(self, text: str) -> str:
        """Convert heading text to anchor"""
        anchor = text.lower()
        anchor = re.sub(r'\s+', '-', anchor)
        anchor = re.sub(r'[^\w\-]', '', anchor)
        return anchor
    
    def _categorize_file(self, file_path: Path) -> str:
        """Categorize file by directory"""
        parts = file_path.parts
        
        if 'guides' in parts:
            return 'Guides'
        elif 'resources' in parts:
            return 'Resources'
        elif 'architecture' in parts:
            return 'Architecture'
        elif 'api' in parts:
            return 'API'
        elif 'operations' in parts:
            return 'Operations'
        elif 'docs' in parts:
            return 'Documentation'
        else:
            return 'Other'
    
    def _calculate_totals(self) -> None:
        """Calculate total statistics"""
        total_lines = 0
        total_words = 0
        total_size = 0
        
        for file_info in self.stats['files']:
            total_lines += file_info['lines']
            total_words += file_info['words']
            total_size += file_info['size']
        
        self.stats['total_files'] = len(self.stats['files'])
        self.stats['total_lines'] = total_lines
        self.stats['total_words'] = total_words
        self.stats['total_size'] = total_size
    
    def get_size_display(self, size: int) -> str:
        """Format size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def get_summary_text(self) -> str:
        """Generate text summary"""
        summary = []
        summary.append("="*70)
        summary.append(f"{'Documentation Summary':^70}")
        summary.append("="*70)
        summary.append("")
        
        # Overall statistics
        summary.append("OVERALL STATISTICS")
        summary.append(f"  Total Files:    {self.stats['total_files']}")
        summary.append(f"  Total Lines:    {self.stats['total_lines']:,}")
        summary.append(f"  Total Words:    {self.stats['total_words']:,}")
        summary.append(f"  Total Size:     {self.get_size_display(self.stats['total_size'])}")
        summary.append("")
        
        # By category
        summary.append("BY CATEGORY")
        for category, stats in sorted(self.stats['categories'].items()):
            summary.append(f"\n  {category}:")
            summary.append(f"    Files:  {stats['count']}")
            summary.append(f"    Lines:  {stats['lines']:,}")
            summary.append(f"    Words:  {stats['words']:,}")
            summary.append(f"    Size:   {self.get_size_display(stats['size'])}")
        
        summary.append("")
        summary.append("FILES")
        for file_info in sorted(self.stats['files'], key=lambda x: x['name']):
            summary.append(f"\n  {file_info['name']}")
            summary.append(f"    Path:     {file_info['path']}")
            summary.append(f"    Category: {file_info['category']}")
            summary.append(f"    Lines:    {file_info['lines']}")
            summary.append(f"    Words:    {file_info['words']}")
            summary.append(f"    Sections: {file_info['sections']}")
        
        summary.append("")
        summary.append("="*70)
        summary.append(f"Generated: {self.stats['generated_at']}")
        summary.append("="*70)
        
        return "\n".join(summary)
    
    def get_summary_markdown(self) -> str:
        """Generate markdown summary"""
        md = []
        md.append("# Documentation Summary\n")
        md.append(f"*Generated: {self.stats['generated_at']}*\n")
        
        # Overview
        md.append("## Overview\n")
        md.append(f"- **Total Files:** {self.stats['total_files']}")
        md.append(f"- **Total Lines:** {self.stats['total_lines']:,}")
        md.append(f"- **Total Words:** {self.stats['total_words']:,}")
        md.append(f"- **Total Size:** {self.get_size_display(self.stats['total_size'])}\n")
        
        # By category
        md.append("## By Category\n")
        md.append("| Category | Files | Lines | Words | Size |")
        md.append("|----------|-------|-------|-------|------|")
        
        for category, stats in sorted(self.stats['categories'].items()):
            md.append(
                f"| {category} | {stats['count']} | {stats['lines']:,} | "
                f"{stats['words']:,} | {self.get_size_display(stats['size'])} |"
            )
        
        md.append("")
        md.append("## Files\n")
        
        for file_info in sorted(self.stats['files'], key=lambda x: x['name']):
            md.append(f"### {file_info['name']}\n")
            md.append(f"- **Path:** {file_info['path']}")
            md.append(f"- **Category:** {file_info['category']}")
            md.append(f"- **Lines:** {file_info['lines']}")
            md.append(f"- **Words:** {file_info['words']}")
            md.append(f"- **Sections:** {file_info['sections']}\n")
        
        return "\n".join(md)
    
    def export_json(self, output_path: str) -> None:
        """Export statistics as JSON"""
        with open(output_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print_success(f"Exported to: {output_path}")
    
    def print_summary(self) -> None:
        """Print summary to console"""
        print("\n" + self.get_summary_text())

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Generate documentation summary and statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 generate_summary.py docs/
  python3 generate_summary.py docs/ --output summary.json
  python3 generate_summary.py docs/ --format md > summary.md
        '''
    )
    
    parser.add_argument(
        'path',
        help='Path to documentation directory'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for JSON export'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'md', 'txt'],
        default='txt',
        help='Output format'
    )
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = DocumentationAnalyzer(args.path)
    
    # Analyze documentation
    stats = analyzer.analyze()
    
    # Output results
    if args.format == 'json':
        if args.output:
            analyzer.export_json(args.output)
        else:
            print(json.dumps(stats, indent=2))
    elif args.format == 'md':
        print(analyzer.get_summary_markdown())
    else:  # txt
        analyzer.print_summary()
    
    sys.exit(0)

if __name__ == '__main__':
    main()
