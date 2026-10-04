# Protocol v1 freeze

Frozen 2026-10-04 at git tag `protocol-v1`. **No test-set case had been sent to any model before this freeze.** Development used only `dev-*.jsonl` and `examples/`.

| Artifact | sha256 |
|---|---|
| `data/test-v1.jsonl` (240 cases, primary) | `24967d892bc2f5f0370d97b79dcbfe8ffe8e115965c5b1ef22e6185ca81bb0a6` |
| `data/test-crowded-v1.jsonl` (240 cases) | `d4b7b56e4d0efa0fd9e17dbb81bed3926c44fe85c9267aae8e90625df9e57879` |
| `data/dev-v1.jsonl` (48 cases, development only) | `88d4646f321eab85458ca3b7852eb410dc8e3b17394135cd48f59b84425bf8e3` |
| `data/dev-crowded-v1.jsonl` (48 cases, development only) | `a7dcf7a11c37bf5637fa9e282a51b6938a412e0e1eba3ffaec3686b42f43ef2a` |
| `src/local_trust/prompt.py` (template hash `403f3b108a0e4437`) | `13ba9fa16589e15eafa69f0811bcb38ce9e54480d4ae882b415f8fa4cb61f96c` |
| `src/local_trust/scoring.py` (`SCORER_VERSION = "v1"`) | `b708dca6e74de4fb1c99324628f3fe3b3bed14ff20c7a4652ad42b26ada63049` |
| `src/local_trust/generate.py` (`GENERATOR_VERSION = "v1"`, seeds 20261004 test / 7 dev, crowded +12) | `0c10b92e4d9471fbb51dcc8d5de2bc89fc227927eb308b11b9fe03bf8862fb2f` |
| `configs/models.json` (local roster, pinned revisions) | `627c29d30567594b3644319ac4d83f449a683c23d34ead8f3bf56875c3fbdace` |

The Kaggle task files in `kaggle/local-trust-test-*.py` are generated from these exact files by `python -m local_trust export-kaggle`.

**Rules after freeze.** The test data, prompt and scorer aren't edited in place. A fix means `v2` files, a disclosed amendment, and rerunning every affected model. Analysis code (`analysis.py`) may change, since it only reads saved outputs. The hosted model list is chosen on run day from Kaggle's registry and recorded with the results. Adding a local model is allowed but must be disclosed. Removing a model after seeing its results is not.
