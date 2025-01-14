#!/usr/bin/env python3
import sys

from litellm import completion
import os

# Ensure color output isn't disabled
os.environ["FORCE_COLOR"] = "1"
from rich.console import Console
from rich.live import Live
from rich.text import Text


def analyze_script(script_content):
    """Analyze the script using LLM and stream the response"""
    model = os.environ.get("BASH_INSPECTOR_MODEL", "openai/gpt-4")

    prompt = f"""Analyze this bash script for signs of malicious intent ONLY. 
Do not report on general security best practices or potential vulnerabilities - focus solely on code that appears deliberately malicious.

Look for:
1. Intentional data theft or exfiltration
2. Malware downloads or malicious connections
3. Deliberate system compromise attempts
4. Intentionally obfuscated malicious code
5. Backdoor installation attempts

Script to analyze:
```bash
{script_content}
```

Use Rich console markup in your response. Format as follows:

If you find potentially malicious code, for each finding use:

[bold red]Finding #[/bold red]

[white on grey15]<paste the relevant lines>[/white on grey15]

[bold red]Why it's suspicious:[/bold red] [red]<very brief, one-line explanation>[/red]

If you find NO malicious content, respond ONLY with:

[bold green]✅ No malicious content found[/bold green]
[bold red]🚨 but still proceed at your own risk[/bold red]

If you DO find suspicious content, append this line after all findings:

[bold red]🚨 Potentially malicious content found. See above.[/bold red]

There should be no additional content beyond the findings and the final line."""

    console = Console(stderr=True)
    console.print("\n[bold blue]Analyzing script security...[/bold blue]\n")

    full_response = ""
    with Live(
        Text.from_markup(full_response), refresh_per_second=1, console=console
    ) as live:
        response = completion(
            model=model,
            messages=[{"content": prompt, "role": "user"}],
            stream=True,
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                live.update(Text.from_markup(full_response))

    print("\n")


def prompt_user():
    """Prompt user to proceed or abort"""
    sys.stderr.write("\nAnalysis complete.\n")

    while True:
        sys.stderr.write("\nDo you want to proceed with the installation? [y/N]: ")
        sys.stderr.flush()

        try:
            # Try using /dev/tty directly
            with open("/dev/tty", "r") as tty:
                response = tty.readline().strip().lower()
        except:
            # Fallback to basic input if /dev/tty is not available
            try:
                response = input().strip().lower()
            except EOFError:
                # If we can't get input, default to no
                sys.stderr.write("Could not get user input, aborting for safety\n")
                return False

        if response in ["y", "yes"]:
            return True
        if response in ["", "n", "no"]:
            return False
        sys.stderr.write("Please answer 'y' or 'n'\n")


def main():
    if sys.stdin.isatty():
        console = Console(stderr=True)
        console.print("[red]Usage:[/red] curl URL | binspect | bash", style="bold")
        sys.exit(1)

    # Read the script content from stdin
    script_content = sys.stdin.read()

    # Analyze the script
    analyze_script(script_content)

    # Now that user has seen the analysis, ask for their decision
    if prompt_user():
        # Proceed: output the original script
        print(script_content)
    else:
        print("Installation aborted by user", file=sys.stderr)
        sys.exit(1)
