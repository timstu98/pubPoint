# Use React for the frontend

> **Accepted**

PubPoint needs a browser interface where people can adjust group members and starting locations on a map, then compare venue options. I will use React with TypeScript for the frontend. React's components suit the map, forms, and results views, and its broad adoption makes libraries and help easy to find. TypeScript should help keep data passed between those views clear as the project grows or more people contribute. Vite will handle the frontend build.

A plain JavaScript frontend would need less setup but would leave more of the interactive state and UI structure to us. Vue or Svelte could also support this interface; I do not see an advantage for this MVP that outweighs React's ecosystem. React adds framework and build-tool complexity, but it gives us a useful foundation for the expected UI. Its skills could also transfer to a future React Native app if mobile becomes important; that would be a separate decision.
