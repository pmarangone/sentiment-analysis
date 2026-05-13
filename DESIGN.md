# Design: Clean Architecture Implementation

## 1. Introduction
The current codebase exhibits tight coupling between business logic and infrastructure (FastAPI, SQLAlchemy, Celery). This design proposes a refactoring to align with Clean Architecture principles, ensuring that the domain logic remains independent of external frameworks.

## 2. Identified Issues
- **Direct Infrastructure Dependencies:** Business logic in `app/core` depends directly on `celery_app`, which is an infrastructure concern.
- **Leaky Framework Logic:** The `core` functions return HTTP response objects, coupling business processes directly to the web API layer.
- **Repository Coupling:** Business logic is directly using repository implementations instead of abstractions (interfaces).

## 3. Proposed Architecture
The project will be refactored into the following layers:

### A. Domain Layer
- **Entities:** Simple Python classes/dataclasses representing core business objects (`Review`, `Customer`).
- **Interfaces:** Abstract Base Classes (ABCs) defining interfaces for repositories and message brokers.

### B. Use Case Layer (Application)
- Orchestrates the flow of data.
- Does not know about HTTP, Database, or specific Task Queues.
- Depends on domain interfaces.

### C. Interface Adapters
- **Controllers:** FastAPI routers that call use cases. They handle HTTP request parsing and response formatting.
- **Gateways:** Concrete implementations of the interfaces defined in the domain layer.

### D. Infrastructure
- **Frameworks:** FastAPI, SQLAlchemy, Celery implementations.

## 4. Refactoring Plan

### 4.1. Domain Layer (`app/domain`)
- Create `app/domain/models.py` for pure entities.
- Create `app/domain/interfaces.py` defining:
  - `IReviewRepository`
  - `ICustomerRepository`
  - `IMessageBroker`

### 4.2. Use Case Layer (`app/use_cases`)
- Replace `app/core` with `app/use_cases`.
- Each function (e.g., `create_review`) will be a class or function that takes repository and broker interfaces as arguments (Dependency Injection).
- Returns domain objects, NOT HTTP responses.

### 4.3. Interface Adapters (`app/adapters`)
- **Controllers:** FastAPI routes handle HTTP-specific logic, convert requests to domain models, call use cases, and convert results back to HTTP responses.
- **Repositories:** Implement the interfaces defined in the Domain layer using SQLAlchemy.

### 4.4. Infrastructure (`app/infrastructure`)
- Contains concrete implementations of the `IMessageBroker` interface (e.g., using Celery).
- Database session management remains here.

## 5. Implementation Details

### Example: Repository Interface
```python
# app/domain/interfaces.py
from abc import ABC, abstractmethod
from app.domain.models import Review

class IReviewRepository(ABC):
    @abstractmethod
    async def create(self, review: Review) -> Review:
        pass
```

### Example: Use Case
```python
# app/use_cases/create_review.py
class CreateReviewUseCase:
    def __init__(self, repository: IReviewRepository, broker: IMessageBroker):
        self.repository = repository
        self.broker = broker

    async def execute(self, review_data: dict):
        # Business Logic
        review = Review(**review_data)
        saved_review = await self.repository.create(review)
        await self.broker.publish("review-created", saved_review)
        return saved_review
```

## 6. Edge Cases
- **Dependency Injection:** Use dependency injection (e.g., FastAPI `Depends`) to inject concrete implementations into the controllers.
- **Error Handling:** Use custom domain exceptions. The controller layer should map these domain exceptions to appropriate HTTP status codes (404, 500, etc.).
- **Async/Sync:** Ensure all interfaces are asynchronous to maintain compatibility with the current stack.
