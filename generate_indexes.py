import os
import re
import urllib.parse

ROOT_DIR = 'tool_pages'
OUTPUT_FILE = 'index.html'
SITEMAP_FILE = 'sitemap.xml'
BASE_URL = 'https://rahulgpu.github.io/free-ai-tools-list-directory/'  # Update this to your actual GitHub Pages URL

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_tool_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    title = title_match.group(1) if title_match else "Unknown Tool"
    
    # Try to extract logo
    logo_match = re.search(r'<img src="(.*?)" alt=".*? Logo"', content)
    logo_url = logo_match.group(1) if logo_match else ""
    
    # Try to extract description (bio)
    desc_match = re.search(r'<p class="bio">(.*?)</p>', content)
    description = desc_match.group(1) if desc_match else ""
    
    return {
        'title': title,
        'logo_url': logo_url,
        'description': description,
        'filename': os.path.basename(file_path)
    }

def generate_indexes():
    categories = []
    
    # Walk through tool_pages directory
    if not os.path.exists(ROOT_DIR):
        print(f"Directory {ROOT_DIR} does not exist.")
        return

    for category_name in sorted(os.listdir(ROOT_DIR)):
        category_path = os.path.join(ROOT_DIR, category_name)
        if not os.path.isdir(category_path):
            continue
            
        tools = []
        # Get all html files in category folder
        for filename in sorted(os.listdir(category_path)):
            if filename.endswith('.html') and filename != 'index.html':
                file_path = os.path.join(category_path, filename)
                tool_info = get_tool_info(file_path)
                tools.append(tool_info)
        
        if not tools:
            continue

        # Create Category Index Page
        category_index_path = os.path.join(category_path, 'index.html')
        create_category_page(category_name, tools, category_index_path)
        
        # Add to categories list (use first tool's logo as category thumbnail if available)
        categories.append({
            'name': category_name,
            'count': len(tools),
            'thumbnail': tools[0]['logo_url'] if tools and tools[0]['logo_url'] else '',
            'path': f"{ROOT_DIR}/{category_name}/index.html"
        })

    # Create Root Index Page
    create_root_index(categories)
    
    # Create Sitemap
    create_sitemap(categories)

def create_category_page(category_name, tools, output_path):
    tools_html = ""
    for tool in tools:
        logo_html = f'<img src="{tool["logo_url"]}" alt="{tool["title"]}" loading="lazy">' if tool['logo_url'] else '<div class="no-logo">AI</div>'
        tools_html += f"""
        <a href="{tool['filename']}" class="tool-card">
            <div class="tool-icon">
                {logo_html}
            </div>
            <div class="tool-info">
                <h3>{tool['title']}</h3>
                <p>{tool['description']}</p>
            </div>
        </a>
        """
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} AI Tools - Free AI Tools Directory</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f7fa;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 0;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        h1 {{ margin: 0; color: #1a1a1a; }}
        .breadcrumb {{ margin-bottom: 20px; color: #666; }}
        .breadcrumb a {{ color: #007bff; text-decoration: none; }}
        
        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        .tool-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            align-items: start;
            gap: 15px;
            border: 1px solid #e1e4e8;
        }}
        .tool-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .tool-icon {{
            width: 50px;
            height: 50px;
            flex-shrink: 0;
            border-radius: 8px;
            overflow: hidden;
            background: #f0f2f5;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .tool-icon img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .no-logo {{
            font-weight: bold;
            color: #999;
        }}
        .tool-info h3 {{
            margin: 0 0 5px 0;
            color: #1a1a1a;
            font-size: 1.1rem;
        }}
        .tool-info p {{
            margin: 0;
            color: #666;
            font-size: 0.9rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
    </style>
</head>
<body>
    <div class="breadcrumb">
        <a href="../../index.html">Home</a> &gt; <span>{category_name}</span>
    </div>
    <header>
        <h1>{category_name} AI Tools</h1>
        <p>Discover {len(tools)} best AI tools for {category_name}</p>
    </header>
    <main class="tools-grid">
        {tools_html}
    </main>
</body>
</html>
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_root_index(categories):
    categories_html = ""
    for cat in categories:
        # URL encode the path components for the link
        cat_url = urllib.parse.quote(cat['path'])
        
        logo_html = f'<img src="{cat["thumbnail"]}" alt="{cat["name"]}" loading="lazy">' if cat['thumbnail'] else '<div class="no-logo">📂</div>'
        
        categories_html += f"""
        <a href="{cat_url}" class="category-card">
            <div class="category-icon">
                {logo_html}
            </div>
            <div class="category-info">
                <h3>{cat['name']}</h3>
                <span class="count">{cat['count']} tools</span>
            </div>
        </a>
        """
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free AI Tools Directory - 11,000+ AI Tools List</title>
    <meta name="description" content="Discover 11,000+ free AI tools. The largest directory of artificial intelligence software for developers, marketers, and creators. Updated daily.">
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f7fa;
        }}
        header {{
            text-align: center;
            margin-bottom: 50px;
            padding: 60px 20px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        h1 {{
            font-size: 3rem;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #007bff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-text {{
            font-size: 1.25rem;
            color: #555;
            max-width: 700px;
            margin: 0 auto;
        }}
        .categories-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }}
        .category-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            text-decoration: none;
            color: inherit;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 15px;
            border: 1px solid #e1e4e8;
        }}
        .category-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-color: #007bff;
        }}
        .category-icon {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #f0f7ff;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        .category-icon img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .category-info h3 {{
            margin: 0 0 5px 0;
            font-size: 1.1rem;
        }}
        .count {{
            color: #666;
            font-size: 0.85rem;
            background: #f0f2f5;
            padding: 2px 8px;
            border-radius: 10px;
        }}
        .search-bar {{
            margin: 30px auto;
            max-width: 500px;
            position: relative;
        }}
        .search-bar input {{
            width: 100%;
            padding: 15px 25px;
            border-radius: 30px;
            border: 2px solid #e1e4e8;
            font-size: 1.1rem;
            outline: none;
            transition: border-color 0.3s;
        }}
        .search-bar input:focus {{
            border-color: #007bff;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Free AI Tools Directory</h1>
        <p class="hero-text">Explore the world's largest collection of 11,000+ AI tools. Find the perfect AI software for your needs, categorized and curated.</p>
        
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="Search categories...">
        </div>
    </header>

    <main class="categories-grid" id="categoriesGrid">
        {categories_html}
    </main>

    <script>
        document.getElementById('searchInput').addEventListener('keyup', function(e) {{
            const term = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.category-card');
            
            cards.forEach(card => {{
                const title = card.querySelector('h3').textContent.toLowerCase();
                if (title.includes(term)) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }});
    </script>
</body>
</html>
"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_sitemap(categories):
    # This is a basic sitemap generator
    # It lists the root index and all category pages
    # For a full sitemap including 11k tools, it might be too large for a single file, 
    # but we can list the categories at least.
    
    urlset = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{BASE_URL}</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
"""
    
    for cat in categories:
        cat_url_path = urllib.parse.quote(cat['path'])
        urlset += f"""    <url>
        <loc>{BASE_URL}{cat_url_path}</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
"""
        # Also add individual tools if needed, but keeping it light for now
        # To add tools: iterate again and add tool['filename']
    
    urlset += "</urlset>"
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(urlset)

if __name__ == "__main__":
    print("Generating indexes...")
    generate_indexes()
    print("Done!")
