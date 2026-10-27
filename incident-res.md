# Security Incident Investigation Report

**Case ID:** INV-001  
**Project:** InvoiceFlow — Simulated SaaS Security Incident  
**Date:** 27 October 2026  
**Environment:** Local Python Flask Application  
**Classification:** Educational Security Simulation  
**Vulnerability:** Broken Object Level Authorization (BOLA/IDOR)  
**Status:** Vulnerability identified in demonstration code; remediation planned

---

## 1. Executive Summary

A simulated security investigation was conducted on InvoiceFlow, a fictional SaaS invoicing platform developed using Python Flask.

The investigation examined whether users could retrieve invoice records belonging to other customers.

The demonstration application was intentionally developed without object-level authorization checks. As a result, an API request could retrieve another fictional customer's invoice by changing the invoice identifier.

This represents a Broken Object Level Authorization (BOLA) vulnerability, potentially resulting in unauthorized disclosure of sensitive customer information in a real-world application.

No real customer information or production systems were involved.

## 2. Application Overview

The application provides an API endpoint for retrieving invoice records.

**Endpoint:** `GET /api/invoices/<invoice_id>`

The demonstration uses two fictional customer records:

| User | User ID | Invoice ID | Invoice Amount |
|---|---|---|---|
| Alice | 1 | 101 | $250 |
| Bob | 2 | 102 | $780 |

The `demo_user` query parameter simulates the requesting user. It does not provide genuine authentication.

## 3. Investigation and Evidence

### Test 1 — Authorized Invoice Access

**Request:**

`GET /api/invoices/101?demo_user=1`

**Expected result:** Alice retrieves her own invoice.

**Observed result:** [Record your actual HTTP status and response.]

**Evidence:** `evidence/01-authorized-access.png`

### Test 2 — Cross-User Invoice Access

**Request:**

`GET /api/invoices/102?demo_user=1`

**Expected secure behavior:** The application rejects the request because invoice 102 belongs to Bob.

**Expected vulnerable-demo behavior:** The API returns Bob's invoice despite the simulated requesting user being Alice.

**Observed result:** [Record your actual HTTP status and response.]

**Evidence:** `evidence/02-cross-user-access.png`

### Finding

The application retrieves invoices based on the requested invoice ID without verifying that the simulated requesting user owns the resource.

This demonstrates missing object-level authorization.

## 4. Root Cause Analysis

The vulnerable implementation uses:

```python
invoice = invoices.get(invoice_id)
return jsonify(invoice)
```

Although each invoice contains an `owner_id`, the application does not compare this value with the requesting user's identity before returning the invoice.

Consequently, any accepted demonstration user can retrieve either invoice by supplying its ID.

The application also trusts a client-controlled `demo_user` parameter to represent identity. This is acceptable for a clearly labeled educational simulation but would be insecure as a real authentication mechanism.

## 5. Security Impact and Risk Assessment

**Potential confidentiality impact:** High, if a real application exposed sensitive customer invoice records.

**Integrity impact:** None demonstrated; the endpoint only retrieves data.

**Availability impact:** None demonstrated.

**Likelihood:** Not assessed for a production environment.

**Overall risk:** Potentially high in a real multi-tenant SaaS application, depending on accessible data, exposure, and compensating controls.

The local demonstration establishes the authorization flaw but does not establish a real-world breach, customer impact, or production risk rating.

## 6. Proposed Incident Response

If this issue were discovered in a real SaaS application, the recommended response would be:

1. **Validate:** Confirm the vulnerability through authorized testing and preserve relevant evidence.
2. **Contain:** Restrict access to the affected functionality or implement an appropriate temporary control.
3. **Investigate:** Review logs, affected endpoints, customer records, and possible unauthorized access.
4. **Remediate:** Implement trusted authentication and server-side object-level authorization.
5. **Verify:** Test permitted and prohibited requests and monitor for recurrence.

Any customer notifications or regulatory obligations would require assessment based on the actual facts and applicable requirements.

## 7. Recommended Remediation

The API should establish the user's identity through a verified authentication mechanism and enforce invoice ownership before returning a resource.

The authorization condition should conceptually require:

`invoice.owner_id == authenticated_user.id`

Requests that fail this condition should be denied.

Additional controls include centralized authorization checks, automated negative tests, appropriate audit logging, and review of other endpoints for similar vulnerabilities.

**Remediation status:** Planned for the next development iteration.

## 8. Verification Plan

After remediation, test the following:

| Test | Expected secure result |
|---|---|
| Alice accesses invoice 101 | 200 OK |
| Alice accesses Bob's invoice 102 | 403 Forbidden or intentionally concealed 404 |
| Bob accesses invoice 102 | 200 OK |
| Unauthenticated request | 401 Unauthorized |
| Request for nonexistent invoice | 404 Not Found |

Actual results will be recorded after the secure implementation is completed.

## 9. Key Lessons Learned

This simulation highlights that:

- Authentication and authorization solve different security problems.
- Resource identifiers must not determine access permissions by themselves.
- Object-level authorization should be enforced on every protected request.
- Security findings should include reproducible evidence and clear remediation guidance.
- A simulated vulnerability should not be presented as evidence of a real incident.

## 10. References

- OWASP API Security Top 10 — API1:2023 Broken Object Level Authorization: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
- PortSwigger Web Security Academy — Access Control: https://portswigger.net/web-security/access-control
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

---

**Disclaimer:** This project is an intentionally vulnerable, locally hosted educational simulation. All users, invoices, and incident details are fictional.