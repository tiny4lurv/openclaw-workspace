/**
 * Dusk Chat Widget
 * Paste this snippet in every page footer on navahc.com:
 *   <div id="dusk-chat-widget"></div>
 *   <script src="https://askdusk.tinymanyonga.online/widget.js"></script>
 */

(function () {
  var containerId = 'dusk-chat-widget';
  var widgetHost = 'https://askdusk.tinymanyonga.online';

  // State
  var isOpen = false;
  var isLoading = true;
  var messages = [];
  var ticketId = null;
  var pollInterval = null;
  var name = '';
  var state = 'new'; // new | waiting_for_name | active

  // Create DOM
  var container = document.getElementById(containerId);
  if (!container) return;

  // Inject styles
  var style = document.createElement('style');
  style.textContent = [
    '#dusk-widget-btn {',
    '  position: fixed;',
    '  bottom: 24px;',
    '  right: 24px;',
    '  width: 60px;',
    '  height: 60px;',
    '  border-radius: 50%;',
    '  background: #122A38;',
    '  border: 2px solid #FF9583;',
    '  cursor: pointer;',
    '  z-index: 999998;',
    '  display: flex;',
    '  align-items: center;',
    '  justify-content: center;',
    '  box-shadow: 0 4px 16px rgba(0,0,0,0.3);',
    '  transition: transform 0.2s, background 0.2s;',
    '}',
    '#dusk-widget-btn:hover {',
    '  transform: scale(1.08);',
    '  background: #1a3a4a;',
    '}',
    '#dusk-widget-btn svg {',
    '  width: 28px;',
    '  height: 28px;',
    '  fill: #FF9583;',
    '}',
    '#dusk-widget-panel {',
    '  position: fixed;',
    '  bottom: 96px;',
    '  right: 24px;',
    '  width: 380px;',
    '  height: 560px;',
    '  background: #fff;',
    '  border-radius: 16px;',
    '  box-shadow: 0 8px 40px rgba(0,0,0,0.25);',
    '  z-index: 999999;',
    '  display: none;',
    '  flex-direction: column;',
    '  overflow: hidden;',
    '  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
    '}',
    '#dusk-widget-panel.open {',
    '  display: flex;',
    '}',
    '#dusk-widget-header {',
    '  background: #122A38;',
    '  padding: 16px 20px;',
    '  display: flex;',
    '  align-items: center;',
    '  justify-content: space-between;',
    '}',
    '#dusk-widget-header-title {',
    '  color: #fff;',
    '  font-size: 16px;',
    '  font-weight: 600;',
    '}',
    '#dusk-widget-header-sub {',
    '  color: #FF9583;',
    '  font-size: 12px;',
    '  margin-top: 2px;',
    '}',
    '#dusk-widget-close {',
    '  background: none;',
    '  border: none;',
    '  cursor: pointer;',
    '  padding: 4px;',
    '}',
    '#dusk-widget-close svg {',
    '  width: 20px;',
    '  height: 20px;',
    '  fill: #fff;',
    '  opacity: 0.7;',
    '}',
    '#dusk-widget-close:hover svg {',
    '  opacity: 1;',
    '}',
    '#dusk-widget-body {',
    '  flex: 1;',
    '  overflow-y: auto;',
    '  padding: 16px 20px;',
    '  display: flex;',
    '  flex-direction: column;',
    '  gap: 12px;',
    '}',
    '.dusk-msg {',
    '  max-width: 80%;',
    '  padding: 10px 14px;',
    '  border-radius: 12px;',
    '  font-size: 14px;',
    '  line-height: 1.5;',
    '  white-space: pre-wrap;',
    '  word-break: break-word;',
    '}',
    '.dusk-msg.bot {',
    '  background: #f0f4f7;',
    '  color: #1a1a1a;',
    '  align-self: flex-start;',
    '  border-bottom-left-radius: 4px;',
    '}',
    '.dusk-msg.user {',
    '  background: #122A38;',
    '  color: #fff;',
    '  align-self: flex-end;',
    '  border-bottom-right-radius: 4px;',
    '}',
    '.dusk-msg.typing {',
    '  font-style: italic;',
    '  color: #888;',
    '}',
    '#dusk-widget-footer {',
    '  padding: 12px 16px;',
    '  border-top: 1px solid #eee;',
    '  display: flex;',
    '  gap: 8px;',
    '}',
    '#dusk-widget-input {',
    '  flex: 1;',
    '  padding: 10px 14px;',
    '  border: 1px solid #ddd;',
    '  border-radius: 24px;',
    '  font-size: 14px;',
    '  outline: none;',
    '  font-family: inherit;',
    '}',
    '#dusk-widget-input:focus {',
    '  border-color: #122A38;',
    '}',
    '#dusk-widget-send {',
    '  background: #122A38;',
    '  color: #FF9583;',
    '  border: none;',
    '  border-radius: 50%;',
    '  width: 40px;',
    '  height: 40px;',
    '  cursor: pointer;',
    '  display: flex;',
    '  align-items: center;',
    '  justify-content: center;',
    '  flex-shrink: 0;',
    '}',
    '#dusk-widget-send svg {',
    '  width: 18px;',
    '  height: 18px;',
    '  fill: #FF9583;',
    '}',
    '#dusk-widget-send:hover {',
    '  background: #1a3a4a;',
    '}',
    // Pre-canned buttons
    '#dusk-widget-buttons {',
    '  padding: 8px 16px 12px;',
    '  display: flex;',
    '  flex-direction: column;',
    '  gap: 6px;',
    '  border-top: 1px solid #eee;',
    '}',
    '.dusk-btn {',
    '  background: #f0f4f7;',
    '  border: 1px solid #d0d8e0;',
    '  border-radius: 8px;',
    '  padding: 8px 12px;',
    '  font-size: 13px;',
    '  color: #122A38;',
    '  cursor: pointer;',
    '  text-align: left;',
    '  transition: background 0.15s;',
    '  font-family: inherit;',
    '}',
    '.dusk-btn:hover {',
    '  background: #e4ecf2;',
    '}',
    // Responsive
    '@media (max-width: 480px) {',
    '  #dusk-widget-panel {',
    '    width: calc(100vw - 32px);',
    '    height: calc(100vh - 120px);',
    '    bottom: 88px;',
    '    right: 16px;',
    '    left: 16px;',
    '  }',
    '  #dusk-widget-btn {',
    '    bottom: 20px;',
    '    right: 20px;',
    '  }',
    '}'
  ].join('\n');
  document.head.appendChild(style);

  // Blinking cursor keyframes — injected as separate style to avoid array join complexity
  var cursorStyle = document.createElement('style');
  cursorStyle.textContent = '@keyframes blink { 50% { border-color: transparent; } } .dusk-msg.bot span { display: inline-block; }';
  document.head.appendChild(cursorStyle);

  // Build button
  var btn = document.createElement('button');
  btn.id = 'dusk-widget-btn';
  btn.title = 'Chat with Dusk';
  btn.innerHTML = [
    '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">',
    '<path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>',
    '</svg>'
  ].join('');
  btn.onclick = togglePanel;
  container.appendChild(btn);

  // Build panel
  var panel = document.createElement('div');
  panel.id = 'dusk-widget-panel';
  panel.innerHTML = [
    '<div id="dusk-widget-header">',
    '  <div>',
    '    <div id="dusk-widget-header-title">Ask Dusk</div>',
    '    <div id="dusk-widget-header-sub">Nava Healthcare Recruitment</div>',
    '  </div>',
    '  <button id="dusk-widget-close">',
    '    <svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>',
    '  </button>',
    '</div>',
    '<div id="dusk-widget-body"></div>',
    '<div id="dusk-widget-buttons" style="display:none"></div>',
    '<div id="dusk-widget-footer">',
    '  <input id="dusk-widget-input" type="text" placeholder="Type a message..." autocomplete="off" />',
    '  <button id="dusk-widget-send">',
    '    <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>',
    '  </button>',
    '</div>'
  ].join('');
  container.appendChild(panel);

  // Elements
  var body = document.getElementById('dusk-widget-body');
  var input = document.getElementById('dusk-widget-input');
  var sendBtn = document.getElementById('dusk-widget-send');
  var closeBtn = document.getElementById('dusk-widget-close');
  var buttonsDiv = document.getElementById('dusk-widget-buttons');

  closeBtn.onclick = closePanel;
  sendBtn.onclick = sendMessage;
  input.onkeydown = function (e) {
    if (e.key === 'Enter') sendMessage();
  };

  // Canned button definitions (matches relay CANNED_RESPONSES)
  var cannedButtons = [
    { id: '1', label: 'What does Nava do?' },
    { id: '2', label: 'What problems do you solve?' },
    { id: '3', label: 'Summarise this page' }
  ];

  // Build canned buttons once
  cannedButtons.forEach(function (b) {
    var btn = document.createElement('button');
    btn.className = 'dusk-btn';
    btn.textContent = b.label;
    btn.onclick = (function (id, label) {
      return function () {
        showMessage(label, 'user');
        sendToRelay('BTN:' + id);
      };
    })(b.id, b.label);
    buttonsDiv.appendChild(btn);
  });

  // Panel open/close
  function togglePanel() {
    isOpen = !isOpen;
    panel.classList.toggle('open', isOpen);
    if (isOpen && isLoading) {
      initSession();
    }
    if (isOpen) {
      input.focus();
    }
  }

  function closePanel() {
    isOpen = false;
    panel.classList.remove('open');
  }

  // Messages
  function showMessage(text, who, isHtml) {
    // Remove typing indicator if present
    var typing = body.querySelector('.typing');
    if (typing) typing.remove();

    var div = document.createElement('div');
    div.className = 'dusk-msg ' + who;
    if (isHtml) {
      div.innerHTML = text;
    } else {
      div.textContent = text;
    }
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
    messages.push({ who: who, text: text });
  }


  // Parse basic markdown → HTML
  function parseMarkdown(text) {
    if (!text) return '';
    return text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`(.+?)`/g, '<code>$1</code>')
      .replace(/(https?:\/\/[^\s<>"')]+)/g, '<a href="$1" target="_blank" style="color:#FF9583;text-decoration:underline;">$1</a>')
      .replace(/\n/g, '<br>');
  }

  function showTyping() {
    var existing = body.querySelector('.typing');
    if (existing) return;
    var div = document.createElement('div');
    div.className = 'dusk-msg bot typing';
    div.textContent = 'Dusk is typing...';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }

  function clearTyping() {
    var typing = body.querySelector('.typing');
    if (typing) typing.remove();
  }


  // Typewriter effect for bot messages
  async function streamMessageBot(text) {
    var div = document.createElement('div');
    div.className = 'dusk-msg bot';
    body.appendChild(div);

    var paragraphs = text.split(/\n\n/);
    for (var p = 0; p < paragraphs.length; p++) {
      var para = paragraphs[p];
      var words = para.split(/(\s+)/);
      var currentText = '';

      for (var i = 0; i < words.length; i++) {
        currentText += words[i];
        var fullText = paragraphs.slice(0, p).join('\n\n') + (p > 0 ? '\n\n' : '') + currentText;
        div.innerHTML = parseMarkdown(fullText) + '<span style="border-right:2px solid #FF9583;margin-left:2px;animation:blink 0.8s step-end infinite;"></span>';
        body.scrollTop = body.scrollHeight;

        if (words[i].trim().length > 0) {
          var delay = Math.max(15, Math.min(50, words[i].length * 10));
          await new Promise(function(r) { setTimeout(r, delay); });
        }
      }

      var finalText = paragraphs.slice(0, p + 1).join('\n\n');
      div.innerHTML = parseMarkdown(finalText);
      body.scrollTop = body.scrollHeight;

      if (p < paragraphs.length - 1) {
        var sentenceCount = paragraphs[p].split(/[.!?]+\s+/).filter(function(s) { return s.trim().length > 0; }).length;
        var pause = 2000;
        if (sentenceCount >= 4) pause = 4000;
        else if (sentenceCount >= 3) pause = 3000;
        await new Promise(function(r) { setTimeout(r, pause); });
      }
    }

    messages.push({ who: 'bot', text: text });
  }

  // Send to relay
  function sendToRelay(text) {
    // Hide buttons after first interaction
    buttonsDiv.style.display = 'none';

    clearTyping();
    showTyping();

    var pageText = (document.body.innerText || '').substring(0, 15000);
    var pageUrl = window.location.href;

    var formData = new URLSearchParams();
    formData.append('message', text);
    formData.append('fingerprint', 'widget-' + fingerprint());

    fetch(widgetHost + '/message', {
      method: 'POST',
      headers: {
        'X-Access-Token': 'nava-dusk-2026',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: text,
        fingerprint: 'widget-' + fingerprint(),
        page_url: pageUrl,
        page_text: pageText
      })
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        ticketId = data.ticket;
        state = data.state || state;
        // Show canned/immediate response after 6 second delay
        if (data.immediate_response) {
          (async function() {
            await new Promise(function(r) { setTimeout(r, 6000); });
            clearTyping();
            streamMessageBot(data.immediate_response);
          })();
        }
        // Show canned buttons if returned
        if (data.remaining !== undefined && data.remaining.length > 0) {
          // For now just poll
        }
        pollResponse();
      })
      .catch(function (err) {
        console.error('Widget fetch error:', err);
        clearTyping();
        showMessage('Sorry, I\'m having trouble connecting. Please try again. [' + err.message + ']', 'bot');
      });
  }

  function pollResponse() {
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(function () {
      fetch(widgetHost + '/response?ticket=' + ticketId, {
        headers: {
        'X-Access-Token': 'nava-dusk-2026'
      }
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.response) {
            clearTyping();
            streamMessageBot(data.response);
            clearInterval(pollInterval);
            pollInterval = null;
          } else if (data.pending && data.partial) {
            clearTyping();
            var partialDiv = document.createElement('div');
            partialDiv.className = 'dusk-msg bot';
            partialDiv.innerHTML = parseMarkdown(data.partial) + '<span style="border-right:2px solid #FF9583;margin-left:2px;animation:blink 0.8s step-end infinite;"></span>';
            body.appendChild(partialDiv);
            body.scrollTop = body.scrollHeight;
          }
        })
        .catch(function () {
          clearInterval(pollInterval);
        });
    }, 1000);
  }

  // Send user message
  function sendMessage() {
    var text = input.value.trim();
    if (!text) return;
    input.value = '';
    showMessage(text, 'user');
    sendToRelay(text);
  }

  // Init session with greeting
  function initSession() {
    isLoading = false;
    // Show canned buttons
    buttonsDiv.style.display = 'flex';
    // Initial greeting
    showMessage(
      'Hi! I\'m Dusk — here to help with Nava Healthcare Recruitment.\n\nWhat would you like to know?',
      'bot'
    );
  }

  // Lightweight fingerprint
  function fingerprint() {
    return navigator.userAgent + '-' + (new Date().getTimezoneOffset());
  }

  // Initialise session on first open
  isLoading = true;
})();
