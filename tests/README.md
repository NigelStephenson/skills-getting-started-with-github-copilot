# Test Suite for Mergington High School API

This directory contains comprehensive pytest tests for the FastAPI application.

## Test Structure

- **`conftest.py`**: Pytest configuration and fixtures
  - `client` fixture: Provides a FastAPI TestClient for making HTTP requests
  - `reset_activities` fixture: Resets the activities database before each test to ensure isolation

- **`test_activities.py`**: Tests for basic endpoints
  - Root redirect functionality
  - Getting all activities
  - Activity structure validation
  - Participant data validation

- **`test_signup.py`**: Tests for the signup endpoint
  - Successful signup
  - Duplicate signup prevention
  - Nonexistent activity handling
  - Multiple student signups
  - URL encoding support

- **`test_unregister.py`**: Tests for the unregister endpoint
  - Successful unregistration
  - Nonexistent activity/participant handling
  - Participant preservation
  - Complete signup/unregister workflows
  - Re-signup after unregistration

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run with coverage:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Run specific test file:
```bash
pytest tests/test_signup.py -v
```

### Run specific test:
```bash
pytest tests/test_signup.py::test_signup_for_activity_success -v
```

## Test Coverage

The test suite achieves **100% code coverage** of the FastAPI application, ensuring all endpoints and edge cases are thoroughly tested.

## Key Features

- **Isolation**: Each test runs independently with a fresh database state
- **Comprehensive**: Tests cover success cases, error cases, and edge cases
- **Fast**: All tests complete in under 1 second
- **Maintainable**: Clear test names and well-documented test cases
