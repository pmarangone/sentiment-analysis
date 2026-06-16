# Design: Clean Architecture Refactoring

## Problem
The current codebase lacks clear separation of concerns, violating clean architecture principles. Business logic, data access, and infrastructure concerns are tightly coupled.

## Proposed Changes
1. **Decouple Data Access**: Create repositories to abstract data access from business logic.
2. **Implement Use Cases**: Move business logic into dedicated UseCase classes.
3. **Dependency Injection**: Ensure high-level modules depend on abstractions rather than low-level implementations.
4. **Separation of Concerns**: Ensure domain entities are independent of frameworks and databases.

## Scope
- Analyze backend services.
- Analyze consumer services.
- Refactor to isolate domain logic from external concerns.

