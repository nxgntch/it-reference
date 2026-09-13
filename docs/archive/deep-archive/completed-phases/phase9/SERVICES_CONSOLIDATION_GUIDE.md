# Phase 9B: Services Consolidation Guide

**Status**: ✅ COMPLETE  
**Date**: 2026-09-10  
**Effort**: 2-3 hours  
**Impact**: 3 services + 5 monitoring components documented & consolidated

---

## Summary

**Objective**: Consolidate and document nxgntch microservices architecture.

**Deliverables**:
1. ✅ `services/README.md` hub (navigation & service overview)
2. ✅ Services consolidation guide (this document)
3. ✅ Service architecture & dependencies mapping
4. ✅ Deployment procedures & health checks

**Outcomes**:
- Clear service architecture for team
- Deployment procedures documented
- Inter-service dependencies explicit
- Team can deploy/troubleshoot confidently
- Operations can monitor effectively

---

## Services Inventory

### Total Count
- **3 major services** with clear purposes
- **5 monitoring stack components** (Prometheus, Grafana, AlertManager, Loki, Promtail)
- **3 configuration files** per component
- **All documented** ✅

### Service Breakdown

| Service | Purpose | Type | Status |
|---------|---------|------|--------|
| **MCP Chat Server** | Claude Chat integration | Integration | ✅ Active |
| **Monitoring Stack** | Full observability | Observability | ✅ Active |
| **Metrics Service** | Metrics collection | Collection | ✅ Active |

---

## Services Documented

### Service 1: MCP Chat Server

**Location**: `services/mcp-chat/`  
**Purpose**: Standalone MCP server for Claude Chat integration  
**Architecture**: Reads configuration from workspace `config/` directory  

**Key Features**:
- Configuration-driven (no hardcoded values)
- Loads models, agents, skills from YAML
- Cost calculation and budget checking
- Health checks and validation
- Automatic workspace root detection

**Configuration Files**:
- `config/models.yaml` — Model definitions & pricing
- `config/agents.yaml` — Agent definitions & capabilities
- `config/governance.yaml` — Budget caps & limits
- `config/orchestration.yaml` — Timeouts & SLA targets

**Usage**:
```bash
# Start MCP Chat Server
python -m mpc_chat.server

# Verify health
python -c "from mpc_chat import MCPChatServer; MCPChatServer()"
```

**Dependencies**:
- Python 3.9+
- PyYAML
- Workspace `config/` directory accessible

---

### Service 2: Monitoring Stack

**Location**: `services/monitoring/`  
**Purpose**: Comprehensive observability for nxgntch platform  
**Architecture**: Docker Compose-based, multi-component stack

#### Component 2.1: Prometheus
**Purpose**: Metrics collection and time-series database  
**Port**: 9090  
**Config**: `prometheus.yml`  

**Features**:
- Scrapes nxgntch API `/metrics` every 10 seconds
- Evaluates alert rules every 30 seconds
- Stores metrics in time-series database
- Sends alerts to AlertManager
- 15-day retention by default

**Metrics Collected**:
- API latency (p50, p95, p99)
- Request throughput
- Error rates (4xx, 5xx)
- Cost tracking metrics
- Agent performance

#### Component 2.2: Grafana
**Purpose**: Visualization and dashboarding  
**Port**: 3000  
**Credentials**: admin / admin  

**Features**:
- Pre-configured dashboards
- Real-time metric visualization
- Custom dashboard creation
- Alert rule visualization
- Log exploration (with Loki integration)

**Pre-configured Dashboards**:
- nxgntch Platform Overview (API, cost, agents)
- Monitoring Stack Health
- Log Analysis

#### Component 2.3: AlertManager
**Purpose**: Alert routing and deduplication  
**Port**: 9093  
**Config**: `alertmanager.yml`  

**Features**:
- Routes alerts by severity and service
- Critical → immediate (email + webhook)
- Warnings → batched (Slack)
- Cost alerts → finance team
- Alert deduplication and grouping

**Alert Levels**:
- **Critical**: Immediate response (API down, budget exceeded)
- **Warning**: Batched (high latency, error rate)
- **Info**: Silent (Grafana only)

#### Component 2.4: Loki
**Purpose**: Log aggregation and search  
**Port**: 3100  
**Config**: `loki-config.yml`  

**Features**:
- Aggregates Docker container logs
- 30-day retention by default
- Filesystem storage (upgradeable to object storage)
- Integrated with Grafana for log exploration
- Label-based querying

**Log Sources**:
- Docker containers
- Kubernetes pods
- System logs (`/var/log/`)

#### Component 2.5: Promtail
**Purpose**: Log collector and forwarder  
**Config**: `promtail-config.yml`  

**Features**:
- Collects Docker container logs
- Supports Kubernetes pod logs
- System log collection
- Forwards all logs to Loki
- Automatic label extraction

---

### Service 3: Metrics Service

**Location**: `services/metrics/`  
**Purpose**: Metrics collection and aggregation  
**Architecture**: Python service  

**Features**:
- Collects platform metrics
- Aggregates per agent/team
- Exports for external consumption
- Integrates with monitoring stack

**Metrics Tracked**:
- Cost per agent
- Cost per team
- Task execution statistics
- Performance metrics

---

## Service Dependencies & Architecture

### Dependency Graph

```
Application API (Port 8000)
├─ Exposes /metrics endpoint
│
└─ Monitoring Stack Dependencies
   ├─ Prometheus
   │  ├─ Depends on → API /metrics
   │  └─ Feeds → Grafana
   ├─ AlertManager
   │  ├─ Depends on → Prometheus alerts
   │  └─ Sends → Slack/Email
   ├─ Loki
   │  ├─ Receives from → Promtail
   │  └─ Feeds → Grafana
   └─ Promtail
      └─ Collects → Docker logs
      └─ Sends → Loki

MCP Chat Server (Port 5005)
└─ Independent (reads workspace config/)
```

### Startup Order (Critical)

```
Phase 1: Application API
├─ Condition: Must be running before monitoring
├─ Health Check: curl http://localhost:8000/health
└─ Metrics Endpoint: curl http://localhost:8000/metrics

Phase 2: Monitoring Stack
├─ Prometheus (depends on API metrics)
├─ AlertManager (depends on Prometheus)
├─ Loki + Promtail (independent)
└─ Grafana (feeds from Prometheus + Loki)

Phase 3: MCP Chat Server (independent, any time)
```

### Network Communication

| From | To | Protocol | Port | Purpose |
|------|-----|----------|------|---------|
| Prometheus | API | HTTP | 8000 | Scrape /metrics |
| AlertManager | Slack | HTTPS | 443 | Send notifications |
| Promtail | Loki | HTTP | 3100 | Forward logs |
| Grafana | Prometheus | HTTP | 9090 | Query metrics |
| Grafana | Loki | HTTP | 3100 | Query logs |

---

## Deployment Procedures

### Quick Start (All Services)

```bash
# 1. Ensure API is running
curl http://localhost:8000/health

# 2. Start monitoring stack
cd services/monitoring
docker-compose -f docker-compose.monitoring.yml up -d

# 3. Verify stack health
docker ps | grep nxgntch

# 4. Access dashboards
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
# AlertManager: http://localhost:9093
```

### Service-Specific Deployment

#### Deploy Monitoring Stack

```bash
docker-compose -f docker-compose.monitoring.yml up -d

# Wait for startup (30-60 seconds)
sleep 30

# Verify all containers running
docker ps | grep nxgntch

# Check component health
curl http://localhost:9090/-/healthy  # Prometheus
curl http://localhost:3000/api/health  # Grafana
curl http://localhost:3100/ready       # Loki
curl http://localhost:9093            # AlertManager
```

#### Start MCP Chat Server

```bash
python -m mpc_chat.server

# Expected output:
# ✓ MCP Chat server initialized with workspace config
# ✓ MPC Chat server ready to accept connections
```

#### Deploy Metrics Service

```bash
python -m services.metrics

# Verify metrics endpoint
curl http://localhost:8000/metrics
```

### Production Deployment

**Environment Setup**:

```bash
# Set required variables for AlertManager
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
export SMTP_PASSWORD=your-email-password

# Optional
export WORKSPACE_ROOT=/path/to/workspace
export LOG_LEVEL=INFO

# Load from .env
export $(cat .env | xargs)
```

**Deployment Steps**:

```bash
# 1. Verify API running
curl -s http://localhost:8000/health | jq .

# 2. Deploy monitoring with environment
docker-compose -f docker-compose.monitoring.yml up -d

# 3. Verify all services
docker exec nxgntch-prometheus curl -s http://localhost:9090/-/healthy
docker exec nxgntch-grafana curl -s http://localhost:3000/api/health
docker exec nxgntch-loki curl -s http://localhost:3100/ready

# 4. Configure alerts in AlertManager
# Verify Slack webhook set: docker exec nxgntch-alertmanager env | grep SLACK

# 5. Test alert flow
# Trigger manual alert in UI: http://localhost:9093
```

---

## Monitoring & Health Checks

### Health Check Script

```bash
#!/bin/bash
echo "Service Health Check"
echo "===================="

# API
echo -n "API: "
curl -s http://localhost:8000/health | jq -r .status || echo "FAIL"

# Prometheus
echo -n "Prometheus: "
curl -s http://localhost:9090/-/healthy | grep "OK" && echo "OK" || echo "FAIL"

# Grafana
echo -n "Grafana: "
curl -s http://localhost:3000/api/health | jq -r .status || echo "FAIL"

# Loki
echo -n "Loki: "
curl -s http://localhost:3100/ready | jq -r .status || echo "FAIL"

# AlertManager
echo -n "AlertManager: "
curl -s http://localhost:9093 | grep -q "Alertmanager" && echo "OK" || echo "FAIL"

# MCP Chat
echo -n "MCP Chat: "
pgrep -f "mpc_chat.server" > /dev/null && echo "OK" || echo "FAIL"
```

### Key Metrics to Monitor

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| API Uptime | > 99.5% | < 99% |
| API Latency P99 | < 5s | > 10s |
| API Error Rate | < 1% | > 5% |
| Monthly Cost | < $10,000 | > $9,000 |
| Agent Success | > 95% | < 90% |
| Memory Usage | < 80% | > 90% |

---

## Troubleshooting

### Service Won't Start

**Problem**: Docker container fails to start  
**Solution**:
1. Check logs: `docker logs <container>`
2. Verify ports not in use: `netstat -tln | grep <port>`
3. Check dependencies: API must be running first

### No Metrics in Grafana

**Problem**: Prometheus datasource has no data  
**Solution**:
1. Verify Prometheus scrape: http://localhost:9090/targets
2. Check metrics endpoint: `curl http://localhost:8000/metrics`
3. Confirm datasource connection: Grafana UI → Configuration → Data Sources

### Alerts Not Firing

**Problem**: AlertManager not sending notifications  
**Solution**:
1. Check AlertManager logs: `docker logs nxgntch-alertmanager`
2. Verify rules in Prometheus: http://localhost:9090/alerts
3. Test manual alert: Prometheus UI → Alerts → Create test

### High Disk Usage

**Problem**: Prometheus or Loki consuming too much space  
**Solution**:
1. Reduce retention in `prometheus.yml` (global section)
2. Reduce Loki retention in `loki-config.yml`
3. Increase scrape interval (trades latency for storage)
4. Cleanup old data: `docker-compose down -v` (WARNING: deletes all data)

---

## Backup & Disaster Recovery

### Backup Procedures

**Prometheus Data**:
```bash
docker exec nxgntch-prometheus \
  tar -czf - /prometheus > prometheus-backup.tar.gz
```

**Grafana Dashboards**:
- Export from UI: Dashboards → Export → Save JSON
- Or use API: `curl -H "Authorization: Bearer $GRAFANA_TOKEN" http://localhost:3000/api/dashboards/uid/<uid>`

**Configuration Files**:
```bash
tar -czf services-backup.tar.gz \
  services/monitoring/*.yml \
  config/
```

### Restore Procedures

**Prometheus**:
```bash
docker-compose down
tar -xzf prometheus-backup.tar.gz -C services/monitoring/
docker-compose up -d
```

**Grafana**:
- Import JSON files via UI: Dashboards → Import

---

## Performance & Scaling

### Resource Requirements

| Component | CPU | Memory | Disk |
|-----------|-----|--------|------|
| Prometheus | 50-200m | 256-512Mi | 1-2 GB/month |
| Grafana | 20-50m | 128-256Mi | 100 MB |
| Loki | 20-100m | 256-512Mi | 500MB-1GB/month |
| AlertManager | 10-20m | 64-128Mi | 10 MB |
| **Total** | **100-450m** | **704-1456Mi** | **2-4 GB/month** |

### Optimization

- Adjust scrape interval in `prometheus.yml` (trade latency for resources)
- Reduce retention periods (trade history for storage)
- Use object storage for Loki (S3, GCS, etc)
- Enable compression for logs

---

## Key Findings

### Strengths ✅
1. **Well-documented services**: Clear READMEs for each
2. **Standard components**: Industry-standard tools (Prometheus, Grafana)
3. **Configuration-driven**: YAML-based, flexible
4. **Clear architecture**: Service dependencies explicit
5. **Documented**: Now has central hub + guide

### Areas Improved ✅
1. **Central hub**: services/README.md created
2. **Architecture**: Service dependencies mapped
3. **Deployment**: Clear startup procedures
4. **Health checks**: Scripts and procedures
5. **Best practices**: Guides and recommendations

---

## Integration Points

### Linked From
- **docs/guides/operations/DEPLOYMENT.md** — Full deployment procedures
- **docs/guides/development/README.md** — Development guide hub
- **CLAUDE.md** — Quick links (Deploying role)
- **docs/INDEX.md** — Operations section

### Backward Compatibility
- All existing service files unchanged
- New hub extends, doesn't replace
- Existing deployments still work
- Configuration files preserved

---

## Metrics

| Metric | Value | Status |
|--------|-------|--------|
| **Services documented** | 3 | ✅ Complete |
| **Stack components** | 5 | ✅ Complete |
| **Deployment procedures** | 3+ | ✅ Complete |
| **Health checks** | Automated | ✅ Complete |
| **Lines of documentation** | 400+ | ✅ Complete |
| **Integration points** | 4 | ✅ Complete |

---

## Next Steps

### Immediate
- [x] Create services/README.md hub
- [x] Write consolidation guide
- [x] Map dependencies
- [x] Document deployment

### Short-term
- [ ] Create service monitoring dashboards
- [ ] Add alerting rules per service
- [ ] Document service SLAs
- [ ] Create runbooks for common operations

### Long-term (Phase 10+)
- [ ] SDKs documentation (Phase 10)
- [ ] Tests documentation (Phase 10)
- [ ] Skills documentation (Phase 11)

---

## Success Criteria

✅ All services have documented purpose  
✅ Architecture clearly mapped  
✅ Deployment procedures documented  
✅ Health check procedures provided  
✅ Hub created and integrated  
✅ Team can deploy/troubleshoot confidently  

---

**Phase 9B Status**: ✅ **COMPLETE**  
**Services Documented**: 3 + 5 components  
**Documentation**: 400+ lines  
**Architecture**: Fully mapped  
**Ready for**: Phase 10 (SDKs + Tests)

---

**Last Updated: 2026-09-10  
**Consolidated by**: Phase 9B  
**Next Phase**: Phase 10 (SDKs + Tests Consolidation)
