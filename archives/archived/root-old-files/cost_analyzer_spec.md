# Cost Analysis Report Generator - Specification

**Created**: 2026-09-12  
**Feature**: Cost Analysis Report Generator CLI  
**Phase**: 1 - Brainstorming (Superpowers methodology)

---

## Feature Overview

Generate cost analysis reports from task execution data to provide visibility into agent spending patterns, trends, and optimization opportunities.

**Problem**: Teams executing agents don't have visibility into:
- Which agents cost the most
- Cost trends over time (daily, weekly, monthly)
- Anomalous spending patterns
- Forecast of monthly/annual costs at current run rate

**Solution**: CLI tool that generates reports with:
- Cost aggregation by agent, operation type, time period
- Trend analysis (moving averages, forecasts)
- Anomaly detection (unusual spikes)
- Text summary + JSON export

---

## Acceptance Criteria

### Input Requirements
- [x] Date range filtering (start_date, end_date)
- [x] Agent ID filtering (single agent or all)
- [x] Cost threshold filtering (show only >$X)
- [x] Operation type filtering (model_call, api_call, database_query)
- [x] Report format choice (text, json, both)

### Output Requirements
- [x] **Text Report**: Human-readable summary with key metrics
- [x] **JSON Report**: Structured data for integration
- [x] **Metrics included**:
  - Total costs (by agent, by operation, by day)
  - Average cost per task
  - Cost distribution (P50, P95, P99)
  - Trend: daily average, weekly average
  - Forecast: 30-day projection at current rate
  - Anomalies: days with 2x+ average cost

### Query Requirements
- [x] Load cost data from database (tasks table)
- [x] Aggregate by agent_id
- [x] Aggregate by operation type
- [x] Aggregate by day/week/month
- [x] Calculate statistics (sum, avg, min, max, percentiles)

### Performance Requirements
- [x] Query 10,000+ tasks in <5 seconds
- [x] Generate report in <1 second
- [x] Memory usage <100MB for large datasets
- [x] CLI responds in <10 seconds total

### Error Handling
- [x] Invalid date range → Clear error message
- [x] No data found → Report "no data" instead of crash
- [x] Database unavailable → Graceful fallback
- [x] Invalid filters → Show help text

### Edge Cases
- [x] No agents executing (empty result)
- [x] Single task vs 10,000+ tasks
- [x] Date range with no data
- [x] All tasks same cost (no variance)
- [x] Extreme outliers (one 100x cost task)

---

## Data Model

### Input: Task Cost Records

```
task_history {
  id: str
  agent_id: str
  operation_type: str (model_call | api_call | database_query | storage)
  cost_cents: int
  created_at: datetime
  duration_ms: int
}
```

### Output: Report

```json
{
  "period": {
    "start_date": "2026-09-01",
    "end_date": "2026-09-12",
    "days": 12
  },
  "summary": {
    "total_tasks": 1250,
    "total_cost_dollars": 42.50,
    "average_cost_per_task": 0.034,
    "agents_count": 5
  },
  "by_agent": [
    {
      "agent_id": "research-001",
      "cost_dollars": 25.30,
      "task_count": 500,
      "avg_cost_per_task": 0.051
    }
  ],
  "by_operation": [
    {
      "operation": "model_call",
      "cost_dollars": 35.20,
      "percentage": 82.8
    }
  ],
  "daily_breakdown": [
    {
      "date": "2026-09-01",
      "cost_dollars": 3.50,
      "task_count": 100
    }
  ],
  "statistics": {
    "min_cost": 0.0001,
    "max_cost": 1.25,
    "p50": 0.015,
    "p95": 0.150,
    "p99": 0.500,
    "std_dev": 0.045
  },
  "forecast": {
    "daily_average": 3.54,
    "monthly_projection": 106.20,
    "yearly_projection": 1274.40
  },
  "anomalies": [
    {
      "date": "2026-09-05",
      "cost_dollars": 7.80,
      "reason": "2.2x daily average"
    }
  ],
  "recommendations": [
    {
      "type": "high_cost_agent",
      "agent_id": "research-001",
      "cost_dollars": 25.30,
      "suggestion": "Consider using cheaper model for research agent"
    }
  ]
}
```

---

## CLI Interface

### Usage

```bash
# Basic report (all agents, last 7 days, text output)
cost-analyzer --period 7d

# Specific date range
cost-analyzer --from 2026-09-01 --to 2026-09-12

# Single agent
cost-analyzer --agent research-001

# Filter by cost threshold
cost-analyzer --min-cost 0.05

# JSON output
cost-analyzer --format json > report.json

# Combined
cost-analyzer --agent engineering-001 --from 2026-09-01 --format json
```

### Help Text

```
cost-analyzer - Generate cost analysis reports

USAGE:
  cost-analyzer [OPTIONS]

OPTIONS:
  --period DAYS         Last N days (default: 7)
  --from DATE           Start date (YYYY-MM-DD)
  --to DATE             End date (YYYY-MM-DD)
  --agent ID            Filter by agent ID
  --operation TYPE      Filter by operation (model_call, api_call, etc)
  --min-cost DOLLARS    Show only costs >= threshold
  --format FORMAT       Output format: text|json (default: text)
  --help                Show this help

EXAMPLES:
  cost-analyzer --period 30  # Last 30 days
  cost-analyzer --agent research-001  # Single agent
  cost-analyzer --from 2026-09-01 --to 2026-09-12 --format json
```

---

## Success Metrics (Phase 4)

| Metric | Target | Success Indicator |
|--------|--------|-------------------|
| **Spec clarity** | 0 ambiguities | Acceptance criteria all clear |
| **Task decomposition** | 4-5 tasks | Implementation plan feasible |
| **Complexity** | Medium | Good test for full stack |
| **Estimated LOC** | 250-350 baseline | 75-100 with ponytail |
| **Test coverage goal** | >90% | Comprehensive testing |

---

## Phase 1 Results

✅ **Brainstorming Complete**
- Feature clearly specified with 7 acceptance criteria
- Data model documented
- CLI interface defined
- Edge cases identified
- Ready for Phase 2 Planning

