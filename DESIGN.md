# Technical Design: Database Abstraction and Repository Pattern

## 1. Problem Statement
The current implementation of `backend/app/core/core.py` directly instantiates and interacts with concrete database repositories (`ReviewRepository` and `CustomerRepository`). This violates the Dependency Inversion Principle, making the code tightly coupled to specific database implementations and difficult to test or swap.

## 2. Proposed Solution
We will implement the Repository Pattern using Abstract Base Classes (ABCs) to define interfaces for our repositories. The `core` logic will then depend on these abstractions rather than concrete implementations, allowing for better testability and decoupling.

### 2.1. Defining Interfaces (Abstract Base Classes)
We will introduce `app/db/repositories/base.py` (or similar location) containing the following definitions:

*   `ICustomerRepository`: Defines methods like `get_customer_by_name`, `create_customer`, `insert_many`.
*   `IReviewRepository`: Defines methods like `create_reviews_many`, `create_review`, `get_review_by_id`, `get_reviews`, `get_classification_count`.

### 2.2. Updating Existing Repositories
Concrete repositories in `backend/app/db/` will inherit from these ABCs:

```python
# Example for ReviewRepository
class ReviewRepository(IReviewRepository):
    # implementation
```

### 2.3. Refactoring `backend/app/core/core.py`
The `core` functions will be refactored to accept repository instances as arguments or via a dependency injection framework (e.g., FastAPI's `Depends`).

Current state:
```python
review_repository = ReviewRepository()
# ...
async def core_create_reviews_many(...):
    # uses global review_repository
```

New state:
```python
async def core_create_reviews_many(
    db_session: Session,
    reviews: RequestReviewModel,
    review_repo: IReviewRepository,
    customer_repo: ICustomerRepository
):
    # use injected repos
```

## 3. Implementation Steps

1.  **Create Abstract Interfaces**: Define `AbstractReviewRepository` and `AbstractCustomerRepository` in `backend/app/db/repository_interfaces.py`.
2.  **Ensure Implementations conform**: Update `backend/app/db/review_repository.py` and `backend/app/db/customer_repository.py` to inherit from the defined interfaces.
3.  **Refactor Core**:
    *   Update all functions in `backend/app/core/core.py` to accept repository arguments.
    *   Remove global instantiation of repositories in `core.py`.
4.  **Update API Layer**: Update `backend/app/api/reviews.py` (and any other files calling `core` functions) to instantiate the concrete repositories and inject them when calling the `core` functions.

## 4. Edge Cases and Considerations
*   **Database Sessions**: Ensure that the `db_session` continues to be passed correctly alongside the repositories.
*   **Dependency Injection**: Use standard dependency injection practices compatible with FastAPI.
*   **Performance**: Since the repositories are lightweight objects, dependency injection should not introduce significant overhead.

## 5. Benefits
*   **Testability**: We can easily inject mock repositories into `core` functions for unit testing.
*   **Flexibility**: We can swap database implementations (e.g., changing SQL databases or adding caching layers) without modifying the `core` logic.
*   **Maintainability**: Clear separation of concerns between business logic and database access.
