
import xml.etree.ElementTree as ET
import os
import re
from pathlib import Path

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def parse_xml_and_generate_pages(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespaces
    namespaces = {
        'wp': 'http://wordpress.org/export/1.2/',
        'content': 'http://purl.org/rss/1.0/modules/content/'
    }

    channel = root.find('channel')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count = 0
    for item in channel.findall('item'):
        # Check post type
        post_type = item.find('wp:post_type', namespaces).text
        if post_type != 'toolbox-tool':
            continue

        # Extract data
        title = item.find('title').text
        if not title:
            continue
            
        link = item.find('link').text
        
        # Get Post Meta
        meta_data = {}
        for meta in item.findall('wp:postmeta', namespaces):
            key = meta.find('wp:meta_key', namespaces).text
            value = meta.find('wp:meta_value', namespaces).text
            meta_data[key] = value

        slug = meta_data.get('toolbox_seo_page_slug')
        if not slug:
            # Fallback to extracting from link or title
            if link:
                slug = link.strip('/').split('/')[-1]
            else:
                slug = title.lower().replace(' ', '-')

        bio = meta_data.get('toolbox_user_bio', '')
        description = meta_data.get('toolbox_product_information', '')
        external_url = meta_data.get('toolbox_external_website', '')
        logo_url = meta_data.get('toolbox_tool_logo_id_url', '')
        
        # Category
        category_element = item.find('category')
        category = "Uncategorized"
        if category_element is not None:
            category = category_element.text

        # Create Category Directory
        cat_dir = os.path.join(output_dir, sanitize_filename(category))
        if not os.path.exists(cat_dir):
            os.makedirs(cat_dir)

        # Generate HTML content
        logo_html = f'<img src="{logo_url}" alt="{title} Logo" style="width: auto; height: 100px; margin-bottom: 20px;">' if logo_url else ''
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI Tool</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        .bio {{
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 20px;
        }}
        .button {{
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            font-size: 1.1rem;
            transition: background-color 0.3s;
        }}
        .button:hover {{
            background-color: #0056b3;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .meta {{
            margin-top: 20px;
            font-size: 0.9rem;
            color: #888;
        }}
    </style>
</head>
<body>
    <header>
        {logo_html}
        <h1>{title}</h1>
        <p class="bio">{bio}</p>
        <a href="https://aitoolslist.xyz/{slug}/" class="button">Visit Tool Page</a>
    </header>

    <main>
        <div class="content">
            <h2>About {title}</h2>
            <p>{description}</p>
        </div>

        <div class="meta">
            <p>Category: {category}</p>
        </div>
    </main>
</body>
</html>"""

        # Write HTML file
        file_path = os.path.join(cat_dir, f"{sanitize_filename(slug)}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        count += 1

    print(f"Generated {count} tool pages in '{output_dir}'")

if __name__ == "__main__":
    xml_file = "aitoolhub.WordPress.2026-02-19.xml"
    output_dir = "tool_pages"
    parse_xml_and_generate_pages(xml_file, output_dir)
