import sys
import json
import os
import urllib.request

API_KEY = os.environ.get("OPENROUTER_API_KEY")
DEFAULT_MODEL = "cohere/north-mini-code:free"
MODELS = [
    "cohere/north-mini-code:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
]
MODEL = DEFAULT_MODEL
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_config.json")


def _system_context() -> str:
    os_name = "Windows" if os.name == "nt" else "Linux/Mac"
    shell = os.environ.get("AI_SHELL", "unknown")
    return f"System: {os_name}, Shell: {shell}. "


def load_model_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            return cfg.get("model", DEFAULT_MODEL)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_MODEL


def save_model_config(model):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"model": model}, f, indent=2)


def choose_model():
    print("\nDostupni modeli:")
    for i, m in enumerate(MODELS, 1):
        print(f"  [{i}] {m}")
    while True:
        try:
            choice = input(f"\nOdaberi broj (1-{len(MODELS)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(MODELS):
                selected = MODELS[idx]
                print(f"[AI]: Odabran model: {selected}\n")
                save_model_config(selected)
                return selected
        except (ValueError, EOFError, KeyboardInterrupt):
            pass
        print(f"Neispravan unos. Korišten zadan: {DEFAULT_MODEL}")
        return DEFAULT_MODEL


def call_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": _system_context() + "Respond extremely concisely, briefly, and directly to the point. No fluff, no introductory or concluding remarks."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        req = urllib.request.Request(url, headers=headers, data=json.dumps(data).encode("utf-8"))
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error communicating with API: {str(e)}"


def print_help():
    print("Usage: ai [OPTIONS] \"prompt\"")
    print()
    print("Options:")
    print("  -m, --model    Interaktivni odabir modela")
    print("  -h, --help     Prikaži ovu pomoć")
    print()
    print("Examples:")
    print("  ai \"what is python?\"")
    print("  dir | ai \"explain this output\"")
    print()
    print("Paste mode (ai bez argumenata):")
    print("  ai    paste-aj tekst, Ctrl+Z za kraj")


def main():
    global MODEL
    if not API_KEY:
        print("Error: OPENROUTER_API_KEY is not set in the environment!")
        sys.exit(1)

    MODEL = load_model_config()

    # Filter out flags from argv
    argv = [a for a in sys.argv if a not in ("-h", "--help", "-m", "--model")]

    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        sys.exit(0)

    if "-m" in sys.argv or "--model" in sys.argv:
        if sys.stdin.isatty():
            MODEL = choose_model()
        else:
            print("[AI]: -m ignored in pipe mode, using default.", file=sys.stderr)

    if len(argv) == 1 and sys.stdin.isatty():
        print("\n[AI]: Paste your content below. Press Ctrl+Z (Enter) when done.\n")
        try:
            paste_content = sys.stdin.read().strip()
        except KeyboardInterrupt:
            print()
            sys.exit(0)
        if paste_content:
            print(f"\n[AI]: Thinking...\n")
            reply = call_openrouter(paste_content)
            print(reply)
        sys.exit(0)

    if len(argv) > 1 or not sys.stdin.isatty():
        user_args = " ".join(argv[1:])
        pipe_content = ""

        if not sys.stdin.isatty():
            pipe_content = sys.stdin.read().strip()

        if user_args and pipe_content:
            full_prompt = f"{user_args}\n\n[TERMINAL CONTEXT]:\n{pipe_content}"
        elif pipe_content:
            full_prompt = f"Analyze this terminal output:\n{pipe_content}"
        else:
            full_prompt = user_args

        if full_prompt.strip():
            print(f"\n[AI]: Thinking...\n")
            reply = call_openrouter(full_prompt)
            print(reply)
            sys.exit(0)


if __name__ == "__main__":
    main()
