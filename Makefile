.PHONY: clean default pull-latest-simple-css tangle test website

default: website

website:
	./bin/build-site.el

tangle: $(addsuffix .py,$(basename $(wildcard src/chapter_*.org))) \
  src/utils.py

test:
	python -m pytest -v test/

clean:
	rm -rf public
	rm -f src/chapter_*.py src/utils.py

# A minimalist "classless css framework".
# See also https://simplecss.org/
pull-latest-simple-css:
	curl https://raw.githubusercontent.com/kevquirk/simple.css/main/simple.css -o ./src/css/simple.css

src/%.py: src/%.org
	emacs --batch --script ./bin/build-site.el --eval "(org-babel-tangle-file \"$<\" \"$@\")"
