import sys
import os
import argparse
import yaml
import subprocess
import shlex
from typing import Dict, Any, List

CONFIG_FILE = "config.yaml"

def load_config(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        print(f"Error: Config file '{path}' not found.")
        sys.exit(1)
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def build_command(agent_name: str, agent_config: Dict[str, Any], prompt: str) -> List[str]:
    cmd = agent_config.get("cmd", "")
    if not cmd:
        print(f"Error: No command defined for agent '{agent_name}'")
        sys.exit(1)

    # Split command into parts (e.g., "wsl -u user tool" -> ["wsl", "-u", "user", "tool"])
    command_parts = shlex.split(cmd)
    
    # Add static flags
    static_flags = agent_config.get("static_flags", [])
    command_parts.extend(static_flags)
    
    # Add the prompt. 
    # Note: specific handling might be needed per tool if they don't all accept the prompt as the final arg.
    # Copilot: -p "prompt" (handled in static_flags or here)
    # Gemini: -p "prompt" (usually)
    # Codex: exec "prompt" (or piped)
    
    # Simple append strategy for now, assuming static_flags handles the -p switch if needed
    # or if the tool accepts the prompt as a positional arg.
    
    # Special handling based on agent type if needed (can be generalized in config later)
    if agent_name == "gemini":
        if "-p" not in static_flags:
            command_parts.append("-p")
        command_parts.append(prompt)
    elif agent_name == "copilot":
        # Copilot usually needs -p flag, assuming it's in static_flags or we add it
        if "-p" not in command_parts: # simple check
             # command_parts.append("-p") # assumed in config for now
             pass
        command_parts.append(prompt)
    elif agent_name == "cursor":
        # Cursor agent usually accepts prompt as positional
        command_parts.append(prompt)
    elif agent_name == "codex":
        # Codex exec "prompt"
        command_parts.append(prompt)
    else:
        command_parts.append(prompt)
        
    return command_parts

def main():
    parser = argparse.ArgumentParser(description="Universal Agent Bridge")
    parser.add_argument("agent", help="The agent to use (gemini, cursor, codex, copilot)")
    parser.add_argument("template", help="The template key (analyze, code, review) or 'raw' for direct prompt")
    parser.add_argument("--task", help="Task description")
    parser.add_argument("--context", help="Additional context", default="")
    parser.add_argument("--files", help="Target files", default="")
    parser.add_argument("--reqs", help="Requirements", default="")
    parser.add_argument("--focus", help="Review focus", default="General")
    parser.add_argument("--dir", help="Target directory (for Gemini)", default="")
    
    # Allow passing raw prompt as a positional arg if template is 'raw'
    parser.add_argument("raw_prompt", nargs="?", help="Raw prompt text if template is 'raw'")

    args = parser.parse_args()
    config = load_config(CONFIG_FILE)
    
    agent_config = config["agents"].get(args.agent)
    if not agent_config:
        print(f"Error: Agent '{args.agent}' not configured.")
        sys.exit(1)

    # Prepare prompt
    prompt = ""
    if args.template == "raw":
        prompt = args.raw_prompt or args.task # Fallback to task if raw_prompt empty
    else:
        template_str = config["templates"].get(args.template)
        if not template_str:
            print(f"Error: Template '{args.template}' not found.")
            sys.exit(1)
            
        # Format template
        try:
            prompt = template_str.format(
                task=args.task,
                context=args.context,
                files=args.files,
                reqs=args.reqs,
                focus=args.focus
            )
        except KeyError as e:
            print(f"Error processing template: Missing argument {e}")
            sys.exit(1)

    # Prepend Directory context for Gemini if provided
    if args.agent == "gemini" and args.dir:
        # Gemini CLI usually takes -d or @dir syntax. 
        # Let's prepend it to the prompt text for the 'wrapper' style 
        # or if using the actual CLI, we might need to inject args.
        # For this bridge, we'll prepend to prompt as standard instruction
        prompt = f"Target Directories: {args.dir}\n\n{prompt}"

    # Build Command
    cmd_list = build_command(args.agent, agent_config, prompt)
    
    print(f"\n[Bridge] Agent: {config['agents'][args.agent]['name']}")
    print(f"[Bridge] Template: {args.template}")
    # print(f"[Bridge] Command: {' '.join(cmd_list)}") # Debug only
    
    # Execute
    try:
        # Using shell=False for security, passing list
        subprocess.run(cmd_list, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing agent: {e}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Error: Executable for {args.agent} not found in path.")
        sys.exit(1)

if __name__ == "__main__":
    main()
