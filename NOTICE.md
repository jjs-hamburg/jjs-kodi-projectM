# Notice and upstream attribution

## JJS KODI projectM

**JJS KODI projectM** is an unofficial community stability build of Kodi's
`visualization.projectm` add-on for Kodi 21/Omega.

It is not an official release of Team Kodi, the Kodi Foundation, the projectM
project, or their maintainers.

The add-on ID intentionally remains:

`visualization.projectm`

This preserves Kodi compatibility and update behavior. The visible add-on name
is changed to **JJS KODI projectM** so users can distinguish this build from the
unmodified upstream add-on.

## Upstream projects

### Kodi visualization.projectm

Upstream repository:

https://github.com/xbmc/visualization.projectm

Pinned revision used for the current build:

`d91f39d9ee9f06f998fe83d58154d36331d2c666`

License: **GPL-2.0-or-later**.

The repository-level `LICENSE.md` is copied from the upstream add-on license
text.

### projectM

Upstream repository:

https://github.com/projectM-visualizer/projectm

Pinned projectM 3.1.12 revision used for the current build:

`b3c3282eb00fae210e9499fa9d11bcfcccffbd96`

License: **LGPL-2.1-or-later**.

The repository-level `LICENSE-projectM-LGPL-2.1.txt` is copied from the
projectM 3.1.12 source tree.

## JJS modification

The projectM 3.1.12 source itself is deliberately left unmodified.

The functional JJS change is in the Kodi add-on wrapper's
`CVisualizationProjectM::AudioData()` implementation. Upstream takes
`m_pmMutex` with a blocking lock. The JJS build changes that acquisition to
`std::try_to_lock`.

If projectM is busy rendering or changing a preset, the Kodi audio callback no
longer waits for projectM. Only that visualizer PCM block is skipped.

This change was introduced to eliminate audible playback interruptions observed
when particular projectM presets were changed on Kodi 21/Omega running on an
NVIDIA Shield.

The exact transformation is public in:

`patch/apply_changes.py`

It is fail-closed: if the expected upstream source no longer matches exactly,
the build stops instead of guessing how to patch a different source version.

## Names and affiliation

Kodi and projectM are names of their respective upstream projects. Their use
here identifies compatibility and the upstream software from which this build
is derived. No endorsement or affiliation is implied.
