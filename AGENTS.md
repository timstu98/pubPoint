# pubPoint agent instructions

## Project

- This is a Docker Compose application with frontend, backend, and MySQL services.
- Backend code and migrations live under `app/backend`.
- Frontend code lives under `app/frontend`.

## Setup and development

See `README.md` for setup, development, and verification commands. Read `docs/README.md` to find product requirements, architecture guidance, and decision records relevant to the task.

## Scripts

- Use `bash_scripts` for host-side Bash helpers, `pwsh_scripts` for PowerShell equivalents, and `docker_scripts` for scripts run inside the backend container.
- GitHub automation belongs in `.github/scripts`; keep it separate from developer workflow scripts.
- When adding a script, place it in the folder matching where and how it runs, and keep equivalent Bash and PowerShell helpers aligned when both are provided.

## Working agreements

- When exploring a ticket, implementing a feature or fix, reviewing changes, or handing off work, follow [the AI development workflow](docs/development/ai-workflow.md).
- When a GitHub issue is provided, use it for task scope and status. Record durable architectural and product decisions in `docs/`, linking them from the relevant issue when one exists.
- Use Conventional Commits format for PR titles: `<type>[optional scope]: <description>` (for example, `docs: clarify MVP algorithm`).
- Update the README when setup or development commands change.
- Before considering a change complete, run the most relevant available tests or checks and report anything not run.

## GitHub pull requests

- When creating a pull request related to a GitHub issue, append its reference in square brackets (for example, `[#123]`) to the end of the PR title. Omit the reference when the PR is unrelated to an issue.

## Code review

Review changes against the relevant issue, when provided, and the project conventions and documents indexed in `docs/README.md`.
