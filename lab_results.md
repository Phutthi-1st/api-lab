# API lab results

## Part 0
Step 0.1, the number of pizza names: 10  
Step 0.3, status code of the request without a token: 401  
Step 0.4, the name of your pizza: "Americana"  
Step 0.12, results of the three runs without a session (optional): Failed 46 out of 49 runs with status code 401 Unauthorized due to multi-server load balancing without sticky session cookies.  
Step 0.16, blocks of "how many of the three tools are excluded":
- 0 tools excluded (valid request)
- 1 tool excluded (valid request)
- 2 tools excluded (valid request)
- 3 tools excluded (excluding all tools causes 500 server crash error)

## Defect report
**Title:** Excluding all available pizza tools causes 500 Internal Server Error  
**Request:** `POST https://quickpizza.grafana.com/api/pizza` with body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`  
**Expected result:** Status 400 Bad Request with a clear JSON error message explaining that no valid pizza cutting tool remains.  
**Actual result:** Status 500 Internal Server Error with an empty response body.  
**Severity:** Medium (Unhandled server exception on boundary input).

## Part A
Step A4, status codes when the other user reads, changes and deletes:
- Read attempt: 404 Not Found
- Change attempt: 404 Not Found
- Delete attempt: 404 Not Found

## Part B
1. **Real server integration vs. Unit tests with stubs:**
   - *Failures found by real server tests:* (1) Sticky session and load balancing failures (e.g., missing `AWSALB` cookie causing authentication state loss across backend nodes), and (2) Database layer constraint errors or actual JSON response format mismatches.
   - *Reason for unit tests with stubs:* Unit tests run extremely fast (in milliseconds), run offline without network reliance, and easily isolate internal business logic edge cases without depending on external system state.

2. **Creating own user vs. using public token:**
   - *Reason:* Creating a new user per test ensures test independence, avoiding race conditions or data pollution from other users or concurrent test runs.
   - *Project 2 Application:* Programmatically create a unique user account, session, or shopping cart fixture for each test case and perform teardown afterwards.

3. **Session usage & Step 0.12 results:**
   - *Session explanation:* `requests.Session` preserves sticky session cookies (`AWSALB` and `AWSALBCORS`), guaranteeing all requests from the same test suite land on the exact same backend node behind the load balancer.
   - *Step 0.12 experience:* Without a session, individual requests hit different backend nodes that had not stored the newly created user in memory, causing frequent `401 Unauthorized` errors (flaky test behavior).

4. **Excluded tools defect analysis:**
   - *Block that revealed defect:* The "excluding all 3 tools" block (`["Knife", "Pizza cutter", "Scissors"]`).
   - *Why 500 is worse:* A 500 Internal Server Error with an empty body indicates an unhandled server crash without actionable feedback for the client, whereas a 400 status provides structured error information.
   - *Why keep as xfail:* `@pytest.mark.xfail(strict=True)` keeps the test active without failing the CI pipeline, while `strict=True` ensures pytest will flag an error as soon as developers fix the bug so the mark can be removed.

5. **Base choice coverage vs. All combinations count:**
   - *Base choice coverage:* $1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9$ tests.
   - *All combinations coverage:* $3 \times 4 \times 2 \times 3 = 72$ tests.

6. **Step A4 status codes:**
   - *Actual status codes:* `404 Not Found` for read, change, and delete attempts.
   - *Is it a defect?:* No, returning `404 Not Found` when a non-owner attempts to access a resource is a standard security practice (Resource Hiding) to prevent unauthorized users from enumerating existing resource IDs.

7. **Madeup token behavior:**
   - *Response:* `200 OK` with `{"ratings": []}`.
   - *Is it a defect?:* Yes, accepting an arbitrary fake token instead of returning `401 Unauthorized` is an authentication bypass vulnerability. On a production system, an attacker could forge authorization headers to gain unauthorized access.

8. **API tests vs. Web UI tests:**
   - *API tests check better:* Backend status codes, exact JSON payload data structures, response headers, and execution speed.
   - *Web UI tests check better:* Browser layout rendering, CSS visual presentation, end-to-end user experience workflows, and client-side JavaScript interactions.