# Learning site

The learning site is a dependency-free static app. Open it directly:

```bash
open learning/index.html
```

You can also serve it from the repository root:

```bash
python3 -m http.server 8000 --directory learning
```

Then open `http://localhost:8000`.

## Adding another lesson

1. Add the lesson to the curriculum in `js/lessons.js` and set its status to
   `ready`.
2. Put algorithm-specific trace generation and visualization behavior in its
   own module under `js/`.
3. Add the lesson article to `index.html`, or move lesson markup into a renderer
   when the second lesson is introduced.
4. Initialize its visualizer from `js/app.js`.

Shared navigation, typography, cards, controls, quizzes, and responsive styles
live in `index.html`, `js/app.js`, and `styles.css`.
