#!/usr/bin/env python3
"""Smoke test for the Literature Gap Radar pipeline."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("[cmd]", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    script = Path(__file__).resolve().parent / "local_first_literature.py"
    with tempfile.TemporaryDirectory(prefix="local_first_literature_smoke_") as tmp:
        base = Path(tmp)
        local = base / "local_papers"
        out = base / "out"
        local.mkdir()
        out.mkdir()

        (local / "2024 growth-factor hydrogel release.txt").write_text(
            "Title: Growth-factor hydrogel for tissue repair\n"
            "DOI: 10.1234/example.hydrogel\n"
            "Abstract: A dynamic biomaterial hydrogel was developed for controlled growth-factor release and tissue repair.\n"
            "Materials and methods: ELISA release assay, rheology, confocal imaging, immunofluorescence and qPCR were performed. Figure 1 shows the material workflow.",
            encoding="utf-8",
        )
        (local / "2023 BiOI MXene photocatalytic membrane.txt").write_text(
            "Title: BiOI MXene photocatalytic membrane\n"
            "DOI: 10.1234/example.photo\n"
            "Abstract: A photocatalytic membrane was evaluated for pollutant degradation. Methods include XPS, SEM, EIS, PL, ESR and cycling stability.",
            encoding="utf-8",
        )
        (local / "zotero-export.ris").write_text(
            "TY  - JOUR\n"
            "TI  - Injectable coacervate hydrogel for regenerative immunomodulation\n"
            "AU  - Example, Ada\n"
            "PY  - 2025\n"
            "JO  - Advanced Materials\n"
            "DO  - 10.9999/example.ris\n"
            "AB  - A metadata-only record from a Zotero or EndNote RIS export with macrophage polarization and release assays.\n"
            "ER  -\n",
            encoding="utf-8",
        )
        obsidian = local / "obsidian_vault"
        obsidian.mkdir()
        (obsidian / ".obsidian").mkdir()
        (obsidian / "paper-note.md").write_text(
            "# Phase separation paper note\n\nDOI: 10.7777/example.note\n\nAbstract: Notes about liquid-liquid phase separation, FRAP, and hydrogel mechanics.",
            encoding="utf-8",
        )

        index = out / "index.jsonl"
        profile = out / "profile.json"
        gap = out / "gap.json"
        candidates = out / "candidates.jsonl"
        scored = out / "scored.jsonl"

        run([sys.executable, "-X", "utf8", str(script), "index", "--roots", str(local), "--output", str(index), "--source-manifest", str(out / "source_manifest.json")])
        run([sys.executable, "-X", "utf8", str(script), "infer-profile", "--index", str(index), "--output", str(profile)])
        run([sys.executable, "-X", "utf8", str(script), "gap-map", "--profile", str(profile), "--output", str(gap)])

        records = [
            {
                "title": "Growth-factor hydrogel for tissue repair",
                "doi": "10.1234/example.hydrogel",
                "year": 2024,
                "journal": "Biomaterials",
                "abstract": "Hydrogel ELISA release rheology confocal imaging tissue repair",
            },
            {
                "title": "Stress relaxation coacervate hydrogel promotes stem-cell skin repair",
                "doi": "10.5678/new.paper",
                "year": 2026,
                "journal": "Nature Biomedical Engineering",
                "abstract": "Viscoelastic hydrogel coacervate stress relaxation regulates YAP mechanotransduction, qPCR, immunofluorescence and in vivo skin repair.",
            },
        ]
        with candidates.open("w", encoding="utf-8", newline="\n") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

        run([
            sys.executable, "-X", "utf8", str(script), "score",
            "--index", str(index), "--candidates", str(candidates),
            "--profile", str(profile), "--gap-map", str(gap),
            "--output", str(scored),
        ])
        run([sys.executable, "-X", "utf8", str(script), "render", "--scored", str(scored), "--output-dir", str(out / "report")])

        assert index.exists()
        indexed = [json.loads(line) for line in index.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert any(rec.get("source_adapter") == "ris" for rec in indexed)
        assert (out / "source_manifest.json").exists()
        assert profile.exists()
        assert gap.exists()
        assert scored.exists()
        assert (out / "report" / "literature_evidence_matrix.csv").exists()
        assert (out / "report" / "reading_priority_report.html").exists()
        print(f"Smoke test passed. Temporary output was: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
