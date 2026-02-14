# Zerve Platform Usage Success Analysis

## Project Description

This project delivers a fully reproducible, end-to-end behavioral analysis built 
entirely within **Zerve**, the agentic development environment for data professionals. 
The objective is to understand what drives successful long-term usage of the Zerve platform 
by analyzing user interaction events, workflow execution patterns, and engagement signals.

All data inspection, transformation, analysis, and modeling were executed using Zerve blocks 
with no external datasets or offline processing. 
The workflow progresses from raw CSV ingestion to validated insights 
and interpretable success definitions, ensuring every result can be reproduced 
from start to finish within a single Zerve project.

The analysis focuses on identifying meaningful behavioral thresholds that distinguish trial 
users from active and power users, with special emphasis on execution-driven workflows, 
tool invocation frequency, and paid commitment through credit usage.

---

## Problem Statement

While Zerve captures detailed event-level analytics, raw event data alone does not clearly 
define what “success” looks like on the platform. 
The challenge is to translate low-level interaction events into a structured, 
measurable definition of user success.

This project answers the following questions:

- What behavioural patterns distinguish successful users from trial users?
- Which actions best predict long-term engagement?
- Can early user behaviour signal future success?
- How do execution events, tool usage, and credit consumption influence outcomes?

---

## Dataset Overview

- **Rows:** 409,287 event records  
- **Columns:** 107 event and property fields  
- **Source:** Platform event tracking via PostHog  
- **Granularity:** Event-level user interactions  

Each row represents a single user interaction event with associated metadata including session 
context, browser information, execution activity, and engagement signals.

---

## Methodology: Step-by-Step Solution

### 1. Data Ingestion & Initial Inspection

- Imported the raw CSV dataset directly into Zerve
- Verified dataset dimensions, column structure, and data types
- Identified core identifiers (`distinct_id`, `person_id`, `session_id`) and event timestamps
- Confirmed data quality and structural integrity

**Outcome:** A clean, production-grade analytics dataset suitable for behavioural analysis

---

### 2. Event & User Structure Analysis

- Examined the distribution and meaning of event types
- Validated consistency across user and session identifiers
- Analyzed null patterns across properties to understand event applicability
- Distinguished user-level, session-level, and event-level features

**Outcome:** Clear understanding of how user actions are represented in the data

---

### 3. Feature Engineering

Derived user-level metrics including:

- Total events per user
- Days active and session frequency
- Unique event types (workflow diversity)
- Tool invocation count
- Execution events (code runs)
- Credit usage and paid engagement indicators

These features transform raw event logs into interpretable behavioral signals.

---

### 4. User Segmentation & Success Tiers

Users were segmented into five distinct success tiers based on engagement intensity:

- Power Users
- Active Users
- Regular Users
- Casual Users
- Trial Users

Each tier exhibits dramatically different behavior in terms of activity frequency, workflow depth, 
and tool usage.

**Outcome:** A clear behavioural gradient from exploration to power usage

---

### 5. Correlation & Success Driver Analysis

Analyzed correlations between user features and sustained engagement (7+ active days):

Key predictors identified:

- Tool invocation frequency
- Early activity intensity
- Workflow completeness
- Credit usage

**Outcome:** Quantitative validation of the strongest success drivers

---

### 6. Workflow & Sequence Pattern Analysis

- Examined event sequences of high-performing users
- Identified recurring execution-heavy workflows
- Analyzed session-level completeness across workflow categories

**Outcome:** Evidence that execution and automation drive success more than passive exploration

---

### 7. Composite Success Modeling

Developed a composite success framework balancing:

- Sustained usage (time-based engagement)
- Workflow depth (behavioral diversity)
- Serious engagement (credits and execution)

This model aligns closely with observed power-user behavior.

---

## Definition of User Success

### Power User Threshold
- ≥1 credit used
- ≥7 days active
- ≥20 unique event types
- Heavy tool invocation and execution activity

### Active User Threshold
- Multiple sessions across ≥2 days
- Moderate workflow diversity
- Regular execution events

### At-Risk Trial Indicators
- Zero credits after first week
- Single-session usage
- No execution or tool activity

---

## Key Insights

- Early momentum strongly predicts long-term success
- Tool-centric, execution-driven workflows outperform exploratory usage
- Credit usage represents a critical behavioral threshold
- Successful users build multi-step, reproducible workflows

---

## Conclusion

Successful usage of the Zerve platform is driven by early engagement, repeated tool invocation, 
and execution-focused workflows. Users who commit to automation and reproducible pipelines quickly 
differentiate themselves from trial users and demonstrate sustained platform value.

This project demonstrates how Zerve’s agentic, execution-first environment enables deep behavioural 
insight while maintaining full reproducibility and analytical rigor.