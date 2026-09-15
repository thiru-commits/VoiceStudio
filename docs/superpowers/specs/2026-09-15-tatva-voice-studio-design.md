# Tatva Voice Studio Local Installation Design

## Goal

Install VoiceStudio v0.5.2 as an editable, local-only desktop application named **Tatva Voice Studio** on this Apple Silicon Mac.

## Scope

- Keep the application in `/Users/thiruppathyrs/Documents/Website Repositories/Tatva VoiceStudio`.
- Preserve VoiceStudio's existing Tauri, React/Vite, FastAPI, and local SQLite architecture.
- Change only the visible product name and the minimum matching desktop metadata.
- Retain the upstream AGPL-3.0 license, copyright notices, model-license prompts, and upstream attribution.
- Keep the backend bound to loopback and leave remote workers, remote ASR, analytics, and other network-backed features disabled unless the user explicitly enables them later.
- Do not deploy, publish, configure accounts, or alter the existing `tatva-crm` repository.

## Implementation

1. Use the upstream stable `v0.5.2` source as the base and keep its Git history available for future updates.
2. Install the repository's existing Bun dependencies and initialize required submodules; add no new dependencies.
3. Locate the canonical product-name values and reusable brand assets before editing. Replace user-visible `VoiceStudio` naming with `Tatva Voice Studio` through the existing i18n/config paths, without renaming internal APIs, data directories, package identifiers, or compatibility-sensitive symbols.
4. Apply Tatva colours or a Tatva mark only where the existing theme and asset pipeline already provide a direct replacement point. Avoid a UI redesign.
5. Launch the source desktop workflow. Allow first-run Python/model installation only through VoiceStudio's own managed setup flow.

## Data and Privacy

Generated audio, voice samples, projects, logs, settings, and model files remain in VoiceStudio's local data directory. No feature that sends content or telemetry off-device will be enabled as part of this setup. The application will keep existing consent and security controls intact.

## Verification

- Confirm the checkout is on the local customization branch and the upstream release tag is `v0.5.2`.
- Confirm dependency installation completes using the pinned lockfiles.
- Run the smallest existing tests that cover branding/configuration, followed by the frontend build.
- Start the desktop application and verify the window opens, the backend listens only on loopback, and visible branding reads `Tatva Voice Studio`.
- Report model downloads separately because their completion depends on the user's first-run engine choice and can consume substantial disk space.

## Risks and Boundaries

- First launch can download several gigabytes of Python packages and model weights.
- Some optional models have separate commercial or attribution restrictions; branding the application does not change those terms.
- Broadly renaming internal `VoiceStudio` or `OmniVoice` identifiers could break stored data, APIs, updater behavior, or upstream merges, so those identifiers remain unchanged unless they are purely presentational.
- This is a local customization branch, not a redistributed Tatva product build.
