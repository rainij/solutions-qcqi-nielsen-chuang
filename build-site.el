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
       :with-author nil
       :with-creator t ;; shows emacs and org version
       :headline-levels 6
       :section-numbers nil
       :time-stamp-file t
       ;;:completion-function '(copy-images copy-css)
       :with-inlinetasks nil
       :with-toc 3)
      ("static"
       ,@rs/default-publish-params
       :base-extension "css\\|svg"
       :publishing-function org-publish-attachment)
      ("all" :components ("pages" "static"))))

(org-publish "all" t)
(message "DONE")
