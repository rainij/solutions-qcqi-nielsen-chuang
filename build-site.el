#!/usr/bin/env -S emacs --script

;; Set the package installation directory so that packages aren't stored in the
;; ~/.emacs.d/elpa path.
(require 'package)
(setq package-user-dir (expand-file-name "./.packages"))

;; Load packages but do not activate them.
(package-initialize nil)

;; Activate dependencies, ensure installation if necessary
(setq use-package-verbose t)
(use-package htmlize :ensure)
(use-package org)
(use-package ox-publish)

(message "Using org-mode version: %s" org-version)

(setq org-html-html5-fancy t
    org-html-validation-link t  ;; TODO
    org-html-head-include-scripts nil
    org-html-head-include-default-style nil
    org-html-head (concat
                      "<link rel=\"stylesheet\" href=\"./css/simple.css\" />\n"
                      "<link rel=\"stylesheet\" href=\"./css/style.css\" />\n")
    )

(setq python-indent-guess-indent-offset-verbose nil ; otherwise we get tons of "Can’t guess python-indent-offset, using defaults: 4"
    org-cite-global-bibliography (list (expand-file-name "./bibliography.bib")))

(defun copy-images (props)
    (let ((images (concat (plist-get  props :base-directory) "/images"))
             (pubdir (concat (plist-get  props :publishing-directory) "/")))
        (message "Copy %s to %s" images pubdir)
        (copy-directory images pubdir)))

;; TODO: avoid code duplication
(defun copy-css (props)
    (let ((css (concat (plist-get  props :base-directory) "/css"))
             (pubdir (concat (plist-get  props :publishing-directory) "/")))
        (message "Copy %s to %s" css pubdir)
        (copy-directory css pubdir)))

(setq org-publish-project-alist
    (list
        (list "org-site:main"
            :recursive t
            :base-directory "./src"
            :publishing-function 'org-html-publish-to-html
            :publishing-directory "./public"
            :with-author nil
            :with-creator t ;; shows emacs and org version
            :headline-levels 6
            :section-numbers nil
            :time-stamp-file t
            :completion-function '(copy-images copy-css)
            :with-inlinetasks nil
            :with-toc 3)))

(org-publish-all t)

(message "DONE")
