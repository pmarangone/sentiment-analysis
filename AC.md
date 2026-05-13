# Acceptance Criteria (AC) and Implementation Steps

- **Skills used:** `improve-codebase-architecture`

## Acceptance Criteria (AC)
- [ ] **Decoupling from Frameworks:** Business logic (`use_cases`) must not import or use `fastapi`, `sqlalchemy`, or `celery`.
- [ ] **Dependency Inversion:** Business logic must depend on abstract interfaces (ABCs) rather than concrete repository classes.
- [ ] **Pure Return Values:** `use_cases` must return domain entities or primitive types, never HTTP response objects.
- [ ] **Error Handling:** Domain exceptions should be defined and handled by the controller layer (Interface Adapters) to translate into appropriate HTTP status codes.
- [ ] **Testing:** Refactored components must maintain or improve test coverage.

## Implementation Steps

### Phase 1: Domain Layer
1.  [x] Define domain entities in `app/domain/models.py`.
2.  [x] Define abstract interfaces in `app/domain/interfaces.py` for `IReviewRepository`, `ICustomerRepository`, and `IMessageBroker`.

### Phase 2: Use Cases
1.  [x] Create `app/use_cases/`.
2.  [x] Implement use case classes that take repository/broker interfaces via dependency injection.
3.  [ ] Logic currently in `app/core/core.py` (e.g., `core_create_review_celery`) should be moved to these classes.
4.  [ ] Remove all imports of `app.api.responses` and framework-specific modules from these classes.

### Phase 3: Infrastructure / Adapters
1.  Implement concrete gateways for repositories and the message broker that satisfy the interfaces in `app/domain/interfaces.py`.
2.  Refactor `app/api/` (controllers) to:
    *   Parse HTTP requests into domain models.
    *   Invoke use cases via Dependency Injection (FastAPI `Depends`).
    *   Map domain results and custom exceptions to HTTP responses (e.g., `JSONResponse`, 404s, 500s).
3.  Ensure `celery_app` usage is moved exclusively to the concrete `MessageBroker` implementation in `app/infrastructure`.

### Phase 4: Cleanup
1.  Delete `app/core/core.py` once logic has been migrated.
2.  Ensure backward compatibility if required or update dependent code (tests/other modules).
