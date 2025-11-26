# Universal Agent Bridge & Skill System: Design Document

## Overview
This system implements the **AI Quadrumvirate** pattern by providing a structured bridge between a primary Orchestrator (Claude) and specialized Sub-Agents (Gemini, Cursor, Copilot, Codex). Unlike API-based MCP servers, this system leverages **subscription-based CLI tools** already authenticated in the user's environment.

The system consists of two layers:
1.  **The Bridge (`bridge` CLI)**: A uniform execution layer that normalizes interaction with diverse underlying CLIs.
2.  **The Skills (`.skills/*.md`)**: A semantic interface that teaches Claude *how* and *when* to invoke the Bridge.

---

## 1. The Agents (The Backend)

| Agent | Role | Underlying CLI | Specialization |
| :--- | :--- | :--- | :--- |
| **Gemini** | "The Eyes" | `gemini` | Unlimited context analysis, large file reading, bug tracing, architectural review. |
| **Cursor** | "The Hands #1" | `cursor-agent` | Complex reasoning, refactoring, hard problems. (Best for logic/architecture). |
| **Codex** | "The Hands #2" | `codex` | UI/Visual implementation, Frontend, React/Next.js. (Best for visual/web). |
| **Copilot**| "The Hands #3" | `copilot` | Backend, Terminal, Git operations, high-volume boilerplate. |

---

## 2. The Bridge (Execution Layer)

The Bridge is a configurable Python script (`bridge.py`) that accepts high-level intents and translates them into specific CLI commands.

### Configuration (`config.yaml`)
```yaml
defaults:
  mode: "yolo" # "safe" (ask) or "yolo" (force)
  output: "text"

agents:
  gemini:
    cmd: "gemini"
    args: "--all-files -p"
  
  cursor:
    cmd: "cursor-agent" # Run in WSL if needed
    args: "--model sonnet-4.5 --force"
    
  codex:
    cmd: "codex"
    args: "--model gpt-5 --dangerously-bypass-approvals-and-sandbox exec"
    capabilities: ["search"]
    
  copilot:
    cmd: "copilot"
    args: "--allow-all-tools -p"

templates:
  analyze: "Context: {context}\nTask: {task}\nProvide: File paths and code snippets."
  code: "Task: {task}\nFiles: {files}\nRequirements: {reqs}"
```

### Command Interface
```bash
# Generic Syntax
bridge <agent> <template> [options]

# Examples
bridge gemini analyze --dir src/ "Explain the auth flow"
bridge codex code --file src/App.tsx "Add a dark mode toggle"
bridge copilot task --allow-git "Commit changes"
```

---

## 3. The Skills (The Interface)

These Markdown files (located in `.skills/`) define "tools" that Claude effectively "installs" into its context.

### File Structure
```text
.skills/
├── CLAUDE.md                  # Main System Prompt / Orchestrator Instructions
├── analysis_tools.md          # Tools for reading/analyzing (Gemini)
├── coding_frontend.md         # Tools for UI/Visual (Codex)
├── coding_backend.md          # Tools for Logic/System (Cursor/Copilot)
└── project_management.md      # Tools for Git/Planning
```

### Skill Definitions (Example: `analysis_tools.md`)

Each skill is defined as a **Virtual Tool** with a specific trigger, usage pattern, and underlying `bridge` command.

#### `large_file_review`
*   **Description**: Reviews huge files or entire directories that exceed Claude's token limit.
*   **When to use**: When you need to understand a file >100 lines, or analyze directory structure.
*   **Underlying Command**: 
    ```bash
    bridge gemini analyze --dir "{target_dir}" "{question}"
    ```

#### `trace_bug`
*   **Description**: Traces error stacks across multiple files to find the root cause.
*   **When to use**: When debugging complex issues spanning modules.
*   **Underlying Command**:
    ```bash
    bridge gemini analyze "Error: {error_msg}. Trace root cause in {dirs}."
    ```

---

## 4. Orchestrator Instruction (`CLAUDE.md`)

This file serves as the entry point for Claude.

**Key Directives:**
1.  **Token Economy**: "You are the Orchestrator. Your context window is expensive. Do not read code files directly unless they are tiny (<50 lines). Use `large_file_review` instead."
2.  **Delegation**: "Do not write implementation code. Delegate UI tasks to `implement_ui` (Codex) and backend tasks to `implement_logic` (Cursor/Copilot)."
3.  **Tool Usage**: "To use a tool, output the specific `bridge` command defined in the skill file."

---

## Implementation Plan

1.  **Generate `.skills/CLAUDE.md`**: The master instruction file.
2.  **Generate `.skills/analysis.md`**: Gemini-based skills.
3.  **Generate `.skills/frontend.md`**: Codex-based skills.
4.  **Generate `.skills/backend.md`**: Cursor/Copilot-based skills.
5.  **Generate `bridge.py`**: The python script to handle the logic.
6.  **Generate `config.yaml`**: The configuration file.

This approach allows Claude to "see" a suite of powerful tools that map directly to the CLI agents, abstracting away the complexity of flags and environments.