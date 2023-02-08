.PHONY: clean default pull-latest-simple-css

default:
	./build-site.el

clean:
	rm -rf public

# A minimalist "classless css framework".
# See also https://simplecss.org/
pull-latest-simple-css:
	curl https://raw.githubusercontent.com/kevquirk/simple.css/main/simple.css -o ./src/css/simple.css
