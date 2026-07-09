document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) lucide.createIcons();

  const menuToggle = document.getElementById("menuToggle");
  if (menuToggle) {
    menuToggle.addEventListener("click", () => document.body.classList.toggle("sidebar-open"));
  }

  document.querySelectorAll("[data-count]").forEach((el) => {
    const target = Number(el.dataset.count || 0);
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 36));
    const tick = () => {
      current = Math.min(target, current + step);
      el.textContent = current;
      if (current < target) requestAnimationFrame(tick);
    };
    tick();
  });

  const progressChart = document.getElementById("progressChart");
  if (progressChart && window.Chart) {
    const completed = Number(progressChart.dataset.completed || 0);
    const total = Number(progressChart.dataset.total || 1);
    new Chart(progressChart, {
      type: "doughnut",
      data: {
        labels: ["Completed", "Remaining"],
        datasets: [{ data: [completed, Math.max(total - completed, 0)], backgroundColor: ["#20e3b2", "#1f2a44"], borderWidth: 0 }]
      },
      options: { plugins: { legend: { labels: { color: "#d7e7ff" } } }, cutout: "68%" }
    });
  }

  const moduleChart = document.getElementById("moduleChart");
  const moduleScores = document.getElementById("moduleScores");
  if (moduleChart && moduleScores && window.Chart) {
    const labels = JSON.parse(moduleChart.dataset.labels || "[]");
    const scores = JSON.parse(moduleScores.textContent || "{}");
    new Chart(moduleChart, {
      type: "bar",
      data: {
        labels,
        datasets: [{ label: "Completion Score", data: labels.map((label) => scores[label] || 0), backgroundColor: "#35a7ff", borderRadius: 8 }]
      },
      options: {
        scales: {
          x: { ticks: { color: "#a9b8d8" }, grid: { color: "rgba(255,255,255,.06)" } },
          y: { max: 100, ticks: { color: "#a9b8d8" }, grid: { color: "rgba(255,255,255,.06)" } }
        },
        plugins: { legend: { labels: { color: "#d7e7ff" } } }
      }
    });
  }

  const attackChart = document.getElementById("attackChart");
const radarDataElement = document.getElementById("radarData");

if (attackChart && radarDataElement && window.Chart) {

  const radarData = JSON.parse(radarDataElement.textContent || "[]");

  new Chart(attackChart, {
    type: "radar",
    data: {
      labels: ["Passwords", "Phishing", "SQLi", "XSS", "Network", "Malware", "CTF"],
      datasets: [{
        label: "Training Coverage",
        data: radarData,
        fill: true,
        backgroundColor: "rgba(32, 227, 178, .18)",
        borderColor: "#20e3b2",
        pointBackgroundColor: "#35a7ff"
      }]
    },
    options: {
      scales: {
        r: {
          min: 0,
          max: 100,
          angleLines: { color: "rgba(255,255,255,.12)" },
          grid: { color: "rgba(255,255,255,.1)" },
          pointLabels: { color: "#d7e7ff" },
          ticks: { color: "#09111f", backdropColor: "#20e3b2" }
        }
      },
      plugins: {
        legend: {
          labels: { color: "#d7e7ff" }
        }
      }
    }
  });
}

  const timer = document.getElementById("quizTimer");
  if (timer) {
    let seconds = 300;
    setInterval(() => {
      seconds = Math.max(0, seconds - 1);
      const m = String(Math.floor(seconds / 60)).padStart(2, "0");
      const s = String(seconds % 60).padStart(2, "0");
      timer.textContent = `${m}:${s}`;
      if (seconds < 31) timer.classList.add("danger-text");
    }, 1000);
  }
});

