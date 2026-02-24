
import re

def categorize_tool(description):
    desc_lower = description.lower()
    
    # Categories and keywords
    categories = {
        "🤖 ChatGPT & Writing Tools": ["chatgpt", "writing", "content", "essay", "chatting", "text", "copy", "blog", "summary", "summaries", "translation", "language", "grammar", "story", "script", "email", "poem", "poet"],
        "🎨 Image Generation AI": ["image", "art", "photo", "picture", "drawing", "painting", "design", "logo", "icon", "avatar", "3d", "texture", "background", "edit", "enhance", "upscale", "remove", "color", "filter", "visual"],
        "🎥 Video AI Tools": ["video", "movie", "film", "clip", "shorts", "reel", "tiktok", "youtube", "animation", "subtitle", "caption", "transcription", "audio", "speech", "voice", "dubbing", "podcast", "music"],
        "💻 Coding AI Assistants": ["code", "programming", "developer", "dev", "git", "sql", "database", "test", "debug", "api", "sdk", "web", "app", "software", "cloud", "server", "linux", "terminal", "shell", "css", "html", "javascript", "python"],
        "📈 Marketing AI Tools": ["marketing", "seo", "ad", "advertising", "social media", "instagram", "facebook", "twitter", "linkedin", "email marketing", "campaign", "lead", "sales", "analytics", "growth", "brand", "business", "market research", "customer"],
        "⚙️ Automation AI": ["automation", "workflow", "task", "agent", "bot", "rpa", "zapier", "integration", "productivity", "time", "calendar", "schedule", "meeting", "assistant", "browser", "extension"]
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    
    return "Other AI Tools"

def main():
    readme_path = "README.md"
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split content into header and list
    # The list starts after "### Top 1000 AI Tools (Alphabetically Sorted)"
    split_marker = "### Top 1000 AI Tools (Alphabetically Sorted)"
    if split_marker not in content:
        # Try finding it line by line to debug or match partial
        lines = content.splitlines()
        found_index = -1
        for i, line in enumerate(lines):
            if "Top 1000 AI Tools" in line:
                found_index = i
                break
        
        if found_index != -1:
            header_part = "\n".join(lines[:found_index])
            list_part = "\n".join(lines[found_index+1:])
        else:
            print("Could not find the list marker even partially.")
            return
    else:
        header_part, list_part = content.split(split_marker)
    
    # Parse list items
    # Lines starting with a number and a dot, e.g., "1. [Name](url) - Description"
    list_items = []
    lines = list_part.splitlines()
    
    tool_regex = re.compile(r"^\d+\.\s+\[(.*?)\]\((.*?)\)\s+-\s+(.*)$")
    
    other_lines = [] # Lines that are not tool items
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match = tool_regex.match(line)
        if match:
            name, url, description = match.groups()
            list_items.append({
                "name": name,
                "url": url,
                "description": description,
                "original_line": line
            })
        else:
            other_lines.append(line)

    # Categorize items
    categorized_items = {
        "🤖 ChatGPT & Writing Tools": [],
        "🎨 Image Generation AI": [],
        "🎥 Video AI Tools": [],
        "💻 Coding AI Assistants": [],
        "📈 Marketing AI Tools": [],
        "⚙️ Automation AI": [],
        "Other AI Tools": []
    }
    
    for item in list_items:
        category = categorize_tool(item["description"])
        categorized_items[category].append(item)
    
    # Build new README content
    new_content = header_part
    
    # Add PDF Section
    pdf_section = """
## 📁 AI Tools PDF Library

Download curated AI tools PDFs:

- [ChatGPT Tools PDF](pdfs/wp-best-ai-chat-tools.pdf)
- [AI Image Tools PDF](pdfs/wp-best-ai-image-tools.pdf)
- [Marketing AI Tools PDF](pdfs/wp-best-ai-text-tools.pdf)

Full directory: `https://aitoolslist.xyz`

"""
    # Insert PDF section before "## Browse AI Tools" if it exists, otherwise just append to header
    if "## Browse AI Tools" in new_content:
        new_content = new_content.replace("## Browse AI Tools", pdf_section + "## Browse AI Tools")
    else:
        new_content += pdf_section

    # Add Category Headings
    new_content += "\n## AI Tools by Category\n\n"
    
    category_order = [
        "🤖 ChatGPT & Writing Tools",
        "🎨 Image Generation AI",
        "🎥 Video AI Tools",
        "💻 Coding AI Assistants",
        "📈 Marketing AI Tools",
        "⚙️ Automation AI",
        "Other AI Tools"
    ]
    
    for category in category_order:
        items = categorized_items[category]
        if not items:
            continue
            
        new_content += f"### {category}\n\n"
        for i, item in enumerate(items, 1):
            new_content += f"{i}. [{item['name']}]({item['url']}) - {item['description']}\n"
        new_content += "\n"
        
    # Write back to README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("README.md updated successfully.")

if __name__ == "__main__":
    main()
