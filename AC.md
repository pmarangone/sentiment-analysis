# AC.md

## Implementation Acceptance Criteria

- [ ] **Architecture Overview**: Add a section describing the interaction flow (FastAPI -> RabbitMQ -> Consumer -> DB).
- [ ] **Mermaid Diagram**: Embed the requested architecture flow chart using Mermaid syntax.
- [ ] **Component Documentation**: Include brief descriptions for `backend/` and `consumer/` folders.
- [ ] **Project Structure**: Include a directory tree or summary.
- [ ] **Technical Accuracy**: Ensure README references correctly align with existing service ports (8000) and `docker-compose.yml` configurations.
- [ ] **Formatting**: Ensure professional tone, clear headings, and consistent styling.

## Testing

### Current Testing State
The project includes unit and integration tests located within the `backend/tests/` directory.

### PR Validation
- Visual verification of the Mermaid diagram rendering.
- Cross-check of all command examples against `docker-compose.yml` and folder structure.
- Manual verification that the README correctly guides a new developer through the setup flow.
- Links to Docker documentation have been manually verified as valid.

