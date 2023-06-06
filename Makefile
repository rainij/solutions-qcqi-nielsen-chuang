.PHONY: clean default pull-latest-simple-css tangle test website html-files

THIS_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

ORG_FILES := $(wildcard src/*.org)

# TODO: use ORG_FILES here:
TANGLED_PYFILES := $(addsuffix .py,$(basename $(wildcard src/chapter_*.org)))
TANGLED_PYFILES += $(addsuffix .py,$(basename $(wildcard src/appendix_*.org)))
TANGLED_PYFILES += src/continued_fractions.py src/utils.py
TANGLED_ZIP := src/tangled.tar.gz

default: website

website: $(TANGLED_ZIP)
	./bin/build-site.el

tangle: $(TANGLED_PYFILES)

tangle-zip: $(TANGLED_ZIP)

test:
	python -m pytest -v test/

clean:
	rm -rf public
	rm -f $(TANGLED_PYFILES) $(TANGLED_ZIP)

# A minimalist "classless css framework".
# See also https://simplecss.org/
pull-latest-simple-css:
	curl https://raw.githubusercontent.com/kevquirk/simple.css/main/simple.css -o ./src/css/simple.css

src/%.py: src/%.org
	emacs --batch --script ./bin/build-site.el --eval "(org-babel-tangle-file \"$<\" \"$@\")"

$(TANGLED_ZIP): $(TANGLED_PYFILES)
	tar -C src/ -czf $@ $(notdir $(TANGLED_PYFILES))

# This is for faster rebuilds of single HTML pages.
# TODO: Why does ordinary publish always recreate everything?
# TODO: Why do I need the absolute path here (THIS_DIR)?
HTML_FILES := $(addprefix public/,$(addsuffix .html,$(basename $(notdir $(ORG_FILES)))))
html-files: $(HTML_FILES)
public/%.html: src/%.org
	emacs --batch --script ./bin/build-site.el --eval "(org-publish-file \"$(THIS_DIR)/$<\")"
