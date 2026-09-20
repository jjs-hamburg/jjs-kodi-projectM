# JJS KODI projectM

Reproducible build repository for **JJS KODI projectM**, the JJS stability variant of Kodi's `visualization.projectm` for Kodi 21/Omega on Android AArch64.

The canonical branch is `main`.

## Current known-good version

- Visible add-on name: **JJS KODI projectM**
- Add-on ID: `visualization.projectm` (intentionally unchanged)
- Add-on version: `21.0.3.3`
- Provider: `Team Kodi; JJS`
- Target: Kodi 21/Omega
- Platform: Android AArch64
- Android API: 21
- Android NDK: r21e / `21.4.7075529`
- projectM: 3.1.12

The binary reference known to be good and tested on the NVIDIA Shield remains the 21.0.3.2 build produced by workflow run 34722353681:

`visualization.projectm-21.0.3.2-omega-android-aarch64.zip`

Known-good SHA256:

`086d63cb229579ba7f65823fadc01586f123fd0ed38024b60d419d3306203185`

## What is changed

The projectM 3.1.12 source itself is intentionally left unmodified.

The Kodi add-on wrapper changes only the audio callback in `visualization.projectm/src/Main.cpp`:

- upstream behavior: `AudioData()` blocks while waiting for `m_pmMutex`
- JJS behavior: `AudioData()` uses `std::try_to_lock`
- if projectM is busy rendering or switching presets, only that visualizer PCM block is skipped
- Kodi's audio callback is therefore not held up by projectM preset work

This is the stability change that eliminated the audible dropouts triggered by problematic preset changes in the tested Shield/Kodi setup.

The transformation is kept as a readable, fail-closed source transformer:

`patch/apply_changes.py`

It requires exact source matches and aborts instead of guessing if the upstream source no longer matches the expected Kodi Omega code.

## Pinned upstream revisions

The successful 21.0.3.2 reference build used these exact revisions, and the workflow pins them explicitly:

| Component | Revision |
| --- | --- |
| Kodi Omega | `f8815ee40f49a700c047982d752be4b2a61420e2` |
| xbmc/visualization.projectm Omega | `d91f39d9ee9f06f998fe83d58154d36331d2c666` |
| projectM 3.1.12 | `b3c3282eb00fae210e9499fa9d11bcfcccffbd96` |

This prevents future movement of an `Omega` branch from silently changing the build input.

## Build

GitHub Actions performs the complete Android AArch64 build:

1. checks out the exact pinned Kodi, add-on and projectM revisions
2. validates and applies `patch/apply_changes.py`
3. builds the Kodi Android dependency environment
4. builds only `visualization.projectm`
5. packages a directly installable Kodi ZIP
6. verifies add-on version, platform, AArch64 ELF format and GLES dependency

Caches are used only to shorten the build; they are keyed to the pinned Kodi revision, API level and NDK version.

## Release

A successful build on `main` publishes the installable ZIP directly under GitHub Releases.

There is deliberately no GitHub Actions artifact for normal distribution, because GitHub wraps Actions artifacts in another ZIP. The Release asset itself is the ZIP Kodi can install directly.

Current release tag:

`v21.0.3.3-jjs`

21.0.3.3 is a naming/metadata release on the same pinned source and stability patch as the tested 21.0.3.2 reference. The add-on ID remains `visualization.projectm`, so Kodi continues to treat it as the same visualization add-on.

## Repository history

The former `jjs-async-transition` branch is historical development material. It is retained until the cleaned `main` build has been verified, but it is no longer intended to be the canonical source.

The previously split `patch/part00` … `patch/part04` representation was only a transport workaround. The canonical repository stores the transformer normally as `patch/apply_changes.py`.
