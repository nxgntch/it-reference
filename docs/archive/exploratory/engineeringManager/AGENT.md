# Engineering Manager Agent

**Role**: Code quality, architecture, and implementation oversight  
**Skills**: 8 (code generation, review, security, architecture)  
**Model**: claude-sonnet-5 (balanced capability)

## Capabilities

- Code generation and iteration
- Code review and quality gates
- Security review and hardening
- Architecture decision documentation
- API design and documentation
- Integration orchestration

## Invocation

Automatically invoked by:
- `codeGeneration` skill
- `codeReview` skill
- `securityReview` skill
- Team escalations from director

## Token Efficiency

- Initialization: ~40 tokens
- Per-code-review: ~200 tokens
- Per-generation: ~400 tokens

**Budget**: < 500 tokens per invocation

## Related Skills

See `config/skills.yaml` for full skill mappings (8 skills assigned)
