# Incident Postmortem: Webhook Retry Delivery Failure

**Document ID**: DOC-INC-2026-10-02  
**Author**: Priya Sharma, Senior Backend Engineer  
**Reviewer**: Dev Kapoor, Engineering Manager  
**Date**: October 2, 2026  
**Status**: Resolved & Closed  

## Executive Summary
On October 2nd at 09:15 UTC, enterprise customer **Acme Corp** reported that outgoing webhook delivery retries were failing systematically after 3 attempts. This was tracked under ticket **TCK-101** and logged as critical bug **LOOP-482**.

## Root Cause Analysis
Priya Sharma investigated the webhook dispatch queue in the notification microservice. The retry scheduler was configured with a fixed 1-second delay instead of exponential backoff with jitter. Under transient network hiccups, customer webhook endpoints were overwhelmed by rapid retries, resulting in rate-limit 429 drops.

## Remediation & Resolution
- **Priya Sharma** refactored the retry dispatcher to implement truncated exponential backoff (initial delay 2s, max delay 60s, randomized jitter).
- Deployed hotfix to production on October 3rd at 14:20 UTC.
- Verification confirmed Acme Corp webhook delivery success reached 99.98%.
- Dev Kapoor reviewed and signed off on the postmortem on October 4th.

## Related Engineering Documentation
- Rate Limiting Guide: Maintained by Rahul Verma (Frontend Engineer). Followed bug LOOP-501 reported by Globex Inc, default limit was raised to 500 req/min with Dev Kapoor's approval.
- Loopwave Onboarding Guide: Maintained by Meera Nair (Support Lead) for webhook endpoint and API key configuration.
