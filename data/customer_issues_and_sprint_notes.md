# Customer Support Tickets & Sprint Decisions Log

**Document ID**: DOC-SYNC-2026-10  
**Maintained By**: Meera Nair, Customer Support Lead  
**Contributors**: Rahul Verma (Frontend Engineer), Dev Kapoor (Engineering Manager), Priya Sharma (Backend Engineer)  

## Active Customer Support Tickets

### Ticket TCK-101
- **Customer**: Acme Corp  
- **Reported By**: Meera Nair, Support Lead  
- **Issue Description**: Webhook delivery retries are failing after 3 attempts.  
- **Associated Bug**: Tracked as bug LOOP-482.  
- **Assignee**: Priya Sharma, Backend Engineer, assigned for investigation.  
- **Resolution**: Resolved by implementing exponential backoff with jitter.  

### Ticket TCK-107
- **Customer**: Globex Inc  
- **Reported By**: Meera Nair, Support Lead  
- **Issue Description**: API requests hitting rate limit errors too quickly during bulk sync.  
- **Associated Bug**: Tracked as bug LOOP-501.  
- **Assignee**: Rahul Verma, Frontend Engineer.  
- **Resolution**: Default API rate limit increased from 100 to 500 requests per minute with Dev Kapoor's approval.  

### Ticket TCK-112
- **Customer**: Initech  
- **Reported By**: Meera Nair, Support Lead  
- **Issue Description**: Dashboard analytics charts are not loading on customer portal.  
- **Associated Bug**: Tracked as bug LOOP-517.  
- **Assignee**: Rahul Verma, Frontend Engineer.  
- **Resolution**: Prioritized for upcoming sprint cycle.  

## Sprint Meeting Notes & Strategic Decisions

### Incident Review Meeting (October 2nd)
- **Attendees**: Priya Sharma, Dev Kapoor, Meera Nair.  
- **Discussion**: Analyzed bug LOOP-482 reported by customer Acme Corp. Root cause was identified as fixed retry delay.  
- **Action Item**: Priya Sharma committed to implement exponential backoff and ship a production hotfix within 24 hours.  

### Sprint Planning Meeting (October 5th)
- **Attendees**: Rahul Verma, Dev Kapoor.  
- **Discussion**: Reviewed rate limit bug LOOP-501 reported by Globex Inc.  
- **Decision**: Rahul Verma increased default rate limit from 100 to 500 requests per minute. Dev Kapoor approved deployment.  

### Support Sync Meeting (October 8th)
- **Attendees**: Meera Nair, Rahul Verma, Dev Kapoor.  
- **Discussion**: Meera Nair raised Initech customer ticket TCK-112 regarding dashboard charts (LOOP-517).  
- **Decision**: Rahul Verma assigned to lead LOOP-517 fix in the next sprint cycle since he is actively maintaining frontend modules.
