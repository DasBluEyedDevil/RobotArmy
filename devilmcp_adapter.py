import sys
import os
import argparse
import asyncio
import json
import logging

# Add DevilMCP to path
DEVILMCP_PATH = r"C:\Users\dasbl\PycharmProjects\DevilMCP"
sys.path.append(DEVILMCP_PATH)

try:
    from devilmcp.database import DatabaseManager
    from devilmcp.context_manager import ContextManager
    from devilmcp.decision_tracker import DecisionTracker
    # Add other managers as needed
except ImportError as e:
    print(f"Error importing DevilMCP modules: {e}")
    print("Ensure you have the required dependencies installed (sqlalchemy, etc.)")
    sys.exit(1)

# Setup Logging to stderr so it doesn't corrupt JSON stdout
logging.basicConfig(level=logging.ERROR, stream=sys.stderr)

async def main():
    parser = argparse.ArgumentParser(description="DevilMCP CLI Adapter")
    parser.add_argument("command", choices=["analyze", "context", "log_decision", "search"])
    parser.add_argument("--path", help="Project path")
    parser.add_argument("--file", help="File path")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--decision", help="Decision text")
    parser.add_argument("--rationale", help="Decision rationale")
    
    args = parser.parse_args()

    # Initialize DB (Use centralized or local storage)
    # For simplicity, using a temp/local storage for the adapter
    storage_path = os.path.join(DEVILMCP_PATH, ".devilmcp", "storage")
    os.makedirs(storage_path, exist_ok=True)
    
    db_manager = DatabaseManager(storage_path)
    await db_manager.init_db()
    
    context_mgr = ContextManager(db_manager)
    decision_tracker = DecisionTracker(db_manager)

    result = {}

    try:
        if args.command == "analyze":
            target_path = args.path or os.getcwd()
            result = await context_mgr.analyze_project_structure(target_path)
            
        elif args.command == "context":
            if args.file:
                result = await context_mgr.get_focused_context(args.file)
            else:
                result = await context_mgr.get_project_context(args.path)
                
        elif args.command == "search":
            if not args.query:
                raise ValueError("--query required for search")
            result = await context_mgr.search_context(args.query)
            
        elif args.command == "log_decision":
            if not args.decision or not args.rationale:
                raise ValueError("--decision and --rationale required")
            # Minimal context for now
            context = {"source": "cli_adapter"} 
            result = await decision_tracker.log_decision(args.decision, args.rationale, context)

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
