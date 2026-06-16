# Acceptance Criteria (AC) and Implementation Checklist

## Acceptance Criteria (AC)

1.  **Repository Abstraction**: Define `ICustomerRepository` and `IReviewRepository` as Abstract Base Classes (ABCs) in a new file `backend/app/db/repository_interfaces.py`.
2.  **Compliance**: `ReviewRepository` and `CustomerRepository` must implement the respective ABCs.
3.  **Decoupling**: Remove the global instantiation of `ReviewRepository` and `CustomerRepository` from `backend/app/core/core.py`.
4.  **Dependency Injection**: Refactor all functions in `backend/app/core/core.py` to accept repository instances via arguments or dependency injection.
5.  **API Integration**: Update callers in `backend/app/api/` to provide concrete instances of the repositories to the core functions.
6.  **Functionality Preservation**: Ensure all existing features (get review, create review, etc.) continue to work as expected without regressions.

## Implementation Steps

### 1. Define Interfaces
- [x] Create `backend/app/db/repository_interfaces.py`.
- [x] Define `ICustomerRepository` with methods: `get_customer_by_name`, `create_customer`, `insert_many`.
- [x] Define `IReviewRepository` with methods: `create_reviews_many`, `create_review`, `get_review_by_id`, `get_reviews`, `get_classification_count`.

### 2. Update Repositories
- [x] Modify `backend/app/db/customer_repository.py` to inherit from `ICustomerRepository`.
- [x] Modify `backend/app/db/review_repository.py` to inherit from `IReviewRepository`.

### 3. Refactor Core Logic
- [x] Remove global `review_repository` and `customer_repository` instances from `backend/app/core/core.py`.
- [x] Update function signatures in `backend/app/core/core.py` (e.g., `core_create_reviews_many`, `core_create_review_celery`, etc.) to accept repositories as parameters.
- [x] Update the internal logic of these functions to use the passed repository instances.

### 4. Update API Layer
- [x] Identify all endpoints or entry points that call the refactored core functions.
- [x] Update `backend/app/api/reviews.py` to instantiate concrete repositories and inject them when calling the `core` functions.
- [x] Ensure that dependency injection (using FastAPI's `Depends` or manual injection) is applied correctly.
- [x] Tools used: `edit`, `write`, `read`, `bash`.

