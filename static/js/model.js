// ============================================================
//  PakTax AI — model.js
// ============================================================

const chatArea   = document.getElementById("chatArea");
const messages   = document.getElementById("messages");
const userInput  = document.getElementById("userInput");
const sendBtn    = document.getElementById("sendBtn");
const welcomeBlock = document.getElementById("welcomeBlock");
const menuBtn    = document.getElementById("menuBtn");
const sidebar    = document.querySelector(".sidebar");

// ── Sidebar Toggle (Mobile) ──────────────────────────────
menuBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
});

document.addEventListener("click", (e) => {
  if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
    sidebar.classList.remove("open");
  }
});

// ── Auto-resize Textarea ─────────────────────────────────
userInput.addEventListener("input", () => {
  userInput.style.height = "auto";
  userInput.style.height = Math.min(userInput.scrollHeight, 140) + "px";
});

// ── Enter to Send (Shift+Enter for newline) ──────────────
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ── Quick Chip Click ─────────────────────────────────────
function sendChip(btn) {
  userInput.value = btn.textContent;
  sendMessage();
}

// ── Hide Welcome, Show Messages ───────────────────────────
function showChat() {
  if (welcomeBlock && welcomeBlock.style.display !== "none") {
    welcomeBlock.style.opacity = "0";
    welcomeBlock.style.transition = "opacity 0.3s";
    setTimeout(() => {
      welcomeBlock.style.display = "none";
    }, 300);
  }
}

// ── Append Message Bubble ─────────────────────────────────
function appendMessage(role, text) {
  showChat();

  const msg = document.createElement("div");
  msg.classList.add("msg", role);

  const avatar = document.createElement("div");
  avatar.classList.add("msg-avatar");
  avatar.textContent = role === "ai" ? "PT" : "👤";

  const bubble = document.createElement("div");
  bubble.classList.add("msg-bubble");

  if (role === "ai") {
    bubble.innerHTML = formatText(text);
  } else {
    bubble.textContent = text;
  }

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  messages.appendChild(msg);

  scrollToBottom();
  return bubble;
}

// ── Typing Indicator ──────────────────────────────────────
function showTyping() {
  showChat();

  const msg = document.createElement("div");
  msg.classList.add("msg", "ai");
  msg.id = "typingMsg";

  const avatar = document.createElement("div");
  avatar.classList.add("msg-avatar");
  avatar.textContent = "PT";

  const bubble = document.createElement("div");
  bubble.classList.add("msg-bubble");
  bubble.innerHTML = `
    <div class="typing">
      <span></span><span></span><span></span>
    </div>`;

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  messages.appendChild(msg);
  scrollToBottom();
}

function removeTyping() {
  const t = document.getElementById("typingMsg");
  if (t) t.remove();
}

// ── Format AI Response (Markdown-like) ───────────────────
function formatText(text) {
  // Convert markdown table to HTML table
  text = convertTable(text);

  // Bold **text**
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Newlines to <br>
  text = text.replace(/\n/g, "<br>");

  return text;
}

function convertTable(text) {
  const lines = text.split("\n");
  let result = [];
  let inTable = false;
  let tableHTML = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    if (line.startsWith("|") && line.endsWith("|")) {
      if (!inTable) {
        inTable = true;
        tableHTML = '<table>';
      }

      // Skip separator row (|---|---|)
      if (line.replace(/[\|\-\s]/g, "") === "") continue;

      const cells = line.split("|").filter(c => c.trim() !== "");
      const isHeader = i === lines.findIndex(l => l.trim().startsWith("|") && l.trim().endsWith("|"));

      if (isHeader && tableHTML === '<table>') {
        tableHTML += "<thead><tr>";
        cells.forEach(c => tableHTML += `<th>${c.trim()}</th>`);
        tableHTML += "</tr></thead><tbody>";
      } else {
        tableHTML += "<tr>";
        cells.forEach(c => tableHTML += `<td>${c.trim()}</td>`);
        tableHTML += "</tr>";
      }
    } else {
      if (inTable) {
        tableHTML += "</tbody></table>";
        result.push(tableHTML);
        tableHTML = "";
        inTable = false;
      }
      result.push(line);
    }
  }

  if (inTable) {
    tableHTML += "</tbody></table>";
    result.push(tableHTML);
  }

  return result.join("\n");
}

// ── Scroll to Bottom ──────────────────────────────────────
function scrollToBottom() {
  chatArea.scrollTo({ top: chatArea.scrollHeight, behavior: "smooth" });
}

// ── Main Send Function ────────────────────────────────────
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  // Clear input
  userInput.value = "";
  userInput.style.height = "auto";

  // Disable send button
  sendBtn.disabled = true;

  // Show user message
  appendMessage("user", text);

  // Show typing
  showTyping();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    removeTyping();

    if (data.answer) {
      appendMessage("ai", data.answer);
    } else if (data.error) {
      appendMessage("ai", `⚠️ Error: ${data.error}`);
    }

  } catch (err) {
    removeTyping();
    appendMessage("ai", "⚠️ Could not connect to PakTax AI server. Please try again.");
  }

  sendBtn.disabled = false;
  userInput.focus();
}