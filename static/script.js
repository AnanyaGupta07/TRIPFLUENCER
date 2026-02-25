const form = document.getElementById('tripForm');
const resultEl = document.getElementById('result');
const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');
const printBtn = document.getElementById('printBtn');
const loaderContainer = document.getElementById('loader-container');
const plannerSection = document.getElementById('planner');

const ctaStart = document.getElementById('ctaStart');
if (ctaStart) {
  ctaStart.addEventListener('click', () => {
    const planner = document.getElementById('planner');
    planner?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function markdownToHtml(md) {
  let html = md
    .replace(/^###\s(.+)$/gm, "<h3>$1</h3>")
    .replace(/^##\s(.+)$/gm, "<h2>$1</h2>")
    .replace(/^#\s(.+)$/gm, "<h1>$1</h1>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/_(.+?)_/g, "<em>$1</em>")
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>')
    .replace(/^-\s(.+)$/gm, "<ul><li>$1</li></ul>");
  html = html.replace(/<\/ul>\n<ul>/g, "\n");
  return html;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    source: document.getElementById("source").value.trim(),
    destination: document.getElementById("destination").value.trim(),
    people: document.getElementById("people").value.trim(),
    duration: Math.max(1, parseInt(document.getElementById("duration").value, 10) || 1),
    interests: document.getElementById("interests").value.trim(),
    budget: document.getElementById("budget").value,
    extras: document.getElementById("extras").value.trim()
  };

  if (!data.source || !data.destination) {
    alert("Please fill Source and Destination.");
    return;
  }

  generateBtn.disabled = true;
  generateBtn.textContent = "Generating...";

  plannerSection.style.display = "none";
  loaderContainer.style.display = "flex";
  resultEl.innerHTML = "";

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (!res.ok) {
      let message = `Request failed with status ${res.status}`;
      try {
        const err = await res.json();
        if (err?.detail) {
          message = Array.isArray(err.detail)
            ? err.detail.map((d) => d.msg || d).join(", ")
            : err.detail;
        }
      } catch {}
      throw new Error(message);
    }

    const payload = await res.json();
    const md = payload?.markdown || "";
    if (!md) throw new Error("Empty itinerary received from server.");

    resultEl.innerHTML = markdownToHtml(md);
  } catch (err) {
    const msg = err?.message || "Something went wrong while generating your itinerary.";
    resultEl.innerHTML = `<p style="color:#b91c1c">${escapeHtml(msg)}</p>`;
  } finally {
    plannerSection.style.display = "block";
    loaderContainer.style.display = "none";
    generateBtn.disabled = false;
    generateBtn.textContent = "Generate Itinerary";
  }
});

if (copyBtn) {
  copyBtn.addEventListener("click", async () => {
    const text = resultEl.innerText || "";
    if (!text.trim()) return alert("Nothing to copy.");
    try {
      await navigator.clipboard.writeText(text);
      alert("Copied!");
    } catch {
      alert("Unable to copy.");
    }
  });
}

if (printBtn) {
  printBtn.addEventListener("click", () => window.print());
}
