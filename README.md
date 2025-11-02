# Dusty Print Books Micro Blog

This is a static micro blogging site generator styled with tufte.css. You can create posts from the command line and publish them to the top of the site. Posts support images, links, epigraphs (quotes), and sidenotes.

## Getting Started

1. **Clone the repository** and enter the project directory.
2. **Set up the Python environment:**
	```sh
	make setup
	```
	This creates a virtual environment and installs dependencies.

## Creating a Post

Use the Makefile to add a post:

```sh
make add-post TITLE="Your Post Title" CONTENT="Your post content" LINK="https://example.com" IMAGE="https://example.com/image.jpg" EPIGRAPH="A quote --Source"
```

- `TITLE` (required): The title of your post.
- `CONTENT` (required): The main content. You can use markdown formatting.
- `LINK` (optional): A link related to the post.
- `IMAGE` (optional): An image URL or local path. Shown after the title.
- `EPIGRAPH` (optional): A quote, optionally with a source (separate with `--`). Shown after the title if no image is provided.

### Sidenotes

You can add sidenotes using markdown footnote syntax in your content:

```
This is some text.^[This is a sidenote.]
```

Each sidenote will appear in the margin with a margin toggle (⊕) per tufte.css.

## How It Works

- Posts are saved as markdown files in the `posts/` directory, with metadata in YAML front matter.
- The Python script (`add_post.py`) generates `index.html` with tufte.css styling, placing the newest post at the top.
- Images are wrapped in `<figure>`, epigraphs are styled as blockquotes, and sidenotes use tufte.css margin toggles.

## Example

```sh
make add-post TITLE="The Big Lebowski" CONTENT="I'll take a white russian." EPIGRAPH="The dude abides --the dude."
```

## Advanced

- You can use markdown formatting in your post content.
- Multiple posts per day are supported; posts are ordered by timestamp.

## Customization

- To change styling, edit `tufte.css` or add your own CSS.
- To add more features, modify `add_post.py`.

## License

MIT
# dustyprintbooks

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)