/* ─── State ──────────────────────────────────────────────────────────────── */
const API_BASE = "";
let sessionId  = null;
let isLoading  = false;

/* ─── DOM refs ───────────────────────────────────────────────────────────── */
const chatWindow     = document.getElementById("chat-window");
const queryInput     = document.getElementById("query-input");
const sendBtn        = document.getElementById("btn-send");
const welcomeCard    = document.getElementById("welcomeCard");
const sidebar        = document.getElementById("sidebar");
const toggleBtn      = document.getElementById("sidebarToggleBtn");
const typingEl       = document.getElementById("typingIndicator");
const chatTitle      = document.querySelector(".chat-title");

/* ─── Sidebar toggle (toggle button always lives in the header) ──────────── */
toggleBtn.addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");
});

/* ─── Markdown-lite renderer ─────────────────────────────────────────────── */
function renderMarkdown(text) {
  if (!text) return "";
  let html = text
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/```([\s\S]*?)```/g, (_, c) => `<pre><code>${c.trim()}</code></pre>`)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^## (.+)$/gm,  "<h2>$1</h2>")
    .replace(/^# (.+)$/gm,   "<h1>$1</h1>")
    .replace(/^---+$/gm, "<hr>")
    .replace(/^[\-\*] (.+)$/gm, "<li>$1</li>")
    .replace(/((<li>.*<\/li>\n?)+)/g, "<ul>$1</ul>")
    .replace(/^\d+\. (.+)$/gm, "<li>$1</li>")
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

  return html.split(/\n{2,}/).map(block => {
    block = block.trim();
    if (!block) return "";
    if (/^<(h[1-6]|ul|ol|pre|hr)/.test(block)) return block;
    return `<p>${block.replace(/\n/g, "<br>")}</p>`;
  }).join("\n");
}

function escapeHtml(str) {
  return String(str ?? "").replace(/[&<>"']/g, c => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
}

/* ─── Tool badge helper ──────────────────────────────────────────────────── */
const TOOL_META = {
  google_search:        { label: "Web Search", cls: "web" },
  search_faq:           { label: "FAQ",         cls: "faq" },
  calculate:            { label: "Calculator",  cls: "calc" },
  get_current_datetime: { label: "Date/Time",   cls: "time" },
};

function buildToolBadges(tools) {
  if (!tools || tools.length === 0) return "";
  const inner = tools.map(t => {
    const m = TOOL_META[t] || { label: escapeHtml(t) };
    return `<span class="tool-badge">${m.label}</span>`;
  }).join("");
  return `<div class="tool-badges">${inner}</div>`;
}

/* ─── Citation cards helper ──────────────────────────────────────────────── */
function buildCitations(citations) {
  if (!citations || citations.length === 0) return "";
  const items = citations.map((c, i) => {
    const host = (() => {
      try { return new URL(c.uri).hostname.replace(/^www\./, ""); }
      catch (_) { return c.uri; }
    })();
    return `
      <a class="citation-card" href="${escapeHtml(c.uri)}" target="_blank" rel="noopener noreferrer">
        <span class="citation-num">${i + 1}</span>
        <span class="citation-text">
          <span class="citation-title">${escapeHtml(c.title || host)}</span>
          <span class="citation-host">${escapeHtml(host)}</span>
        </span>
        <svg class="citation-arrow" width="12" height="12" viewBox="0 0 12 12" fill="none">
          <path d="M2 10L10 2M10 2H4M10 2V8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>`;
  }).join("");
  return `<div class="citations"><div class="citations-label">Sources</div>${items}</div>`;
}

/* ─── Append messages ────────────────────────────────────────────────────── */
function clearWelcome() {
  if (welcomeCard) welcomeCard.style.display = "none";
}

function appendMessage(role, text, tools = [], citations = [], isError = false) {
  clearWelcome();

  const msg    = document.createElement("div");
  msg.className = `msg ${role}${isError ? " error" : ""}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  if (role === "bot" && !isError) {
    bubble.innerHTML =
      renderMarkdown(text) +
      buildToolBadges(tools) +
      buildCitations(citations);
  } else {
    bubble.textContent = text;
  }

  msg.appendChild(bubble);
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

/* ─── Typing indicator ───────────────────────────────────────────────────── */
function showTyping() {
  typingEl.classList.remove("hidden");
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
function hideTyping() {
  typingEl.classList.add("hidden");
}

/* ─── Send message ───────────────────────────────────────────────────────── */
async function sendMessage() {
  const text = queryInput.value.trim();
  if (!text || isLoading) return;

  isLoading = true;
  sendBtn.disabled = true;
  newChatBtn.disabled = true;
  queryInput.value = "";
  autoResize();

  if (!chatTitle.dataset.set) {
    chatTitle.textContent = text.length > 60 ? text.slice(0, 57) + "…" : text;
    chatTitle.dataset.set = "1";
  }
  appendMessage("user", text);
  showTyping();

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Server error" }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    sessionId = data.session_id;

    hideTyping();
    appendMessage("bot", data.reply, data.tools_used || [], data.citations || []);
  } catch (err) {
    hideTyping();
    appendMessage("bot", `Something went wrong: ${err.message}`, [], [], true);
  } finally {
    isLoading = false;
    sendBtn.disabled = false;
    newChatBtn.disabled = false;
    queryInput.focus();
  }
}

/* ─── New chat ───────────────────────────────────────────────────────────── */
async function startNewChat() {
  if (sessionId) {
    try {
      await fetch(`${API_BASE}/chat/clear?session_id=${sessionId}`, { method: "DELETE" });
    } catch (_) {}
    sessionId = null;
  }
  Array.from(chatWindow.children).forEach(el => {
    if (el.id !== "welcomeCard") el.remove();
  });
  welcomeCard.style.display = "";
  chatTitle.textContent = "New conversation";
  delete chatTitle.dataset.set;
  queryInput.value = "";
  autoResize();
  queryInput.focus();
}

/* ─── Auto-resize textarea ───────────────────────────────────────────────── */
function autoResize() {
  queryInput.style.height = "auto";
  queryInput.style.height = Math.min(queryInput.scrollHeight, 160) + "px";
}

/* ─── Event listeners ────────────────────────────────────────────────────── */
sendBtn.addEventListener("click", sendMessage);

queryInput.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

queryInput.addEventListener("input", autoResize);

/* ─── New chat dialog ───────────────────────────────────────────────────── */
// ── New chat (with confirmation) ─────────────────────────────────────────────
const newChatBtn   = document.getElementById("newChatBtn");
const confirmModal = document.getElementById("confirmModal");
const confirmOk    = document.getElementById("confirmOk");
const confirmCancel = document.getElementById("confirmCancel");

function openConfirm()  { confirmModal.hidden = false; confirmOk.focus(); }
function closeConfirm() { confirmModal.hidden = true; newChatBtn.focus(); }

newChatBtn.addEventListener("click", () => {
  // Nothing to lose if no messages have been sent yet
  if (document.querySelector(".msg")) openConfirm();
});
confirmCancel.addEventListener("click", closeConfirm);
confirmModal.addEventListener("click", e => { if (e.target === confirmModal) closeConfirm(); });
document.addEventListener("keydown", e => { if (e.key === "Escape" && !confirmModal.hidden) closeConfirm(); });
confirmOk.addEventListener("click", async () => {
  closeConfirm();
  await startNewChat();
});

// Sample queries load into textbox (never auto-send)
document.querySelectorAll(".suggestion-chip").forEach(btn => {
  btn.addEventListener("click", () => {
    queryInput.value = btn.dataset.msg;
    autoResize();
    queryInput.focus();
  });
});

// Focus input on load
window.addEventListener("DOMContentLoaded", () => queryInput.focus());
