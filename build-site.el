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
    org-html-head-include-scripts t ;; TODO
    org-html-head-include-default-style t ;; TODO
    ;;org-html-head "<link rel=\"stylesheet\" href=\"https://cdn.simplecss.org/simple.min.css\" />"
    ) ;; TODO

(setq python-indent-guess-indent-offset-verbose nil ; otherwise we get tons of "Can’t guess python-indent-offset, using defaults: 4"
   )

(setq org-publish-project-alist
    (list
        (list "org-site:main"
            :recursive t
            :base-directory "./src/"
            :publishing-function 'org-html-publish-to-html
            :publishing-directory "./public"
            :with-author nil
            :with-creator t ;; shows emacs and org version
            :section-numbers nil
            :time-stamp-file t)))

(org-publish-all t)

(message "DONE")
