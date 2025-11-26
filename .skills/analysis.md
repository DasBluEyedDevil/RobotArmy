# Analysis Skills (The Eyes)
**Agent**: Gemini
**Specialty**: 1M+ Token Context, Whole-Project Analysis

## Skill: `large_file_review`
**Description**: Read and summarize files that are too large for Claude's context.
**Usage**:
```bash
python bridge.py gemini analyze --task "Summarize this file" --files "{filepath}"
```

## Skill: `deep_dive_analysis`
**Description**: Analyze a specific directory or module to answer a complex question.
**Usage**:
```bash
python bridge.py gemini analyze --task "{question}" --dir "{directory_path}"
```

## Skill: `trace_bug`
**Description**: Follow a stack trace or logical error across multiple files to find the root cause.
**Usage**:
```bash
python bridge.py gemini analyze --task "Trace the root cause of: {error_message}" --dir "{relevant_dirs}"
```

## Skill: `security_audit`
**Description**: Scan code for vulnerabilities.
**Usage**:
```bash
python bridge.py gemini review --files "{target_files_or_dir}" --focus "Security Vulnerabilities (XSS, Injection, Auth)"
```
