#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # dotenv is optional


# Color helper functions
def red(text):
    """Format text in red."""
    return f"\033[91m{text}\033[0m"


def yellow(text):
    """Format text in yellow."""
    return f"\033[33m{text}\033[0m"


def bright_yellow(text):
    """Format text in bright yellow."""
    return f"\033[93m{text}\033[0m"


def green(text):
    """Format text in green."""
    return f"\033[32m{text}\033[0m"


def cyan(text):
    """Format text in cyan."""
    return f"\033[36m{text}\033[0m"


def magenta(text):
    """Format text in magenta."""
    return f"\033[95m{text}\033[0m"


def white(text):
    """Format text in white."""
    return f"\033[37m{text}\033[0m"


def bright_white(text):
    """Format text in bright white."""
    return f"\033[97m{text}\033[0m"


def gray(text):
    """Format text in gray."""
    return f"\033[90m{text}\033[0m"


def blue(text):
    """Format text in blue."""
    return f"\033[34m{text}\033[0m"


def log_status_line(input_data, status_line_output, error_message=None):
    """Log status line event to logs directory."""
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "status_line.json"

    # Read existing log data or initialize empty list
    if log_file.exists():
        with open(log_file, "r") as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []

    # Create log entry with input data and generated output
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "version": "v5",
        "input_data": input_data,
        "status_line_output": status_line_output,
    }

    if error_message:
        log_entry["error"] = error_message

    # Append the log entry
    log_data.append(log_entry)

    # Write back to file with formatting
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)


def get_daily_cost():
    """Get today's Claude Code usage cost."""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        result = subprocess.run(
            ['npx', 'ccusage', 'daily', '--json'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            daily_data = data.get('daily', [])
            
            # Find today's data
            for day_data in daily_data:
                if day_data.get('date') == today:
                    cost = day_data.get('totalCost', 0)
                    return f"${cost:.2f}"
            
            return "$0.00"  # No usage today
    except Exception:
        pass
    
    return None  # Error occurred


def get_output_style():
    """Get current output style from settings."""
    try:
        # Style shortcuts for compact display - includes all Claude Code styles
        style_shortcuts = {
            'Default': 'Default',
            'Explanatory': 'Explain',
            'Learning': 'Learn',
            'Markdown Focused': 'MD',
            'Bullet Points': 'Bullets',
            'HTML Structured': 'HTML',
            'YAML Structured': 'YAML',
            'Ultra Concise': 'Concise',
            'Table Based': 'Table',
            'GenUI': 'GenUI'
        }

        # Check for current style in settings
        settings_files = ['settings.local.json', 'settings.json']

        for settings_file in settings_files:
            if Path(settings_file).exists():
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    output_style = settings.get('outputStyle')
                    if output_style:
                        return style_shortcuts.get(output_style, output_style)

        return None  # No output style found
    except Exception:
        pass

    return None  # Error occurred


def parse_transcript_tokens(transcript_path):
    """Parse transcript JSONL file to calculate current context tokens (like /context command)."""
    try:
        if not Path(transcript_path).exists():
            return None

        # Get the most recent assistant message with usage data
        # This represents the current context window calculation
        recent_usage = None

        with open(transcript_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    # Look for assistant messages with usage data (most recent wins)
                    if ('message' in data and 'usage' in data['message'] and
                        data.get('type') == 'assistant'):
                        recent_usage = data['message']['usage']
                except (json.JSONDecodeError, KeyError):
                    continue

        if not recent_usage:
            return None

        # Calculate current context tokens based on Claude's context window logic
        # System tokens (cached): cache_creation + cache_read represent system prompt + tools
        system_tokens = recent_usage.get('cache_creation_input_tokens', 0) + recent_usage.get('cache_read_input_tokens', 0)

        # Current message tokens: input + output for this interaction
        message_tokens = recent_usage.get('input_tokens', 0) + recent_usage.get('output_tokens', 0)

        # Current context = system + recent messages (approximation)
        # This should roughly match what /context shows
        current_context_tokens = system_tokens + message_tokens

        return current_context_tokens

    except Exception:
        return None


def get_token_usage(input_data):
    """Get token usage information from input data."""
    try:
        # Check if we have token information in the input data
        exceeds_200k = input_data.get('exceeds_200k_tokens', False)
        max_tokens = 200000  # Claude's context window

        # Try to get transcript path and parse actual tokens
        transcript_path = input_data.get('transcript_path')
        current_tokens = None

        if transcript_path:
            current_tokens = parse_transcript_tokens(transcript_path)

        # Fallback: If we don't have actual token counts, estimate based on cost and duration
        if current_tokens is None:
            cost_data = input_data.get('cost', {})
            total_duration = cost_data.get('total_duration_ms', 0)

            # Rough estimation: longer conversations use more tokens
            # Assume ~100 tokens per second of conversation
            if total_duration > 0:
                estimated_tokens = min(int(total_duration / 1000 * 100), max_tokens)
                current_tokens = estimated_tokens
            else:
                # If we have the exceeds flag, show we're near the limit
                if exceeds_200k:
                    current_tokens = max_tokens
                else:
                    # No data available, return None
                    return None

        # Format the token usage
        percentage = int((current_tokens / max_tokens) * 100)

        # Use different formatting based on usage level
        if percentage >= 90:
            # Critical - red
            icon = "🔴"
        elif percentage >= 70:
            # Warning - orange
            icon = "🟠"
        elif percentage >= 50:
            # Moderate - yellow
            icon = "🟡"
        else:
            # Good - green
            icon = "🟢"

        # Format tokens with K suffix for readability
        current_k = f"{current_tokens/1000:.0f}k" if current_tokens >= 1000 else str(current_tokens)
        max_k = f"{max_tokens/1000:.0f}k" if max_tokens >= 1000 else str(max_tokens)

        return f"{icon} {current_k}/{max_k} ({percentage}%)"

    except Exception:
        pass

    return None  # Error occurred


def get_git_info():
    """Get comprehensive git information."""
    git_info = {}
    
    try:
        # Get current branch
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            git_info['branch'] = result.stdout.strip()
        
        # Get status (modified files count)
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                lines = changes.split('\n')
                # Count different types of changes
                added = sum(1 for l in lines if l.startswith('A ') or l.startswith('??'))
                modified = sum(1 for l in lines if l.startswith(' M') or l.startswith('M '))
                deleted = sum(1 for l in lines if l.startswith(' D') or l.startswith('D '))
                
                if added + modified + deleted > 0:
                    status_parts = []
                    if added > 0:
                        status_parts.append(f"+{added}")
                    if modified > 0:
                        status_parts.append(f"~{modified}")
                    if deleted > 0:
                        status_parts.append(f"-{deleted}")
                    git_info['changes'] = ''.join(status_parts)
        
        # Get ahead/behind status with upstream
        result = subprocess.run(
            ['git', 'rev-list', '--left-right', '--count', 'HEAD...@{upstream}'],
            capture_output=True,
            text=True,
            timeout=2,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            ahead, behind = result.stdout.strip().split('\t')
            if int(ahead) > 0:
                git_info['ahead'] = ahead
            if int(behind) > 0:
                git_info['behind'] = behind
                
    except Exception:
        pass
    
    return git_info


def get_session_data(session_id):
    """Get session data including agent name, prompts, and extras."""
    session_file = Path(f".claude/data/sessions/{session_id}.json")

    if not session_file.exists():
        return None, f"Session file {session_file} does not exist"

    try:
        with open(session_file, "r") as f:
            session_data = json.load(f)
            return session_data, None
    except Exception as e:
        return None, f"Error reading session file: {str(e)}"


def truncate_prompt(prompt, max_length=80):
    """Truncate prompt to specified length."""
    # Remove newlines and excessive whitespace
    prompt = " ".join(prompt.split())

    if len(prompt) > max_length:
        return prompt[: max_length - 3] + "..."
    return prompt


def get_prompt_icon(prompt):
    """Get icon based on prompt type."""
    if prompt.startswith("/"):
        return "⚡"
    elif "?" in prompt:
        return "❓"
    elif any(
        word in prompt.lower()
        for word in ["create", "write", "add", "implement", "build"]
    ):
        return "💡"
    elif any(word in prompt.lower() for word in ["fix", "debug", "error", "issue"]):
        return "🐛"
    elif any(word in prompt.lower() for word in ["refactor", "improve", "optimize"]):
        return "♻️"
    elif any(word in prompt.lower() for word in ["test", "verify", "check"]):
        return "🧪"
    elif any(word in prompt.lower() for word in ["analyze", "review", "compare"]):
        return "🔍"
    else:
        return "💬"


def format_session_duration(duration_str):
    """Format session duration with color based on length."""
    if not duration_str:
        return None

    # Parse duration to get total minutes for color decision
    total_minutes = 0
    if 'h' in duration_str:
        # Has hours
        parts = duration_str.replace('h', ' ').replace('m', '').split()
        if len(parts) >= 2:
            total_minutes = int(parts[0]) * 60 + int(parts[1])
        else:
            total_minutes = int(parts[0]) * 60
    elif 'm' in duration_str:
        # Only minutes
        total_minutes = int(duration_str.replace('m', '').replace('s', '').split('m')[0])

    # Color based on session length
    if total_minutes >= 120:  # 2+ hours - red (long session)
        return red(f"⏱️ {duration_str}")
    elif total_minutes >= 60:  # 1+ hour - yellow (medium session)
        return yellow(f"⏱️ {duration_str}")
    elif total_minutes >= 30:  # 30+ min - green (active session)
        return green(f"⏱️ {duration_str}")
    else:  # < 30min - white (fresh session)
        return white(f"⏱️ {duration_str}")


def format_extras(extras, git_info, daily_cost=None, output_style=None):
    """Format extras dictionary and git info into a compact string."""
    combined = {}

    # Add daily cost (high priority)
    if daily_cost:
        combined['💰'] = daily_cost

    # Add output style (high priority)
    if output_style:
        combined['📝'] = output_style

    # Add git info to extras
    if git_info:
        if 'branch' in git_info:
            combined['🌿'] = git_info['branch']
            if 'changes' in git_info:
                combined['🌿'] += f" {git_info['changes']}"
            if 'ahead' in git_info:
                combined['🌿'] += f" ↑{git_info['ahead']}"
            if 'behind' in git_info:
                combined['🌿'] += f" ↓{git_info['behind']}"

    # Add other extras
    if extras:
        for key, value in extras.items():
            # Truncate value if too long
            str_value = str(value)
            if len(str_value) > 20:
                str_value = str_value[:17] + "..."
            combined[key] = str_value

    if not combined:
        return None

    # Format each key-value pair
    pairs = []
    for key, value in combined.items():
        if key.startswith('�') or key.startswith('🌿') or key.startswith('💰') or key.startswith('📝'):  # Emoji keys don't need separator
            pairs.append(f"{key} {value}")
        else:
            pairs.append(f"{key} {value}")

    return " | ".join(pairs)


def get_session_duration(session_id):
    """Calculate active session duration (sum of interaction intervals) from last /clear command."""
    try:
        log_file = Path("logs/status_line.json")
        if not log_file.exists():
            return None

        with open(log_file, "r") as f:
            log_data = json.load(f)

        # Find entries for this session_id
        session_entries = []
        for entry in log_data:
            if entry.get("input_data", {}).get("session_id") == session_id:
                session_entries.append(entry)

        if not session_entries:
            return None

        # Sort entries by timestamp to ensure chronological order
        session_entries.sort(key=lambda x: x.get("timestamp", ""))

        # Find the index of the last /clear command
        clear_index = 0
        for i, entry in enumerate(session_entries):
            input_data = entry.get("input_data", {})
            prompt = input_data.get("prompt", "")
            if prompt.strip().startswith("/clear"):
                clear_index = i

        # Get entries since last /clear (including the /clear entry)
        active_entries = session_entries[clear_index:]

        if len(active_entries) < 1:
            return None

        # Calculate active time by summing intervals between consecutive interactions
        from datetime import datetime
        total_active_seconds = 0
        inactivity_threshold = 300  # 5 minutes in seconds

        for i in range(len(active_entries) - 1):
            current_time = datetime.fromisoformat(active_entries[i]["timestamp"])
            next_time = datetime.fromisoformat(active_entries[i + 1]["timestamp"])
            interval_seconds = (next_time - current_time).total_seconds()

            # Only count intervals shorter than inactivity threshold
            if interval_seconds <= inactivity_threshold:
                total_active_seconds += interval_seconds

        # Add time since last interaction (if recent)
        if active_entries:
            last_time = datetime.fromisoformat(active_entries[-1]["timestamp"])
            current_time = datetime.now()
            time_since_last = (current_time - last_time).total_seconds()

            # Only count if last interaction was recent (within threshold)
            if time_since_last <= inactivity_threshold:
                total_active_seconds += time_since_last

        # Format duration
        total_seconds = int(total_active_seconds)
        if total_seconds < 60:
            return f"{total_seconds}s"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}m{seconds}s"
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h{minutes}m"

    except Exception:
        return None


def format_token_usage(token_usage):
    """Format token usage with colors instead of emojis."""
    if not token_usage:
        return None

    # Extract the percentage from token_usage string (format: "emoji current/max (xx%)")
    try:
        # Find percentage in parentheses
        import re
        percentage_match = re.search(r'\((\d+)%\)', token_usage)
        if not percentage_match:
            return white(token_usage)  # Default white if can't parse

        percentage = int(percentage_match.group(1))

        # Remove emoji from the beginning and format with colors
        # Extract the part without emoji (everything after first space)
        parts = token_usage.split(' ', 1)
        if len(parts) < 2:
            token_text = token_usage
        else:
            token_text = parts[1]  # Skip emoji

        # Choose color based on usage level
        if percentage >= 90:
            # Critical - bright red
            return red(token_text)
        elif percentage >= 70:
            # Warning - bright yellow
            return bright_yellow(token_text)
        elif percentage >= 50:
            # Moderate - yellow
            return yellow(token_text)
        else:
            # Good - green
            return green(token_text)

    except Exception:
        # Fallback to white if parsing fails
        return white(token_usage)


def generate_status_line(input_data):
    """Generate the status line with agent, model, version, prompt, and git info."""
    # Extract session ID from input data
    session_id = input_data.get("session_id", "unknown")

    # Get model info
    model_info = input_data.get("model", {})
    model_name = model_info.get("display_name", "Claude")
    
    # Get version info
    version = input_data.get("version", "")

    # Get session data
    session_data, error = get_session_data(session_id)

    if error:
        # Log the error but show a default message
        log_status_line(input_data, f"{model_name} 💭 No session data", error)
        return f"{blue(model_name)} {gray('💭 No session data')}"

    # Extract agent name, prompts, and extras
    agent_name = session_data.get("agent_name", None)
    prompts = session_data.get("prompts", [])
    extras = session_data.get("extras", {})
    
    # Get git information
    git_info = get_git_info()

    # Get daily cost
    daily_cost = get_daily_cost()

    # Get output style
    output_style = get_output_style()

    # Get token usage
    token_usage = get_token_usage(input_data)

    # Get session duration
    session_duration = get_session_duration(session_id)

    # Build status line components
    parts = []

    # Combined Agent + Model + Version - Gradient effect
    if agent_name:
        agent_model_version = f"{agent_name} | {model_name}"
    else:
        agent_model_version = model_name
    if version:
        agent_model_version += f" | v{version}"
    parts.append(magenta(agent_model_version))

    # Last 3 prompts (most recent first)
    if prompts:
        # Current prompt - bright white with icon
        current_prompt = prompts[-1]
        icon = get_prompt_icon(current_prompt)
        truncated = truncate_prompt(current_prompt, 70)
        # Combine icon with colored text to avoid spacing issues
        parts.append(bright_white(f"{icon} {truncated}"))
        
        # Previous prompt - light gray, shorter
        if len(prompts) > 1:
            prev_prompt = prompts[-2]
            prev_icon = get_prompt_icon(prev_prompt)
            truncated = truncate_prompt(prev_prompt, 50)
            parts.append(gray(f"{prev_icon} {truncated}"))
        
        # Older prompt - darker gray, even shorter
        if len(prompts) > 2:
            older_prompt = prompts[-3]
            older_icon = get_prompt_icon(older_prompt)
            truncated = truncate_prompt(older_prompt, 35)
            parts.append(gray(f"{older_icon} {truncated}…"))
    else:
        parts.append(gray("💭 No prompts yet"))

    # Add session duration with colors (separate from extras)
    duration_display = format_session_duration(session_duration)
    if duration_display:
        parts.append(duration_display)

    # Add token usage with colors (separate from extras)
    token_display = format_token_usage(token_usage)
    if token_display:
        parts.append(token_display)

    # Add extras and git info
    extras_str = format_extras(extras, git_info, daily_cost, output_style)
    if extras_str:
        # Display extras in cyan
        parts.append(cyan(extras_str))

    # Join with separator
    status_line = " | ".join(parts)

    return status_line


def main():
    try:
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())

        # Generate status line
        status_line = generate_status_line(input_data)

        # Log the status line event (without error since it's successful)
        log_status_line(input_data, status_line)

        # Output the status line (first line of stdout becomes the status line)
        print(status_line)

        # Success
        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully - output basic status
        print(red("Claude 💭 JSON Error"))
        sys.exit(0)
    except Exception as e:
        # Handle any other errors gracefully - output basic status
        print(red(f"Claude 💭 Error: {str(e)}"))
        sys.exit(0)


if __name__ == "__main__":
    main()
