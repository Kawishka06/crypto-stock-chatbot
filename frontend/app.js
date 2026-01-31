const API_BASE = "http://localhost:8000"; // change to deployed backend later

const chat = document.getElementById("chat");
const msg = document.getElementById("msg");
const send = document.getElementById("send");
const assetEl = document.getElementById("asset");
const horizonEl = document.getElementById("horizon");

let messages = [{ role: "system", content: "You are a market assistant." }];

function addBubble(text, who) {
  const div = document.createElement("div");
  div.className = "bubble " + who;
  div.innerHTML = text.replace(/\n/g, "<br/>");
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function doSend() {
  const text = msg.value.trim();
  if (!text) return;

  addBubble(text, "user");
  messages.push({ role: "user", content: text });
  msg.value = "";

  const payload = {
    messages,
    asset: assetEl.value,
    horizon: parseInt(horizonEl.value, 10),
  };

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) {
    addBubble(`Error: ${data.detail || res.statusText}`, "bot");
    return;
  }

  addBubble(data.reply, "bot");
  messages.push({ role: "assistant", content: data.reply });
}

send.onclick = doSend;
msg.addEventListener("keydown", (e) => {
  if (e.key === "Enter") doSend();
});
