const siteHeader = document.querySelector(".site-header");
const buildList = document.getElementById("build-list");
const player = document.getElementById("player");
const playerTitle = document.getElementById("player-title");
const playerGeneratedAt = document.getElementById("player-generated-at");
const audioEl = document.getElementById("audio-el");
const playPauseBtn = document.getElementById("play-pause");
const skipBackBtn = document.getElementById("skip-back");
const skipForwardBtn = document.getElementById("skip-forward");
const speedToggleBtn = document.getElementById("speed-toggle");
const timeElapsedEl = document.getElementById("time-elapsed");
const timeTotalEl = document.getElementById("time-total");
const scrubber = document.getElementById("scrubber");
const timelineEl = document.getElementById("timeline");
const backButton = document.getElementById("back-button");
const ecoCountEls = {
  food: document.getElementById("eco-food"),
  wood: document.getElementById("eco-wood"),
  gold: document.getElementById("eco-gold"),
  stone: document.getElementById("eco-stone"),
};

const SKIP_IN_GAME_SECONDS = 5;
const RESOURCE_TYPES = ["food", "wood", "gold", "stone"];
const SPEED_LEVELS = [1, 2, 4];

let speedIndex = 0;

let currentSteps = []; // [{ time, text, audioTime }]
let currentStepEls = [];
let activeIndex = -1;
let isScrubbing = false;
let currentGameSpeed = 1;
let economyCheckpoints = []; // [{ audioTime, food, wood, gold, stone }]
let currentEconomyIndex = -1;
let currentManifest = [];

function formatTime(seconds) {
  if (!isFinite(seconds) || seconds < 0) seconds = 0;
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${String(s).padStart(2, "0")}`;
}

async function loadManifest() {
  const res = await fetch("json/manifest.json");
  currentManifest = await res.json();
  renderBuildList(currentManifest);
}

function formatGeneratedAt(isoString) {
  if (!isoString) return "";
  const date = new Date(isoString);
  return date.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
}

function renderBuildList(manifest) {
  buildList.innerHTML = "";
  for (const build of manifest) {
    const button = document.createElement("button");
    button.className = "build-button";
    button.innerHTML = `<span class="build-title">${build.title}</span><span class="duration">${formatTime(build.duration_in_game_seconds)}</span>`;
    button.addEventListener("click", () => openBuild(build.id));
    buildList.appendChild(button);
  }
}

async function openBuild(id) {
  const res = await fetch(`json/${id}.json`);
  const build = await res.json();

  audioEl.pause();
  playPauseBtn.innerHTML = "&#9658;";
  playPauseBtn.setAttribute("aria-label", "Play");
  setSpeed(0);

  playerTitle.textContent = build.title;
  const manifestEntry = currentManifest.find((b) => b.id === id);
  playerGeneratedAt.textContent = formatGeneratedAt(manifestEntry && manifestEntry.audio_generated_at);
  audioEl.src = `audio/${id}.mp3`;
  audioEl.currentTime = 0;
  currentGameSpeed = build.game_speed;

  currentSteps = build.steps
    .map((step) => ({ ...step, audioTime: step.time / build.game_speed }))
    .sort((a, b) => a.audioTime - b.audioTime);
  activeIndex = -1;

  economyCheckpoints = currentSteps
    .filter((step) => step.economy)
    .map((step) => {
      const checkpoint = { audioTime: step.audioTime };
      for (const type of RESOURCE_TYPES) {
        checkpoint[type] = step.economy[type] || 0;
      }
      return checkpoint;
    });
  currentEconomyIndex = -1;
  setEconomyTally(null);

  renderTimeline();

  siteHeader.hidden = true;
  buildList.hidden = true;
  player.hidden = false;
  window.scrollTo({ top: 0 });
}

function renderTimeline() {
  timelineEl.innerHTML = "";
  currentStepEls = currentSteps.map((step) => {
    const li = document.createElement("li");
    li.className = step.mute ? "timeline-step muted" : "timeline-step";
    li.innerHTML = `<span class="step-time">${formatTime(step.time)}</span><span class="step-text">${step.text}</span>${renderIcons(step.icons)}`;
    li.addEventListener("dblclick", () => {
      audioEl.currentTime = step.audioTime;
      audioEl.play();
    });
    timelineEl.appendChild(li);
    return li;
  });
}

function renderIcons(icons) {
  if (!icons || icons.length === 0) return "";

  const parts = icons.map((tag) => {
    const label = tag.label ? `<span class="resource-label">${tag.label}</span>` : "";
    const icon = `<img class="resource-icon" src="images/${tag.icon}.webp" alt="${tag.icon}">`;
    const inner = tag.label_position === "before" ? label + icon : icon + label;
    return `<span class="resource">${inner}</span>`;
  });

  return `<span class="step-resources">${parts.join('<span class="resource-sep">|</span>')}</span>`;
}

function closeBuild() {
  audioEl.pause();
  audioEl.removeAttribute("src");
  audioEl.load();
  player.hidden = true;
  siteHeader.hidden = false;
  buildList.hidden = false;
}

function updateActiveStep(currentTime) {
  let newIndex = -1;
  for (let i = 0; i < currentSteps.length; i++) {
    if (currentSteps[i].audioTime <= currentTime) {
      newIndex = i;
    } else {
      break;
    }
  }

  if (newIndex === activeIndex) return;
  activeIndex = newIndex;

  currentStepEls.forEach((el, i) => {
    el.classList.toggle("current", i === activeIndex);
    el.classList.toggle("past", i < activeIndex);
  });

  if (activeIndex >= 0) {
    currentStepEls[activeIndex].scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

function setEconomyTally(checkpoint) {
  for (const type of RESOURCE_TYPES) {
    ecoCountEls[type].textContent = checkpoint ? checkpoint[type] : 0;
  }
}

function updateEconomyTally(currentTime) {
  let newIndex = -1;
  for (let i = 0; i < economyCheckpoints.length; i++) {
    if (economyCheckpoints[i].audioTime <= currentTime) {
      newIndex = i;
    } else {
      break;
    }
  }

  if (newIndex === currentEconomyIndex) return;
  currentEconomyIndex = newIndex;
  setEconomyTally(newIndex >= 0 ? economyCheckpoints[newIndex] : null);
}

function setSpeed(index) {
  speedIndex = index;
  const speed = SPEED_LEVELS[speedIndex];
  audioEl.playbackRate = speed;
  speedToggleBtn.textContent = `${speed}x`;
  speedToggleBtn.dataset.speed = String(speed);
}

function togglePlayback() {
  if (audioEl.paused) {
    audioEl.play();
  } else {
    audioEl.pause();
  }
}

playPauseBtn.addEventListener("click", togglePlayback);

document.addEventListener("keydown", (event) => {
  if (event.code !== "Space" || player.hidden) return;
  event.preventDefault();
  togglePlayback();
});

function skipInGameSeconds(seconds) {
  const skipRealSeconds = seconds / currentGameSpeed;
  const duration = isFinite(audioEl.duration) ? audioEl.duration : Infinity;
  audioEl.currentTime = Math.min(Math.max(audioEl.currentTime + skipRealSeconds, 0), duration);
}

skipBackBtn.addEventListener("click", () => skipInGameSeconds(-SKIP_IN_GAME_SECONDS));
skipForwardBtn.addEventListener("click", () => skipInGameSeconds(SKIP_IN_GAME_SECONDS));

speedToggleBtn.addEventListener("click", () => {
  setSpeed((speedIndex + 1) % SPEED_LEVELS.length);
});

audioEl.addEventListener("play", () => {
  playPauseBtn.innerHTML = "&#10074;&#10074;";
  playPauseBtn.setAttribute("aria-label", "Pause");
});

audioEl.addEventListener("pause", () => {
  playPauseBtn.innerHTML = "&#9658;";
  playPauseBtn.setAttribute("aria-label", "Play");
});

audioEl.addEventListener("loadedmetadata", () => {
  scrubber.max = audioEl.duration;
  timeTotalEl.textContent = formatTime(audioEl.duration * currentGameSpeed);
});

audioEl.addEventListener("timeupdate", () => {
  timeElapsedEl.textContent = formatTime(audioEl.currentTime * currentGameSpeed);
  if (!isScrubbing) {
    scrubber.value = audioEl.currentTime;
  }
  updateActiveStep(audioEl.currentTime);
  updateEconomyTally(audioEl.currentTime);
});

scrubber.addEventListener("input", () => {
  isScrubbing = true;
  timeElapsedEl.textContent = formatTime(scrubber.value * currentGameSpeed);
});

scrubber.addEventListener("change", () => {
  audioEl.currentTime = scrubber.value;
  isScrubbing = false;
});

backButton.addEventListener("click", closeBuild);

loadManifest();
