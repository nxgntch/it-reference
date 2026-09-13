# Cost Analysis Report Generator - Implementation Plan

**Created**: 2026-09-12  
**Phase**: 2 - Planning (Superpowers methodology)  
**Status**: Task decomposition complete

---

## Task Breakdown

### Task 1: Cost Data Loader
**File**: `cost_analyzer.py` (core module)

**Responsibility**:
- Query tasks table from database
- Filter by date range, agent, operation type
- Return list of task cost records

**Interface**:
```python
def load_costs(
    db,
    start_date: str,
    end_date: str,
    agent_id: Optional[str] = None,
    operation_type: Optional[str] = None
) -> List[TaskCost]:
    """Load task costs from database."""
    pass
```

**Acceptance**:
- [ ] Queries 10,000+ tasks in <2 seconds
- [ ] Returns TaskCost namedtuple with all fields
- [ ] Handles date filtering correctly
- [ ] Returns empty list if no data (no crash)

**Estimated LOC**: 20-30 lines

---

### Task 2: Cost Analyzer
**File**: `cost_analyzer.py` (analyzer module)

**Responsibility**:
- Aggregate costs by agent, operation type, time period
- Calculate statistics (sum, avg, P50, P95, P99)
- Detect anomalies (days 2x+ average)
- Calculate forecasts (daily avg, monthly/yearly projection)

**Interface**:
```python
class CostAnalyzer:
    def __init__(self, tasks: List[TaskCost]):
        """Initialize with task list."""
        self.tasks = tasks
    
    def aggregate_by_agent(self) -> Dict[str, float]:
        """Sum costs per agent."""
        pass
    
    def daily_breakdown(self) -> List[DailyStats]:
        """Aggregate by day."""
        pass
    
    def statistics(self) -> Stats:
        """Calculate P50, P95, P99, std_dev."""
        pass
    
    def detect_anomalies(self) -> List[Anomaly]:
        """Find days 2x+ average cost."""
        pass
    
    def forecast(self) -> Forecast:
        """Project 30-day and 1-year costs."""
        pass
```

**Acceptance**:
- [ ] Aggregation accurate (verified against manual count)
- [ ] Statistics correct (test with known data)
- [ ] Anomalies detected (at least one if data has spikes)
- [ ] Forecasts reasonable (projection > current rate)

**Estimated LOC**: 60-80 lines

---

### Task 3: Report Formatter
**File**: `cost_analyzer.py` (reporter module)

**Responsibility**:
- Format costs into human-readable text report
- Serialize to JSON
- Handle special cases (no data, single task, etc.)

**Interface**:
```python
class ReportFormatter:
    def __init__(self, analysis: Analysis):
        """Initialize with analysis result."""
        self.analysis = analysis
    
    def text_report(self) -> str:
        """Generate human-readable report."""
        pass
    
    def json_report(self) -> Dict:
        """Generate JSON report."""
        pass
```

**Acceptance**:
- [ ] Text report is readable (no raw data dumps)
- [ ] JSON is valid and parseable
- [ ] Handles empty data gracefully
- [ ] Numbers formatted correctly (2 decimal places for currency)

**Estimated LOC**: 50-70 lines

---

### Task 4: CLI Handler
**File**: `scripts/cost-analyzer.py` (entry point)

**Responsibility**:
- Parse command-line arguments
- Validate inputs (date format, etc.)
- Call loader, analyzer, formatter
- Output results or write to file
- Handle errors gracefully

**Interface**:
```python
def main():
    """CLI entry point."""
    args = parse_args()
    
    db = connect_database()
    costs = load_costs(db, args.from_date, args.to_date, ...)
    
    if not costs:
        print("No data found for specified filters")
        return 1
    
    analysis = CostAnalyzer(costs).analyze()
    
    if args.format == "json":
        report = ReportFormatter(analysis).json_report()
        print(json.dumps(report, indent=2))
    else:
        report = ReportFormatter(analysis).text_report()
        print(report)
    
    return 0
```

**Acceptance**:
- [ ] All CLI arguments work
- [ ] Help text displays correctly
- [ ] Exit codes: 0 success, 1 error
- [ ] Errors are user-friendly (not stack traces)

**Estimated LOC**: 40-60 lines

---

### Task 5: Test Suite
**File**: `tests/test_cost_analyzer.py`

**Coverage**:
- [ ] Test data loading (with/without filters)
- [ ] Test aggregation (by agent, by operation, by day)
- [ ] Test statistics (with known data, verify P50/P95/P99)
- [ ] Test anomaly detection (with spiked data)
- [ ] Test formatting (text and JSON output)
- [ ] Test CLI (with various argument combinations)
- [ ] Test edge cases (no data, single task, outliers)

**Acceptance**:
- [ ] 90%+ code coverage
- [ ] All tests pass
- [ ] No flaky tests (run 3x, all pass)
- [ ] Performance tests included (verify <5s queries)

**Estimated LOC**: 120-150 lines

---

## Total Scope

| Task | LOC Baseline | LOC Minimal (Ponytail) | Target |
|------|--------------|----------------------|--------|
| Loader | 30 | 25 | Remove config class |
| Analyzer | 80 | 55 | Remove custom exceptions |
| Formatter | 70 | 45 | Direct formatting |
| CLI | 60 | 35 | Minimal arg parsing |
| Tests | 150 | 130 | Keep comprehensive |
| **Total** | **390** | **290** | **<300 LOC** ✅ |

**Ponytail savings**: ~100 LOC (26% reduction from baseline)

---

## Dependencies

- Python 3.10+
- SQLAlchemy (for database access) - already available
- No external dependencies for core logic
- pytest for testing

---

## Execution Strategy

1. **Task 1** (Loader): 5 min - straightforward database query
2. **Task 2** (Analyzer): 10 min - core logic, well-defined algorithm
3. **Task 3** (Formatter): 8 min - formatting logic
4. **Task 4** (CLI): 7 min - argument parsing and orchestration
5. **Task 5** (Tests): 15 min - comprehensive test coverage

**Estimated total autonomous execution**: 45 minutes of agent time (~25 turns)

---

## Ponytail Minimalism Approach

**What we WILL minimize**:
- ❌ Config classes → Use module-level constants
- ❌ Custom exceptions → Use ValueError, TypeError
- ❌ Data classes → Use namedtuples or dicts
- ❌ ORM abstractions → Direct SQL queries
- ❌ Logging → Only on errors

**What we WON'T minimize** (required):
- ✅ Type hints (required by standard)
- ✅ Docstrings (required on public functions)
- ✅ Error handling (required for robustness)
- ✅ Tests (required for validation)
- ✅ Comments on algorithms (required if non-obvious)

---

## Phase 2 Results

✅ **Planning Complete**
- [x] 5 concrete tasks identified
- [x] Total scope: ~290 LOC (minimalism target)
- [x] Dependencies clear (only stdlib + SQLAlchemy)
- [x] Execution strategy defined (45 min est.)
- [x] Ready for Phase 3 SDD execution

**Next**: Phase 3 - Autonomous implementation

