DOCS = [
"""[DOC] Webhook Retry Incident Postmortem
Author: Priya Sharma, Backend Engineer.
On October 2nd, customer Acme Corp reported that webhook retries were failing
after 3 attempts, tracked as bug LOOP-482. Priya Sharma investigated and found
the retry logic used a fixed 1-second delay instead of exponential backoff.
Priya Sharma implemented exponential backoff and deployed the fix on October 3rd.
This postmortem was reviewed by Dev Kapoor, the Engineering Manager.""",

"""[DOC] Rate Limiting Guide
Author: Rahul Verma, Frontend Engineer.
This guide explains Loopwave's API rate limits. Following bug LOOP-501 reported
by customer Globex Inc, Rahul Verma increased the default rate limit from 100
to 500 requests per minute. The change was approved by Dev Kapoor.""",

"""[DOC] Loopwave Onboarding Guide
This guide helps new customers set up their Loopwave account, connect webhooks,
and configure API keys. It is maintained by Meera Nair, Support Lead.""",
]

TICKETS = [
"""[TICKET TCK-101] Filed by Meera Nair, Support Lead, on behalf of customer Acme Corp.
Issue: Webhook retries are failing after 3 attempts. This was logged as bug
LOOP-482 and assigned to Priya Sharma, Backend Engineer, for investigation.""",

"""[TICKET TCK-107] Filed by Meera Nair, Support Lead, on behalf of customer Globex Inc.
Issue: API requests are hitting rate limit errors too quickly. This was logged
as bug LOOP-501 and assigned to Rahul Verma, Frontend Engineer.""",

"""[TICKET TCK-112] Filed by Meera Nair, Support Lead, on behalf of customer Initech.
Issue: Dashboard charts are not loading. This was logged as bug LOOP-517 and
assigned to Rahul Verma, Frontend Engineer.""",
]

NOTES = [
"""[MEETING NOTE] Incident Review, October 2nd.
Attendees: Priya Sharma, Dev Kapoor, Meera Nair.
Discussed bug LOOP-482 reported by customer Acme Corp. Root cause: fixed retry
delay instead of exponential backoff. Decision: Priya Sharma to implement
exponential backoff and ship a fix within 24 hours.""",

"""[MEETING NOTE] Sprint Planning, October 5th.
Attendees: Rahul Verma, Dev Kapoor.
Rahul Verma gave an update on bug LOOP-501 reported by customer Globex Inc.
Decision: increase default API rate limit from 100 to 500 requests per minute.""",

"""[MEETING NOTE] Support Sync, October 8th.
Attendees: Meera Nair, Rahul Verma, Dev Kapoor.
Meera Nair raised customer Initech's complaint about dashboard charts not
loading, bug LOOP-517. Decision: Rahul Verma to prioritize LOOP-517 next sprint,
since he is already working on frontend-related bugs.""",
]

ALL_ITEMS = DOCS + TICKETS + NOTES
