# Project Management Skills
**Agent**: Copilot (shell access)

## Skill: `git_commit`
**Description**: Stage and commit changes with a descriptive message.
**Usage**:
```bash
python bridge.py copilot raw --task "Git commit all changes with message: {message}"
```

## Skill: `create_pr`
**Description**: Create a Pull Request (requires gh cli configured).
**Usage**:
```bash
python bridge.py copilot raw --task "Create a PR for the current branch titled '{title}'"
```

## Skill: `scaffold_project`
**Description**: Set up folder structure and initial files.
**Usage**:
```bash
python bridge.py copilot code --task "Scaffold new project structure" --reqs "{structure_description}"
```
