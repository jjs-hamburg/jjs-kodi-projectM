# Source and reproducibility

The complete source needed to reproduce **JJS KODI projectM 21.0.3.3** is
published with the release and is also reconstructible from this repository.

## Exact source revisions

- Kodi Omega build environment:
  `f8815ee40f49a700c047982d752be4b2a61420e2`
- Kodi `visualization.projectm`:
  `d91f39d9ee9f06f998fe83d58154d36331d2c666`
- projectM 3.1.12:
  `b3c3282eb00fae210e9499fa9d11bcfcccffbd96`
- LibreELEC 12.0.2:
  `f3fdd11916f8a47dc5a11c3a4c99cb7c7ffac78b`

The workflows check the relevant exact commit IDs before compiling.

## Local modification

The JJS source transformation is:

`patch/apply_changes.py`

It performs only the documented stability change and the JJS
name/version/provider metadata changes.

## Release source archives

The Android AArch64 release (`v21.0.3.3-jjs`) contains:

`jjs-kodi-projectm-21.0.3.3-source.zip`

That archive contains:

- the patched `visualization.projectm` source tree
- the unmodified projectM 3.1.12 source tree used by the build
- the JJS source transformer
- the GitHub Actions build workflow
- README, notice and license files

The separate LibreELEC 12.0.2 Generic x86_64 release
(`v21.0.3.3-jjs-libreelec-x86_64`) contains:

`jjs-kodi-projectm-21.0.3.3-libreelec-x86_64-source.zip`

That archive contains the patched `visualization.projectm` source tree, the
unmodified projectM 3.1.12 source tree, the JJS source transformer, the exact
LibreELEC workflow, and the modified LibreELEC
`visualization.projectm/package.mk` recipe used for the build.

The Kodi and LibreELEC source trees are not bundled in full because they are
pinned build environments rather than modified components of this add-on. Their
exact revisions are pinned above and in the workflows and can be retrieved from:

https://github.com/xbmc/xbmc

https://github.com/LibreELEC/LibreELEC.tv

## Binary reference

The last pre-naming build tested directly on the NVIDIA Shield was
`21.0.3.2`, SHA256:

`086d63cb229579ba7f65823fadc01586f123fd0ed38024b60d419d3306203185`

Version 21.0.3.3 keeps the same functional audio-isolation patch and pinned
upstream revisions. It changes the visible add-on identity metadata to
**JJS KODI projectM** and publishes the public licensing/source material.
