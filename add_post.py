import os
import sys
from datetime import datetime
import uuid
import markdown
import re

POSTS_DIR = 'posts'


def get_post_filename(post_id, title, timestamp):
    date_str = timestamp.split('T')[0]
    time_str = timestamp.split('T')[1].replace(':', '-')
    safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
    safe_title = safe_title.replace(' ', '_')
    return f"{date_str}_{time_str}_{safe_title}_{post_id}.md"


def save_post(post_id, title, content, link=None, image=None, epigraph=None, timestamp=None):
    if not timestamp:
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    filename = get_post_filename(post_id, title, timestamp)
    filepath = os.path.join(POSTS_DIR, filename)
    date_str = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S').strftime('%B %d, %Y')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(f'id: {post_id}\n')
        f.write(f'title: "{title}"\n')
        f.write(f'date: "{date_str}"\n')
        f.write(f'timestamp: "{timestamp}"\n')
        f.write(f'link: "{link if link else ""}"\n')
        f.write(f'image: "{image if image else ""}"\n')
        f.write(f'epigraph: "{epigraph if epigraph else ""}"\n')
        f.write('---\n\n')
        f.write(content.strip())
    return filepath


def parse_front_matter(lines):
    meta = {}
    if lines[0].strip() == '---':
        i = 1
        while i < len(lines) and lines[i].strip() != '---':
            line = lines[i].strip()
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip().strip('"')
            i += 1
        content = ''.join(lines[i+1:]).strip()
        return meta, content
    return {}, ''.join(lines).strip()

def convert_sidenotes(md_content):
    # Find all ^[sidenote text] and replace with tufte.css sidenote HTML
    sidenote_pattern = re.compile(r'\^\[(.+?)\]')
    count = 1
    def replacer(match):
        nonlocal count
        text = match.group(1)
        html = (f'<label for="sn-{count}" class="margin-toggle">&#8853;</label>'
                f'<input type="checkbox" id="sn-{count}" class="margin-toggle"/>'
                f'<span class="sidenote">{text}</span>')
        count += 1
        return html
    return sidenote_pattern.sub(replacer, md_content)

def load_posts():
    posts = []
    for fname in os.listdir(POSTS_DIR):
        if fname.endswith('.md'):
            with open(os.path.join(POSTS_DIR, fname), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                meta, content_md = parse_front_matter(lines)
                # Convert markdown-style sidenotes to tufte.css HTML
                content_md = convert_sidenotes(content_md)
                content_html = markdown.markdown(content_md, extensions=['extra'])
                posts.append({
                    'id': meta.get('id', ''),
                    'title': meta.get('title', ''),
                    'date': meta.get('date', ''),
                    'timestamp': meta.get('timestamp', ''),
                    'link': meta.get('link', ''),
                    'image': meta.get('image', ''),
                    'epigraph': meta.get('epigraph', ''),
                    'content': content_html
                })
    # Sort posts by timestamp descending
    posts.sort(key=lambda p: p.get('timestamp', ''), reverse=True)
    return posts


def generate_index(posts):
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n')
        f.write('  <meta charset="utf-8">\n')
        f.write('  <meta name="viewport" content="width=device-width, initial-scale=1">\n')
        f.write('  <title>Dusty Print Books</title>\n')
        f.write('  <link rel="stylesheet" href="tufte.css">\n')
        f.write('  <link rel="stylesheet" href="site-custom.css">\n')
        f.write('</head>\n<body>\n')
        f.write('<header>\n')
        f.write('  <h1>Dusty Print Books</h1>\n')
        f.write('</header>\n')
        f.write('<article>\n')
        for post in posts:
            f.write(f'<section class="section" id="post-{post["id"]}">\n')
            f.write(f'<h2>{post["title"]}</h2>\n')
            f.write(f'<p class="date">{post["date"]}</p>\n')
            if post["image"]:
                f.write(f'<figure><img src="{post["image"]}" alt="{post["title"]}" style="max-width:100%;margin-bottom:1em;" /></figure>\n')
            elif post["epigraph"]:
                # Split epigraph into quote and source using -- as separator
                epigraph = post["epigraph"]
                if "--" in epigraph:
                    quote, source = epigraph.split("--", 1)
                    quote = quote.strip()
                    source = source.strip()
                else:
                    quote = epigraph.strip()
                    source = ""
                f.write('<blockquote class="epigraph">')
                f.write(f'<p><em>{quote}</em></p>')
                if source:
                    f.write(f'<footer>{source}</footer>')
                f.write('</blockquote>\n')
            f.write(post["content"] + '\n')
            if post["link"]:
                f.write(f'<p><a href="{post["link"]}" target="_blank" rel="noopener">Link</a></p>\n')
            f.write('</section>\n')
        f.write('</article>\n')
        f.write('<footer>\n')
        f.write('  &copy; 2025 Dusty Print Books &mdash; This is a reading list.\n')
        f.write('</footer>\n')
        f.write('</body>\n</html>\n')


def main():
    if len(sys.argv) < 3:
        print("Usage: python add_post.py 'Title' 'Content' ['Link'] ['Image'] ['Epigraph']")
        sys.exit(1)
    title = sys.argv[1]
    content = sys.argv[2]
    link = sys.argv[3] if len(sys.argv) > 3 else None
    image = sys.argv[4] if len(sys.argv) > 4 else None
    epigraph = sys.argv[5] if len(sys.argv) > 5 else None
    post_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)
    save_post(post_id, title, content, link, image, epigraph, timestamp)
    posts = load_posts()
    generate_index(posts)
    print(f"Post '{title}' added and site updated. ID: {post_id}")


if __name__ == '__main__':
    main()
