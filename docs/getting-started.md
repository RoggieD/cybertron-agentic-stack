# Getting Started

## 1. Install CyberTron Agentic Stack

### macOS / Linux

```bash
git clone https://github.com/RoggieD/cybertron-agentic-stack.git
cd cybertron-agentic-stack
./install.sh claude-code /path/to/your-project
```

Keep the CyberTron repository clone available for future management commands.
The source checkout uses `./install.sh` directly and does not require a
globally installed `agentic-stack` command.

### Windows (PowerShell)

```powershell
git clone https://github.com/RoggieD/cybertron-agentic-stack.git
cd cybertron-agentic-stack
.\install.ps1 claude-code C:\path\to\your-project
```

## 2. Pick your harness

The install command above already selects the initial harness.

To add another adapter later, run this from the CyberTron repository:

```bash
./install.sh add <adapter> /path/to/your-project
```

Supported adapters include:

`claude-code`, `cursor`, `windsurf`, `opencode`, `openclaw`, `copilot-cli`,
`gemini`, `hermes`, `pi`, `codex`, `autohand-code`, `standalone-python`,
and `antigravity`.

The onboarding wizard runs automatically, populating
`.agent/memory/personal/PREFERENCES.md` and `.agent/memory/.features.json`.

Each adapter has its own `README.md` under `adapters/<name>/`.

## 3. Customize `PREFERENCES.md`

Open `.agent/memory/personal/PREFERENCES.md` and fill in 5–10 lines about
your code style, workflow, and constraints. This is the one file every
user should customize on day one. The onboarding wizard pre-populates it,
but you can always edit it later.

## 4. Run the dream cycle on a schedule

```bash
crontab -e
# nightly at 3am:
0 3 * * * cd /path/to/project && python3 .agent/memory/auto_dream.py >> .agent/memory/dream.log 2>&1
```

## 5. Start using it

Open your harness and ask it anything. The first few days it will feel
stateless. After ~2 weeks you'll notice it checking past lessons, logging
failures with reflection, and (if you let it) proposing skill rewrites.

## Managing your project

After the initial setup, run verb-style management commands from the
CyberTron repository:

```bash
./install.sh dashboard /path/to/your-project           # TUI dashboard: health, verify, memory, team, skills
./install.sh mission-control /path/to/your-project     # beta local web dashboard; Ctrl-C turns it off
./install.sh brain status        # optional external Brain CLI integration
./install.sh status /path/to/your-project              # one-screen view: which adapters, brain stats
./install.sh doctor /path/to/your-project              # read-only audit; green / yellow / red per adapter
./install.sh upgrade /path/to/your-project --dry-run   # preview safe .agent infrastructure refresh
./install.sh upgrade /path/to/your-project --yes       # apply latest harness/memory/tools + new skills
./install.sh sync-manifest /path/to/your-project       # rebuild .agent/skills/_manifest.jsonl from SKILL.md
```

### Bounded agentic loops

Initialize and inspect the portable loop contracts before running an action loop:

```bash
./install.sh loop init /path/to/your-project
./install.sh loop validate /path/to/your-project
./install.sh loop run ci-sweeper "make the failing test green" /path/to/your-project --yes
./install.sh loop status /path/to/your-project
```

The lifecycle is maker → deterministic verifier → independent checker. L1
loops report in the current workspace; bundled L2/L3 action loops use owned
worktrees, approvals, finite budgets, deny-path gates, and resumable local
checkpoints. Events contain only allowlisted metadata and hashed identifiers.
The loop supervisor is **not an operating-system sandbox**; pair it with a
harness-native sandbox when hostile or high-impact child code is in scope.
Schedulers should run one bounded command, inspect its exit code, and only then
schedule the next run.

Source checkout users can run the same verbs through the clone:

```bash
./install.sh dashboard /path/to/your-project
./install.sh mission-control /path/to/your-project
./install.sh brain status
./install.sh status /path/to/your-project
./install.sh doctor /path/to/your-project
./install.sh upgrade /path/to/your-project --dry-run
./install.sh upgrade /path/to/your-project --yes
./install.sh sync-manifest /path/to/your-project
```

PowerShell users can run the same verbs through `.\install.ps1`.

Adding or removing adapters:

```bash
./install.sh add cursor /path/to/your-project
./install.sh remove cursor /path/to/your-project
./install.sh manage /path/to/your-project
```

PowerShell users can use the equivalent `.\install.ps1` commands.

## Optional: add a visual system with `DESIGN.md`

If your project has UI, drop a Google Stitch-style `DESIGN.md` file in the
project root. The bundled `design-md` skill tells compatible agents to use
that file as the source of truth for colors, typography, spacing, component
rules, and design rationale instead of inventing visual choices.

When Node tooling is available, agents can validate the file with:

```bash
npx @google/design.md lint DESIGN.md
```

## Keeping up to date

Update the CyberTron repository clone first:

```bash
cd /path/to/cybertron-agentic-stack
git pull --ff-only
./install.sh upgrade /path/to/your-project --dry-run
./install.sh upgrade /path/to/your-project --yes
```

The upgrade command refreshes skeleton-owned
(harness scripts, top-level memory/tools Python files, skill index, and new
skill directories) but never overwrites `CLAUDE.md`, `.claude/settings.json`,
personal/semantic/episodic/working memory, candidates, or existing skill
directories.

## Verify the wiring

```bash
python3 .agent/tools/budget_tracker.py "commit and push"
# tokens_used, chars, budget, headroom
```

If `tokens_used` is 0, your memory files aren't being read — check paths.
