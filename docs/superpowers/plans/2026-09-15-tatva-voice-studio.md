# Tatva Voice Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install VoiceStudio v0.5.2 locally on this Apple Silicon Mac and present it as Tatva Voice Studio without changing compatibility-sensitive internals.

**Architecture:** Keep the upstream Tauri + React/Vite + FastAPI stack and pinned dependencies intact. Apply branding only through existing desktop metadata, existing identity views, the current i18n title key, and the default CSS theme tokens; preserve internal OmniVoice/VoiceStudio identifiers, storage paths, engine labels, APIs, and updater endpoints.

**Tech Stack:** Bun 1.4, React 19, Vite, Tauri 2/Rust, FastAPI/Python managed by uv, Vitest, pytest

**Spec:** `docs/superpowers/specs/2026-09-15-tatva-voice-studio-design.md`

## Global Constraints

- The source base is the upstream stable tag `v0.5.2` on branch `codex/tatva-voice-studio`.
- Add no dependencies and do not change lockfiles.
- Keep `com.debpalash.omnivoice-studio`, `OMNIVOICE_*`, `omnivoice_data/`, backend/API identity strings, engine names, upstream repository URLs, and updater artifact names unchanged.
- Retain AGPL-3.0, copyright notices, upstream attribution, consent controls, and model-license prompts.
- Do not enable analytics, remote workers, remote ASR, network sharing, deployment, publishing, or accounts.
- Use Tatva Navy Dark `#1a1a2e`, Sky `#1fb8ff`, Tatva Blue `#0077c2`, Orange `#f7941d`, and light text `#f8fafc` in the existing default theme only.
- Model installation remains an explicit first-run user choice because downloads are large and some models have separate terms.

---

### Task 1: Install the pinned development runtime

**Files:**
- Verify only: `.gitmodules`
- Verify only: `bun.lock`
- Verify only: `uv.lock`
- Verify only: `.python-version`

**Interfaces:**
- Consumes: upstream `v0.5.2` checkout and the installed `bun`, `uv`, Rust, and Apple developer command-line tools.
- Produces: initialized submodules plus lockfile-exact JavaScript and Python environments used by Tasks 2 and 3.

- [ ] **Step 1: Confirm the isolated checkout and toolchain**

Run:

```bash
git status --short --branch
git describe --tags --exact-match 38c2405fa17841e9b53cb43a8af7641969bea90b || git show -s --format='%H %D'
bun --version
uv --version
rustc --version
```

Expected: branch `codex/tatva-voice-studio`; base commit is tagged `v0.5.2`; each tool prints a version.

- [ ] **Step 2: Initialize the pinned submodule**

Run:

```bash
git submodule update --init --recursive
git submodule status
```

Expected: `omnivoice-gallery` is checked out at `22e8e6da806fb1904a75db99adb1759832b6ebd0` with no leading `-`.

- [ ] **Step 3: Install JavaScript dependencies without changing the lockfile**

Run:

```bash
bun install --frozen-lockfile
git diff --exit-code -- bun.lock frontend/package.json package.json
```

Expected: install succeeds and the second command exits 0.

- [ ] **Step 4: Install the pinned Python environment**

Run:

```bash
uv sync --frozen
uv run python --version
git diff --exit-code -- uv.lock pyproject.toml
```

Expected: uv selects a Python version allowed by `pyproject.toml`, installs from `uv.lock`, and leaves both dependency files unchanged.

---

### Task 2: Apply the minimal Tatva identity and default palette

**Files:**
- Create: `tests/test_tatva_branding.py`
- Modify: `frontend/index.html`
- Modify: `frontend/src-tauri/tauri.conf.json`
- Modify: `frontend/src/pages/SetupWizard.jsx`
- Modify: `frontend/src/components/settings/AboutTab.jsx`
- Modify: `frontend/src/components/settings/AppearancePanel.jsx`
- Modify: `frontend/src/components/settings/AppearancePanel.test.jsx`
- Modify: `frontend/src/index.css`
- Modify: `frontend/src/i18n/locales/*.json`
- Modify: `tests/test_identity_paths_survive_the_rename.py`

**Interfaces:**
- Consumes: existing Tauri product/window metadata, `bootstrap.title` in all 21 locale JSON files, existing identity JSX, and the default `@theme` token block.
- Produces: visible product name `Tatva Voice Studio`, default theme label `Tatva`, and Tatva colour tokens while compatibility-sensitive identifiers remain unchanged.

- [ ] **Step 1: Write the failing branding contract**

Create `tests/test_tatva_branding.py`:

```python
import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
PRODUCT_NAME = "Tatva Voice Studio"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_visible_product_identity_is_tatva():
    tauri = json.loads(read("frontend/src-tauri/tauri.conf.json"))
    assert tauri["productName"] == PRODUCT_NAME
    assert tauri["app"]["windows"][0]["title"] == PRODUCT_NAME
    assert f"<title>{PRODUCT_NAME}</title>" in read("frontend/index.html")
    assert PRODUCT_NAME in read("frontend/src/pages/SetupWizard.jsx")
    assert PRODUCT_NAME in read("frontend/src/components/settings/AboutTab.jsx")


def test_bootstrap_title_is_tatva_in_every_locale():
    locales = sorted((ROOT / "frontend/src/i18n/locales").glob("*.json"))
    assert len(locales) == 21
    for locale in locales:
        assert json.loads(locale.read_text(encoding="utf-8"))["bootstrap"]["title"] == PRODUCT_NAME


def test_default_theme_uses_tatva_tokens():
    css = read("frontend/src/index.css")
    for token in ("#1a1a2e", "#1fb8ff", "#0077c2", "#f7941d", "#f8fafc"):
        assert token in css
    appearance = read("frontend/src/components/settings/AppearancePanel.jsx")
    assert "{ id: 'gruvbox', label: 'Tatva', dot: '#1fb8ff' }" in appearance


def test_compatibility_identity_stays_upstream():
    tauri = json.loads(read("frontend/src-tauri/tauri.conf.json"))
    assert tauri["identifier"] == "com.debpalash.omnivoice-studio"
    assert "debpalash/VoiceStudio/releases/latest" in read(
        "frontend/src-tauri/tauri.conf.json"
    )
    assert "OMNIVOICE_DATA_DIR" in read("backend/core/config.py")
```

- [ ] **Step 2: Run the branding contract and verify it fails**

Run:

```bash
uv run pytest tests/test_tatva_branding.py -q
```

Expected: FAIL because the product metadata, visible names, locale titles, and theme tokens still use upstream VoiceStudio/Gruvbox values.

- [ ] **Step 3: Change only the visible identity surfaces**

Apply these exact substitutions:

```text
frontend/index.html:
  <title>VoiceStudio</title> -> <title>Tatva Voice Studio</title>

frontend/src-tauri/tauri.conf.json:
  "productName": "VoiceStudio" -> "productName": "Tatva Voice Studio"
  main window "title": "VoiceStudio" -> "title": "Tatva Voice Studio"

frontend/src/pages/SetupWizard.jsx:
  masthead text VoiceStudio -> Tatva Voice Studio

frontend/src/components/settings/AboutTab.jsx:
  About identity text VoiceStudio -> Tatva Voice Studio

frontend/src/i18n/locales/*.json:
  bootstrap.title value VoiceStudio -> Tatva Voice Studio in every locale
```

Do not replace other VoiceStudio occurrences: engine names, API descriptions, support/legal copy, paths, logs, diagnostics, and upstream links describe the upstream software or compatibility contract.

- [ ] **Step 4: Apply Tatva colours to the existing default theme**

In the first `@theme` block of `frontend/src/index.css`, set:

```css
--color-fg:            #f8fafc;
--color-brand:         #1fb8ff;
--color-brand-hover:   #0077c2;
--color-brand-glow:    rgba(31, 184, 255, 0.4);
--color-accent:        #f7941d;
--color-chrome-bg:     #1a1a2e;
--color-chrome-fg:     #f8fafc;
```

Also change the default focus-ring colour to `rgba(31, 184, 255, 0.45)`. Do not alter named optional theme blocks.

In `frontend/src/components/settings/AppearancePanel.jsx`, keep the compatibility ID `gruvbox` but change its visible entry to:

```js
{ id: 'gruvbox', label: 'Tatva', dot: '#1fb8ff' },
```

Update `AppearancePanel.test.jsx` to query the default theme by accessible name `Tatva` instead of `Gruvbox`.

- [ ] **Step 5: Update the existing desktop identity assertion**

In `tests/test_identity_paths_survive_the_rename.py`, update only `test_the_product_name_is_the_new_one` to expect `Tatva Voice Studio` for `productName` and the main window title. Keep every storage, API, Cargo, process, and release-artifact assertion unchanged.

- [ ] **Step 6: Run the focused tests**

Run:

```bash
uv run pytest tests/test_tatva_branding.py tests/test_identity_paths_survive_the_rename.py -q
bun run --cwd frontend test src/components/settings/AppearancePanel.test.jsx src/test/tokenParity.test.js src/test/themeCascade.test.js
```

Expected: all selected tests pass; optional themes still override the Tatva default correctly.

- [ ] **Step 7: Commit the branding change**

Run:

```bash
git add -- tests/test_tatva_branding.py tests/test_identity_paths_survive_the_rename.py frontend/index.html frontend/src-tauri/tauri.conf.json frontend/src/pages/SetupWizard.jsx frontend/src/components/settings/AboutTab.jsx frontend/src/components/settings/AppearancePanel.jsx frontend/src/components/settings/AppearancePanel.test.jsx frontend/src/index.css frontend/src/i18n/locales/*.json
git commit -m "feat: brand local app as Tatva Voice Studio"
```

---

### Task 3: Build and verify the local desktop application

**Files:**
- Verify only: all Task 2 files
- Generated and ignored: `node_modules/`, `.venv/`, `frontend/dist/`, `frontend/src-tauri/target/`

**Interfaces:**
- Consumes: installed pinned environments and the branded source from Task 2.
- Produces: a locally runnable Tatva Voice Studio desktop development build with a loopback-only backend.

- [ ] **Step 1: Verify the repository remains clean except for intentional commits**

Run:

```bash
git status --short --branch
git diff --check HEAD~1 HEAD
git diff --exit-code -- bun.lock uv.lock frontend/package.json package.json pyproject.toml
```

Expected: no uncommitted source changes, no whitespace errors, and no dependency drift.

- [ ] **Step 2: Run the existing frontend build**

Run:

```bash
bun run --cwd frontend build
```

Expected: Vite completes and writes `frontend/dist/` without errors.

- [ ] **Step 3: Start the desktop development workflow without choosing a model**

Run:

```bash
bun run desktop
```

Expected: the backend becomes healthy on `127.0.0.1:3900`, the Tauri window opens, and the first-run interface appears. Stop before accepting a model license or starting a large model download.

- [ ] **Step 4: Verify loopback and visible branding**

Run in a second terminal while the application is open:

```bash
curl --fail --silent http://127.0.0.1:3900/system/info
lsof -nP -iTCP:3900 -sTCP:LISTEN
```

Expected: the health endpoint returns JSON and the listener is bound to loopback, not `*` or a LAN address. Visually confirm the setup masthead/window identity reads `Tatva Voice Studio`, the default accent is Tatva Sky/Blue with Orange emphasis, and Settings → About shows `Tatva Voice Studio`.

- [ ] **Step 5: Stop the development processes and record final evidence**

Quit the Tauri application normally, then run:

```bash
lsof -nP -iTCP:3900 -sTCP:LISTEN
git status --short --branch
git log -3 --oneline --decorate
```

Expected: no listener remains on port 3900; source is clean; the design and branding commits are present. Report model installation as pending user choice if no model was downloaded.
