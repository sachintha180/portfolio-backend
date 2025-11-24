# ABSOLUTES - Backend Development Rules

This document defines the absolute rules that must be followed when developing the backend API. These rules are non-negotiable and must be adhered to at all times.

---

## Rule 1: No Unnecessary Data Returns

**Principle:** Routes should not return unnecessary data. Only return data that is absolutely necessary for the client.

**Examples:**

- **Good:** Return user data after registration/login (necessary)
- **Good:** Return verification data from `/auth/verify` (necessary)
- **Good:** No return body for DELETE operations (204 No Content)
- **Bad:** Return success messages like `{"message": "Operation successful"}`

**Implementation:**

- If an operation succeeds but doesn't need to return data, use `204 No Content` status code
- Only return data that the frontend/client actually needs

---

## Rule 2: Request/Response Schema Suffix

**Principle:** All route data schemas must be suffixed with `Request` or `Response` respectively.

**Examples:**

- **Good:** `AuthLoginRequest`, `AuthLoginResponse`
- **Good:** `UserUpdateRequest`, `GetUserResponse`
- **Bad:** `AuthLogin`, `UserUpdate` (without suffix)

**Implementation:**

- Request schemas: `{RouteName}Request` (e.g., `AuthRegisterRequest`)
- Response schemas: `{RouteName}Response` (e.g., `AuthRegisterResponse`)
- Nested schemas used within responses don't need Request/Response suffix (e.g., `AuthVerifyUser`)

---

## Rule 3: Explicit Status Codes

**Principle:** All routes must have an explicit status code defined.

**Examples:**

- **Good:** `status_code=status.HTTP_200_OK`
- **Good:** `status_code=status.HTTP_201_CREATED`
- **Good:** `status_code=status.HTTP_204_NO_CONTENT`
- **Bad:** Relying on FastAPI defaults without explicit declaration

**Implementation:**

- Always include `status_code` parameter in route decorator
- Use appropriate HTTP status codes for each operation

---

## Rule 4: No HTTPExceptions in Routes

**Principle:** Routes must not directly raise HTTPExceptions. All complex business logic and exception handling must be handled in services. All exceptions must be defined in `custom_types/exceptions.py`.

**Examples:**

- **Good:** Route calls `auth_service.verify_authentication()` which raises `NotAuthenticatedError`
- **Bad:** Route directly raises `HTTPException(status_code=401, detail="Not authenticated")`

**Implementation:**

- Routes should be thin - they call services and return responses
- Services contain all business logic and raise appropriate exceptions
- All custom exceptions inherit from `HTTPException` and are defined in `custom_types/exceptions.py`
- Dependencies can call services but should not raise exceptions directly

---

## Rule 5: No Imports in Middle of Code

**Principle:** Absolutely no importing in the middle of your code, unless it breaks the program. All imports must be made at the top of the code file.

**Examples:**

- **Good:** All imports at top of file
- **Bad:** `from fastapi import HTTPException` inside a function
- **Bad:** `import os` in the middle of a class method

**Implementation:**

- All imports go at the top of the file
- Group imports: standard library, third-party, local imports
- Only exception: circular import issues that genuinely break the program

---

## Rule 6: No Bundled Dependency Factories

**Principle:** Don't build any bundled dependency factories. Use individual dependencies instead.

**Examples:**

- **Good:** `get_current_user()` dependency that returns `User`
- **Good:** Routes use `current_user: CurrentUserDep` and `session: DBSessionDep` separately
- **Bad:** `get_authenticated_context()` that returns a NamedTuple with both user and session

**Implementation:**

- Each dependency should return a single, focused value
- Routes can use multiple dependencies if needed
- Avoid creating wrapper dependencies that bundle multiple values

---

## Rule 7: Route Schema Naming Convention

**Principle:** Route schemas must follow the pattern `<service><method><Response/Request>`. The service name comes from the route prefix, the method is the HTTP verb (capitalized), and it ends with Request or Response. Internal/non-route schemas in the same file should be given different names (e.g., `TokenPayload` in `auth.py`).

**Examples:**

- **Good:** `/auth/login` POST → `AuthLoginRequest`, `AuthLoginResponse`
- **Good:** `/auth/register` POST → `AuthRegisterRequest`, `AuthRegisterResponse`
- **Good:** `/users/{user_id}` GET → `UserGetResponse`
- **Good:** `/users/{user_id}` PATCH → `UserUpdateRequest`, `UserUpdateResponse`
- **Good:** Internal schema in `auth.py` → `TokenPayload` (not `AuthTokenPayload`)
- **Bad:** `/users/{user_id}` GET → `GetUserResponse` (wrong order)
- **Bad:** `/auth/login` → `LoginRequest` (missing service prefix)

**Implementation:**

- Pattern: `<Service><Method><Request/Response>`
- Service: Route prefix capitalized (`/auth` → `Auth`, `/users` → `User`)
- Method: HTTP verb capitalized (`GET` → `Get`, `POST` → `Post`, `PATCH` → `Update`, `DELETE` → `Delete`)
- Type: `Request` for request bodies, `Response` for responses
- Internal/non-route schemas get descriptive names without service prefix
- Keep schemas organized by route group in schema files

---

## Rule 8: Code Spacing and Formatting

**Principle:** There must be one blank line ALWAYS between the method body and the return statement. The remaining blocks of code must be spaced out semantically.

**Examples:**

```python
# Good
def example_function():
    # Method body logic
    result = some_operation()

    return result

# Bad - no blank line before return
def example_function():
    result = some_operation()
    return result

# Good - semantic spacing
def complex_function():
    # First logical block
    user = get_user()

    # Second logical block
    if user:
        process_user(user)

    # Return statement
    return user
```

**Implementation:**

- Always have one blank line before `return` statement
- Group related code blocks together
- Separate logical sections with blank lines
- Maintain consistent spacing throughout the codebase

---

## Rule 9: Parameter Naming Convention

**Principle:** Parameters must be prefixed with appropriate names suiting their use case. Generic names like `service` or `session` are not allowed. This applies to all layers: routes, services, and database.

**Examples:**

- **Good:** `auth_service: AuthServiceDep`, `user_service: UserServiceDep`
- **Good:** `db_session: DBSessionDep` (in routes)
- **Good:** `db_session: Session` (in services and database layer)
- **Good:** `request_data: AuthLoginRequest`
- **Bad:** `service: AuthServiceDep` (too generic)
- **Bad:** `session: DBSessionDep` or `session: Session` (too generic, must be `db_session`)
- **Bad:** `data: AuthLoginRequest` (too generic)

**Implementation:**

- Service dependencies: Prefix with service type (`auth_service`, `user_service`)
- Database session: **Always** prefix with `db_` (`db_session`) in routes, services, and database layer
- Request data: Use descriptive name (`request_data`, `user_data`)
- Request object: Use `request: Request`
- Response object: Use `response: Response`
- All parameters should clearly indicate their purpose and type
- Consistency across all layers: routes, services, and database must all use `db_session` for database session parameters

---

## Rule 10: Router-Level Dependencies Prohibition

**Principle:** Router-level dependencies (`dependencies=[Depends(...)]` in `APIRouter`) **MUST NOT** be used. Router-level dependencies do not inject return values into route functions, which causes dependency resolution conflicts and validation errors.

**Examples:**

- **Good:** All dependencies declared as function parameters: `def route(authenticated_user: AuthenticatedUserDep, service: ServiceDep)`
- **Good:** Each route explicitly declares its dependencies, making dependencies clear and injectable
- **Good:** Unused dependencies replaced with underscore: `def route(_: AuthenticatedUserDep, service: ServiceDep)` when authentication is needed but user object isn't used
- **Bad:** `router = APIRouter(dependencies=[Depends(get_authenticated_user)])` - return value not injected
- **Bad:** Router-level dependency + function parameter for same dependency - causes 422 validation errors
- **Bad:** Assuming router-level dependencies inject values into route functions
- **Bad:** `def route(authenticated_user: AuthenticatedUserDep, ...)` when `authenticated_user` is never used in the function body (should be `_: AuthenticatedUserDep`)

**Implementation:**

- **Never** use `dependencies` parameter in `APIRouter()` constructor
- Always declare dependencies as function parameters in route handlers
- Each route must explicitly declare all dependencies it needs
- If a dependency is required for side effects (like authentication checks) but its return value is not used in the function body, replace the parameter name with a single underscore: `_: AuthenticatedUserDep`, `_: DBSessionDep`, etc.
- This ensures dependencies are properly injected and avoids FastAPI validation conflicts
- Router-level dependencies only execute for side effects but don't inject return values
- If you need the return value, you MUST declare it as a function parameter, making router-level dependency redundant
- Using `_` clearly indicates the dependency is intentionally unused but required for side effects

---

## Rule 11: Exception Detail Messages

**Principle:** Do not pass detail strings to exceptions if they match the default message defined in the exception class. Only pass a detail parameter when you need a custom message that differs from the default.

**Examples:**

- **Good:** `raise UserNotFoundError()` when the default message "User not found" is appropriate
- **Good:** `raise EmailAlreadyExistsError()` when the default message "Email already in use" is appropriate
- **Good:** `raise UserNotFoundError("User with ID 123 not found")` when you need a more specific message
- **Bad:** `raise UserNotFoundError("User not found")` when it matches the default exactly
- **Bad:** `raise EmailAlreadyExistsError("Email already in use")` when it matches the default exactly

**Implementation:**

- Check the exception class definition in `custom_types/exceptions.py` for the default detail message
- Only pass a `detail` parameter if you need a message that differs from the default
- This reduces redundancy and keeps code cleaner
- Default messages are defined in exception constructors with `detail: str = "default message"`

---

## Rule 12: Top-Down Development Approach

**Principle:** Always build features top-down, starting from routes and working down to database operations. This ensures only necessary methods are implemented, reducing code bloat and technical debt.

**Development Order:**

1. **Routes Layer** (`routes/`): Start by defining routes with hypothetical service methods and schemas
2. **Services Layer** (`services/`): Implement service methods with hypothetical database operations
3. **Database Layer** (`database/`): Finally implement only the database methods actually needed

**Examples:**

- **Good:** Start with route `@router.post("/users")` calling `user_service.create_user()`, then implement `create_user()` calling `db.create_user()`, then implement `db.create_user()`
- **Good:** Create schemas (`UserCreateRequest`, `UserCreateResponse`) as needed when defining routes
- **Good:** Create exceptions (`UserNotFoundError`) as needed when implementing services
- **Bad:** Building all database methods first, then services, then routes (bottom-up approach)
- **Bad:** Implementing database methods that are never actually called by services

**Implementation:**

- Begin with route definitions and create placeholder service calls
- Define request/response schemas as you need them in routes
- Implement service methods to fulfill route requirements, creating placeholder database calls
- Define custom exceptions in `custom_types/exceptions.py` as needed during service implementation
- Finally implement only the database methods that services actually call
- This approach ensures every method serves a purpose and reduces unnecessary code
- If a method isn't called from the layer above, it shouldn't exist

---

## Rule 13: Route Ordering

**Principle:** Specific routes (literal paths) **MUST** be defined before parameterized routes (path parameters) in the same router. FastAPI matches routes in order, and if a parameterized route comes first, it will try to match specific paths as parameters, causing 422 validation errors.

**Examples:**

- **Good:** `/all` route defined before `/{syllabus_id}` route
- **Good:** `/search` route defined before `/{id}` route
- **Good:** `/me` route defined before `/{user_id}` route
- **Bad:** `/{syllabus_id}` route defined before `/all` route - FastAPI tries to parse "all" as UUID → 422 error
- **Bad:** `/{id}` route defined before `/search` route - FastAPI tries to parse "search" as parameter → validation error

**Implementation:**

- Always define specific/literal routes before parameterized routes
- Order routes from most specific to least specific
- Pattern: `/specific-path` → `/{parameter}` → `/{param1}/{param2}`
- This prevents FastAPI from incorrectly matching specific paths as parameters
- If you get 422 validation errors on specific routes, check route ordering first

---

## Rule 14: Route Prefix and Filename Consistency

**Principle:** Route file names should be singular (e.g., `user.py`), while the `APIRouter` prefix must be plural (e.g., `/users`). This follows REST API conventions where endpoints are pluralized.

**Examples:**

- **Good:** File `routes/user.py` with `prefix="/users"`
- **Good:** File `routes/auth.py` with `prefix="/auth"` (auth is already a collective noun)
- **Good:** File `routes/lesson.py` with `prefix="/lessons"`
- **Bad:** File `routes/users.py` with `prefix="/users"` (filename should be singular)
- **Bad:** File `routes/user.py` with `prefix="/user"` (prefix should be plural)

**Implementation:**

- Route files use singular nouns: `user.py`, `lesson.py`, `post.py`
- Router prefixes use plural nouns: `/users`, `/lessons`, `/posts`
- Exceptions:
  - Collective nouns like `auth` remain singular in both filename and prefix
- This maintains consistency with REST API conventions where resource endpoints are pluralized
