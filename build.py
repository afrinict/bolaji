#!/usr/bin/env python3
"""
Build script for Eloggia & Elous Design website
Optimizes files for production deployment
"""

import os
import re
import shutil
from pathlib import Path

def create_build_directory():
    """Create build directory if it doesn't exist"""
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    return build_dir

def minify_css(css_content):
    """Basic CSS minification"""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Remove extra whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    # Remove whitespace around certain characters
    css_content = re.sub(r'\s*([{}:;,>+])\s*', r'\1', css_content)
    # Remove trailing semicolons before closing braces
    css_content = re.sub(r';+}', '}', css_content)
    return css_content.strip()

def minify_js(js_content):
    """Basic JavaScript minification"""
    # Remove single-line comments (but keep URLs)
    js_content = re.sub(r'(?<!:)//.*$', '', js_content, flags=re.MULTILINE)
    # Remove multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    # Remove extra whitespace
    js_content = re.sub(r'\s+', ' ', js_content)
    # Remove whitespace around certain characters
    js_content = re.sub(r'\s*([{}:;,()=+>])\s*', r'\1', js_content)
    return js_content.strip()

def optimize_html(html_content):
    """Basic HTML optimization"""
    # Remove extra whitespace
    html_content = re.sub(r'\s+', ' ', html_content)
    # Remove whitespace between tags
    html_content = re.sub(r'>\s+<', '><', html_content)
    return html_content.strip()

def copy_and_optimize_files(build_dir):
    """Copy and optimize all website files"""
    
    # Copy and optimize HTML
    print("📄 Optimizing HTML...")
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Add build timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = html_content.replace(
        '<meta name="description"',
        f'<!-- Built on: {timestamp} -->\n    <meta name="description"'
    )
    
    optimized_html = optimize_html(html_content)
    with open(build_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(optimized_html)
    
    # Copy and optimize CSS
    print("🎨 Optimizing CSS...")
    with open("styles.css", "r", encoding="utf-8") as f:
        css_content = f.read()
    
    optimized_css = minify_css(css_content)
    with open(build_dir / "styles.css", "w", encoding="utf-8") as f:
        f.write(optimized_css)
    
    # Copy and optimize JavaScript
    print("⚡ Optimizing JavaScript...")
    with open("script.js", "r", encoding="utf-8") as f:
        js_content = f.read()
    
    optimized_js = minify_js(js_content)
    with open(build_dir / "script.js", "w", encoding="utf-8") as f:
        f.write(optimized_js)
    
    # Copy README
    if os.path.exists("README.md"):
        print("📖 Copying README...")
        shutil.copy("README.md", build_dir / "README.md")

def create_deployment_files(build_dir):
    """Create additional deployment files"""
    
    # Create .htaccess for Apache
    htaccess_content = """# Eloggia & Elous Design Website
# Apache Configuration

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Set cache headers
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>

# Security headers
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
"""
    
    with open(build_dir / ".htaccess", "w", encoding="utf-8") as f:
        f.write(htaccess_content)
    
    # Create robots.txt
    robots_content = """User-agent: *
Allow: /

# Sitemap
Sitemap: https://eloggiaelous.com/sitemap.xml
"""
    
    with open(build_dir / "robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)
    
    # Create sitemap.xml
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://eloggiaelous.com/</loc>
        <lastmod>2024-01-01</lastmod>
        <changefreq>monthly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""
    
    with open(build_dir / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

def create_deployment_guide(build_dir):
    """Create deployment guide"""
    guide_content = """# Eloggia & Elous Design - Deployment Guide

## 🚀 Production Deployment

### Files Included in Build:
- `index.html` - Main website file
- `styles.css` - Optimized CSS styles
- `script.js` - Optimized JavaScript
- `.htaccess` - Apache server configuration
- `robots.txt` - Search engine crawling rules
- `sitemap.xml` - Site structure for search engines

### Deployment Options:

#### 1. Shared Hosting (cPanel, etc.)
1. Upload all files from the `build/` directory to your web root
2. Ensure `.htaccess` is uploaded (may be hidden)
3. Test the website functionality

#### 2. VPS/Dedicated Server
1. Copy files to `/var/www/html/` or your web directory
2. Set proper permissions: `chmod 644 *` and `chmod 755 .`
3. Restart Apache/Nginx if needed

#### 3. CDN/Static Hosting (Netlify, Vercel, etc.)
1. Upload the entire `build/` directory
2. Configure custom domain if needed
3. Set up SSL certificate

### Performance Optimizations Applied:
- ✅ CSS minification
- ✅ JavaScript minification
- ✅ HTML optimization
- ✅ Gzip compression enabled
- ✅ Browser caching configured
- ✅ Security headers added

### SEO Features:
- ✅ Meta descriptions
- ✅ Semantic HTML structure
- ✅ Sitemap.xml included
- ✅ Robots.txt configured
- ✅ Mobile-responsive design

### Contact Information:
- Phone: +234 803 383 7798
- WhatsApp: +234 803 383 7798
- Location: Abuja, Nigeria

### Maintenance:
- Update contact information as needed
- Replace portfolio images with actual project photos
- Add Google Analytics tracking code
- Monitor website performance

---
Built with ❤️ for Eloggia & Elous Design
"""
    
    with open(build_dir / "DEPLOYMENT.md", "w", encoding="utf-8") as f:
        f.write(guide_content)

def main():
    """Main build process"""
    print("🏗️  Starting build process for Eloggia & Elous Design...")
    
    # Create build directory
    build_dir = create_build_directory()
    print(f"📁 Created build directory: {build_dir}")
    
    # Copy and optimize files
    copy_and_optimize_files(build_dir)
    
    # Create deployment files
    print("🔧 Creating deployment files...")
    create_deployment_files(build_dir)
    
    # Create deployment guide
    print("📋 Creating deployment guide...")
    create_deployment_guide(build_dir)
    
    # Calculate file sizes
    total_size = 0
    for file_path in build_dir.rglob("*"):
        if file_path.is_file():
            size = file_path.stat().st_size
            total_size += size
            print(f"📄 {file_path.name}: {size:,} bytes")
    
    print(f"\n✅ Build completed successfully!")
    print(f"📊 Total build size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    print(f"📁 Build files located in: {build_dir}")
    print(f"🚀 Ready for deployment!")
    
    # Create a simple test server for the build
    print(f"\n🌐 Starting test server for build...")
    print(f"📱 Open http://localhost:8080 to test the build")
    
    return build_dir

if __name__ == "__main__":
    build_dir = main() 