# InvoiceFlow — Broken Object Level Authorization Investigation

**A hands-on application security project exploring how missing authorization checks can expose customer data in a multi-user SaaS application.**

## Project Overview

InvoiceFlow is a fictional SaaS invoicing application developed using Python and Flask to demonstrate Broken Object Level Authorization (BOLA), also commonly associated with Insecure Direct Object Reference (IDOR).

The project simulates a security incident where one customer can retrieve another customer's invoice because the application fails to verify resource ownership.

The objective is not only to reproduce the vulnerability but also to investigate its root cause, assess its potential business impact, and develop a secure remediation.

**Environment:** Local educational simulation  
**Technology:** Python, Flask, JSON REST API  
**Security focus:** OWASP API1:2023 — Broken Object Level Authorization  
**Current phase:** Vulnerability demonstration and incident investigation

## The Security Problem

In a multi-tenant SaaS application, users should only access resources they are authorized to view.

Consider two fictional customers:

| Customer | User ID | Invoice ID |
|---|---|---|
| Alice | 1 | 101 |
| Bob | 2 | 102 |

Alice should be able to access invoice 101 but not Bob's invoice 102.

However, the intentionally vulnerable API retrieves invoices using their identifiers without verifying ownership.

This allows a cross-user invoice request to return another customer's information.

## Project Objectives

1. Understand the difference between authentication and authorization.
2. Reproduce an object-level authorization vulnerability in a controlled environment.
3. Document the HTTP evidence and underlying root cause.
4. Evaluate the potential business consequences for a SaaS startup.
5. Implement and verify a secure authorization mechanism in the next project phase.

## Technology Stack

- Python — application logic
- Flask — API development
- JSON — HTTP response format
- curl or Postman — API testing
- Git and GitHub — version control and documentation

## Project Structure

```text
SaaS_Injection/
├── app.py
├── requirements.txt
├── README.md
├── incident.md
└── evidence/
    ├── 01-authorized-access.png
    └── 02-cross-user-access.png
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd SaaS_Injection
```

**2. Create a virtual environment**

```bash
python3 -m venv .venv
```

**3. Activate the environment**

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Run the application**

```bash
python app.py
```

The application starts locally at:

`http://127.0.0.1:5000`

## Demonstrating the Vulnerability

The application provides an endpoint:

`GET /api/invoices/<invoice_id>`

The `demo_user` query parameter represents a fictional user for testing. It is not a secure authentication mechanism.

### Test 1 — Authorized Access

```bash
curl -i "http://127.0.0.1:5000/api/invoices/101?demo_user=1"
```

Expected vulnerable-demo behavior: Alice's invoice is returned.

### Test 2 — Cross-User Access

```bash
curl -i "http://127.0.0.1:5000/api/invoices/102?demo_user=1"
```

Expected vulnerable-demo behavior: Bob's invoice is returned even though the simulated requesting user is Alice.

**Root cause:** The API retrieves invoices without checking whether the requesting user is authorized to access them.

The observed HTTP responses and screenshots are documented in `incident.md`.

## Security Impact

In a real SaaS application, a similar authorization failure could potentially expose sensitive customer information.

Possible consequences include:

- Unauthorized access to customer records.
- Loss of customer trust.
- Incident investigation and remediation costs.
- Regulatory or contractual consequences, depending on the affected data and circumstances.

This demonstration does not involve real customer data or a real security breach.

## Incident Investigation

The project includes a simulated incident report documenting:

- Investigation scope
- HTTP request and response evidence
- Vulnerability root cause
- Potential business impact
- Proposed containment and remediation
- Verification plan

See [Incident Investigation Report](incident.md).

## Planned Remediation

The next development phase will introduce:

- Verified user authentication.
- Server-side object-level authorization.
- Automated tests for permitted and prohibited access.
- Comparison of vulnerable and secured API behavior.

The current version is intentionally vulnerable and must not be deployed to a public environment.

## Key Learning Outcomes

This project explores how a seemingly small missing authorization check can create a serious confidentiality risk.

It reinforces the importance of validating user permissions at the resource level, separating authentication from authorization, and documenting findings with reproducible evidence.

## References

- [OWASP API Security Top 10 — Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [PortSwigger — Access Control Vulnerabilities](https://portswigger.net/web-security/access-control)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

## Disclaimer

This is an intentionally vulnerable educational project developed for authorized local testing. All customer information and incident scenarios are fictional. Do not expose the vulnerable application to the public internet.