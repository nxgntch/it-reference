# Phase 18.2: Enterprise Scale & Hardening (Planning)

**Overview**: Transforms nxgntch from single-tenant local optimization to enterprise-ready, multi-region, fully-compliant platform. Multi-tenancy, distributed caching, advanced analytics, 99.9% SLA compliance, marketplace v1.0.0. Phase duration 13-14 weeks.

**Status**: 📋 PLANNING | **Start**: 2026-09-06 | **Duration**: 13-14 weeks | **Effort**: Comprehensive enterprise transformation

---

## Strategic Overview

### Objectives

1. **Refactor sync scripts** to use BaseSyncModule (consistency, code reuse)
2. **Automate documentation generation** (reduce manual effort, ensure accuracy)
3. **Modernize CLI interface** (unified experience across tools)
4. **Achieve 95% test coverage** across all scripts

### Why This Matters

- Phase 4 proved base class pattern works (BaseProfiler)
- Sync scripts currently have scattered implementations
- Documentation maintenance is manual and error-prone
- CLI tools have inconsistent interfaces

---

## Phase Structure

### 5.1: Sync Scripts (BaseSyncModule Pattern)

**Goal**: Refactor `scripts/sync/` to use BaseSyncModule

**Scope**:
- Extract common sync patterns → `scripts/sync/base.py` (BaseSyncModule)
- Refactor 5-8 existing sync scripts to inherit BaseSyncModule
- Add dry-run, statistics, and error handling
- 100% test coverage for base class + all sync scripts

**Modules to Refactor**:
- `scripts/sync/repos/` — Repository sync
- `scripts/sync/config/` — Configuration sync
- `scripts/sync/docs/` — Documentation sync
- `scripts/sync/marketplace/` — Marketplace sync (if exists)
- Other sync utilities

**Timeline**: Weeks 1-4 (parallel with 5.2)

**Gate Criteria**:
- [ ] BaseSyncModule implemented (base.py)
- [ ] All sync scripts use BaseSyncModule
- [ ] 95%+ test coverage
- [ ] Dry-run mode working
- [ ] Statistics collected and logged
- [ ] No sync script runs without these patterns

---

### 5.2: Documentation Generation Scripts

**Goal**: Automate doc generation (docs that are currently manual)

**Scope**:
- Identify docs that are manually maintained (phase history, tables, etc.)
- Create generators for: phase status, roadmap, metrics, summaries
- Integrate with skill system (docUpdater, docOptimizer)
- 95%+ test coverage

**Documentation to Automate**:
- `docs/work/current/phase-status.md` — Auto-generated from AUDIT.md
- `docs/work/current/active-tasks.md` — Auto-generated from task tracking
- `docs/work/planned/roadmap.md` — Auto-generated from phase plan
- `AUDIT.md` metrics — Validated and updated automatically
- `LINK_MAP.md` — Cross-reference index (auto-generated)
- Phase completion summaries (auto-generated)

**Implementation**:
- Create `scripts/docs/base.py` (BaseDocGenerator if pattern needed)
- Create generators for each doc type
- Integrate with skill system (runtime + automation)
- Add validation layer (check links, references, structure)

**Timeline**: Weeks 1-4 (parallel with 5.1)

**Gate Criteria**:
- [ ] All identified docs have generators
- [ ] Generators produce valid output
- [ ] 95%+ test coverage
- [ ] Docs can be regenerated in < 5 seconds
- [ ] Cross-references validated (no dead links)
- [ ] Integration with docUpdater skill working

---

### 5.3: CLI Scripts Refactoring

**Goal**: Modernize CLI interface and consolidate common patterns

**Scope**:
- Identify CLI entry points
- Extract common patterns → CLI base (consistent argument parsing, help, logging)
- Refactor all CLI tools to use unified interface
- 95%+ test coverage

**CLI Tools to Refactor**:
- `scripts/cli/` — Main CLI entry point
- `scripts/profiling/` — Profiling CLI
- `scripts/sync/` — Sync CLI (from 5.1)
- `scripts/validate/` — Validation CLI
- `scripts/docs/` — Documentation generation CLI (from 5.2)

**Implementation**:
- Create `scripts/cli/base.py` (BaseCLITool)
- Unified argument parsing, help text, error handling
- Consistent logging output format
- Progress indicators for long operations
- Exit codes and error reporting

**Timeline**: Weeks 4-6 (after 5.1 & 5.2 foundation)

**Gate Criteria**:
- [ ] BaseCLITool implemented
- [ ] All CLI tools use unified interface
- [ ] 95%+ test coverage
- [ ] Consistent help output (--help works everywhere)
- [ ] Consistent error messages and exit codes
- [ ] Progress indicators for long operations
- [ ] No tool-specific quirks (unified UX)

---

## Week-by-Week Schedule

### Week 1: Foundation & Parallel Start
**Duration**: ~30-35 hours  
**Parallel Track A (5.1) & Track B (5.2)**

**Monday-Tuesday (5.1 Foundation)**:
- Design BaseSyncModule interface
- Identify sync scripts to refactor
- Create base.py with core patterns
- Add logging, statistics, dry-run support
- Write base class tests (10-15 tests)

**Monday-Tuesday (5.2 Foundation)**:
- Audit which docs are manually maintained
- Design BaseDocGenerator (if needed)
- Identify automation gaps
- Create scripts/docs/ directory structure
- Write generator base tests

**Wednesday-Friday (Both Tracks)**:
- Start refactoring first 2-3 sync scripts (5.1)
- Create first 2 doc generators (5.2)
- Test coverage for new code
- Integration testing

**End of Week 1 Checkpoint**:
- ✅ BaseSyncModule working with 2-3 scripts
- ✅ 2 doc generators working
- ✅ 80%+ coverage on base classes

---

### Week 2: Parallel Expansion
**Duration**: ~35-40 hours

**Track A (5.1)**:
- Refactor remaining sync scripts (3-4 more)
- Add dry-run mode across all scripts
- Statistics collection and reporting
- Error handling and recovery

**Track B (5.2)**:
- Create remaining doc generators
- Test generators with real AUDIT.md data
- Implement cross-reference validation
- Create regeneration script

**Integration Points**:
- Both tracks test with sample data
- No external dependencies yet (mocked)

**End of Week 2 Checkpoint**:
- ✅ All sync scripts use BaseSyncModule
- ✅ All doc generators working
- ✅ 90%+ coverage on both tracks

---

### Week 3: Testing & Validation
**Duration**: ~30-35 hours

**Track A (5.1)**:
- Comprehensive test coverage (95% target)
- Test dry-run mode thoroughly
- Test error scenarios
- Test statistics accuracy

**Track B (5.2)**:
- Test generators with real documentation
- Validate generated docs (links, references)
- Performance testing (< 5 sec regeneration)
- Test integration with docUpdater skill

**Integration**:
- Test both tracks together (sync + doc generation)
- Verify no conflicts or dependencies

**End of Week 3 Checkpoint**:
- ✅ 5.1: 95%+ coverage, all tests passing
- ✅ 5.2: 95%+ coverage, all tests passing
- ✅ Ready for 5.3 foundation work

---

### Week 4: 5.3 Foundation & Transition
**Duration**: ~40-45 hours

**Parallel Completion (5.1 & 5.2)**:
- Final testing and edge cases
- Performance optimization
- Documentation of patterns
- Prepare for merge

**Sequential Start (5.3)**:
- Design BaseCLITool interface
- Identify all CLI entry points
- Create base.py with unified argument parsing
- Add help generation, logging, progress indicators
- Write base class tests

**Integration Planning**:
- Plan CLI tool refactoring order
- Identify dependencies between CLI tools
- Create refactoring checklist

**End of Week 4 Checkpoint**:
- ✅ 5.1 & 5.2: Complete and tested
- ✅ 5.3: Foundation ready
- ✅ BaseCLITool interface designed

---

### Week 5: CLI Refactoring Phase 1
**Duration**: ~40-45 hours

**Refactor CLI Tools**:
- Refactor profiling CLI (leverage Phase 4 scripts)
- Refactor sync CLI (leverage 5.1 scripts)
- Refactor docs CLI (leverage 5.2 generators)
- Add progress indicators
- Add consistent error handling

**Testing**:
- Unit tests for each refactored tool
- Integration tests (CLI + underlying scripts)
- Manual testing with real commands

**Coverage**:
- Target 95%+ on all CLI tools

**End of Week 5 Checkpoint**:
- ✅ 3-4 CLI tools refactored
- ✅ 90%+ coverage
- ✅ Half of CLI modernization complete

---

### Week 6: CLI Completion & Gate Assessment
**Duration**: ~35-40 hours

**Remaining CLI Tools**:
- Refactor validation CLI
- Refactor any remaining CLI tools
- Unified help and usage documentation

**Final Testing & Coverage**:
- Achieve 95%+ coverage across all CLI tools
- Edge case testing
- Performance testing
- User experience testing

**Documentation**:
- Document unified CLI patterns
- Create CLI tool guide for developers
- Update README for CLI usage

**Gate Assessment**:
- [ ] All criteria met (see below)
- [ ] 95%+ coverage verified
- [ ] All tests passing
- [ ] Ready for merge

**End of Week 6 Checkpoint**:
- ✅ Phase 5 complete
- ✅ 95%+ coverage across all sub-phases
- ✅ Ready for gate assessment

---

## Task Inventory

### Phase 5.1: Sync Scripts (Weeks 1-4)

**Foundation** (Week 1):
- [ ] Design BaseSyncModule interface (2h)
- [ ] Implement base.py with core patterns (4h)
- [ ] Add logging and statistics collection (3h)
- [ ] Write base class tests (5h)
- [ ] Total: ~14h

**Refactoring** (Weeks 2-3):
- [ ] Identify all sync scripts (1h)
- [ ] Refactor script 1 (3h + 2h tests)
- [ ] Refactor script 2 (3h + 2h tests)
- [ ] Refactor script 3 (3h + 2h tests)
- [ ] Refactor script 4 (3h + 2h tests)
- [ ] Refactor script 5 (3h + 2h tests) — if exists
- [ ] Add dry-run mode to all (4h)
- [ ] Total: ~40-50h

**Testing & Validation** (Week 3):
- [ ] Comprehensive unit tests (8h)
- [ ] Integration tests (6h)
- [ ] Performance testing (4h)
- [ ] Edge case coverage (4h)
- [ ] Total: ~22h

**5.1 Total**: ~76-86h

---

### Phase 5.2: Documentation Generation (Weeks 1-4)

**Foundation** (Week 1):
- [ ] Audit manual docs (2h)
- [ ] Design doc generator patterns (3h)
- [ ] Create scripts/docs/ structure (1h)
- [ ] Write base tests (4h)
- [ ] Total: ~10h

**Implementation** (Weeks 2-3):
- [ ] Create phase-status generator (4h + 2h tests)
- [ ] Create active-tasks generator (4h + 2h tests)
- [ ] Create roadmap generator (4h + 2h tests)
- [ ] Create AUDIT.md validator (4h + 2h tests)
- [ ] Create LINK_MAP generator (5h + 3h tests)
- [ ] Create phase-summary generator (4h + 2h tests)
- [ ] Total: ~38-42h

**Validation & Integration** (Week 3):
- [ ] Cross-reference validation (4h + 2h tests)
- [ ] Performance testing (2h)
- [ ] Skill integration (docUpdater) (4h)
- [ ] Edge case testing (4h)
- [ ] Total: ~16-18h

**5.2 Total**: ~64-70h

---

### Phase 5.3: CLI Refactoring (Weeks 4-6)

**Foundation** (Week 4):
- [ ] Design BaseCLITool interface (3h)
- [ ] Implement base.py (5h)
- [ ] Add argument parsing utilities (4h)
- [ ] Add help/logging/progress (4h)
- [ ] Write base tests (6h)
- [ ] Total: ~22h

**Refactoring** (Weeks 5-6):
- [ ] Refactor profiling CLI (4h + 3h tests)
- [ ] Refactor sync CLI (4h + 3h tests)
- [ ] Refactor docs CLI (4h + 3h tests)
- [ ] Refactor validation CLI (4h + 3h tests)
- [ ] Refactor remaining CLIs (if any) (8h + 6h tests)
- [ ] Total: ~42-48h

**Final Testing & Documentation** (Week 6):
- [ ] CLI integration tests (6h)
- [ ] Manual CLI testing (4h)
- [ ] User experience review (3h)
- [ ] Documentation and guides (5h)
- [ ] Edge case coverage (4h)
- [ ] Total: ~22h

**5.3 Total**: ~86-92h

---

## Phase 5 Gate Criteria

### 5.1 Gate: Sync Scripts Complete

- [ ] **Implementation**: All sync scripts use BaseSyncModule
- [ ] **Testing**: 95%+ coverage (base.py + all sync scripts)
- [ ] **Features**: Dry-run mode, statistics, error handling working
- [ ] **Performance**: No regression vs. original scripts
- [ ] **Documentation**: BaseSyncModule patterns documented

### 5.2 Gate: Documentation Generation Complete

- [ ] **Implementation**: All identified docs have working generators
- [ ] **Testing**: 95%+ coverage (generators + validation)
- [ ] **Accuracy**: Generated docs valid and up-to-date
- [ ] **Performance**: Regeneration < 5 seconds
- [ ] **Integration**: docUpdater skill working

### 5.3 Gate: CLI Refactoring Complete

- [ ] **Implementation**: All CLI tools use BaseCLITool
- [ ] **Testing**: 95%+ coverage (base.py + all CLI tools)
- [ ] **UX**: Consistent help, errors, progress across all tools
- [ ] **Documentation**: CLI usage guide created

### Phase 5 Final Gate

- [ ] **Coverage**: 95%+ across all modules (5.1, 5.2, 5.3)
- [ ] **Tests**: All 1000+ tests passing
- [ ] **Commits**: Clean git history, conventional commits
- [ ] **Documentation**: All patterns documented, guide created
- [ ] **No Regressions**: Existing functionality unchanged

---

## Effort Estimate

### Hours & Lines of Code

| Sub-Phase | Weeks | Hours | LOC (Code) | LOC (Tests) | Total LOC | Notes |
|-----------|-------|-------|-----------|------------|-----------|-------|
| **5.1: Sync Scripts** | 1-4 | 76-86 | 950-1200 | 600-800 | 1550-2000 | BaseSyncModule + 5-8 scripts |
| **5.2: Doc Generation** | 1-4 | 64-70 | 1600-2000 | 800-1000 | 2400-3000 | 6 doc generators + validators |
| **5.3: CLI Refactoring** | 4-6 | 86-92 | 1200-1450 | 1000-1200 | 2200-2650 | BaseCLITool + 4-5 CLI tools |
| **Total** | 6 weeks | 226-248 | **3750-4650** | **2400-3000** | **6150-7650** | ~160-200 solo hours (parallel discount) |

### LOC Breakdown by Component

**Phase 5.1: Sync Scripts** (1550-2000 LOC)
- `scripts/sync/base.py` (BaseSyncModule): ~150-200 LOC
- Refactored sync scripts (5-8): ~800-1000 LOC (smaller due to base reuse)
- Test suite (base + scripts): ~600-800 LOC
- Pattern: Reduces duplication, improves consistency

**Phase 5.2: Doc Generation** (2400-3000 LOC)
- Doc generators (6 types): ~1600-2000 LOC (~270 LOC/generator avg)
  - phase-status, active-tasks, roadmap, AUDIT validator, LINK_MAP, phase-summary
- Validation & utilities: ~400-500 LOC
- Test suite (generators + validators): ~800-1000 LOC
- Pattern: New automation features (not refactoring)

**Phase 5.3: CLI Refactoring** (2200-2650 LOC)
- `scripts/cli/base.py` (BaseCLITool): ~200-250 LOC
- Refactored CLI tools (4-5): ~1200-1450 LOC (smaller due to base reuse)
- Test suite (base + CLI tools): ~1000-1200 LOC
- Pattern: Consolidates scattered CLI implementations

### Comparison to Phase 4

**Phase 4** (Profiling Scripts): ~1200 LOC (13 scripts refactored)
- BaseProfiler + metrics + 13 scripts + tests
- All 13 scripts now follow unified pattern

**Phase 5** Scope: ~6150-7650 LOC (3 initiatives)
- 5-8 sync scripts + 6 doc generators + 4-5 CLI tools
- Larger than Phase 4 due to 3 parallel tracks

### Estimated Final Codebase Size

| Area | Current | Phase 5 Adds | Total |
|------|---------|-------------|-------|
| app/ | ~5000 LOC | 0 | ~5000 |
| scripts/ | ~3200 LOC | 3750-4650 | ~6950-7850 |
| tests/ | ~8000 LOC | 2400-3000 | ~10400-11000 |
| **Total** | **~16200** | **~6150-7650** | **~22350-23850** |

---

## Effort Estimate Summary

| Metric | Value | Notes |
|--------|-------|-------|
| **Total Hours** | 226-248 | ~160-200 solo (parallel discount) |
| **Total LOC** | 6150-7650 | Code + tests |
| **Code LOC** | 3750-4650 | Implementation across 3 tracks |
| **Test LOC** | 2400-3000 | Tests for all new code (95% coverage) |
| **Test Count** | 1000+ | Across 5.1, 5.2, 5.3 |
| **Duration** | 6 weeks | Parallel tracks + sequential |
| **Coverage** | 95% | All new code |

---

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Test Coverage | 95%+ | TBD |
| Tests Passing | 100% | TBD |
| Phase Duration | 6 weeks | TBD |
| Scripts Using Base Classes | 100% | TBD |
| CLI UX Consistency | 100% | TBD |
| Doc Generation Accuracy | 100% | TBD |

---

## Dependencies & Risks

### Positive Dependencies
- ✅ Phase 4 (BaseProfiler) provides proven pattern
- ✅ Phase 13 (Skills) already has docUpdater for integration
- ✅ Existing scripts already functional (low risk refactoring)

### Risks

| Risk | Mitigation |
|------|-----------|
| Over-engineering CLI base class | Keep BaseCLITool minimal; iterate if needed |
| Doc generator complexity | Start simple (AUDIT.md → phase-status); expand gradually |
| Sync script dependencies | Audit dependencies before refactoring; test dry-run first |
| Coverage gaps in base classes | Comprehensive edge case testing; parametrized tests |
| Time overrun on CLI (longest phase) | Split CLI tools across Week 5-6 evenly; prioritize high-value tools |

### Mitigation Strategies
- **Weekly checkpoints**: Verify coverage targets are on track
- **Parallel tracks**: 5.1 & 5.2 don't block each other
- **Incremental refactoring**: Small batches of CLI tools (3-4 per week)
- **Early validation**: Test generators and CLI with real data (Week 2-3)

---

## Next Steps

1. **Approve Phase 5 plan** (this document)
2. **Create phase-5 branch** from main
3. **Week 1 start**:
   - Kick off 5.1 and 5.2 in parallel
   - Design BaseSyncModule and BaseDocGenerator
   - Create first generators and sync scripts
4. **Weekly status updates** (Mondays)
5. **Gate assessment** (end of Week 6)

---

## Related Documentation

- **Phase 4 Complete**: `AUDIT.md` (BaseProfiler pattern reference)
- **Phase 17 Plan**: Parallel execution example
- **Scripts Audit**: `docs/SCRIPTS_AUDIT_2026-08-27.md`
- **Rules**: `.claude/rules/development-workflow-gates.md`

---

**Status**: Ready for approval  
**Created**: 2026-08-27  
**Last Updated**: 2026-08-27
