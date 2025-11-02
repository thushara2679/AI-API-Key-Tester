#!/usr/bin/env python3

"""
update_toc.py - Table of Contents Update Script

Purpose: Automatically generate and update table of contents in markdown files
Usage: python3 update_toc.py [path] [--in-place] [--max-depth 3]

Features:
- Generates TOC from markdown headings
- Updates existing TOC automatically
- Handles nested levels
- Generates proper anchor links
- Supports multiple files
- Can write in-place or to stdout
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(msg: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}", file=sys.stderr)

def print_success(msg: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {msg}", file=sys.stderr)

def print_warning(msg: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}", file=sys.stderr)

def print_error(msg: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {msg}", file=sys.stderr)

class TableOfContentsGenerator:
    """Generates and updates table of contents for markdown files"""
    
    def __init__(self, max_depth: int = 3, in_place: bool = False):
        """Initialize generator"""
        self.max_depth = max_depth
        self.in_place = in_place
        self.toc_marker = '<!-- toc -->'
        self.toc_end_marker = '<!-- tocend -->'
        self.heading_regex = re.compile(r'^(#+)\s+(.+)$', re.MULTILINE)
    
    def extract_headings(self, content: str) -> List[Tuple[int, str]]:
        """Extract headings from markdown content"""
        headings = []
        
        for match in self.heading_regex.finditer(content):
            level = len(match.group(1))
            text = match.group(2)
            
            # Skip H1 (usually document title)
            if level == 1:
                continue
            
            # Skip if exceeds max depth
            if level - 1 > self.max_depth:
                continue
            
            headings.append((level, text))
        
        return headings
    
    def text_to_anchor(self, text: str) -> str:
        """Convert heading text to markdown anchor format"""
        # Remove markdown formatting
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)       # Italic
        text = re.sub(r'`(.+?)`', r'\1', text)         # Code
        
        # Convert to anchor
        anchor = text.lower()
        anchor = re.sub(r'\s+', '-', anchor)           # Spaces to hyphens
        anchor = re.sub(r'[^\w\-]', '', anchor)        # Remove special chars
        
        return anchor
    
    def generate_toc(self, headings: List[Tuple[int, str]]) -> str:
        """Generate table of contents from headings"""
        if not headings:
            return ""
        
        toc_lines = ["## Table of Contents\n"]
        
        for level, text in headings:
            # Calculate indentation
            indent = "  " * (level - 2)
            anchor = self.text_to_anchor(text)
            toc_lines.append(f"{indent}- [{text}](#{anchor})")
        
        return "\n".join(toc_lines) + "\n"
    
    def extract_toc_section(self, content: str) -> Optional[Tuple[int, int]]:
        """Find existing TOC section in content"""
        start_match = re.search(re.escape(self.toc_marker), content)
        end_match = re.search(re.escape(self.toc_end_marker), content)
        
        if start_match and end_match:
            return (start_match.start(), end_match.end())
        
        return None
    
    def update_content_with_toc(self, content: str, toc: str) -> str:
        """Update content with new TOC"""
        toc_section = self.extract_toc_section(content)
        
        if toc_section:
            # Replace existing TOC
            start, end = toc_section
            new_content = (
                content[:start] +
                self.toc_marker + "\n\n" +
                toc + "\n" +
                self.toc_end_marker +
                content[end:]
            )
        else:
            # Insert TOC after first heading
            heading_match = self.heading_regex.search(content)
            if heading_match:
                insert_pos = heading_match.end()
                # Find end of line
                insert_pos = content.find('\n', insert_pos) + 1
                new_content = (
                    content[:insert_pos] + "\n" +
                    self.toc_marker + "\n\n" +
                    toc + "\n" +
                    self.toc_end_marker + "\n" +
                    content[insert_pos:]
                )
            else:
                # No headings found
                return content
        
        return new_content
    
    def process_file(self, file_path: Path) -> bool:
        """Process single markdown file"""
        if not file_path.exists():
            print_error(f"File not found: {file_path}")
            return False
        
        if file_path.suffix != '.md':
            print_warning(f"Not a markdown file: {file_path}")
            return False
        
        print_info(f"Processing: {file_path.name}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print_error(f"Cannot read file: {e}")
            return False
        
        # Extract headings
        headings = self.extract_headings(content)
        
        if not headings:
            print_warning(f"No headings found in {file_path.name}")
            return False
        
        # Generate TOC
        toc = self.generate_toc(headings)
        
        # Update content
        new_content = self.update_content_with_toc(content, toc)
        
        if self.in_place:
            # Write back to file
            try:
                file_path.write_text(new_content, encoding='utf-8')
                print_success(f"Updated: {file_path.name} ({len(headings)} headings)")
                return True
            except Exception as e:
                print_error(f"Cannot write file: {e}")
                return False
        else:
            # Print to stdout
            print(new_content)
            return True
    
    def process_directory(self, dir_path: Path) -> Tuple[int, int]:
        """Process all markdown files in directory"""
        if not dir_path.is_dir():
            print_error(f"Not a directory: {dir_path}")
            return (0, 0)
        
        md_files = sorted(dir_path.rglob('*.md'))
        
        if not md_files:
            print_warning("No markdown files found")
            return (0, 0)
        
        print_info(f"Found {len(md_files)} markdown files")
        
        success_count = 0
        error_count = 0
        
        for file_path in md_files:
            if self.process_file(file_path):
                success_count += 1
            else:
                error_count += 1
        
        return (success_count, error_count)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Generate and update table of contents in markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate TOC for single file (print to stdout)
  python3 update_toc.py docs/README.md
  
  # Update TOC in-place for single file
  python3 update_toc.py docs/README.md --in-place
  
  # Update all markdown files in directory
  python3 update_toc.py docs/ --in-place
  
  # Generate TOC with max depth of 2
  python3 update_toc.py docs/ --in-place --max-depth 2
        '''
    )
    
    parser.add_argument(
        'path',
        help='Path to markdown file or directory'
    )
    
    parser.add_argument(
        '--in-place',
        action='store_true',
        help='Update files in-place instead of printing to stdout'
    )
    
    parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Maximum heading depth to include in TOC (default: 3)'
    )
    
    args = parser.parse_args()
    
    # Create generator
    generator = TableOfContentsGenerator(
        max_depth=args.max_depth,
        in_place=args.in_place
    )
    
    path = Path(args.path)
    
    if path.is_file():
        # Process single file
        success = generator.process_file(path)
        sys.exit(0 if success else 1)
    else:
        # Process directory
        success_count, error_count = generator.process_directory(path)
        
        print_info(f"\n{'='*50}")
        print_success(f"Successfully updated: {success_count} files")
        if error_count > 0:
            print_error(f"Failed: {error_count} files")
        
        sys.exit(0 if error_count == 0 else 1)

if __name__ == '__main__':
    main()
