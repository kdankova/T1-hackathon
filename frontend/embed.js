(function(){
  if (window.__RAG_PANEL__) return;
  window.__RAG_PANEL__ = true;

  const panel = document.createElement('iframe');
  panel.src = 'http://localhost:8080/embed.html';
  panel.style.cssText = `
    position: fixed; 
    top: 0; 
    right: 0; 
    height: 100vh; 
    width: 420px;
    border: none; 
    z-index: 2147483647; 
    box-shadow: -8px 0 24px rgba(0,0,0,.15);
    transition: transform 0.3s ease;
  `;
  document.body.appendChild(panel);

  let isVisible = true;

  document.addEventListener('keydown', (e) => {
    const isMac = /Mac|iPod|iPhone|iPad/.test(navigator.platform);
    const modKey = isMac ? e.metaKey : e.ctrlKey;
    
    if (modKey && e.shiftKey && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      isVisible = !isVisible;
      panel.style.transform = isVisible ? 'translateX(0)' : 'translateX(100%)';
    }
  });

  const selectedText = window.getSelection().toString();
  if (selectedText && selectedText.length > 0) {
    panel.addEventListener('load', () => {
      panel.contentWindow.postMessage({
        type: 'PREFILL_QUESTION',
        text: selectedText
      }, '*');
    });
  }
})();

