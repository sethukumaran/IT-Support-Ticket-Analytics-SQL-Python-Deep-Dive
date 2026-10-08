# IT-Support-Ticket-Analytics-SQL-Python-Deep-Dive

## 1. Project Overview

This project performs an end-to-end analysis of a synthetic IT support ticket dataset containing **100,000 tickets** across **9,999 customers** from **January 2022 to December 2025**.

The analysis is designed as a portfolio-quality Data Analyst project and combines:

- Python-based Exploratory Data Analysis (EDA)
- Data quality assessment
- Business KPI analysis
- SQL-based operational analysis
- Customer-support performance analysis
- Trend analysis
- Segmentation by issue, product, priority, channel, customer segment, SLA plan, platform and region
- Customer sentiment and CSAT analysis
- Operational risk identification
- Visualization and business recommendations

> **Important:** The dataset is synthetic. Business recommendations are therefore analytical demonstrations rather than claims about a real support organization.

---

## 2. Business Problem

An IT support organization wants to understand:

1. How large is the support workload?
2. How much of the queue is unresolved?
3. Which issue types create the greatest customer dissatisfaction?
4. Which product areas need the most attention?
5. How effectively are priorities being handled?
6. Which channels perform better?
7. Which customer segments or SLA plans show elevated operational risk?
8. Are negative sentiment and CSAT concentrated in specific issue categories?
9. Where should management focus process improvement and support capacity?

---

## 3. Dataset

**File:** `synthetic_it_support_tickets.csv`

### Main fields

| Column | Description |
|---|---|
| `ticket_id` | Unique support ticket identifier |
| `created_at` | Ticket creation timestamp |
| `customer_id` | Customer identifier |
| `customer_segment` | Customer segment |
| `channel` | Support intake channel |
| `product_area` | Product area associated with the ticket |
| `issue_type` | Type of support issue |
| `priority` | Ticket priority |
| `status` | Current ticket status |
| `sla_plan` | Customer SLA plan |
| `initial_message` | Customer's initial support message |
| `agent_first_reply` | Agent's first response text |
| `resolution_summary` | Resolution summary |
| `resolution_time_hours` | Resolution duration in hours |
| `reopened` | Reopen indicator |
| `customer_sentiment` | Customer sentiment |
| `csat_score` | Customer satisfaction score |
| `has_attachment` | Attachment indicator |
| `platform` | Platform involved |
| `region` | Customer region |

---

# 4. Executive KPI Summary

| KPI | Result |
|---|---:|
| Total tickets | **100,000** |
| Unique customers | **9,999** |
| Analysis period | **2022-01-01 to 2025-12-30** |
| Resolved tickets | **50.13%** |
| Operational backlog | **39.89%** |
| Closed without action | **9.98%** |
| Reopen rate | **5.05%** |
| Average CSAT | **2.24 / 5** |
| Negative / very negative sentiment | **42.45%** |
| Median resolution time | **23.53 hours** |
| Average resolution time | **27.77 hours for resolved tickets** |
| High-risk unresolved tickets | **4,284** |

### Backlog definition

For this analysis, backlog is defined as:

- `open`
- `in_progress`
- `on_hold`

These statuses collectively represent **39.89% of all tickets**.

---

# 5. Exploratory Data Analysis — EDA

## 5.1 Dataset structure

The dataset contains:

- 100,000 rows
- 20 original columns
- categorical, timestamp and numeric fields
- one unique ticket ID per ticket
- no duplicate rows
- no duplicate ticket IDs

## 5.2 Data-quality findings

### Missing values

| Field | Missing |
|---|---:|
| `region` | **19,997 / 20.00%** |
| `resolution_summary` | **39,887 / 39.89%** |
| `resolution_time_hours` | **39,887 / 39.89%** |

The missing resolution fields align with tickets that are still open/in progress/on hold.

The `agent_first_reply` column is **text content**, not a timestamp. Therefore, a true first-response-time KPI cannot be calculated from this field without an actual response timestamp.

### Data-quality recommendation

Add these fields to a production support dataset:

- `agent_first_reply_at`
- `resolved_at`
- `closed_at`
- `sla_due_at`
- `sla_breached`
- `escalation_flag`
- `agent_id`
- `team_id`

These fields would enable true SLA, response-time and agent productivity analysis.

---

# 6. Major Business Findings

## Finding 1 — Backlog is the biggest operational concern

Approximately **39.89% of tickets are still in an operational backlog state**.

The largest status categories are:

- Resolved: 50.13%
- In progress: 19.78%
- On hold: 10.17%
- Closed without action: 9.98%
- Open: 9.94%

### Business implication

The organization has a significant amount of unresolved work. Management should focus on:

- backlog aging
- queue ownership
- escalation rules
- staffing by workload
- automation for repetitive issues
- root-cause elimination

---

## Finding 2 — Customer satisfaction is weak

Average CSAT is only **2.24 / 5**.

Approximately **42.45% of tickets have negative or very negative sentiment**.

This indicates that ticket closure alone is not sufficient. The organization should optimize for **resolution quality and customer experience**, not simply ticket throughput.

---

## Finding 3 — Account access, performance and security are the most problematic issue types

### Lowest CSAT issue types

| Issue type | Avg CSAT | Negative sentiment |
|---|---:|---:|
| Account access | **1.97** | **59.7%** |
| Performance | **1.97** | **60.2%** |
| Security concern | **1.97** | **60.4%** |
| Billing problem | **1.98** | **59.7%** |

These four issue groups are the clearest customer-experience problem areas.

### Highest CSAT

`how_to` tickets have approximately **2.61 / 5 CSAT** and only **19.3% negative sentiment**.

### Business recommendation

Prioritize:

1. Login and account recovery automation
2. Performance monitoring and proactive incident detection
3. Security incident playbooks
4. Billing-error prevention
5. Better self-service documentation for common issues

---

## Finding 4 — Priority handling appears directionally sensible

Average resolution time decreases as priority increases:

| Priority | Avg resolution time |
|---|---:|
| Low | **55.61 hrs** |
| Medium | **43.28 hrs** |
| High | **31.56 hrs** |
| Urgent | **26.71 hrs** |

This suggests that higher-priority tickets receive faster attention.

However, **2,044 urgent tickets remain in the backlog**, so urgent-ticket queue management deserves monitoring.

---

## Finding 5 — Product areas have relatively similar ticket volumes

Ticket volume is distributed fairly evenly across the seven product areas.

The lowest average CSAT among the major product areas is **billing**, at approximately **2.22 / 5**.

### Business recommendation

Do not allocate resources only according to ticket volume. Combine:

- ticket volume
- CSAT
- negative sentiment
- resolution time
- reopen rate
- backlog rate

A lower-volume product can still be strategically important if it generates severe customer dissatisfaction.

---

## Finding 6 — Channel performance is relatively stable

The five support channels have similar ticket volumes and broadly similar KPIs.

Average CSAT is approximately in the **2.23–2.26** range across channels.

This means there is no dramatic channel-performance gap in this dataset.

### Recommendation

Rather than immediately shifting volume between channels, investigate:

- issue mix by channel
- agent/team assignment
- escalation rate
- response time
- customer segment by channel

---

## Finding 7 — SLA plans do not show a large performance separation

Standard, Gold and Platinum plans have broadly similar resolution and backlog rates.

Platinum customers have approximately **40.9% backlog**, which is slightly higher than Standard.

This could indicate that premium customers are receiving more complex tickets or that premium-service expectations are not being fully translated into operational performance.

### Recommendation

Segment SLA analysis by:

- priority
- issue type
- customer segment
- resolution time
- SLA breach
- escalation

Do not judge SLA performance using only overall averages.

---

# 7. High-Risk Queue

A high-risk ticket is defined here as:

- unresolved/backlog status
- high or urgent priority
- negative or very negative sentiment

This produces **4,284 high-risk tickets**.

This should be treated as a management-priority queue.

### Recommended workflow

1. Identify all high-risk tickets.
2. Sort by age.
3. Escalate urgent tickets.
4. Assign clear ownership.
5. Track daily reduction in high-risk backlog.
6. Perform root-cause analysis for recurring issue types.

---

# 8. Customer Concentration

The dataset contains **9,999 customers**.

The top 10 customers generated **223 tickets**, representing approximately **0.22% of all tickets**.

This suggests that ticket demand is not heavily concentrated among a small number of customers.

---

# 9. Trend Analysis

Monthly ticket volumes remain relatively stable across the four-year period.

The highest monthly ticket volume occurs around **July 2023**, with approximately **2,263 tickets**.

The dataset therefore does not show an extreme long-term workload explosion; the major business challenge is more closely related to **resolution quality, backlog and customer satisfaction**.

---

# 10. SQL Analysis

The project includes `sql_analysis.sql` containing business-focused SQL queries for:

- Executive KPIs
- Status distribution
- Monthly trends
- Issue-type performance
- Product performance
- Priority performance
- Channel comparison
- Customer segment analysis
- SLA plan analysis
- Regional analysis
- Customer ticket concentration
- High-risk queue identification

The queries are written using common SQL patterns such as:

- `GROUP BY`
- `CASE WHEN`
- `COUNT`
- `AVG`
- window functions
- conditional aggregation
- ranking / ordering
- date extraction

---

# 11. Python Analysis

`analysis.py` performs:

### EDA

- Dataset shape
- Data types
- Missing values
- Duplicate checks
- Numeric summaries
- categorical distributions
- data-quality inspection

### Feature engineering

- resolved flag
- backlog flag
- negative sentiment flag
- year-month field

### KPI analysis

- resolution rate
- backlog rate
- reopen rate
- CSAT
- sentiment
- resolution time

### Segmentation

- issue type
- product area
- channel
- priority
- customer segment
- SLA plan
- platform
- region

# 13. Business Recommendations

## Priority 1 — Reduce backlog

Create a dedicated backlog-management process.

Track:

- backlog size
- backlog aging
- owner
- priority
- issue type
- SLA risk

## Priority 2 — Fix high-dissatisfaction issues

Focus engineering and support collaboration on:

- account access
- performance
- security
- billing

These areas combine low CSAT with high negative sentiment.

## Priority 3 — Improve data collection

Capture actual timestamps for:

- first response
- resolution
- closure
- SLA deadline

This enables:

- First Response Time
- Mean Time to Resolution
- SLA compliance
- SLA breach rate
- aging analysis

## Priority 4 — Introduce proactive support

Use recurring issue patterns to create:

- knowledge-base articles
- self-service workflows
- automated account recovery
- proactive performance alerts
- billing validation
- security notifications

## Priority 5 — Measure quality, not only volume

A support team should not be judged only by:

> Tickets closed

A stronger scorecard should include:

> Ticket volume + backlog + resolution time + CSAT + sentiment + reopen rate + SLA compliance

# 18. Final Conclusion

The analysis shows that the primary challenge is **not ticket demand alone; it is the combination of backlog, low customer satisfaction and high negative sentiment in specific issue categories**.

The organization resolves approximately half of all tickets, while nearly **40% remain in an active backlog state**. Customer experience is also weak, with an average CSAT of only **2.24/5** and approximately **42.45% negative or very negative sentiment**.

The strongest opportunity is to focus operational and engineering resources on **account access, performance, security and billing issues**, which have the lowest CSAT and highest negative sentiment. Priority handling appears directionally effective because urgent tickets have substantially lower average resolution times than low-priority tickets, but the presence of more than **2,000 unresolved urgent tickets** indicates that the urgent queue still needs active management.

From a data perspective, the next major improvement should be better timestamp and SLA instrumentation. Capturing first-response time, resolution time, SLA deadline and SLA-breach status would allow the organization to move from descriptive reporting to a complete operational-performance management system.

