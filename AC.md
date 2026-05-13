# Acceptance Criteria (AC)

## Project Goals
- Decouple domain logic from frameworks (FastAPI/Celery) and infrastructure (SQLAlchemy/DB).
- Ensure core business logic is testable without mocking infrastructure.
- Establish clear separation between Domain, Application, and Infrastructure layers.

## Checklist of Acceptance Criteria

### 1. Domain Layer
- [ ] Create `domain/` directory.
- [ ] Define Domain Entities (e.g., `Review`, `Customer`) as pure Python data classes.
- [ ] Define abstract Repository interfaces (ABCs) in `domain/repository_interface.py` (e.g., `ReviewRepository`, `CustomerRepository`).

### 2. Application Layer (Use Cases)
- [ ] Create `application/` directory.
- [ ] Implement Use Cases as classes (e.g., `CreateReviewUseCase`).
- [ ] Inject repository interfaces into Use Cases via constructors (Dependency Injection).
- [ ] Ensure Use Cases do not import framework-specific code (FastAPI/Celery/SQLAlchemy).
- [ ] Use Cases return Domain models or custom Result objects instead of HTTP responses.
- [ ] Use Cases raise custom Domain exceptions to be handled at the Interface layer.

### 3. Infrastructure Layer
- [ ] Implement concrete Repository classes in `infrastructure/` (or refactor existing `db/`) that implement the Domain repository interfaces.
- [ ] Handle database transactions at the API/Interface level (e.g., via middleware or controller logic).
- [ ] Update Celery/Consumer tasks to use the same Use Case classes, ensuring framework independence.

### 4. Interface Adapters
- [ ] Update API (`api/`) to handle HTTP request validation, call the appropriate Use Case, and map the Use Case result to the final HTTP response.
- [ ] Ensure that only the Controller layer is aware of HTTP/Celery framework specifics.

## Implementation Steps

1.  **Refactor Domain Models**: Move entities from `models/` to `domain/`.
2.  **Define Interfaces**: Create `domain/repository_interface.py` specifying the required repository methods.
3.  **Migrate Logic**: Move code from `app/core/core.py` to `application/` layer use cases.
4.  **Inject Dependencies**: Update the `api/` endpoints to initialize Use Cases with concrete repositories (e.g., `SQLAlchemyReviewRepository`).
5.  **Remove Dependencies**: Delete imports of `app.api.responses` and `sqlalchemy.orm.Session` from all business logic files.
6.  **Verify Tests**: Update tests to use mocked repository interfaces rather than real database/API calls.
