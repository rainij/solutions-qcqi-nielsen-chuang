.PHONY: clean default pull-latest-simple-css test

default:
	./build-site.el

test:
	python -m pytest -v test/

clean:
	rm -rf public

# A minimalist "classless css framework".
# See also https://simplecss.org/
pull-latest-simple-css:
	curl https://raw.githubusercontent.com/kevquirk/simple.css/main/simple.css -o ./src/css/simple.css
