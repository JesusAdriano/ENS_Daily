const API_BASE = "/api";

const streakEl = document.getElementById("streak");
const titleEl = document.getElementById("title");
const previewEl = document.getElementById("preview");

const readBtn = document.getElementById("readBtn");
const completeBtn = document.getElementById("completeBtn");

const missionCard = document.getElementById("mission");
const readingCard = document.getElementById("reading");

const readingTitle = document.getElementById("readingTitle");
const contentEl = document.getElementById("content");
const backBtn = document.getElementById("backBtn");

let currentTextId = null;

/* =====================
   CARREGAR MISSÃO
===================== */
async function loadMission() {
    const response = await fetch(`${API_BASE}/mission/daily`);
    const data = await response.json();

    streakEl.textContent = `🔥 Streak: ${data.streak}`;
    titleEl.textContent = data.mission.text.title;
    previewEl.textContent = data.mission.text.preview;

    currentTextId = data.mission.text.id;
}

/* =====================
   LER TEXTO COMPLETO
===================== */
readBtn.onclick = async () => {
    const response = await fetch(`${API_BASE}/text/${currentTextId}`);
    const text = await response.json();

    readingTitle.textContent = text.title;
    contentEl.textContent = text.content;

    missionCard.classList.add("hidden");
    readingCard.classList.remove("hidden");
};

/* =====================
   VOLTAR
===================== */
backBtn.onclick = () => {
    readingCard.classList.add("hidden");
    missionCard.classList.remove("hidden");
};

/* =====================
   CONCLUIR MISSÃO
===================== */
completeBtn.onclick = async () => {
    const response = await fetch(`${API_BASE}/mission/daily/complete`);
    const data = await response.json();

    if (!data.success) {
        alert("Missão já concluída hoje.");
        return;
    }

    alert("Missão concluída! 🔥");

    streakEl.textContent = `🔥 Streak: ${data.streak}`;
};

/* =====================
   INIT
===================== */
loadMission();
