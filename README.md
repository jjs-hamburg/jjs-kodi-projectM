# JJS KODI projectM

**JJS KODI projectM** is an unofficial stability build of Kodi's
`visualization.projectm` add-on for **Kodi 21/Omega on Android AArch64 and
LibreELEC Generic x86_64**.

It was created to solve a very specific playback problem: on the tested NVIDIA
Shield setup, some projectM preset changes could briefly stall Kodi's audio
callback and cause audible dropouts. This variant changes the add-on wrapper so
projectM can never make the audio callback wait for rendering or preset setup.

The add-on ID deliberately remains:

`visualization.projectm`

Kodi therefore continues to treat it as the same visualization add-on. The
visible name is **JJS KODI projectM** so this modified build is clearly
distinguishable from the unmodified upstream version.

> This is an unofficial community build. It is not an official release of Team
> Kodi, the Kodi Foundation, projectM, or their maintainers.

## Current release

**JJS KODI projectM 21.0.3.3**

Target environments:

- Kodi 21/Omega
- Android AArch64
- Android API 21
- Android NDK r21e / 21.4.7075529
- LibreELEC 12.0.2 Generic x86_64
- projectM 3.1.12

The last pre-naming binary tested directly on the NVIDIA Shield was version
**21.0.3.2**. Its SHA256 is:

`086d63cb229579ba7f65823fadc01586f123fd0ed38024b60d419d3306203185`

Version **21.0.3.3** keeps the same functional stability patch and the same
pinned upstream revisions. It changes the visible add-on name/provider metadata
to JJS KODI projectM and adds the public source/license material.

## What was changed

Upstream `visualization.projectm` protects access to projectM with
`m_pmMutex`.

In the original Kodi add-on wrapper, `CVisualizationProjectM::AudioData()`
takes that mutex with a normal blocking lock. If projectM is busy rendering or
performing preset setup at exactly that moment, Kodi's audio callback waits for
the mutex.

For a visualization that is the wrong priority: audio playback must never wait
for the visualizer.

The JJS variant changes only that lock acquisition from blocking to
non-blocking:

- upstream: wait until `m_pmMutex` becomes available
- JJS variant: attempt the lock with `std::try_to_lock`
- if the mutex is currently busy, return immediately
- only that visualizer PCM block is skipped
- Kodi's audio callback is never stalled by projectM

The projectM 3.1.12 source itself is deliberately **not modified**.

The complete transformation is implemented in:

`patch/apply_changes.py`

The transformer is fail-closed. It requires exactly the expected upstream source
text. If the pinned source no longer matches, the build stops instead of trying
to apply a guessed patch.

## Why this fixes the dropout

The visualizer and the audio path do not have the same importance.

Missing one short PCM block in a visualization may cause an imperceptible visual
difference. Blocking Kodi's audio callback can produce an audible interruption.

The JJS change makes that priority explicit: if projectM is busy, the
visualization yields to audio instead of making audio wait.

On the tested Shield/Kodi Omega installation, this eliminated the dropouts that
had occurred with particular presets during preset changes.

## What is not changed

The build does **not** modify projectM 3.1.12 itself. It does not change preset
rendering, preset content, projectM timing, Kodi's audio engine, or normal audio
decoding.

The functional source change is limited to the mutex behavior in the Kodi
`visualization.projectm` wrapper. Version 21.0.3.3 additionally changes only
the add-on name, provider attribution, version metadata, and source URL.

## Exact upstream revisions

The build is intentionally pinned to the exact revisions used by the known-good
21.0.3.2 reference build:

| Component | Exact revision |
| --- | --- |
| Kodi Omega build environment | `f8815ee40f49a700c047982d752be4b2a61420e2` |
| xbmc/visualization.projectm | `d91f39d9ee9f06f998fe83d58154d36331d2c666` |
| projectM 3.1.12 | `b3c3282eb00fae210e9499fa9d11bcfcccffbd96` |
| LibreELEC 12.0.2 | `f3fdd11916f8a47dc5a11c3a4c99cb7c7ffac78b` |

The workflows verify the relevant pinned revisions before patching or compiling.
Moving upstream branches therefore cannot silently change the build input.

## Reproducible build

The GitHub Actions workflow performs the complete Android AArch64 build:

1. checks out the exact pinned Kodi, visualization.projectm and projectM revisions
2. verifies `patch/apply_changes.py`
3. applies the JJS source transformation
4. builds the Kodi Android dependency environment
5. builds only `visualization.projectm`
6. packages a directly installable Kodi ZIP
7. verifies version, visible name, provider, platform, AArch64 ELF format and GLES dependency
8. creates a corresponding-source ZIP
9. publishes both files directly under GitHub Releases

The build caches are keyed to the pinned Kodi revision, Android API level and
NDK version. They shorten the build but do not define the source version.

The LibreELEC workflow performs the corresponding Generic x86_64 build from the
same transformed `visualization.projectm` source. It pins LibreELEC 12.0.2,
preflights and SHA-verifies the LibreELEC source dependency plan, builds the
add-on with LibreELEC's own `scripts/create_addon`, normalizes the installable
ZIP, preserves that ZIP as a GitHub Actions artifact before validation, verifies
the add-on metadata and x86-64 ELF binary, and creates a corresponding-source
archive containing the exact build recipe used.

## Installation

Open the current GitHub Release and download the ZIP for your platform:

Android AArch64:

`visualization.projectm-21.0.3.3-omega-android-aarch64.zip`

LibreELEC Generic x86_64:

`visualization.projectm-21.0.3.3-omega-libreelec-x86_64.zip`

In Kodi use:

**Add-ons → Install from zip file**

and select that ZIP directly.

Do not unpack it first.

## Release files

A public release contains:

`visualization.projectm-21.0.3.3-omega-android-aarch64.zip`

The directly installable Android AArch64 Kodi add-on.

`visualization.projectm-21.0.3.3-omega-libreelec-x86_64.zip`

The directly installable LibreELEC Generic x86_64 Kodi add-on.

`jjs-kodi-projectm-21.0.3.3-source.zip`

The corresponding source package containing the patched
`visualization.projectm` tree, the unmodified projectM 3.1.12 source used by
the build, the source transformer, build workflow, README, notices and license
texts.

`jjs-kodi-projectm-21.0.3.3-libreelec-x86_64-source.zip`

The corresponding source package for the LibreELEC build, including the exact
LibreELEC package recipe used for that build.

`SHA256SUMS.txt`

Checksums for the Android release files.

`SHA256SUMS-libreelec-x86_64.txt`

Checksums for the LibreELEC release files.

## Disclaimer

This project was originally created for my own personal use. I am making the
source code and builds available for anyone who may find them useful, but this
is not an official Kodi or projectM project and comes without any warranty,
support commitment, or obligation to provide future updates or maintenance.

To the maximum extent permitted by applicable law, the maintainer of this
unofficial build shall not be liable for loss of data, loss of functionality,
incompatibility, interruption, or other damages arising from the use of, or
inability to use, this software.

## Source and licensing

The modified Kodi add-on is distributed under **GPL-2.0-or-later**, matching the
upstream `visualization.projectm` licensing.

projectM 3.1.12 is distributed under **LGPL-2.1-or-later**.

The repository includes:

- `LICENSE.md` — GPLv2 license text from Kodi visualization.projectm
- `LICENSE-projectM-LGPL-2.1.txt` — LGPL 2.1 license text from projectM 3.1.12
- `NOTICE.md` — upstream attribution and description of the JJS modification
- `SOURCE.md` — exact source revisions and source/reproducibility information

The installable Kodi ZIP contains these notices and license texts as well.

## Upstream

Kodi visualization.projectm:

https://github.com/xbmc/visualization.projectm

projectM:

https://github.com/projectM-visualizer/projectm

Kodi:

https://github.com/xbmc/xbmc

## Repository history

The former `jjs-async-transition` branch contains historical development work.
The canonical release source is `main`.

Earlier development builds stored the source transformer in split
`patch/part00` … `patch/part04` files as a transport workaround. The public
canonical repository stores it normally as:

`patch/apply_changes.py`

That file is the complete JJS transformation used by the release build.
