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

The workflow checks these exact commit IDs before compiling.

## Local modification

The JJS source transformation is:

`patch/apply_changes.py`

It performs only the documented stability change and the JJS
name/version/provider metadata changes.

## Release source archive

Every public 21.0.3.3 release contains:

`jjs-kodi-projectm-21.0.3.3-source.zip`

That archive contains:

- the patched `visualization.projectm` source tree
- the unmodified projectM 3.1.12 source tree used by the build
- the JJS source transformer
- the GitHub Actions build workflow
- README, notice and license files

The Kodi source tree is not bundled into that archive because it is the build
environment rather than a modified component of this add-on. The exact Kodi
revision is pinned above and in the workflow and can be retrieved from:

https://github.com/xbmc/xbmc

## Binary reference

The last pre-naming build tested directly on the NVIDIA Shield was
`21.0.3.2`, SHA256:

`086d63cb229579ba7f65823fadc01586f123fd0ed38024b60d419d3306203185`

Version 21.0.3.3 keeps the same functional audio-isolation patch and pinned
upstream revisions. It changes the visible add-on identity metadata to
**JJS KODI projectM** and publishes the public licensing/source material.
