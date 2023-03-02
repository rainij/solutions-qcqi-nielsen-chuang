;; Use `load-file' on this file (once) to set these environment variables. Necessary when
;; working with the pytests. Not nice but works for now!
(setenv "PYTHONPATH"
        (concat (expand-file-name "./src/") path-separator
                (getenv "PYTHONPATH")))
