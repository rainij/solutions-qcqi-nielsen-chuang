#!/usr/bin/env -S emacs --funcall rs/publish --script

;; Set the package installation directory so that packages aren't stored in the
;; ~/.emacs.d/elpa path.
(require 'package)
(setq package-user-dir (expand-file-name "./.packages")
      package-archive-priorities '(("gnu" . 30) ("nongnu" . 20) ("melpa" . 10)))

(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)

;; Load packages but do not activate them:
(package-initialize nil)
;; This *seems* to be not needed on emacs-29:
(unless package-archive-contents
  (package-refresh-contents))

;; Install use-package if necessary (builtin in emacs-29)
(unless (package-installed-p 'use-package)
  (package-install 'use-package))
(require 'use-package)

;; Activate dependencies, ensure installation if necessary
(setq use-package-verbose t)
(use-package esxml :ensure) ; use s-expressions to write xml (or html)
(use-package htmlize :ensure)
(use-package sage-shell-mode :ensure)
(use-package ob-sagemath :ensure)
(use-package org
  :config
  (org-babel-do-load-languages
   'org-babel-load-languages
   '((emacs-lisp . t)
     (python . t)
     (sagemath . t))))
(use-package ox-publish)


(message "Using org-mode version: %s" org-version)


(setq org-cite-global-bibliography (list (expand-file-name "./src/bibliography.bib"))
      org-html-html5-fancy t
      org-html-htmlize-output-type 'css ; use classes for syntax highlighting of code blocks
      ;; Otherwise we get tons of "Can’t guess python-indent-offset, using defaults: 4":
      python-indent-guess-indent-offset-verbose nil)


(defun rs/site-footer (info)
  (let ((creator (plist-get info :creator)))
    `(footer ((class . "footer"))
             (p nil
                "Made by " (a ((href . "https://github.com/rainij")) "Reinhard Stahn")
                " with " (raw-string ,creator))
             (p nil
                "Find the source code on " ;; TODO: set link, once repo is on github
                (a ((href . "https://github.com/rainij/solutions-qcqi-nielsen-chuang")) "Github")))))

(defun rs/nav (info)
  `(nav nil (a ((href . "index.html")) "HOME")))

;; This is our custom html template (written as s-expression):
(defun rs/org-html-template (contents info)
  (let ((title (org-export-data (and (plist-get info :with-title) (plist-get info :title)) info))
        (mathjax (plist-get info :rs/mathjax)))
    (concat
     "<!DOCTYPE html>"
     (esxml-to-xml
      `(html ((lang . "en"))
             (head nil
                   (meta ((charset . "utf-8")))
                   (meta ((name . "viewport") (content . "width=device-width, initial-scale=1.0")))
                   (meta ((name . "author") (content . "Reinhard Stahn")))
                   (title nil ,title)
                   (link ((rel . "icon") (type . "image/x-icon") (sizes . "any")
                          (href . "./favicon/favicon.ico")))
                   (raw-string "<!-- https://simplecss.org - License: MIT - We are using ./simple.css from commit dcb3545f2304356985c99acce9471ba3f559976b from https://github.com/kevquirk/simple.css -->")
                   (link ((rel . "stylesheet") (href . "./css/simple.css")))
                   (link ((rel . "stylesheet") (href . "./css/style.css")))
                   (script ((src . "./js/perf.js")) "")
                   (script ((src . "./js/mathjax.js")) "")
                   (script ((async . "")
                            (src . ,(plist-get mathjax :url))
                            (integrity . ,(plist-get mathjax :integrity))
                            (crossorigin . "anonymous"))
                           ""))
             (body nil
                   ,(rs/nav info)
                   (h1 ((class . "title")) ,title)
                   (raw-string ,contents)
                   ,(rs/site-footer info)))))))

(setq rs/default-publish-params
      (list
       :recursive t
       :base-directory "./src"
       :publishing-directory "./public"))


(org-export-define-derived-backend 'rs/pages-html 'html
  :translate-alist
  '((template . rs/org-html-template)))

;; Override this function with our own backend
(defun org-html-publish-to-html (plist filename pub-dir)
  (org-publish-org-to 'rs/pages-html filename ".html" plist pub-dir))


(setq org-publish-project-alist
    `(("pages"
       ,@rs/default-publish-params
       :rs/mathjax ,(list
                     :url "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"
                     :integrity "sha384-Wuix6BuhrWbjDBs24bXrjf4ZQ5aFeFWBuKkFekO2t8xFU0iNaLQfp2K6/1Nxveei")
       :base-extension "org"
       :exclude "inc/.*\.org$"  ; org files to be included in other org files
       :publishing-function org-html-publish-to-html
       :headline-levels 6
       :section-numbers nil
       :time-stamp-file t
       :with-inlinetasks nil
       :with-toc nil) ; `nil' enables us to place the toc where we want it to be
      ("static"
       ,@rs/default-publish-params
       :base-extension "css\\|js\\|svg\\|png\\|ico\\|txt\\|tar.gz"
       :publishing-function org-publish-attachment)
      ("all" :components ("pages" "static"))))


;; Wrapping the publishing action in a function to be able to load the file into emacs.
(defun rs/publish ()
  (interactive)
  (org-publish-all t)
  (message "DONE"))
