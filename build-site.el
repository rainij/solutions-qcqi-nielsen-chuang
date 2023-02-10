#!/usr/bin/env -S emacs --script

;; Set the package installation directory so that packages aren't stored in the
;; ~/.emacs.d/elpa path.
(require 'package)
(setq package-user-dir (expand-file-name "./.packages")
      package-archive-priorities '(("gnu" . 30) ("nongnu" . 20) ("melpa" . 10)))

(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)

;; Load packages but do not activate them:
(package-initialize nil)

;; Activate dependencies, ensure installation if necessary
(setq use-package-verbose t)
(use-package esxml :ensure) ; use s-expressions to write xml (or html)
(use-package htmlize :ensure)
(use-package org)
(use-package ox-publish)


(message "Using org-mode version: %s" org-version)


(setq org-html-html5-fancy t
      ;;org-html-validation-link nil  ;; TODO
      org-html-head-include-scripts nil
      org-html-head-include-default-style nil
      org-html-head (concat
                     "<link rel=\"stylesheet\" href=\"./css/simple.css\" />\n"
                     "<link rel=\"stylesheet\" href=\"./css/style.css\" />\n")
      org-html-postamble #'rs/site-footer
      org-cite-global-bibliography (list (expand-file-name "./bibliography.bib"))
      ;; Otherwise we get tons of "Can’t guess python-indent-offset, using defaults: 4":
      python-indent-guess-indent-offset-verbose nil)


(defun rs/site-footer (options)
  (let ((creator (plist-get options :creator))
        (foo (plist-get options :foo)))
    (esxml-to-xml ; from esxml
     `(footer ((class . "footer"))
              (p nil
                 "Made by " (a ((href . "https://github.com/rainij")) "Reinhard Stahn")
                 " with " (raw-string ,creator))
              (p nil
                 "Sources on " ;; TODO: set link once repo is on github
                 (a ((href . "https://github.com/rainij"))
                    "Github"))))))

(setq rs/default-publish-params
      (list
       :recursive t
       :base-directory "./src"
       :publishing-directory "./public"))


(setq org-publish-project-alist
    `(("pages"
       ,@rs/default-publish-params
       :base-extension "org"
       :publishing-function org-html-publish-to-html
       :headline-levels 6
       :section-numbers nil
       :time-stamp-file t
       :with-inlinetasks nil
       :with-toc 3)
      ("static"
       ,@rs/default-publish-params
       :base-extension "css\\|svg"
       :publishing-function org-publish-attachment)
      ("all" :components ("pages" "static"))))


(org-publish "all" t)
(message "DONE")
