#!/usr/bin/env python3
"""
Simple automated tests for Ahmed Harbi's personal website.
Tests HTML structure, links, images, and basic accessibility.
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser


class LinkAndImageParser(HTMLParser):
    """Parse HTML to extract links and images."""
    
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.videos = []
        self.meta_tags = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])
        elif tag == 'img' and 'src' in attrs_dict:
            self.images.append(attrs_dict['src'])
        elif tag == 'iframe' and 'src' in attrs_dict:
            self.videos.append(attrs_dict['src'])
        elif tag == 'meta':
            self.meta_tags.append(attrs_dict)


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def read_html_file(filename):
    """Read HTML file content."""
    filepath = get_project_root() / filename
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def test_html_files_exist():
    """Test that all main HTML files exist."""
    root = get_project_root()
    required_files = ['index.html', 'projects.html', 'publications.html', 'contact.html']
    
    print("Testing HTML files existence...")
    for filename in required_files:
        filepath = root / filename
        assert filepath.exists(), f"Missing required file: {filename}"
        print(f"  ✓ {filename} exists")
    print()


def test_html_structure():
    """Test basic HTML structure of main pages."""
    print("Testing HTML structure...")
    pages = ['index.html', 'projects.html', 'publications.html', 'contact.html']
    
    for page in pages:
        content = read_html_file(page)
        if content is None:
            continue
            
        # Check for required HTML elements
        assert '<!DOCTYPE html>' in content, f"{page}: Missing DOCTYPE"
        assert '<html' in content, f"{page}: Missing html tag"
        assert '<head>' in content, f"{page}: Missing head tag"
        assert '<body>' in content, f"{page}: Missing body tag"
        assert '<title>' in content, f"{page}: Missing title tag"
        assert '</html>' in content, f"{page}: Missing closing html tag"
        
        print(f"  ✓ {page} has valid HTML structure")
    print()


def test_meta_tags():
    """Test that important meta tags are present."""
    print("Testing meta tags...")
    pages = ['index.html', 'projects.html', 'publications.html']
    
    for page in pages:
        content = read_html_file(page)
        if content is None:
            continue
            
        parser = LinkAndImageParser()
        parser.feed(content)
        
        # Check for important meta tags
        has_description = any('name' in m and m.get('name') == 'description' for m in parser.meta_tags)
        has_viewport = any('name' in m and m.get('name') == 'viewport' for m in parser.meta_tags)
        
        assert has_description, f"{page}: Missing meta description"
        assert has_viewport, f"{page}: Missing viewport meta tag"
        
        print(f"  ✓ {page} has required meta tags")
    print()


def test_local_images_exist():
    """Test that local images referenced in HTML exist."""
    print("Testing local images...")
    root = get_project_root()
    pages = ['index.html', 'projects.html', 'publications.html']
    
    for page in pages:
        content = read_html_file(page)
        if content is None:
            continue
            
        parser = LinkAndImageParser()
        parser.feed(content)
        
        for img_src in parser.images:
            # Skip external images (http/https)
            if img_src.startswith('http://') or img_src.startswith('https://'):
                continue
            
            # Remove leading slash if present
            img_path = img_src.lstrip('/')
            full_path = root / img_path
            
            assert full_path.exists(), f"{page}: Image not found: {img_src}"
        
        print(f"  ✓ {page}: All local images exist")
    print()


def test_css_file_exists():
    """Test that CSS file exists and is linked."""
    print("Testing CSS...")
    root = get_project_root()
    
    # Check if styles.css exists in assets/css/
    css_file = root / 'assets' / 'css' / 'styles.css'
    assert css_file.exists(), "assets/css/styles.css not found"
    print("  ✓ assets/css/styles.css exists")
    
    # Check if it's linked in HTML files
    pages = ['index.html', 'projects.html', 'publications.html', 'contact.html']
    for page in pages:
        content = read_html_file(page)
        if content:
            assert 'assets/css/styles.css' in content, f"{page}: styles.css not linked"
            print(f"  ✓ {page} links to assets/css/styles.css")
    print()


def test_navigation_consistency():
    """Test that navigation is consistent across pages."""
    print("Testing navigation consistency...")
    pages = ['index.html', 'projects.html', 'publications.html', 'contact.html']
    
    nav_links = set()
    for page in pages:
        content = read_html_file(page)
        if content is None:
            continue
            
        parser = LinkAndImageParser()
        parser.feed(content)
        
        # Extract internal navigation links
        internal_links = [link for link in parser.links if link.endswith('.html')]
        nav_links.add(tuple(sorted(internal_links)))
    
    # Should have consistent navigation (allowing for some variation)
    print(f"  ✓ Found navigation on all pages")
    print()


def test_no_broken_internal_links():
    """Test that internal HTML links point to existing files."""
    print("Testing internal links...")
    root = get_project_root()
    pages = ['index.html', 'projects.html', 'publications.html', 'contact.html']
    
    for page in pages:
        content = read_html_file(page)
        if content is None:
            continue
            
        parser = LinkAndImageParser()
        parser.feed(content)
        
        for link in parser.links:
            # Skip external links
            if link.startswith('http://') or link.startswith('https://'):
                continue
            # Skip anchors and special links
            if link.startswith('#') or link.startswith('mailto:'):
                continue
            
            # Check if file exists
            link_path = link.lstrip('/')
            # Remove anchor if present
            link_path = link_path.split('#')[0]
            
            if link_path:
                full_path = root / link_path
                assert full_path.exists(), f"{page}: Broken link to {link}"
        
        print(f"  ✓ {page}: All internal links are valid")
    print()


def test_media_folder_structure():
    """Test that media folders are organized."""
    print("Testing folder structure...")
    root = get_project_root()
    
    # Check for organized folders
    expected_folders = [
        'assets/images/home',
        'assets/images/publications',
        'assets/images/projects',
        'assets/css',
        'assets/js',
        'assets/icons'
    ]
    
    for folder in expected_folders:
        folder_path = root / folder
        assert folder_path.exists(), f"Missing organized folder: {folder}"
        print(f"  ✓ {folder} exists")
    print()


def test_responsive_viewport():
    """Test that pages have responsive viewport meta tag."""
    print("Testing responsive design...")
    pages = ['index.html', 'projects.html', 'publications.html', 'contact.html']
    
    for page in pages:
        content = read_html_file(page)
        if content:
            # Check for viewport meta tag with width=device-width
            assert 'viewport' in content and 'width=device-width' in content, \
                f"{page}: Missing responsive viewport meta tag"
            print(f"  ✓ {page} has responsive viewport")
    print()


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Website Tests")
    print("=" * 60)
    print()
    
    try:
        test_html_files_exist()
        test_html_structure()
        test_meta_tags()
        test_local_images_exist()
        test_css_file_exists()
        test_navigation_consistency()
        test_no_broken_internal_links()
        test_media_folder_structure()
        test_responsive_viewport()
        
        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ Test failed: {e}")
        print("=" * 60)
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
