/**
 * Dashboard: loads stats and recent entries via API.
 */
(async function () {
  "use strict";

  const MOOD_COLORS = {
    amazing: "#f4a261",
    happy:   "#52b788",
    neutral: "#adb5bd",
    sad:     "#74b3ce",
    awful:   "#e07a5f",
  };

  async function loadStats() {
    const res = await fetch("/api/stats");
    const stats = await res.json();

    const topMoodEl    = document.getElementById("topMood");
    const topLabelEl   = document.getElementById("topMoodLabel");
    const totalEl      = document.getElementById("totalEntries");
    const chartEmpty   = document.getElementById("chartEmpty");

    const total = stats.reduce((s, r) => s + r.count, 0);
    totalEl.textContent = total;

    if (stats.length === 0) {
      topMoodEl.textContent  = "—";
      topLabelEl.textContent = "no entries yet";
      chartEmpty.style.display = "block";
      return;
    }

    const top = stats[0];
    topMoodEl.textContent  = top.emoji;
    topLabelEl.textContent = `${top.mood} (${top.count}×)`;

    const ctx = document.getElementById("moodChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: stats.map((s) => `${s.emoji} ${s.mood}`),
        datasets: [{
          data:            stats.map((s) => s.count),
          backgroundColor: stats.map((s) => MOOD_COLORS[s.mood] || "#ccc"),
          borderRadius:    8,
          borderSkipped:   false,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1, font: { family: "'DM Sans'" } },
            grid:  { color: "#e8e0d4" },
          },
          x: {
            ticks: { font: { family: "'DM Sans'", size: 13 } },
            grid:  { display: false },
          },
        },
      },
    });
  }

  async function loadRecent() {
    const res      = await fetch("/api/entries");
    const entries  = await res.json();
    const list     = document.getElementById("recentList");

    if (entries.length === 0) {
      list.innerHTML = '<li class="recent-placeholder">No entries yet.</li>';
      return;
    }

    list.innerHTML = entries.slice(0, 5).map((e) => `
      <li class="recent-item">
        <span class="recent-emoji">${e.emoji}</span>
        <div class="recent-meta">
          <div class="recent-mood">${e.mood}</div>
          <div class="recent-time">${formatDate(e.created_at)}</div>
        </div>
      </li>
    `).join("");
  }

  await Promise.all([loadStats(), loadRecent()]);
})();
