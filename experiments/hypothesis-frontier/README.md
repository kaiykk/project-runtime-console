# Hypothesis Frontier

This directory contains development-time probes for the Step 1 input-path
question. It is not a product surface and must not be imported by the console
runtime.

Each hypothesis lives in its own branch and worktree:

```text
codex/prc-step1-h1-transcript-first
codex/prc-step1-h2-hook-first
codex/prc-step1-h3-dual-channel
```

The comparison agent receives the three branch results only after all three
spikes are complete. It must not receive a preferred winner in advance.
