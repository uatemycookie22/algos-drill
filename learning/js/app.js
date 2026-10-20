(() => {
const { curriculum, quickselectQuiz } = window.AlgoDrillLessons;
const { QuickselectVisualizer } = window.AlgoDrillQuickselect;

const byId = (id) => document.getElementById(id);

function renderCurriculum() {
  const root = byId("curriculum");
  const fragment = document.createDocumentFragment();

  curriculum.forEach((group) => {
    const section = document.createElement("section");
    section.className = "curriculum-group";

    const title = document.createElement("h2");
    title.className = "curriculum-group-title";
    title.textContent = group.title;
    section.append(title);

    group.lessons.forEach((lesson) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `lesson-link ${lesson.status}`;
      if (lesson.id === "quickselect") button.classList.add("active");

      const label = document.createElement("span");
      label.textContent = lesson.title;
      const status = document.createElement("span");
      status.className = "lesson-status";
      status.textContent = lesson.status === "ready" ? "Open" : "Soon";

      button.append(label, status);
      if (lesson.status === "ready") {
        button.addEventListener("click", () => {
          window.scrollTo({ top: 0, behavior: "smooth" });
          closeSidebar();
        });
      } else {
        button.addEventListener("click", () =>
          showToast(`${lesson.title} is mapped into the curriculum and ready for a future lesson.`),
        );
      }
      section.append(button);
    });

    fragment.append(section);
  });

  root.replaceChildren(fragment);
}

function renderQuiz() {
  const grid = byId("quiz-grid");
  grid.replaceChildren(
    ...quickselectQuiz.map((question, questionIndex) => {
      const card = document.createElement("article");
      card.className = "quiz-card";

      const number = document.createElement("span");
      number.className = "quiz-number";
      number.textContent = `Question ${questionIndex + 1}`;

      const heading = document.createElement("h4");
      heading.textContent = question.question;

      const options = document.createElement("div");
      options.className = "quiz-options";

      const feedback = document.createElement("p");
      feedback.className = "quiz-feedback";
      feedback.textContent = "Choose one answer.";

      question.options.forEach((option, optionIndex) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "quiz-option";
        button.textContent = option;
        button.addEventListener("click", () => {
          options.querySelectorAll("button").forEach((candidate, candidateIndex) => {
            candidate.disabled = true;
            if (candidateIndex === question.answer) candidate.classList.add("correct");
          });
          if (optionIndex !== question.answer) button.classList.add("incorrect");
          feedback.textContent = question.explanation;
        });
        options.append(button);
      });

      card.append(number, heading, options, feedback);
      return card;
    }),
  );
}

function setupCodeExplorer() {
  const notes = [...document.querySelectorAll(".code-note")];
  const lines = [...document.querySelectorAll("#code-block [data-line]")];

  notes.forEach((note) => {
    note.addEventListener("click", () => {
      notes.forEach((candidate) => candidate.classList.remove("active"));
      note.classList.add("active");

      const [start, end = start] = note.dataset.lines.split("-").map(Number);
      lines.forEach((line) => {
        const lineNumber = Number(line.dataset.line);
        line.classList.toggle("highlighted", lineNumber >= start && lineNumber <= end);
      });
    });
  });

  notes[0].click();

  byId("reveal-code-button").addEventListener("click", (event) => {
    const cover = byId("code-cover");
    const isHidden = cover.classList.toggle("hidden");
    event.currentTarget.textContent = isHidden ? "Hide implementation" : "Reveal implementation";
  });
}

function setupNavigation() {
  const sidebar = byId("sidebar");
  const menuButton = byId("menu-button");

  menuButton.addEventListener("click", () => {
    const isOpen = sidebar.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });

  document.addEventListener("click", (event) => {
    if (
      window.innerWidth <= 760 &&
      sidebar.classList.contains("open") &&
      !sidebar.contains(event.target) &&
      !menuButton.contains(event.target)
    ) {
      closeSidebar();
    }
  });
}

function closeSidebar() {
  byId("sidebar").classList.remove("open");
  byId("menu-button").setAttribute("aria-expanded", "false");
}

let toastTimer;
function showToast(message) {
  const toast = byId("toast");
  toast.textContent = message;
  toast.classList.add("visible");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("visible"), 2600);
}

function setupCopyCommand() {
  byId("copy-command").addEventListener("click", async () => {
    const command = "python3 -m pytest -k quickselect";
    try {
      await navigator.clipboard.writeText(command);
      showToast("Test command copied.");
    } catch {
      showToast(command);
    }
  });
}

renderCurriculum();
renderQuiz();
setupCodeExplorer();
setupNavigation();
setupCopyCommand();

new QuickselectVisualizer({
  arrayInput: byId("array-input"),
  kInput: byId("k-input"),
  buildButton: byId("build-button"),
  restartButton: byId("restart-button"),
  previousButton: byId("previous-button"),
  nextButton: byId("next-button"),
  playButton: byId("play-button"),
  playIcon: byId("play-icon"),
  playLabel: byId("play-label"),
  inputError: byId("input-error"),
  variableGrid: byId("variable-grid"),
  arrayStage: byId("array-stage"),
  stepCount: byId("step-count"),
  progressFill: byId("progress-fill"),
  stepKind: byId("step-kind"),
  stepMessage: byId("step-message"),
});
})();
