\# Test Plan: Ecommerce API Quality Platform



Last updated: 31 Oct 2026



\## Legend

\- \*\*Type\*\*: Positive / Negative / Boundary

\- \*\*Priority\*\*: High / Medium / Low

\- \*\*Actual Result\*\*: Pass / Fail / Pending (not yet re-verified)



\---



\### TC-001: User Signup (valid data)

\- \*\*Feature/Endpoint\*\*: POST /auth/signup

\- \*\*Preconditions\*\*: Email not already registered

\- \*\*Test Data\*\*: `{"email": "<unique>@example.com", "password": "testpass123"}`

\- \*\*Steps\*\*: Send POST with valid email/password

\- \*\*Expected Result\*\*: 201, response has id, email, is\_admin:false, no password field

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive



\### TC-002: User Signup (duplicate email)

\- \*\*Feature/Endpoint\*\*: POST /auth/signup

\- \*\*Preconditions\*\*: Email already exists in system

\- \*\*Test Data\*\*: Same email as an existing user

\- \*\*Steps\*\*: Send POST with already-registered email

\- \*\*Expected Result\*\*: 400, detail "Email already registered"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Negative



\### TC-003: User Login (valid credentials)

\- \*\*Feature/Endpoint\*\*: POST /auth/login

\- \*\*Preconditions\*\*: User account exists

\- \*\*Test Data\*\*: Correct email + password (form-encoded)

\- \*\*Steps\*\*: Send POST with valid username/password

\- \*\*Expected Result\*\*: 200, response has access\_token and token\_type "bearer"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive



\### TC-004: User Login (wrong password)

\- \*\*Feature/Endpoint\*\*: POST /auth/login

\- \*\*Preconditions\*\*: User account exists

\- \*\*Test Data\*\*: Correct email, incorrect password

\- \*\*Steps\*\*: Send POST with wrong password

\- \*\*Expected Result\*\*: 401, detail "Incorrect email or password"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Negative



\### TC-005: Get Current User (valid token)

\- \*\*Feature/Endpoint\*\*: GET /auth/me

\- \*\*Preconditions\*\*: Valid JWT token from login

\- \*\*Test Data\*\*: Bearer token in Authorization header

\- \*\*Steps\*\*: Send GET with valid token

\- \*\*Expected Result\*\*: 200, returns id/email/is\_admin of logged-in user

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: Medium

\- \*\*Type\*\*: Positive



\### TC-006: Get Current User (no/invalid token)

\- \*\*Feature/Endpoint\*\*: GET /auth/me

\- \*\*Preconditions\*\*: None

\- \*\*Test Data\*\*: No Authorization header, or expired token

\- \*\*Steps\*\*: Send GET without valid token

\- \*\*Expected Result\*\*: 401 Unauthorized

\- \*\*Actual Result\*\*: Pending

\- \*\*Priority\*\*: Medium

\- \*\*Type\*\*: Negative



\### TC-007: Create Product (valid data)

\- \*\*Feature/Endpoint\*\*: POST /products/

\- \*\*Preconditions\*\*: None

\- \*\*Test Data\*\*: `{"name": "Wireless Mouse", "price\_paise": 59900, "stock": 25}`

\- \*\*Steps\*\*: Send POST with valid product fields

\- \*\*Expected Result\*\*: 201, returns product with id and is\_active:true

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive



\### TC-008: Create Product (negative price)

\- \*\*Feature/Endpoint\*\*: POST /products/

\- \*\*Preconditions\*\*: None

\- \*\*Test Data\*\*: `price\_paise: -100`

\- \*\*Steps\*\*: Send POST with negative price

\- \*\*Expected Result\*\*: 422, detail "price\_paise must be positive"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: Medium

\- \*\*Type\*\*: Boundary



\### TC-009: Create Product (negative stock)

\- \*\*Feature/Endpoint\*\*: POST /products/

\- \*\*Preconditions\*\*: None

\- \*\*Test Data\*\*: `stock: -1`

\- \*\*Steps\*\*: Send POST with negative stock

\- \*\*Expected Result\*\*: 422, detail "stock cannot be negative"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: Medium

\- \*\*Type\*\*: Boundary



\### TC-010: List Products

\- \*\*Feature/Endpoint\*\*: GET /products/

\- \*\*Preconditions\*\*: At least one active product exists

\- \*\*Test Data\*\*: None

\- \*\*Steps\*\*: Send GET

\- \*\*Expected Result\*\*: 200, returns array of active products

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive



\### TC-011: Get Product by ID (exists)

\- \*\*Feature/Endpoint\*\*: GET /products/{id}

\- \*\*Preconditions\*\*: Product with given id exists and is active

\- \*\*Test Data\*\*: Valid product id

\- \*\*Steps\*\*: Send GET with valid id

\- \*\*Expected Result\*\*: 200, returns product details

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: Medium

\- \*\*Type\*\*: Positive



\### TC-012: Get Product by ID (not found)

\- \*\*Feature/Endpoint\*\*: GET /products/{id}

\- \*\*Preconditions\*\*: None

\- \*\*Test Data\*\*: Non-existent product id (e.g. 9999)

\- \*\*Steps\*\*: Send GET with invalid id

\- \*\*Expected Result\*\*: 404, detail "Product not found"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: Medium

\- \*\*Type\*\*: Negative



\### TC-013: Delete Product (soft delete)

\- \*\*Feature/Endpoint\*\*: DELETE /products/{id}

\- \*\*Preconditions\*\*: Product exists and is active

\- \*\*Test Data\*\*: Valid product id

\- \*\*Steps\*\*: Send DELETE, then GET the same id

\- \*\*Expected Result\*\*: DELETE returns 204; subsequent GET returns 404

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive



\### TC-014: Update Product (valid data)

\- \*\*Feature/Endpoint\*\*: PATCH /products/{id}

\- \*\*Preconditions\*\*: Product exists

\- \*\*Test Data\*\*: Updated price/stock values

\- \*\*Steps\*\*: Send PATCH with new values

\- \*\*Expected Result\*\*: 200, product reflects updated values

\- \*\*Actual Result\*\*: Pending

\- \*\*Priority\*\*: Medium

\- \*\*Type\*\*: Positive



\### TC-015: Admin Inventory Report (non-admin user)

\- \*\*Feature/Endpoint\*\*: GET /products/admin/inventory

\- \*\*Preconditions\*\*: Logged in as a non-admin user

\- \*\*Test Data\*\*: Valid token, is\_admin:false

\- \*\*Steps\*\*: Send GET with non-admin token

\- \*\*Expected Result\*\*: 403, detail "Admin access required"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Negative



\### TC-016: Add Item to Cart (valid)

\- \*\*Feature/Endpoint\*\*: POST /cart/items

\- \*\*Preconditions\*\*: Valid token, product exists with sufficient stock

\- \*\*Test Data\*\*: `{"product\_id": 1, "quantity": 2}`

\- \*\*Steps\*\*: Send POST with valid product/quantity

\- \*\*Expected Result\*\*: 201, cart contains the added item

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive



\### TC-017: Add Item to Cart (no token)

\- \*\*Feature/Endpoint\*\*: POST /cart/items

\- \*\*Preconditions\*\*: None

\- \*\*Test Data\*\*: Valid body, no Authorization header

\- \*\*Steps\*\*: Send POST without token

\- \*\*Expected Result\*\*: 401 Unauthorized

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Negative



\### TC-018: Add Item to Cart (invalid product id)

\- \*\*Feature/Endpoint\*\*: POST /cart/items

\- \*\*Preconditions\*\*: Valid token

\- \*\*Test Data\*\*: `{"product\_id": 9999, "quantity": 1}`

\- \*\*Steps\*\*: Send POST with non-existent product id

\- \*\*Expected Result\*\*: 404, detail "Product not found"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: Medium

\- \*\*Type\*\*: Negative



\### TC-019: Add Item to Cart (quantity exceeds stock)

\- \*\*Feature/Endpoint\*\*: POST /cart/items

\- \*\*Preconditions\*\*: Valid token, product exists

\- \*\*Test Data\*\*: `{"product\_id": 1, "quantity": 99999}`

\- \*\*Steps\*\*: Send POST with quantity greater than available stock

\- \*\*Expected Result\*\*: 409, detail mentions "exceeds available stock"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Boundary



\### TC-020: Create Order from Cart (valid)

\- \*\*Feature/Endpoint\*\*: POST /orders/

\- \*\*Preconditions\*\*: Valid token, cart has at least one item within stock

\- \*\*Test Data\*\*: None (order built from current cart)

\- \*\*Steps\*\*: Send POST

\- \*\*Expected Result\*\*: 201, order status "pending\_payment", items include price\_paise\_at\_purchase snapshot; product stock decreases; cart is cleared

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive



\### TC-021: Create Payment for Order (valid)

\- \*\*Feature/Endpoint\*\*: POST /payments/

\- \*\*Preconditions\*\*: Valid token, order exists with status pending\_payment

\- \*\*Test Data\*\*: `{"order\_id": <id>, "idempotency\_key": "<unique>"}`

\- \*\*Steps\*\*: Send POST with valid order\_id and new idempotency\_key

\- \*\*Expected Result\*\*: 201, status is "success" or "declined"; if success, order status updates to "paid"

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive



\### TC-022: Pay for Already-Paid Order

\- \*\*Feature/Endpoint\*\*: POST /payments/

\- \*\*Preconditions\*\*: Order exists with status "paid"

\- \*\*Test Data\*\*: `{"order\_id": <paid order id>, "idempotency\_key": "<new unique key>"}`

\- \*\*Steps\*\*: Send POST targeting an already-paid order

\- \*\*Expected Result\*\*: 409, detail mentions order is already paid

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Negative



\### TC-023: Duplicate Payment (same idempotency key)

\- \*\*Feature/Endpoint\*\*: POST /payments/

\- \*\*Preconditions\*\*: A payment was already made with a specific idempotency\_key

\- \*\*Test Data\*\*: Same idempotency\_key resent

\- \*\*Steps\*\*: Send POST twice with identical idempotency\_key

\- \*\*Expected Result\*\*: Second request returns the same payment result, no duplicate payment record created

\- \*\*Actual Result\*\*: Pending

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Boundary



\### TC-024: Regression — Full Purchase Flow

\- \*\*Feature/Endpoint\*\*: Signup → Login → Browse Products → Add to Cart → Create Order → Pay → Verify Order

\- \*\*Preconditions\*\*: Backend and database running

\- \*\*Test Data\*\*: Dynamic email, product id 1

\- \*\*Steps\*\*: Execute all 7 requests in sequence via Collection Runner

\- \*\*Expected Result\*\*: All steps return expected status codes; final order status is "paid" or "pending\_payment" depending on simulated payment outcome

\- \*\*Actual Result\*\*: Pass

\- \*\*Priority\*\*: High

\- \*\*Type\*\*: Positive

