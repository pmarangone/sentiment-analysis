# Clean Architecture Design Proposal

## Overview
The current codebase exhibits tight coupling between the delivery mechanism (FastAPI), the business logic (core), and the data access/infrastructure layer (SQLAlchemy/DB). To adhere to Clean Architecture, we need to decouple these layers.

## Goals
1.  **Independence of Frameworks**: Business logic should not depend on FastAPI or Celery.
2.  **Independence of UI/Delivery**: The core should be agnostic of how it's called (API, CLI, message consumer).
3.  **Testability**: Core logic should be testable without mocking HTTP requests or database connections.
4.  **Separation of Concerns**: Clearly define Domain, Application (Use Case), and Infrastructure layers.

## Technical Design

### 1. Domain Layer (`domain/`)
Create a new directory for domain models (Entities). These are plain Python objects with no database decorators.
- Example: `domain/review.py`
- Contains: `Review`, `Customer` data classes (Pure Python).

### 2. Application/Use Case Layer (`application/`)
Refactor the existing `core/` logic into Use Case classes.
- Each use case class (e.g., `CreateReviewUseCase`) should implement a single responsibility.
- Use Cases will receive Repository interfaces as dependencies (Dependency Injection).
- Use Cases return domain objects, NOT HTTP responses.

### 3. Infrastructure/Repository Layer (`infrastructure/` or `db/`)
- Define abstract interfaces (`repository_interface.py`) for data access.
- Implement these interfaces using SQLAlchemy models (`repository_impl.py`).
- Decouple the database models from domain objects by using mappers.

### 4. Interface Adapters (Controllers/Consumers)
- **API (`api/`)**: FastAPI routes should only handle request validation, input mapping, invoking the use case, and formatting the output (HTTP responses).
- **Consumers (`consumer/`)**: These should act as adapters that invoke the same Use Cases as the API.

## Proposed Structure

```
backend/
├── app/
│   ├── domain/           # Entities (Pure Python)
│   ├── application/      # Use Cases (Business Logic)
│   ├── infrastructure/   # DB Repositories, External Services (Adapters)
│   ├── interfaces/       # API Controllers, DI containers
│   └── main.py           # Entry point
consumer/
├── app/
│   ├── application/      # Reused Use Cases
│   └── infrastructure/   # Adapters for tasks
```

## Changes Required

### 1. Refactor `app/core/core.py`
- Extract logic into a class-based structure.
- Remove references to `app.api.responses` (e.g., `created()`, `not_found()`). Use cases should raise exceptions or return result objects.
- Move serialization logic out of the use case.

### 2. Dependency Injection
- Use a DI container or simple factory patterns to inject implementations of repositories into the Use Case instances.

### 3. Standardize Interfaces
- Use Abstract Base Classes (ABCs) to define `ReviewRepository` and `CustomerRepository`. This allows swapping the real DB implementation with mocks during testing without changing the use case.

## Edge Cases
- **Transactions**: Ensure that database transactions are managed at the entry point (controller/consumer) or via a decorator, not inside the core business logic.
- **Error Handling**: Use custom Domain exceptions to map to HTTP statuses at the controller level.

## Example Refactoring Plan
1.  Define `Repository` interfaces in `domain/`.
2.  Create `CreateReviewUseCase` that takes `review_repo: AbstractRepository`.
3.  Update `api/reviews.py` to instantiate `CreateReviewUseCase` with a concrete `SQLAlchemyReviewRepository`.
4.  Repeat for other core functions.
