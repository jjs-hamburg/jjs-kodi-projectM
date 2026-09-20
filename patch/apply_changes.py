#!/usr/bin/env python3
from pathlib import Path
import argparse
import sys


def replace_exact(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one source match in {path}, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"OK  {label}: {path}")


def patch_addon(addon: Path) -> None:
    main = addon / "src" / "Main.cpp"
    old = """void CVisualizationProjectM::AudioData(const float* pAudioData, size_t iAudioDataLength)
{
  std::unique_lock<std::mutex> lock(m_pmMutex);
  if (m_projectM)
    m_projectM->pcm()->addPCMfloat_2ch(pAudioData, iAudioDataLength);
}
"""
    new = """void CVisualizationProjectM::AudioData(const float* pAudioData, size_t iAudioDataLength)
{
  // Kodi's audio callback must never wait for projectM rendering or preset setup.
  // If projectM is busy, skip only this visualizer PCM block.
  std::unique_lock<std::mutex> lock(m_pmMutex, std::try_to_lock);
  if (!lock.owns_lock())
    return;

  if (m_projectM)
    m_projectM->pcm()->addPCMfloat_2ch(pAudioData, iAudioDataLength);
}
"""
    replace_exact(main, old, new, "non-blocking AudioData")

    addon_xml = addon / "visualization.projectm" / "addon.xml.in"
    replace_exact(addon_xml, '  version="21.0.3"\n', '  version="21.0.3.3"\n', "local addon version")
    replace_exact(addon_xml, '  name="projectM"\n', '  name="JJS KODI projectM"\n', "JJS add-on name")
    replace_exact(addon_xml, '  provider-name="Team Kodi">\n', '  provider-name="Team Kodi; JJS">\n', "JJS provider attribution")
    replace_exact(addon_xml, '    <source>https://github.com/xbmc/visualization.projectm</source>\n', '    <source>https://github.com/jjs-hamburg/projectm-omega-build</source>\n', "modified source URL")


def verify_projectm(projectm: Path) -> None:
    # Stability build: projectM 3.1.12 itself intentionally remains unmodified.
    required = [
        projectm / "src" / "libprojectM" / "projectM.cpp",
        projectm / "src" / "libprojectM" / "projectM.hpp",
        projectm / "src" / "libprojectM" / "Renderer" / "Renderer.cpp",
    ]
    for path in required:
        if not path.is_file():
            raise RuntimeError(f"missing expected projectM 3.1.12 source file: {path}")
    print("OK  projectM 3.1.12 left unmodified for stability")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply the Omega/projectM 3.1.12 audio-isolation stability change"
    )
    parser.add_argument("--addon", required=True, type=Path, help="visualization.projectm Omega checkout root")
    parser.add_argument("--projectm", required=True, type=Path, help="projectM 3.1.12 source root")
    args = parser.parse_args()

    try:
        patch_addon(args.addon.resolve())
        verify_projectm(args.projectm.resolve())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("Audio-isolation stability transformation applied successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
