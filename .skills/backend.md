# Backend Skills (The Logic Hands)
**Agents**: Cursor (Complex), Copilot (Boilerplate/Ops)

## Skill: `implement_logic` (Cursor)
**Description**: Implement complex algorithms, business logic, or system architecture.
**Usage**:
```bash
python bridge.py cursor code --task "{logic_task}" --files "{files}" --reqs "{constraints}"
```

## Skill: `implement_ops` (Copilot)
**Description**: Write scripts, config files, or standard boilerplate code.
**Usage**:
```bash
python bridge.py copilot code --task "{task}" --files "{files}"
```

## Skill: `generate_tests` (Cursor)
**Description**: Create unit or integration tests for existing code.
**Usage**:
```bash
python bridge.py cursor code --task "Generate Unit Tests" --files "{source_file}" --reqs "Use Jest/Pytest"
```

## Skill: `cross_check` (Copilot)
**Description**: Have Copilot review code written by another agent.
**Usage**:
```bash
python bridge.py copilot review --files "{files}" --focus "Logic and Standards"
```
