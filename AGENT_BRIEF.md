# AGENT_BRIEF

This is a new standalone Fabric mod project. The `yansheng-source` repository in the workspace is reference-only for workflow and 26.1/Fabric practices; do not place this project's source inside it.

First steps for future agents:

1. Read this file.
2. Read `CURRENT_BASELINE.md`.
3. Read `NEXT_TASK.md`.
4. Read `CHANGELOG.md`.

Rules:

- User's current request > current source/resources > current docs > old memory.
- Java owns mechanics, registries, events, sync, and validation.
- JSON/resources own content data, lang, models, recipes, tags, and balance where a loader exists.
- Target environment: MC 26.3, Fabric Loader 0.19.5, Fabric API 0.160.7+26.3, Fabric Loom 1.17.20, Gradle 9.5.1, Java 25.
