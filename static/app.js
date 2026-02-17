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

const missionsContainer = document.getElementById("missionsContainer");
const resetBtn = document.getElementById("resetBtn");

let currentTextId = null;
let currentMissionId = null;
let allMissions = [];
let nextAvailableMissionId = null;

/* =====================
   CARREGAR MAPA DE MISSÕES
===================== */
async function loadMissionsMap() {
    const response = await fetch(`${API_BASE}/missions`);
    const data = await response.json();
    allMissions = data.missions;
    nextAvailableMissionId = null;

    missionsContainer.innerHTML = "";

    allMissions.forEach((mission, index) => {
        const div = document.createElement("div");
        div.className = "mission-node-tooltip";

        let statusClass = "pending";
        let icon = "🔒";

        if (mission.status === "completed") {
            statusClass = "completed";
            icon = "✓";
            
            // A próxima missão após uma completada fica disponível
            if (index + 1 < allMissions.length && !nextAvailableMissionId) {
                nextAvailableMissionId = allMissions[index + 1].id;
            }
        } else if (mission.status === "pending") {
            // Missão atual ou próxima disponível
            if (mission.id === currentMissionId) {
                statusClass = "active";
                icon = "→";
            } else if (mission.id === nextAvailableMissionId) {
                statusClass = "active";
                icon = "→";
            } else {
                statusClass = "locked";
                icon = "🔒";
            }
        }

        div.innerHTML = `
            <div class="mission-node ${statusClass}" data-mission-id="${mission.id}">
                ${icon}
            </div>
            <span class="tooltip-text">${mission.title}</span>
        `;

        div.querySelector(".mission-node").onclick = () => selectMission(mission.id);
        missionsContainer.appendChild(div);
    });
}

/* =====================
   SELECIONAR MISSÃO
===================== */
async function selectMission(missionId) {
    const mission = allMissions.find(m => m.id === missionId);

    // Só permite acessar se for a missão ativa ou já concluída
    if (mission.status === "locked") {
        alert("Complete a missão anterior primeiro!");
        return;
    }

    // Se é uma missão anterior concluída, carrega apenas para visualização
    if (mission.status === "completed" && mission.id !== currentMissionId) {
        viewCompletedMission(missionId);
        return;
    }

    // Carrega a missão atual
    loadMissionById(missionId);
}

/* =====================
   CARREGAR MISSÃO ESPECÍFICA
===================== */
async function loadMissionById(missionId) {
    const response = await fetch(`${API_BASE}/text/${missionId}`);
    const text = await response.json();

    currentTextId = text.id;
    titleEl.textContent = text.title;

    // Obtém o preview (primeiros 120 caracteres)
    const preview = text.content.substring(0, 120) + (text.content.length > 120 ? "..." : "");
    previewEl.textContent = preview;

    // Atualiza UI
    readingCard.classList.add("hidden");
    missionCard.classList.remove("hidden");
}

/* =====================
   VISUALIZAR MISSÃO JÁ CONCLUÍDA
===================== */
async function viewCompletedMission(missionId) {
    const response = await fetch(`${API_BASE}/text/${missionId}`);
    const text = await response.json();

    readingTitle.textContent = `${text.title} (Concluída ✓)`;
    contentEl.textContent = text.content;

    missionCard.classList.add("hidden");
    readingCard.classList.remove("hidden");
}

/* =====================
   CARREGAR MISSÃO DIÁRIA
===================== */
async function loadMission() {
    const response = await fetch(`${API_BASE}/mission/daily`);
    const data = await response.json();

    streakEl.textContent = `🔥 Streak: ${data.streak}`;
    titleEl.textContent = data.mission.text.title;
    previewEl.textContent = data.mission.text.preview;

    currentTextId = data.mission.text.id;
    currentMissionId = data.mission.text.id;
    
    await loadMissionsMap();
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
    
    // Recarrega tudo para atualizar o estado
    await loadMission();
};

/* =====================
   RESET PARA TESTES
===================== */
resetBtn.onclick = async () => {
    if (!confirm("Tem certeza? Isso vai resetar o progresso do dia para testes.")) {
        return;
    }

    const response = await fetch(`${API_BASE}/reset`, {
        method: 'POST'
    });
    const data = await response.json();

    if (data.success) {
        alert("✓ Progresso resetado! Página será recarregada...");
        location.reload();
    }
};

/* =====================
   INIT
===================== */
loadMission();

