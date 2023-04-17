.PHONY: clean default pull-latest-simple-css tangle test website

TANGLED_PYFILES := $(addsuffix .py,$(basename $(wildcard src/chapter_*.org)))
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
