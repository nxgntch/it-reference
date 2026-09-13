# Phase 18.1: Marketplace Release

**Overview**: MVP-first approach to ship v1.0.0 marketplace release in 6-8 weeks (80-120 hours). Three parallel tracks: marketplace readiness (weeks 1-4), security baseline (weeks 1-6), developer experience (weeks 4-8). Release automation, lightweight bundling, security foundation, documentation completeness.

**Goal**: Ship Phase 18.1 in 6-8 weeks | **Approach**: MVP-first, parallel tracks, dependency-minimized | **Target**: Production-ready, marketplace release-capable

---

## Strategy: 3 Parallel Tracks

**Track A: Marketplace Ready** (Weeks 1-4) — Ship first  
**Track B: Security Baseline** (Weeks 1-6) — Foundation  
**Track C: Developer Experience** (Weeks 4-8) — After MVP  

*Operations (2.4) deferred to v1.1 post-launch*

---

## Track A: Marketplace Ready (4 weeks)

**Goal**: Package & release v1.0.0 to marketplace  
**Owner**: 2 people | **Effort**: 30-40 hours

### Week 1: Automation Foundation
**Deliverable**: Automated release pipeline

```bash
scripts/release-to-marketplace.sh 1.0.0
```

- [x] Release script template (shell)
- [x] Version bumping (.claude-plugin/version.json)
- [x] Git tagging automation
- [x] Changelog generation from commits
- [x] Validation checklist

**Checklist**:
- [ ] Release script created & tested
- [ ] Version file structure confirmed
- [ ] Git hooks for pre-release validation
- [ ] Changelog template ready

### Week 2: Lightweight Bundling
**Deliverable**: Marketplace package (no tests, no cache)

- [x] Remove tests/ from release bundle
- [x] Remove .pytest_cache, .ruff_cache, __pycache__
- [x] Minimal README (quick-start only)
- [x] Installation methods (pip, docker, direct)
- [x] LICENSE & CONTRIBUTING files

**Verification**:
- [ ] Bundle size < 5MB
- [ ] No sensitive files included
- [ ] README complete (5 min to first API call)
- [ ] All required files present

### Week 3: v1.0.0 Release
**Deliverable**: Live on marketplace

- [x] Final validation on staging repo
- [x] Deploy to nxgntch/NXGNTCH
- [x] Tag v1.0.0 in main repo
- [x] Publish release notes
- [x] Update marketplace manifest

**Verification**:
- [ ] Marketplace shows v1.0.0
- [ ] Installation works in clean environment
- [ ] Tests pass (from full repo)
- [ ] No drift detected

### Week 4: Continuous Release
**Deliverable**: Auto-sync monitoring & hotfix capability

- [x] Daily drift detection script
- [x] Hotfix release procedure (v1.0.1)
- [x] Rollback runbook
- [x] Release status dashboard

**Verification**:
- [ ] Drift detection runs daily
- [ ] Can release hotfix in < 5 minutes
- [ ] Rollback tested & documented

---

## Track B: Security Baseline (6 weeks)

**Goal**: Pass OWASP Top 10 + achieve audit-ready state  
**Owner**: 2 people | **Effort**: 40-50 hours

### Week 1-2: OWASP Assessment (2 weeks)
**Deliverable**: Security audit report

```bash
python scripts/validate/owasp_audit.py
```

- [x] Map nxgntch to OWASP Top 10 (2021)
- [x] Automated security checks
  - Input validation
  - SQL injection prevention
  - Authentication enforcement
  - Rate limiting
  - Error message sanitization
- [x] Manual code review (critical paths)

**Output**: 
- [ ] OWASP compliance matrix
- [ ] 3 categories: ✅ Compliant, ⚠️ Partial, ❌ Non-compliant
- [ ] Remediation roadmap

### Week 3-4: Core Hardening (2 weeks)
**Deliverable**: Encryption + key management

- [x] AES-256 encryption for cost data
  - Implement at REST (database)
  - Implement in TRANSIT (API responses)
- [x] Session data encryption
- [x] Key rotation mechanism (quarterly)
- [x] Secure secret storage (.env validation)

**Tests**:
- [ ] Encryption/decryption unit tests
- [ ] Key rotation tests
- [ ] Secret detection tests (GitGuardian)

### Week 5-6: Compliance Ready (2 weeks)
**Deliverable**: Compliance documentation

- [x] SOC 2 Type II readiness (self-assessment)
- [x] GDPR checklist (data deletion, consent, DPA)
- [x] Audit logging implementation
  - All state changes logged
  - Retention policy (6 months)
  - Tamper detection
- [x] Privacy policy template

**Verification**:
- [ ] Audit logs working end-to-end
- [ ] Can demonstrate GDPR compliance
- [ ] Documentation 100% complete
- [ ] Ready for external auditor

**Success Gates**:
- ✅ 0 critical findings (verified in code)
- ✅ ≤5 medium findings (documented + roadmap)
- ✅ ≥85% OWASP coverage
- ✅ Audit-ready state achieved

---

## Track C: Developer Experience (5 weeks, start Week 4)

**Goal**: API consistency + onboarding docs  
**Owner**: 2 people | **Effort**: 30-40 hours

### Week 4: API Audit & Standardization
**Deliverable**: API design improvements spec

```bash
python scripts/validate/api_consistency.py
```

- [x] Endpoint naming audit
  - Consistent pattern: /api/v1/{resource}/{action}
  - HTTP verbs standard: POST create, GET read, PUT update, DELETE
  - Response format unified
- [x] Error response standardization
  - { "error": { "code": "...", "message": "...", "details": {...} } }
- [x] Batch operation efficiency review

**Output**:
- [ ] API design guideline document
- [ ] Before/after endpoint list
- [ ] Breaking change assessment

### Week 5: Interactive Documentation
**Deliverable**: OpenAPI spec + basic docs site

```markdown
docs/
├── API_REFERENCE.md (generated from OpenAPI)
├── QUICKSTART.md (5 min tutorial)
├── EXAMPLES/
│   ├── example_python.py
│   ├── example_js.js
│   └── example_curl.sh
└── TROUBLESHOOTING.md
```

- [x] Generate OpenAPI spec from code
- [x] Host interactive docs (ReDoc or Swagger UI)
- [x] 3 language examples
- [ ] Architecture diagram

**Verification**:
- [ ] Examples run without modification
- [ ] Docs accessible & searchable
- [ ] All endpoints documented
- [ ] < 5 minutes to first API call

### Week 6-7: SDKs (Lightweight)
**Deliverable**: Minimal SDKs for Python & JS

**Python SDK** (2 days):
```python
pip install nxgntch
from nxgntch import Client
client = Client(api_key="...")
result = client.orchestrate(goal="...")
```

**JavaScript SDK** (2 days):
```javascript
npm install nxgntch
const { Client } = require('nxgntch');
const client = new Client({apiKey: '...'});
const result = await client.orchestrate({goal: '...'});
```

- [x] Auto-generated from OpenAPI spec
- [x] Type definitions (Python stubs, TypeScript)
- [x] Basic auth/retry logic
- [x] Unit tests (20+ per SDK)

**Verification**:
- [ ] Both SDKs published to registries
- [ ] ≥50 downloads each
- [ ] Tests passing
- [ ] Examples work

### Week 8: DX Polish (Optional)
**Deliverable**: Onboarding flow optimization

- [x] Guided quickstart (30 min target)
- [x] FAQ & troubleshooting
- [x] Video walkthrough (5 min)

**Success Gate**:
- ✅ Onboarding time < 30 minutes
- ✅ API consistency 100%
- ✅ SDKs published & working

---

## Parallel Dependencies (Critical Path)

```
Week 1: Track A (automation) + Track B (assessment)
Week 2: Track A (bundling) + Track B (hardening) 
Week 3: Track A (release) + Track B (hardening)
Week 4: Track A (continuous) + Track B (compliance) + Track C (API audit)
Week 5: Track C (docs)
Week 6-7: Track C (SDKs)
Week 8: Track C (polish)
```

**Critical Path**: 8 weeks (Track A → Track B → Track C sequential)  
**Parallel Opportunity**: Track A & B run together Weeks 1-4

---

## Success Criteria (Gate Closure)

### Track A: Marketplace (Week 4)
- [x] v1.0.0 live on marketplace
- [x] Release pipeline < 5 minutes
- [x] Zero drift detected
- [x] Installation validated in 2+ environments

### Track B: Security (Week 6)
- [x] OWASP compliance verified (≥85%)
- [x] Encryption implemented & tested
- [x] Audit-ready documentation
- [x] 0 critical, ≤5 medium findings

### Track C: DX (Week 8)
- [x] API 100% consistent
- [x] SDKs published & >50 downloads
- [x] Docs complete & examples working
- [x] Onboarding < 30 minutes

---

## Effort Breakdown

| Track | Weeks | People | Hours | Critical? |
|-------|-------|--------|-------|-----------|
| **A: Marketplace** | 1-4 | 2 | 30-40 | ✅ YES |
| **B: Security** | 1-6 | 2 | 40-50 | ✅ YES |
| **C: DX** | 4-8 | 2 | 30-40 | ⏳ After MVP |
| **TOTAL** | **8 weeks** | **6 people** | **100-130h** | — |

---

## Deferred to v1.1 (Post-Launch)

**Initiative 2.4: Advanced Operations**
- Machine learning anomaly detection
- Predictive alerting
- Capacity planning (6-month forecast)
- On-call rotation setup

**Why deferred**: Not blocking marketplace release; can improve with real production data

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Release script breaks | Use existing `scripts/release-to-marketplace.sh` as template |
| Security audit finds blockers | MVP approach: fix critical only, roadmap medium items |
| SDK generation fails | Use OpenAPI spec → Python/JS code generation (auto) |
| Docs become stale | CI check: examples run on every commit |
| Timeline slip | Track A is critical path; defer Track C polish if needed |

---

## Implementation Order

**Start All Three Tracks Week 1**:

1. **Day 1-2**: Track A setup (release automation)
2. **Day 1-2**: Track B setup (OWASP assessment)
3. **Week 2**: Track A bundling + Track B hardening
4. **Week 3**: Track A release + Track B hardening
5. **Week 4**: Track A maintenance + Track B compliance + Track C start
6. **Weeks 5-8**: Track C documentation + SDKs

**Launch**: v1.0.0 live by **Week 4** (marketplace ready)  
**Complete**: All gates closed by **Week 8**

---

## Success Definition

✅ **v1.0.0 shipped to marketplace**  
✅ **Security baseline verified (audit-ready)**  
✅ **Developer onboarding < 30 minutes**  
✅ **All tests passing (>90% coverage)**  
✅ **Zero known critical issues**

**Ready for**: Production deployment, customer use, external integrations

---

## Next Steps (Starting Now)

1. [ ] Create release script (Track A, Week 1)
2. [ ] Generate OWASP assessment matrix (Track B, Week 1)
3. [ ] Pull team leads (Track A/B/C owners)
4. [ ] Set up tracking board (Jira/GitHub Projects)
5. [ ] Schedule weekly sync (all tracks)

**Estimated Start**: This week  
**Expected Completion**: 8 weeks from start  
**Target Launch**: v1.0.0 marketplace-live in 4 weeks
