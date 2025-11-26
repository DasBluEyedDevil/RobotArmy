# DevilMCP Skills (Context & Memory)
**Agent**: DevilMCP (via Adapter)
**Specialty**: Project Structure, Dependencies, Decision Tracking.

## Skill: `analyze_project`
**Description**: Scan the current project to build a dependency graph and context.
**Usage**:
```bash
python bridge.py devilmcp mcp_task --task "analyze --path ."
```

## Skill: `get_file_context`
**Description**: Get imports, dependencies, and usages for a specific file.
**Usage**:
```bash
python bridge.py devilmcp mcp_task --task "context --file {file_path}"
```

## Skill: `search_context`
**Description**: Search the indexed project knowledge.
**Usage**:
```bash
python bridge.py devilmcp mcp_task --task "search --query '{search_term}'"
```

## Skill: `log_decision`
**Description**: Record a significant architectural decision.
**Usage**:
```bash
python bridge.py devilmcp mcp_task --task "log_decision --decision '{decision_title}' --rationale '{reasoning}'"
```