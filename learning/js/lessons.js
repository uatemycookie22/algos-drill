(() => {
const curriculum = [
  {
    title: "Searching & selection",
    lessons: [
      { id: "binary-search", title: "Binary search", status: "planned" },
      { id: "bisect", title: "Bisect boundaries", status: "planned" },
      { id: "search-on-answer", title: "Search on answer", status: "planned" },
      { id: "merge", title: "Merge sorted arrays", status: "planned" },
      { id: "quickselect", title: "Quickselect", status: "ready" },
    ],
  },
  {
    title: "Graphs",
    lessons: [
      { id: "adjacency-list", title: "Adjacency lists", status: "planned" },
      { id: "bfs", title: "Breadth-first search", status: "planned" },
      { id: "dfs", title: "Depth-first search", status: "planned" },
      { id: "islands", title: "Grid traversal", status: "planned" },
      { id: "topological-sort", title: "Topological sort", status: "planned" },
      { id: "dijkstra", title: "Dijkstra", status: "planned" },
    ],
  },
  {
    title: "Data structures",
    lessons: [
      { id: "union-find", title: "Union-Find", status: "planned" },
      { id: "min-heap", title: "Min heap", status: "planned" },
      { id: "trie", title: "Trie", status: "planned" },
    ],
  },
  {
    title: "Lists & trees",
    lessons: [
      { id: "linked-list", title: "Linked-list patterns", status: "planned" },
      { id: "tree-traversal", title: "Tree traversals", status: "planned" },
      { id: "tree-bfs", title: "Tree BFS & depth", status: "planned" },
    ],
  },
  {
    title: "Core patterns",
    lessons: [
      { id: "two-pointers", title: "Two pointers", status: "planned" },
      { id: "sliding-window", title: "Sliding window", status: "planned" },
      { id: "backtracking", title: "Backtracking", status: "planned" },
      { id: "dynamic-programming", title: "Dynamic programming", status: "planned" },
    ],
  },
];

const quickselectQuiz = [
  {
    question: "What does partition guarantee about the pivot?",
    options: [
      "The whole array is sorted",
      "The pivot is at its final sorted index",
      "Both sides have equal length",
    ],
    answer: 1,
    explanation:
      "Only the pivot is settled. Values left of it are smaller; values right of it are greater or equal.",
  },
  {
    question: "Why does a 1-based k become target = k - 1?",
    options: [
      "Python indices start at zero",
      "Partition skips one item",
      "The pivot uses the last index",
    ],
    answer: 0,
    explanation:
      "The 1st smallest value belongs at index 0, the 2nd at index 1, and so on.",
  },
  {
    question: "Why is Quickselect O(n) on average?",
    options: [
      "Partition takes constant time",
      "It sorts with a faster comparison",
      "It continues into only one partition",
    ],
    answer: 2,
    explanation:
      "Each partition scans its range, then Quickselect abandons the side that cannot contain the target.",
  },
];

window.AlgoDrillLessons = {
  curriculum,
  quickselectQuiz,
};
})();
