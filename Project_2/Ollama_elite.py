"""
Ollama Interaction Suite - Professional LLM Interface
---------------------------------------------------------
An elite implementation for seamless interaction with Ollama models
featuring comprehensive error handling, streaming responses, detailed analytics,
and Project 2 COMP 474 specific requirements implementation.
"""

import ollama
import time
import json
import logging
import threading
import sys
import os
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.theme import Theme
from rich.syntax import Syntax

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("ollama_interaction.log"), logging.StreamHandler()]
)

# Initialize Rich console with custom theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "prompt": "bold blue",
    "response": "bright_white",
    "metrics": "dim white",
    "project": "magenta",
})
console = Console(theme=custom_theme)

class OllamaInteractionSuite:
    """Professional interface for Ollama LLM interactions with advanced features."""
    
    def __init__(self, default_model='llama3.2'):
        """Initialize the interaction suite with configuration parameters."""
        self.default_model = default_model
        self.session_start = datetime.now()
        self.interaction_count = 0
        self.models_cache = None
        self.last_response_time = 0
        self.cumulative_token_count = 0
        self.stream_mode = False
        self.conversation_history = []
        self.conversation_file = "conversation_history.json"
        self.load_conversation_history()
        
        # Create output directory for saving responses
        self.output_dir = "llm_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Verify Ollama server connection on startup
        self._verify_ollama_connection()
    
    def _verify_ollama_connection(self):
        """Verify connection to Ollama server and cache available models."""
        with console.status("[info]Connecting to Ollama server...", spinner="dots"):
            try:
                self.models_cache = ollama.list()
                console.print(f"[success]✓ Connected to Ollama server")
                console.print(f"[info]Available models: {len(self.models_cache['models'])}")
            except Exception as e:
                console.print(f"[error]! Failed to connect to Ollama server: {str(e)}")
                console.print("[info]Make sure Ollama is running (https://ollama.ai/download)")
                console.print("[info]Run 'ollama serve' if installed but not running")
                sys.exit(1)
    
    def load_conversation_history(self):
        """Load conversation history from file if exists."""
        try:
            if os.path.exists(self.conversation_file):
                with open(self.conversation_file, 'r') as f:
                    self.conversation_history = json.load(f)
                console.print(f"[info]Loaded {len(self.conversation_history)} previous conversation turns")
        except Exception as e:
            console.print(f"[warning]Could not load conversation history: {str(e)}")
            self.conversation_history = []
    
    def save_conversation_history(self):
        """Save conversation history to file."""
        try:
            with open(self.conversation_file, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
        except Exception as e:
            console.print(f"[warning]Could not save conversation history: {str(e)}")
    
    def list_available_models(self):
        """Display available models in a formatted table."""
        try:
            # Always get fresh model list
            models_data = ollama.list()
            
            # Create and populate table
            table = Table(title="Available Ollama Models")
            table.add_column("Model", style="cyan")
            table.add_column("Size", style="green")
            table.add_column("Modified", style="yellow")
            table.add_column("Quantization", style="magenta")
            
            for model in models_data['models']:
                size_mb = f"{model['size'] / 1024 / 1024:.1f} MB"
                modified = datetime.fromtimestamp(model['modified']).strftime('%Y-%m-%d %H:%M')
                quant = model.get('details', {}).get('quantization_level', 'N/A')
                table.add_row(model['name'], size_mb, modified, quant)
            
            console.print(table)
            return True
        except Exception as e:
            console.print(f"[error]Error listing models: {str(e)}")
            return False
    
    def generate_response(self, prompt, model_name=None, stream=None, system_prompt=None):
        """
        Generate a response from Ollama with detailed metrics.
        
        Args:
            prompt (str): User query to process
            model_name (str, optional): Model to use, defaults to instance default
            stream (bool): Whether to stream the response token by token
            system_prompt (str, optional): System prompt to guide model behavior
            
        Returns:
            dict: Response data with content and metrics
        """
        model = model_name or self.default_model
        stream = self.stream_mode if stream is None else stream
        start_time = time.time()
        self.interaction_count += 1
        
        try:
            # Format the messages for the API
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history for context (with a limit to avoid context length issues)
            for turn in self.conversation_history[-5:]:  # Include last 5 turns
                messages.append({"role": turn["role"], "content": turn["content"]})
            
            # Add the current prompt
            messages.append({"role": "user", "content": prompt})
            
            # Add current prompt to conversation history
            self.conversation_history.append({"role": "user", "content": prompt, "timestamp": datetime.now().isoformat()})
            
            if stream:
                return self._stream_response(model, messages)
            else:
                with console.status(f"[info]Generating response with {model}...", spinner="dots"):
                    response = ollama.chat(model=model, messages=messages)
                    
                # Track performance metrics
                self.last_response_time = time.time() - start_time
                if 'eval_count' in response:
                    self.cumulative_token_count += response['eval_count']
                
                # Add response to conversation history
                if 'message' in response and 'content' in response['message']:
                    self.conversation_history.append({
                        "role": "assistant", 
                        "content": response['message']['content'],
                        "timestamp": datetime.now().isoformat()
                    })
                    self.save_conversation_history()
                
                # Save response to file (Project 2 requirement)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_dir}/response_{timestamp}.md"
                
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"# LLM Response - {timestamp}\n\n")
                        f.write(f"## Prompt\n\n{prompt}\n\n")
                        f.write(f"## Response\n\n{response['message']['content']}\n\n")
                        f.write(f"## Metadata\n\n")
                        f.write(f"- Model: {response.get('model', 'unknown')}\n")
                        f.write(f"- Response time: {self.last_response_time:.2f} seconds\n")
                        f.write(f"- Tokens generated: {response.get('eval_count', 'unknown')}\n")
                    console.print(f"[info]Response saved to {filename}")
                except Exception as e:
                    console.print(f"[warning]Could not save response to file: {str(e)}")
                
                return response
                
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logging.error(error_msg)
            return {"error": error_msg}
    
    def _stream_response(self, model, messages):
        """Stream response token by token with visual progress indicator."""
        full_response = {"message": {"content": ""}}
        
        # Set up the progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"[cyan]Generating response with {model}...", total=None)
            
            try:
                # Generator approach to stream the response
                for chunk in ollama.chat(
                    model=model,
                    messages=messages,
                    stream=True
                ):
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        console.print(content, end="")
                        full_response["message"]["content"] += content
                        
                    # Update full response with metrics
                    for key, value in chunk.items():
                        if key != 'message':
                            full_response[key] = value
                
                console.print()  # Add newline at end
                
                # Add response to conversation history
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": full_response['message']['content'],
                    "timestamp": datetime.now().isoformat()
                })
                self.save_conversation_history()
                
                # Save response to file (Project 2 requirement)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_dir}/stream_response_{timestamp}.md"
                
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"# LLM Streamed Response - {timestamp}\n\n")
                        f.write(f"## Prompt\n\n{messages[-1]['content']}\n\n")
                        f.write(f"## Response\n\n{full_response['message']['content']}\n\n")
                        f.write(f"## Metadata\n\n")
                        f.write(f"- Model: {full_response.get('model', 'unknown')}\n")
                        if 'total_duration' in full_response:
                            duration_ms = full_response["total_duration"] / 1_000_000
                            f.write(f"- Response time: {duration_ms:.2f} ms\n")
                        if 'eval_count' in full_response:
                            f.write(f"- Tokens generated: {full_response['eval_count']}\n")
                    console.print(f"[info]Streamed response saved to {filename}")
                except Exception as e:
                    console.print(f"[warning]Could not save response to file: {str(e)}")
                
                return full_response
                
            except Exception as e:
                error_msg = f"Error in streaming response: {str(e)}"
                logging.error(error_msg)
                return {"error": error_msg}
    
    def display_session_stats(self):
        """Display detailed session statistics."""
        session_duration = datetime.now() - self.session_start
        minutes = session_duration.total_seconds() / 60
        
        table = Table(title="Session Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Session Duration", f"{minutes:.2f} minutes")
        table.add_row("Interactions", str(self.interaction_count))
        table.add_row("Last Response Time", f"{self.last_response_time:.2f} seconds")
        table.add_row("Total Tokens Generated", f"{self.cumulative_token_count}")
        table.add_row("Conversation History Size", f"{len(self.conversation_history)} turns")
        
        if self.interaction_count > 0 and minutes > 0:
            table.add_row("Avg. Tokens per Minute", f"{self.cumulative_token_count / minutes:.1f}")
            table.add_row("Avg. Tokens per Interaction", f"{self.cumulative_token_count / self.interaction_count:.1f}")
        
        console.print(table)

    def clear_conversation_history(self):
        """Clear the current conversation history."""
        self.conversation_history = []
        self.save_conversation_history()
        console.print("[success]Conversation history cleared")

    def save_conversation_to_markdown(self, filename=None):
        """Save the conversation history to a Markdown file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/conversation_{timestamp}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Conversation History - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Model: {self.default_model}\n\n")
                
                for turn in self.conversation_history:
                    role = turn['role']
                    content = turn['content']
                    timestamp = turn.get('timestamp', 'Unknown time')
                    
                    if isinstance(timestamp, str):
                        try:
                            dt = datetime.fromisoformat(timestamp)
                            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            pass  # Keep original timestamp string if parsing fails
                    
                    f.write(f"## {role.title()} ({timestamp})\n\n")
                    f.write(f"{content}\n\n")
                    f.write("---\n\n")
                
                f.write(f"\n\n*Generated by Ollama Interaction Suite*\n")
            
            console.print(f"[success]Conversation saved to {filename}")
            return True
        except Exception as e:
            console.print(f"[error]Error saving conversation: {str(e)}")
            return False
                
    def code_generation(self, prompt, language="python"):
        """
        Generate code based on user requirements.
        Specialized prompt engineering for code generation tasks.
        """
        system_prompt = f"""You are an expert {language} developer. 
        Your task is to generate clean, efficient, well-documented {language} code 
        based on the user's requirements. Include:
        
        1. Appropriate imports and dependencies
        2. Clear comments explaining logic
        3. Error handling where appropriate
        4. Examples of usage where helpful
        
        Format your response using Markdown code blocks with the appropriate language tag.
        """
        
        console.print(f"[project]Generating {language} code based on your requirements...")
        response = self.generate_response(prompt, system_prompt=system_prompt)
        
        if "error" in response:
            return response
        
        # Save code to separate file
        try:
            content = response['message']['content']
            
            # Extract code blocks from markdown
            import re
            code_blocks = re.findall(r'```(?:' + language + r')?\n(.*?)\n```', content, re.DOTALL)
            
            if code_blocks:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                code_filename = f"{self.output_dir}/generated_code_{timestamp}.{self._get_file_extension(language)}"
                
                with open(code_filename, 'w', encoding='utf-8') as f:
                    f.write(code_blocks[0])  # Write the first code block
                
                console.print(f"[success]Generated code saved to {code_filename}")
            
            return response
        except Exception as e:
            console.print(f"[warning]Could not save generated code: {str(e)}")
            return response
    
    def _get_file_extension(self, language):
        """Get the appropriate file extension for a language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "c": "c",
            "cpp": "cpp",
            "csharp": "cs",
            "go": "go",
            "rust": "rs",
            "ruby": "rb",
            "php": "php",
            "swift": "swift",
            "kotlin": "kt",
            "html": "html",
            "css": "css",
            "sql": "sql",
            "bash": "sh",
            "powershell": "ps1",
            "r": "r",
            "matlab": "m",
        }
        return extensions.get(language.lower(), "txt")
    
    def document_summarization(self, text):
        """
        Summarize a document or long text.
        Uses specialized prompt engineering for summarization tasks.
        """
        system_prompt = """You are an expert at summarizing information clearly and concisely.
        Provide a well-structured summary of the text that:
        
        1. Includes the main points and key information
        2. Omits unnecessary details
        3. Is organized with headings and bullet points where appropriate
        4. Is significantly shorter than the original text
        
        Your summary should be accurate and comprehensive despite its brevity.
        """
        
        prompt = f"Please summarize the following text:\n\n{text}"
        
        console.print(f"[project]Generating document summary...")
        return self.generate_response(prompt, system_prompt=system_prompt)
    
    def format_response(self, response):
        """Format the response for display with rich formatting."""
        if "error" in response:
            console.print(Panel(response["error"], title="Error", border_style="red"))
            return
            
        if "message" in response and "content" in response["message"]:
            # Display the main content
            content = response["message"]["content"]
            console.print(Markdown(content))
            
            # Display metrics in a compact format
            metrics = []
            if "model" in response:
                metrics.append(f"Model: {response['model']}")
            if "total_duration" in response:
                duration_ms = response["total_duration"] / 1_000_000
                metrics.append(f"Time: {duration_ms:.2f}ms")
            if "eval_count" in response:
                metrics.append(f"Tokens: {response['eval_count']}")
                
            if metrics:
                console.print(" | ".join(metrics), style="metrics")


def main():
    """Main application entry point with interactive command loop."""
    console.print(Panel.fit(
        "[bold cyan]Ollama Interaction Suite[/bold cyan]\n"
        "[dim]Professional LLM Interface[/dim]\n"
        "[project]COMP 474 - Project 2 Implementation[/project]",
        border_style="cyan"
    ))
    
    # Initialize the interaction suite
    suite = OllamaInteractionSuite()
    
    # Command loop
    while True:
        console.print("\n[prompt]Enter command or prompt[/prompt] [dim](type 'help' for options)[/dim]:", end=" ")
        user_input = input()
        
        # Handle special commands
        if user_input.lower() in ["exit", "quit", "q"]:
            suite.display_session_stats()
            suite.save_conversation_to_markdown()
            console.print("[success]Session ended successfully.")
            break
            
        elif user_input.lower() in ["help", "h", "?"]:
            help_text = """
            # Available Commands
            
            ## Basic Commands
            - `models` or `list`: List available models
            - `stats`: Show session statistics
            - `stream`: Toggle streaming mode (currently: {})
            - `model <name>`: Change the default model
            - `exit` or `quit`: End the session
            
            ## Conversation Management
            - `clear`: Clear conversation history
            - `save`: Save conversation to markdown file
            
            ## Project 2 Features
            - `code <language>`: Generate code (default: Python)
            - `summarize`: Summarize a document (will prompt for text)
            
            Any other input will be treated as a prompt for the model.
            """.format("ON" if suite.stream_mode else "OFF")
            console.print(Markdown(help_text))
            
        elif user_input.lower() in ["models", "list"]:
            suite.list_available_models()
            
        elif user_input.lower() == "stats":
            suite.display_session_stats()
            
        elif user_input.lower() == "stream":
            suite.stream_mode = not suite.stream_mode
            console.print(f"[success]Streaming mode {'enabled' if suite.stream_mode else 'disabled'}")
            
        elif user_input.lower().startswith("model "):
            new_model = user_input[6:].strip()
            suite.default_model = new_model
            console.print(f"[success]Model changed to: [bold]{new_model}[/bold]")
            
        elif user_input.lower() == "clear":
            suite.clear_conversation_history()
            
        elif user_input.lower() == "save":
            suite.save_conversation_to_markdown()
        
        elif user_input.lower().startswith("code"):
            # Extract language if specified
            parts = user_input.split(maxsplit=1)
            language = "python"  # Default language
            
            if len(parts) > 1 and not parts[1].startswith("generate") and len(parts[1]) < 20:
                language = parts[1].strip()
                console.print(f"[info]Code generation language set to: {language}")
                code_prompt = console.input("[prompt]Enter code generation requirements: [/prompt]")
            else:
                code_prompt = console.input("[prompt]Enter Python code generation requirements: [/prompt]")
            
            response = suite.code_generation(code_prompt, language)
            suite.format_response(response)
            
        elif user_input.lower() == "summarize":
            console.print("[info]Enter or paste the text to summarize (type 'END' on a new line when finished):")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            
            text_to_summarize = "\n".join(lines)
            if len(text_to_summarize) < 50:
                console.print("[warning]Text too short to summarize meaningfully")
                continue
                
            response = suite.document_summarization(text_to_summarize)
            suite.format_response(response)
            
        elif user_input.strip():
            # Process as a normal prompt
            response = suite.generate_response(user_input)
            suite.format_response(response)
            
        else:
            # Empty input
            console.print("[warning]Please enter a command or prompt.")


if __name__ == "__main__":
    try:
        # Check for required packages
        try:
            import rich
        except ImportError:
            print("Installing required packages...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
            print("Required packages installed successfully!")
            # Re-import after installation
            import rich
            from rich.console import Console
            from rich.panel import Panel
            from rich.markdown import Markdown
            from rich.progress import Progress, SpinnerColumn, TextColumn
            from rich.table import Table
            from rich.theme import Theme
        
        main()
    except KeyboardInterrupt:
        console.print("\n[info]Session terminated by user.")
    except Exception as e:
        console.print(f"\n[error]Unexpected error: {str(e)}")
        logging.exception("Unhandled exception in main thread")