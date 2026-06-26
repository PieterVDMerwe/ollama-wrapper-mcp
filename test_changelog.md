# Test Failure Changelog

## 2026-06-26

### 1. Test Collection Failure: ModuleNotFoundError
* **Failed Test**: All tests (`test_config.py`, `test_security.py`, `test_server.py`)
* **Reason**: Python could not resolve local project imports (`config`, `security`, `server`) because the root directory was not in `PYTHONPATH`.
* **Resolution**: Configured execution command to explicitly set `PYTHONPATH="."` before running pytest.

### 2. Pydantic ValidationError: URL Parsing
* **Failed Test**: `test_server.py` collection phase
* **Reason**: The FastMCP resource URI `"active_model/status"` was not formatted as a valid URL, triggering a Pydantic Validation error upon server initialization.
* **Resolution**: Updated resource decorator to use a valid scheme (`"active-model://status"`).

### 3. AttributeError: 'coroutine' object has no attribute 'get'
* **Failed Test**: `test_list_local_models` and `test_run_model_completion_success`
* **Reason**: Mocked response object was created using `AsyncMock`, which wrapped the synchronous `.json()` method in a coroutine, returning unawaited futures during validation checks.
* **Resolution**: Replaced the response mock type with a synchronous `MagicMock` so `.json()` returns the mock dictionary directly.
