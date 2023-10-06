.PHONY: clean default pull-latest-simple-css tangle test website html-files

# Specify the files to tangle:
TANGLE_PY := chapter_2 chapter_3 chapter_4 chapter_5 chapter_6
TANGLE_PY += appendix_2
TANGLE_PY += continued_fractions utils
TANGLE_SAGE := chapter_7 chapter_8 chapter_9
TANGLE_SAGE += utils

THIS_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
ORG_FILES := $(wildcard src/*.org)

TANGLED_FILES_PY := $(addprefix src/, $(addsuffix .py,$(TANGLE_PY)))
TANGLED_FILES_SAGE := $(addprefix src/, $(addsuffix .sage,$(TANGLE_SAGE)))
TANGLED_FILES_SAGE_PY := $(addsuffix _sage.py,$(basename $(TANGLED_FILES_SAGE)))
TANGLED_ZIP := src/tangled.tar.gz

default: website

website: $(TANGLED_ZIP)
	./bin/build-site.el

tangle: $(TANGLED_FILES_PY) $(TANGLED_FILES_SAGE)
tangle-full: tangle $(TANGLED_FILES_SAGE_PY)
tangle-zip: $(TANGLED_ZIP)

test: tangle-full
	sage -python -m pytest -v test/

clean:
	rm -rf public
	rm -f $(TANGLED_FILES_PY) $(TANGLED_FILES_SAGE) $(TANGLED_FILES_SAGE_PY) $(TANGLED_ZIP)

# A minimalist "classless css framework".
# See also https://simplecss.org/
pull-latest-simple-css:
	curl https://raw.githubusercontent.com/kevquirk/simple.css/main/simple.css -o ./src/css/simple.css

src/%.py: src/%.org
	emacs --batch --script ./bin/build-site.el --eval "(org-babel-tangle-file \"$<\")"

src/%.sage: src/%.org
	emacs --batch --script ./bin/build-site.el --eval "(org-babel-tangle-file \"$<\")"

src/%_sage.py: src/%.sage
	sage --preparse $<
	mv src/$*.sage.py $@

$(TANGLED_ZIP): $(TANGLED_FILES_PY) $(TANGLED_FILES_SAGE)
	tar -C src/ -czf $@ $(notdir $^)

# This is for faster rebuilds of single HTML pages.
# TODO: Why does ordinary publish always recreate everything?
# TODO: Why do I need the absolute path here (THIS_DIR)?
HTML_FILES := $(addprefix public/,$(addsuffix .html,$(basename $(notdir $(ORG_FILES)))))
html-files: $(HTML_FILES)
public/%.html: src/%.org
	emacs --batch --script ./bin/build-site.el --eval "(org-publish-file \"$(THIS_DIR)/$<\")"
