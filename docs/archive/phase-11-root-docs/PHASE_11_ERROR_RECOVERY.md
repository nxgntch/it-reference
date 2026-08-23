# Phase 11: Error Recovery Implementation Guide

**Focus**: Implement robust error recovery in Orchestrator  
**Target**: 100% test passing (681/681), advanced failure handling  
**Timeline**: Week 2 (3-4 days)

---

## Overview

Phase 11 Week 2 implements four interconnected error recovery systems to handle advanced failure scenarios:

1. **Checkpoint System** - Save/restore execution state
2. **Error Propagation** - Chain errors through agent hierarchy
3. **Network Resilience** - Retry with backoff, circuit breaker
4. **Cascading Error Handler** - Prevent error avalanches

These systems turn 4 currently-failing tests into production-ready error handling.

---

## Currently Failing Tests

```python
# tests/test_orchestrator.py (4 tests, status: SKIPPED)

def testAdvancedErrorRecovery():
    """Test recovery from mid-execution failures"""
    pass

def testAgentErrorPropagation():
    """Test error propagation through agent hierarchy"""
    pass

def testRecoveryFromNetworkFailure():
    """Test recovery when external service fails"""
    pass

def testCascadingErrorHandling():
    """Test handling cascading errors across agents"""
    pass
```

**Objective**: Remove `@pytest.mark.skip()`, implement features, make tests pass.

---

## System 1: Checkpoint System

### Purpose
Save execution state at each step, enabling recovery from mid-execution failures.

### Architecture

```
Task Execution
    ↓
[Step 1] → Save Checkpoint(step=1, state={...})
    ↓
[Step 2] → Save Checkpoint(step=2, state={...})
    ↓
[Step 3] ❌ ERROR → Load Checkpoint(step=2)
    ↓
[Step 3] RETRY → Resume from step 2
    ↓
✅ Completion
```

### Implementation

**File**: `app/core/resilience.py` (new)

```python
from typing import Dict, Any, Optional
from datetime import datetime
import json
import tempfile
from pathlib import Path

class Checkpoint:
    """Represents a single execution checkpoint"""
    
    def __init__(self, execution_id: str, step: int, state: Dict[str, Any]):
        self.execution_id = execution_id
        self.step = step
        self.state = state
        self.timestamp = datetime.utcnow()
    
    def to_json(self) -> str:
        """Serialize checkpoint to JSON"""
        return json.dumps({
            'execution_id': self.execution_id,
            'step': self.step,
            'state': self.state,
            'timestamp': self.timestamp.isoformat()
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Checkpoint':
        """Deserialize checkpoint from JSON"""
        data = json.loads(json_str)
        cp = cls(
            data['execution_id'],
            data['step'],
            data['state']
        )
        cp.timestamp = datetime.fromisoformat(data['timestamp'])
        return cp


class CheckpointManager:
    """Manages execution checkpoints for recovery"""
    
    def __init__(self, storage_dir: Optional[str] = None):
        """Initialize checkpoint manager
        
        Args:
            storage_dir: Directory to store checkpoints (default: temp dir)
        """
        self.storage_dir = Path(storage_dir or tempfile.gettempdir()) / 'nxgntch_checkpoints'
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def createCheckpoint(self, execution_id: str, step: int, state: Dict[str, Any]) -> str:
        """Save execution state at current step
        
        Args:
            execution_id: Unique execution identifier
            step: Step number in execution
            state: Current execution state to save
        
        Returns:
            Checkpoint ID
        """
        checkpoint = Checkpoint(execution_id, step, state)
        checkpoint_file = self.storage_dir / f"{execution_id}_{step}.json"
        checkpoint_file.write_text(checkpoint.to_json())
        return str(checkpoint_file)
    
    def getLastCheckpoint(self, execution_id: str) -> Optional[Checkpoint]:
        """Retrieve last saved checkpoint for execution
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            Last checkpoint, or None if no checkpoints exist
        """
        checkpoints = sorted(
            self.storage_dir.glob(f"{execution_id}_*.json"),
            key=lambda f: int(f.stem.split('_')[-1]),
            reverse=True
        )
        
        if checkpoints:
            return Checkpoint.from_json(checkpoints[0].read_text())
        return None
    
    def resumeFromCheckpoint(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Resume execution from last checkpoint
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            State from last checkpoint, or None if no checkpoint exists
        """
        checkpoint = self.getLastCheckpoint(execution_id)
        if checkpoint:
            return checkpoint.state
        return None
    
    def cleanupCheckpoints(self, execution_id: str, keep: int = 3):
        """Cleanup old checkpoints, keep last N
        
        Args:
            execution_id: Execution identifier
            keep: Number of checkpoints to keep
        """
        checkpoints = sorted(
            self.storage_dir.glob(f"{execution_id}_*.json"),
            key=lambda f: int(f.stem.split('_')[-1]),
            reverse=True
        )
        
        for checkpoint_file in checkpoints[keep:]:
            checkpoint_file.unlink()
```

### Integration with Orchestrator

**File**: `app/core/orchestrator.py`

```python
class Orchestrator:
    def __init__(self, config, checkpoint_manager=None):
        self.config = config
        self.checkpoint_manager = checkpoint_manager or CheckpointManager()
    
    async def invoke(self, agent_id: str, task: dict) -> dict:
        """Invoke agent with checkpoint support"""
        execution_id = f"{agent_id}_{datetime.utcnow().timestamp()}"
        step = 0
        
        try:
            # Check for existing checkpoint
            if state := self.checkpoint_manager.resumeFromCheckpoint(execution_id):
                step = state.get('step', 0)
                logger.info(f"Resuming from checkpoint: step {step}")
            
            # Execute with checkpoints
            while step < MAX_STEPS:
                state = {
                    'step': step,
                    'agent_id': agent_id,
                    'task': task,
                    'progress': f"Executing step {step + 1}"
                }
                
                # Save checkpoint before step
                self.checkpoint_manager.createCheckpoint(execution_id, step, state)
                
                # Execute step
                result = await self._execute_step(step, agent_id, task)
                step += 1
            
            # Cleanup checkpoints on success
            self.checkpoint_manager.cleanupCheckpoints(execution_id, keep=0)
            return result
        
        except Exception as e:
            logger.error(f"Error at step {step}: {e}")
            # Checkpoint saved, can resume later
            raise
```

### Testing

```python
def test_checkpoint_creation():
    """Test checkpoint creation and retrieval"""
    manager = CheckpointManager()
    state = {'data': 'test', 'step': 1}
    
    checkpoint_id = manager.createCheckpoint('exec_1', 1, state)
    retrieved = manager.getLastCheckpoint('exec_1')
    
    assert retrieved is not None
    assert retrieved.state == state
    assert retrieved.step == 1

def test_checkpoint_resume():
    """Test resuming from checkpoint"""
    manager = CheckpointManager()
    state = {'data': 'test', 'progress': 'halfway'}
    
    manager.createCheckpoint('exec_2', 5, state)
    resumed_state = manager.resumeFromCheckpoint('exec_2')
    
    assert resumed_state == state

def testAdvancedErrorRecovery():
    """Test recovery from mid-execution failures (Phase 11)"""
    orchestrator = Orchestrator(config, checkpoint_manager=manager)
    
    # Execute task that will fail
    with pytest.raises(RuntimeError):
        asyncio.run(orchestrator.invoke('agent_1', {'task': 'fail_at_step_3'}))
    
    # Retrieve checkpoint
    checkpoint = manager.getLastCheckpoint('agent_1_*')
    assert checkpoint.step == 3
    
    # Resume and complete
    result = asyncio.run(orchestrator.invoke('agent_1', {'task': 'fail_at_step_3'}))
    assert result['status'] == 'success'
```

---

## System 2: Error Propagation Chain

### Purpose
Chain errors through agent hierarchy with configurable retry strategies.

### Architecture

```
Specialist Agent Error
    ↓
Manager Agent catches error
    ├─ Retry strategy: exponential backoff
    ├─ Max retries: 3
    └─ Timeout: 30 seconds
    ↓
Director Agent notified
    ├─ Can escalate
    ├─ Can downgrade
    └─ Can override
    ↓
Error Audit Trail created
```

### Error Types

**File**: `app/core/exceptions.py` (extend)

```python
class OrchestratorError(Exception):
    """Base error for orchestrator failures"""
    
    def __init__(self, message: str, error_code: str, severity: str = 'medium'):
        self.message = message
        self.error_code = error_code  # e.g., 'ERR_AGENT_EXECUTION'
        self.severity = severity  # 'low' | 'medium' | 'high' | 'critical'
        self.timestamp = datetime.utcnow()
        super().__init__(self.message)

class AgentExecutionError(OrchestratorError):
    """Error during agent execution"""
    pass

class NetworkError(OrchestratorError):
    """Network or external service error"""
    pass

class RecoveryError(OrchestratorError):
    """Error during recovery attempt"""
    pass

class BudgetExceededError(OrchestratorError):
    """Budget limit exceeded"""
    pass

class ValidationError(OrchestratorError):
    """Input validation failed"""
    pass
```

### Error Propagation

**File**: `app/core/orchestrator.py`

```python
class ErrorPropagationChain:
    """Handles error propagation through agent hierarchy"""
    
    def __init__(self, config):
        self.config = config
        self.audit_trail = []
    
    def propagate(self, error: OrchestratorError, agent_id: str, hierarchy_level: int):
        """Propagate error through hierarchy
        
        Args:
            error: The error that occurred
            agent_id: Agent where error occurred
            hierarchy_level: Agent level (1=Specialist, 2=Manager, 3=Director)
        """
        self.audit_trail.append({
            'error': str(error),
            'agent_id': agent_id,
            'level': hierarchy_level,
            'timestamp': datetime.utcnow(),
            'severity': error.severity
        })
        
        # Determine retry strategy based on error type and severity
        retry_strategy = self._get_retry_strategy(error, hierarchy_level)
        
        if retry_strategy:
            return self._attempt_recovery(error, agent_id, retry_strategy)
        elif hierarchy_level < 3:  # Can escalate to higher level
            return self._escalate(error, agent_id, hierarchy_level + 1)
        else:  # Director level - no escalation
            return self._fail(error)
    
    def _get_retry_strategy(self, error: OrchestratorError, level: int) -> Optional[dict]:
        """Get retry strategy for error type"""
        
        if isinstance(error, NetworkError):
            return {
                'maxRetries': 3,
                'backoffMs': 100,
                'maxBackoffMs': 5000
            }
        elif isinstance(error, AgentExecutionError):
            if level < 3:  # Can retry at lower levels
                return {
                    'maxRetries': 2,
                    'backoffMs': 200,
                    'maxBackoffMs': 2000
                }
        elif isinstance(error, BudgetExceededError):
            return None  # Cannot retry budget errors
        
        return None
    
    def _attempt_recovery(self, error, agent_id, strategy) -> bool:
        """Attempt recovery using retry strategy"""
        # Implementation: retry with exponential backoff
        pass
    
    def _escalate(self, error, agent_id, next_level) -> dict:
        """Escalate error to next hierarchy level"""
        # Implementation: notify higher-level agent
        pass
    
    def _fail(self, error):
        """Fail the execution (no recovery possible)"""
        raise error
    
    def get_audit_trail(self) -> list:
        """Get complete error audit trail"""
        return self.audit_trail
```

### Testing

```python
def testAgentErrorPropagation():
    """Test error propagation through agent hierarchy"""
    chain = ErrorPropagationChain(config)
    
    # Simulate Specialist agent error
    error = AgentExecutionError(
        "Task failed",
        error_code="ERR_AGENT_EXECUTION",
        severity="medium"
    )
    
    # Propagate through hierarchy
    result = chain.propagate(error, agent_id='specialist_1', hierarchy_level=1)
    
    # Should attempt recovery at Specialist level
    assert result is not None
    
    # Should log in audit trail
    assert len(chain.get_audit_trail()) > 0
    assert chain.get_audit_trail()[0]['agent_id'] == 'specialist_1'
```

---

## System 3: Network Resilience

### Purpose
Handle network failures with retry, backoff, and circuit breaker patterns.

### Architecture

```
External Request
    ↓
[Attempt 1] → Timeout → Retry with 100ms backoff
    ↓
[Attempt 2] → Timeout → Retry with 200ms backoff
    ↓
[Attempt 3] → Timeout → Retry with 400ms backoff
    ↓
[Failed] → Open Circuit Breaker
    ↓
[Next requests] → Fast-fail (no retry)
```

### Implementation

**File**: `app/core/resilience.py`

```python
from enum import Enum
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, fast-fail
    HALF_OPEN = "half_open"  # Testing recovery

class NetworkResilient:
    """Handles network failures with retries and circuit breaker"""
    
    def __init__(self, maxRetries: int = 3, baseBackoffMs: int = 100):
        self.maxRetries = maxRetries
        self.baseBackoffMs = baseBackoffMs
        self.circuitStates = {}  # service -> state
    
    async def executeWithRetry(self, fn, service: str, maxRetries: int = None) -> Any:
        """Execute function with exponential backoff retry
        
        Args:
            fn: Async function to execute
            service: Service identifier for circuit breaker
            maxRetries: Max retry attempts (default: 3)
        
        Returns:
            Function result
        
        Raises:
            Final exception if all retries fail
        """
        maxRetries = maxRetries or self.maxRetries
        lastError = None
        
        for attempt in range(maxRetries + 1):
            try:
                # Check circuit breaker
                if self.checkCircuitBreaker(service) == CircuitState.OPEN:
                    raise CircuitBreakerOpen(f"Circuit breaker open for {service}")
                
                # Execute function
                return await fn()
            
            except (asyncio.TimeoutError, ConnectionError, IOError) as e:
                lastError = e
                
                if attempt < maxRetries:
                    # Calculate backoff: 100ms, 200ms, 400ms, 800ms, ...
                    backoffMs = self.baseBackoffMs * (2 ** attempt)
                    await asyncio.sleep(backoffMs / 1000)
                else:
                    # All retries exhausted - open circuit breaker
                    self.circuitStates[service] = CircuitState.OPEN
                    raise RecoveryError(
                        f"Failed after {maxRetries + 1} attempts",
                        error_code="ERR_NETWORK_FAILURE",
                        severity="high"
                    )
        
        raise lastError
    
    def checkCircuitBreaker(self, service: str) -> CircuitState:
        """Check if service is in failure state
        
        Args:
            service: Service identifier
        
        Returns:
            Current circuit state
        """
        return self.circuitStates.get(service, CircuitState.CLOSED)
    
    async def executeWithFallback(self, fn, fallback, service: str):
        """Execute with fallback on failure
        
        Args:
            fn: Primary function
            fallback: Function to execute if primary fails
            service: Service identifier
        
        Returns:
            Result from primary or fallback
        """
        try:
            return await self.executeWithRetry(fn, service)
        except Exception as e:
            logger.warning(f"Primary failed, using fallback: {e}")
            return await fallback()
```

### Testing

```python
@pytest.mark.asyncio
async def testNetworkRetryLogic():
    """Test exponential backoff retry"""
    resilient = NetworkResilient(maxRetries=3, baseBackoffMs=10)
    
    attempt_count = 0
    
    async def failing_fn():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ConnectionError("Connection refused")
        return "success"
    
    result = await resilient.executeWithRetry(failing_fn, service="test")
    assert result == "success"
    assert attempt_count == 3

@pytest.mark.asyncio
async def testRecoveryFromNetworkFailure():
    """Test recovery when external service fails"""
    resilient = NetworkResilient()
    
    # Simulate service that recovers after 2 failures
    attempt_count = 0
    
    async def recovering_service():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise asyncio.TimeoutError("Service timeout")
        return {"status": "recovered"}
    
    result = await resilient.executeWithRetry(recovering_service, service="api")
    assert result["status"] == "recovered"
    assert attempt_count == 3
```

---

## System 4: Cascading Error Handler

### Purpose
Prevent error avalanches when one failure cascades through multiple agents.

### Architecture

```
Agent 1 Error
    ↓
Agent 2 fails (cascade)
    ↓
Agent 3 fails (cascade)
    ↓
[Cascading Error Handler]
    ├─ Detect cascade pattern
    ├─ Stop propagation
    ├─ Suppress redundant errors
    └─ Report root cause only
```

### Implementation

**File**: `app/core/resilience.py`

```python
class CascadingErrorHandler:
    """Handles errors cascading through agent hierarchy"""
    
    def __init__(self):
        self.error_chains = {}  # execution_id -> [errors]
    
    def handleCascade(self, initial_error: OrchestratorError, affected_agents: List[str]) -> dict:
        """Handle cascading error across multiple agents
        
        Args:
            initial_error: The root cause error
            affected_agents: List of agents affected by cascade
        
        Returns:
            Aggregated error response
        """
        cascade_id = f"{initial_error.error_code}_{datetime.utcnow().timestamp()}"
        
        # Record cascade
        self.error_chains[cascade_id] = {
            'root_cause': initial_error,
            'affected_agents': affected_agents,
            'timestamp': datetime.utcnow(),
            'suppressed_count': len(affected_agents) - 1
        }
        
        return {
            'cascade_id': cascade_id,
            'root_cause': str(initial_error),
            'affected_agents': affected_agents,
            'recommendation': self._get_recovery_recommendation(initial_error)
        }
    
    def preventAvalanche(self, errors: List[OrchestratorError]) -> List[OrchestratorError]:
        """Suppress redundant errors from cascade
        
        Args:
            errors: List of errors that occurred
        
        Returns:
            Filtered list of unique/root errors only
        """
        if not errors:
            return []
        
        # Group by error code
        error_groups = {}
        for error in errors:
            code = error.error_code
            if code not in error_groups:
                error_groups[code] = error
        
        # Return only first error of each type (root cause)
        return list(error_groups.values())
    
    def aggregateErrors(self, error_list: List[OrchestratorError]) -> dict:
        """Aggregate multiple errors into actionable summary
        
        Args:
            error_list: List of errors to aggregate
        
        Returns:
            Aggregated error summary
        """
        if not error_list:
            return {}
        
        # Filter to prevent avalanche
        unique_errors = self.preventAvalanche(error_list)
        
        return {
            'total_errors': len(error_list),
            'unique_errors': len(unique_errors),
            'suppressed': len(error_list) - len(unique_errors),
            'root_cause': str(unique_errors[0]),
            'error_types': list(set(e.error_code for e in unique_errors)),
            'highest_severity': max(e.severity for e in unique_errors),
            'recommendation': self._get_recovery_recommendation(unique_errors[0])
        }
    
    def _get_recovery_recommendation(self, error: OrchestratorError) -> str:
        """Get recovery recommendation based on error type"""
        if isinstance(error, NetworkError):
            return "Check external service status and retry"
        elif isinstance(error, BudgetExceededError):
            return "Request budget increase or reduce scope"
        elif isinstance(error, AgentExecutionError):
            return "Review agent configuration and logs"
        else:
            return "Review error logs and contact support"
```

### Testing

```python
def testCascadingErrorHandling():
    """Test handling cascading errors across agents"""
    handler = CascadingErrorHandler()
    
    # Create cascading errors (same root cause, different agents)
    root_error = NetworkError("API unavailable", "ERR_NETWORK")
    cascading_errors = [
        root_error,
        AgentExecutionError("Task failed (cascade)", "ERR_CASCADE"),
        AgentExecutionError("Task failed (cascade)", "ERR_CASCADE"),
        AgentExecutionError("Task failed (cascade)", "ERR_CASCADE"),
    ]
    
    # Aggregate errors
    aggregate = handler.aggregateErrors(cascading_errors)
    
    # Should suppress redundant errors
    assert aggregate['total_errors'] == 4
    assert aggregate['unique_errors'] == 2
    assert aggregate['suppressed'] == 2
    assert aggregate['root_cause'] == str(root_error)
    
    # Should provide recovery recommendation
    assert 'recommendation' in aggregate
```

---

## Integration Testing

**File**: `tests/test_phase_11_error_recovery.py`

```python
@pytest.mark.asyncio
async def testCompleteErrorRecoveryFlow():
    """Integration test: checkpoint → error → propagate → recover"""
    
    orchestrator = Orchestrator(config)
    resilient = NetworkResilient()
    chain = ErrorPropagationChain(config)
    
    # Simulate multi-step execution with failure and recovery
    execution_id = "test_exec_1"
    
    # Step 1: Success, create checkpoint
    orchestrator.checkpoint_manager.createCheckpoint(
        execution_id, 1, {'progress': 'step_1_complete'}
    )
    
    # Step 2: Network error - attempt recovery with retry
    try:
        async def failing_call():
            raise ConnectionError("Network timeout")
        
        await resilient.executeWithRetry(failing_call, service="api")
    except Exception as e:
        # Error propagates through chain
        chain.propagate(
            NetworkError(str(e), "ERR_NETWORK"),
            agent_id="orchestrator",
            hierarchy_level=3
        )
    
    # Step 3: Resume from checkpoint after recovery
    state = orchestrator.checkpoint_manager.resumeFromCheckpoint(execution_id)
    assert state is not None
    assert state['progress'] == 'step_1_complete'
```

---

## Success Criteria

- [ ] testAdvancedErrorRecovery passes
- [ ] testAgentErrorPropagation passes
- [ ] testRecoveryFromNetworkFailure passes
- [ ] testCascadingErrorHandling passes
- [ ] All 681 tests passing (100%)
- [ ] Error recovery latency < 100ms
- [ ] Circuit breaker prevents cascading failures
- [ ] Audit trail complete for all errors

---

**Status**: Ready for Phase 11 Week 2 implementation  
**Last Updated**: 2026-08-22
