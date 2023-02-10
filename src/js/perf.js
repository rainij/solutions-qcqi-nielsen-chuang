const t_start = performance.mark('start').duration;
console.log(`[perf] Start: ${t_start}ms`);

window.onload = () => {
  const t = performance.measure('window_onload', 'start').duration;
  console.log(`[perf] Page complete: ${t}ms.`);
}

document.fonts.onloadingdone = () => {
  const t = performance.measure('fonts_loaded', 'start').duration;
  console.log(`[perf] Fonts loaded: ${t}ms.`);
}
