
venv:
	python3 -m venv venv

install-deps:
	. venv/bin/activate && pip install --upgrade pip && pip install markdown

setup: venv install-deps

add-post:
	. venv/bin/activate && python add_post.py "$(TITLE)" "$(CONTENT)" "$(LINK)" "$(IMAGE)" "$(EPIGRAPH)"
