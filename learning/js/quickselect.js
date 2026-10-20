(() => {
function snapshot(array, state) {
  return {
    array: [...array],
    lo: state.lo,
    hi: state.hi,
    target: state.target,
    pivotIndex: state.pivotIndex ?? null,
    pivotValue: state.pivotValue ?? null,
    i: state.i ?? null,
    j: state.j ?? null,
    p: state.p ?? null,
    found: state.found ?? false,
    kind: state.kind,
    message: state.message,
  };
}

function buildQuickselectTrace(values, k) {
  const array = [...values];
  const target = k - 1;
  const steps = [];
  let lo = 0;
  let hi = array.length - 1;

  steps.push(
    snapshot(array, {
      lo,
      hi,
      target,
      kind: "Start",
      message: `We want the ${ordinal(k)} smallest value, so our target array index is k - 1 = ${target}.`,
    }),
  );

  while (lo <= hi) {
    const pivotValue = array[hi];
    let i = lo;

    steps.push(
      snapshot(array, {
        lo,
        hi,
        target,
        pivotIndex: hi,
        pivotValue,
        i,
        kind: "Choose pivot",
        message: `Use the last active value, ${pivotValue}, as the pivot. Boundary i starts at ${i}.`,
      }),
    );

    for (let j = lo; j < hi; j += 1) {
      steps.push(
        snapshot(array, {
          lo,
          hi,
          target,
          pivotIndex: hi,
          pivotValue,
          i,
          j,
          kind: "Compare",
          message:
            array[j] < pivotValue
              ? `${array[j]} < ${pivotValue}, so it belongs in the smaller-than-pivot region.`
              : `${array[j]} is not smaller than ${pivotValue}, so leave it on the right side of boundary i.`,
        }),
      );

      if (array[j] < pivotValue) {
        const leftValue = array[i];
        const scanValue = array[j];
        [array[i], array[j]] = [array[j], array[i]];

        steps.push(
          snapshot(array, {
            lo,
            hi,
            target,
            pivotIndex: hi,
            pivotValue,
            i,
            j,
            kind: i === j ? "Keep" : "Swap",
            message:
              i === j
                ? `${scanValue} is already at boundary i. Grow the smaller region by moving i right.`
                : `Swap ${scanValue} with ${leftValue}. Everything before the next i is now smaller than the pivot.`,
          }),
        );
        i += 1;
      }
    }

    const displaced = array[i];
    [array[i], array[hi]] = [array[hi], array[i]];
    const p = i;

    steps.push(
      snapshot(array, {
        lo,
        hi,
        target,
        pivotIndex: p,
        pivotValue,
        i: p,
        p,
        kind: "Place pivot",
        message:
          p === hi
            ? `The pivot ${pivotValue} already belongs at index ${p}. Its final sorted position is now known.`
            : `Swap the pivot ${pivotValue} with ${displaced}. The pivot's final sorted index is p = ${p}.`,
      }),
    );

    if (p === target) {
      steps.push(
        snapshot(array, {
          lo,
          hi,
          target,
          pivotIndex: p,
          pivotValue,
          p,
          found: true,
          kind: "Found",
          message: `p equals target (${target}). The ${ordinal(k)} smallest value is ${array[p]}.`,
        }),
      );
      break;
    }

    if (p < target) {
      const oldLo = lo;
      lo = p + 1;
      steps.push(
        snapshot(array, {
          lo,
          hi,
          target,
          p,
          kind: "Search right",
          message: `p = ${p} is left of target = ${target}. Discard indices ${oldLo} through ${p}; continue from ${lo}.`,
        }),
      );
    } else {
      const oldHi = hi;
      hi = p - 1;
      steps.push(
        snapshot(array, {
          lo,
          hi,
          target,
          p,
          kind: "Search left",
          message: `p = ${p} is right of target = ${target}. Discard indices ${p} through ${oldHi}; continue through ${hi}.`,
        }),
      );
    }
  }

  return steps;
}

function ordinal(value) {
  const remainder100 = value % 100;
  if (remainder100 >= 11 && remainder100 <= 13) return `${value}th`;
  if (value % 10 === 1) return `${value}st`;
  if (value % 10 === 2) return `${value}nd`;
  if (value % 10 === 3) return `${value}rd`;
  return `${value}th`;
}

class QuickselectVisualizer {
  constructor(elements) {
    this.elements = elements;
    this.steps = [];
    this.index = 0;
    this.timer = null;
    this.bindEvents();
    this.buildFromInputs();
  }

  bindEvents() {
    const {
      buildButton,
      restartButton,
      previousButton,
      nextButton,
      playButton,
      arrayInput,
      kInput,
    } = this.elements;

    buildButton.addEventListener("click", () => this.buildFromInputs());
    restartButton.addEventListener("click", () => this.goTo(0));
    previousButton.addEventListener("click", () => this.goTo(this.index - 1));
    nextButton.addEventListener("click", () => this.goTo(this.index + 1));
    playButton.addEventListener("click", () => this.togglePlay());

    [arrayInput, kInput].forEach((input) => {
      input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") this.buildFromInputs();
      });
    });
  }

  buildFromInputs() {
    this.stop();
    const parsed = this.parseInputs();
    if (!parsed) return;
    this.steps = buildQuickselectTrace(parsed.values, parsed.k);
    this.index = 0;
    this.elements.inputError.textContent = "";
    this.render();
  }

  parseInputs() {
    const rawValues = this.elements.arrayInput.value
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean);

    if (rawValues.length === 0) {
      this.showError("Enter at least one integer.");
      return null;
    }

    if (rawValues.length > 12) {
      this.showError("Use at most 12 values so the trace stays readable.");
      return null;
    }

    if (rawValues.some((value) => !/^-?\d+$/.test(value))) {
      this.showError("Use comma-separated integers, such as 3, 1, 5, 2, 4.");
      return null;
    }

    const values = rawValues.map(Number);
    const k = Number(this.elements.kInput.value);
    if (!Number.isInteger(k) || k < 1 || k > values.length) {
      this.showError(`k must be an integer from 1 through ${values.length}.`);
      return null;
    }

    return { values, k };
  }

  showError(message) {
    this.elements.inputError.textContent = message;
  }

  goTo(nextIndex) {
    this.stop();
    this.index = Math.max(0, Math.min(nextIndex, this.steps.length - 1));
    this.render();
  }

  togglePlay() {
    if (this.timer) {
      this.stop();
      return;
    }

    if (this.index >= this.steps.length - 1) this.index = 0;
    this.setPlayState(true);
    this.timer = window.setInterval(() => {
      if (this.index >= this.steps.length - 1) {
        this.stop();
        return;
      }
      this.index += 1;
      this.render();
    }, 900);
  }

  stop() {
    if (this.timer) window.clearInterval(this.timer);
    this.timer = null;
    this.setPlayState(false);
  }

  setPlayState(isPlaying) {
    this.elements.playIcon.textContent = isPlaying ? "Ⅱ" : "▶";
    this.elements.playLabel.textContent = isPlaying ? "Pause" : "Play";
  }

  render() {
    const step = this.steps[this.index];
    if (!step) return;

    this.renderArray(step);
    this.renderVariables(step);

    this.elements.stepCount.textContent = `Step ${this.index + 1} of ${this.steps.length}`;
    this.elements.progressFill.style.width = `${
      ((this.index + 1) / this.steps.length) * 100
    }%`;
    this.elements.stepKind.textContent = step.kind;
    this.elements.stepMessage.textContent = step.message;
    this.elements.previousButton.disabled = this.index === 0;
    this.elements.nextButton.disabled = this.index === this.steps.length - 1;
  }

  renderArray(step) {
    const min = Math.min(...step.array);
    const max = Math.max(...step.array);
    const spread = Math.max(1, max - min);

    this.elements.arrayStage.replaceChildren(
      ...step.array.map((value, index) => {
        const item = document.createElement("div");
        item.className = "array-item";
        if (index < step.lo || index > step.hi) item.classList.add("discarded");
        if (index === step.target) item.classList.add("target");
        if (index === step.pivotIndex) item.classList.add("pivot");
        if (index === step.j) item.classList.add("scan");
        if (index === step.i) item.classList.add("boundary");
        if (step.found && index === step.target) item.classList.add("found");

        const bar = document.createElement("div");
        bar.className = "array-bar";
        const normalized = (value - min) / spread;
        bar.style.setProperty("--bar-height", `${68 + normalized * 100}px`);
        bar.textContent = value;

        const indexLabel = document.createElement("div");
        indexLabel.className = "array-index";
        indexLabel.textContent = index;

        item.append(bar, indexLabel);
        if (index === step.j) item.append(this.marker("j", "marker-j"));
        if (index === step.i) item.append(this.marker("i", "marker-i"));
        return item;
      }),
    );
  }

  marker(text, className) {
    const marker = document.createElement("span");
    marker.className = `item-marker ${className}`;
    marker.textContent = text;
    return marker;
  }

  renderVariables(step) {
    const variables = [
      ["lo", step.lo],
      ["hi", step.hi],
      ["target", step.target],
      ["pivot", step.pivotValue ?? "—"],
      ["i", step.i ?? "—"],
      ["j", step.j ?? "—"],
    ];

    this.elements.variableGrid.replaceChildren(
      ...variables.map(([name, value]) => {
        const variable = document.createElement("div");
        variable.className = "variable";
        const label = document.createElement("span");
        label.textContent = name;
        const output = document.createElement("strong");
        output.textContent = value;
        variable.append(label, output);
        return variable;
      }),
    );
  }
}

window.AlgoDrillQuickselect = {
  buildQuickselectTrace,
  QuickselectVisualizer,
};
})();
