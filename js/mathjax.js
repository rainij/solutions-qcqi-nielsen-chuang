MathJax = {
  loader: {
    load: ['[tex]/textmacros']
  },
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    packages: {
      '[+]': ['textmacros']
    },
    tags: 'ams',
  },
  startup: {
    pageReady() {
      return MathJax.startup.defaultPageReady().then(() => {
        const mathjaxStartUpTime = performance.measure('mathjax-pageready', 'start');
        console.log(`[perf] mathjax startup end: ${mathjaxStartUpTime.duration}ms`);
      });
    }
  }
};
