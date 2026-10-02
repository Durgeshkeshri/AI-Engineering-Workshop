const API_BASE = window.location.origin.includes("8001")
  ? window.location.origin
  : "http://localhost:8001";

// ── DOM Elements ─────────────────────────────────────────────────────────────
const chatWindow       = document.getElementById("chat-window");
const welcomeCard      = document.getElementById("welcomeCard");
const queryForm        = document.getElementById("query-form");
const queryInput       = document.getElementById("query-input");
const btnSend          = document.getElementById("btn-send");
const btnIngest        = document.getElementById("btn-ingest");
const docUploadInput   = document.getElementById("docUploadInput");
const btnUploadTrigger = document.getElementById("btnUploadTrigger");
const sourcesPanel     = document.getElementById("sources-panel");
const sourcesList      = document.getElementById("sources-list");
const sourcesListSide  = document.getElementById("sourcesList");
const healthCount      = document.getElementById("healthCount");
const topKSlider       = document.getElementById("topKSlider");
const topKValue        = document.getElementById("topKValue");
const typingIndicator  = document.getElementById("typingIndicator");
const toast            = document.getElementById("toast");

// ── Slider Listener ───────────────────────────────────────────────────────────
if (topKSlider && topKValue) {
  topKSlider.addEventListener("input", (e) => {
    topKValue.textContent = e.target.value;
  });
}

// ── Toast Helper ──────────────────────────────────────────────────────────────
function showToast(message, type = "") {
  toast.textContent = message;
  toast.className = `toast ${type}`;
  toast.hidden = false;
  setTimeout(() => { toast.hidden = true; }, 3500);
}

// ── Fetch Health & Active Document List ──────────────────────────────────────
async function fetchHealthAndSources() {
  try {
    // 1. Fetch Health
    const healthRes = await fetch(`${API_BASE}/api/health`);
    if (healthRes.ok) {
      const hData = await healthRes.json();
      healthCount.textContent = `Online (${hData.chunk_count || 0} chunks indexed)`;
    }

    // 2. Fetch Sources
    const sourcesRes = await fetch(`${API_BASE}/sources`);
    if (sourcesRes.ok) {
      const sData = await sourcesRes.json();
      renderSidebarSources(sData.documents);
    }
  } catch (err) {
    healthCount.textContent = "Offline / Backend error";
    console.error("Health check error:", err);
  }
}

function renderSidebarSources(docs) {
  if (!sourcesListSide) return;
  sourcesListSide.innerHTML = "";

  if (!docs || docs.length === 0) {
    sourcesListSide.innerHTML = '<div class="source-loading">No documents indexed yet.</div>';
    return;
  }

  docs.forEach((doc) => {
    const item = document.createElement("div");
    item.className = "source-item";
    item.innerHTML = `
      <span><span class="doc-icon">📄</span>${doc.filename}</span>
      <span class="doc-badge">${doc.chunk_count} chunks</span>
    `;
    sourcesListSide.appendChild(item);
  });
}

// ── Messages Helpers ──────────────────────────────────────────────────────────
function clearWelcome() {
  if (welcomeCard) welcomeCard.style.display = "none";
}

function appendMessage(role, text, declined = false, sources = []) {
  clearWelcome();
  const msg = document.createElement("div");
  msg.className = `msg ${role}${declined ? " declined" : ""}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "🧑" : "🤖";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  if (sources && sources.length > 0 && !declined) {
    const citationContainer = document.createElement("div");
    citationContainer.className = "citations-badges";
    sources.forEach((s) => {
      const badge = document.createElement("span");
      badge.className = "citation-badge";
      const matchPct = Math.round((1 - s.score) * 100);
      badge.innerHTML = `📄 <strong>${s.source}</strong> (Chunk #${s.chunk_index} · ${matchPct}% match)`;
      citationContainer.appendChild(badge);
    });
    bubble.appendChild(citationContainer);
  }

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return msg;
}

// ── Render Right Drawer Sources ───────────────────────────────────────────────
function renderSources(sources) {
  sourcesList.innerHTML = "";

  if (!sources || sources.length === 0) {
    sourcesPanel.hidden = true;
    return;
  }

  sources.forEach((s) => {
    const li = document.createElement("li");
    li.className = "source-card";
    const scorePct = Math.round((1 - s.score) * 100);
    li.innerHTML = `
      <div class="source-name">${s.source}</div>
      <div class="source-score">Chunk #${s.chunk_index} · match: ${scorePct}% (distance ${s.score})</div>
      <div class="source-excerpt">${s.text}</div>`;
    sourcesList.appendChild(li);
  });

  sourcesPanel.hidden = false;
}

// ── Submit Question Core ─────────────────────────────────────────────────────
async function submitQuestion(questionText) {
  const question = questionText || queryInput.value.trim();
  if (!question) return;

  const topK = parseInt(topKSlider.value, 10) || 3;

  appendMessage("user", question);
  queryInput.value = "";
  btnSend.disabled = true;

  if (typingIndicator) typingIndicator.classList.remove("hidden");

  try {
    const res = await fetch(`${API_BASE}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, top_k: topK }),
    });

    const data = await res.json();
    if (typingIndicator) typingIndicator.classList.add("hidden");

    if (!res.ok) {
      appendMessage("bot", `⚠ Error: ${data.detail || "Something went wrong."}`);
      renderSources([]);
      return;
    }

    appendMessage("bot", data.answer, data.declined, data.sources);
    renderSources(data.declined ? [] : data.sources);

  } catch (err) {
    if (typingIndicator) typingIndicator.classList.add("hidden");
    appendMessage("bot", "⚠ Could not reach backend server.");
    console.error(err);
  } finally {
    btnSend.disabled = false;
    queryInput.focus();
  }
}

// ── Form Submit Event ─────────────────────────────────────────────────────────
queryForm.addEventListener("submit", (e) => {
  e.preventDefault();
  submitQuestion();
});

// ── Sample Query Chips Handler (Populate Input Box) ───────────────────────────
document.querySelectorAll(".suggestion-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    const msg = chip.getAttribute("data-msg");
    if (msg) {
      queryInput.value = msg;
      queryInput.focus();
    }
  });
});

// ── PDF Document Upload Handler ───────────────────────────────────────────────
if (btnUploadTrigger && docUploadInput) {
  btnUploadTrigger.addEventListener("click", () => {
    docUploadInput.click();
  });

  docUploadInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      showToast("Only PDF files (.pdf) are supported.", "error");
      return;
    }

    btnUploadTrigger.disabled = true;
    btnUploadTrigger.textContent = "⏳ Uploading & Indexing…";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        showToast(`Upload failed: ${data.detail}`, "error");
      } else {
        showToast(`✓ ${data.filename} uploaded & indexed! (${data.chunks_stored} total chunks)`, "success");
        fetchHealthAndSources();
      }
    } catch (err) {
      showToast("⚠ Upload error.", "error");
      console.error(err);
    } finally {
      btnUploadTrigger.disabled = false;
      btnUploadTrigger.textContent = "📤 Upload PDF Document";
      docUploadInput.value = "";
    }
  });
}

// ── Ingest / Rebuild Trigger ──────────────────────────────────────────────────
btnIngest.addEventListener("click", async () => {
  btnIngest.disabled = true;
  btnIngest.textContent = "⏳ Rebuilding Index…";

  try {
    const res = await fetch(`${API_BASE}/ingest`, { method: "POST" });
    const data = await res.json();

    if (!res.ok) {
      showToast(`Ingestion failed: ${data.detail}`, "error");
    } else {
      showToast(`✓ ${data.documents_ingested} docs · ${data.chunks_stored} chunks indexed`, "success");
      fetchHealthAndSources();
    }
  } catch (err) {
    showToast("⚠ Backend unreachable.", "error");
    console.error(err);
  } finally {
    btnIngest.disabled = false;
    btnIngest.textContent = "⚙ Rebuild Vector Index";
  }
});

// ── Initial Load ─────────────────────────────────────────────────────────────
fetchHealthAndSources();

// Send initial default greeting message from agent
appendMessage(
  "bot",
  "Hello! 👋 I am the Bharati Vidyapeeth Policy Assistant. Ask me any question about admissions, fee refunds, hostel curfews, library borrowing rules, or examination guidelines!"
);
