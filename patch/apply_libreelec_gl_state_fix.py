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

    replace_exact(
        main,
        '#include "Main.h"\n',
        '#include "Main.h"\n\n#include <GLES2/gl2.h>\n',
        "LibreELEC GLES include",
    )

    old_render = """void CVisualizationProjectM::Render()
{
  std::unique_lock<std::mutex> lock(m_pmMutex);
  if (m_projectM)
  {
    m_projectM->renderFrame();
#ifdef DEBUG
      unsigned preset;
      m_projectM->selectedPresetIndex(preset);
      if (m_lastLoggedPresetIdx != preset)
        CLog::Log(ADDON_LOG_DEBUG,"PROJECTM - Changed preset to: %s",g_presets[preset]);
      m_lastLoggedPresetIdx = preset;
#endif
  }
}
"""

    new_render = """void CVisualizationProjectM::Render()
{
  std::unique_lock<std::mutex> lock(m_pmMutex);
  if (m_projectM)
  {
    // projectM 3.1.12 renders inside Kodi's GLES context. Preserve the
    // framebuffer and viewport Kodi had active before handing control to
    // projectM so the visualizer cannot leak those two states into Kodi's GUI.
    GLint previousFramebuffer = 0;
    GLint previousViewport[4] = {0, 0, 0, 0};
    glGetIntegerv(GL_FRAMEBUFFER_BINDING, &previousFramebuffer);
    glGetIntegerv(GL_VIEWPORT, previousViewport);

    m_projectM->renderFrame();

    glBindFramebuffer(GL_FRAMEBUFFER, static_cast<GLuint>(previousFramebuffer));
    glViewport(previousViewport[0], previousViewport[1],
               previousViewport[2], previousViewport[3]);
#ifdef DEBUG
      unsigned preset;
      m_projectM->selectedPresetIndex(preset);
      if (m_lastLoggedPresetIdx != preset)
        CLog::Log(ADDON_LOG_DEBUG,"PROJECTM - Changed preset to: %s",g_presets[preset]);
      m_lastLoggedPresetIdx = preset;
#endif
  }
}
"""

    replace_exact(main, old_render, new_render, "restore Kodi framebuffer and viewport")

    addon_xml = addon / "visualization.projectm" / "addon.xml.in"
    replace_exact(
        addon_xml,
        '  version="21.0.3.3"\n',
        '  version="21.0.3.4"\n',
        "LibreELEC test addon version",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply the LibreELEC-only projectM GLES state isolation test patch"
    )
    parser.add_argument(
        "--addon",
        required=True,
        type=Path,
        help="visualization.projectm Omega checkout root after the shared JJS patch",
    )
    args = parser.parse_args()

    try:
        patch_addon(args.addon.resolve())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("LibreELEC GLES state isolation patch applied successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
