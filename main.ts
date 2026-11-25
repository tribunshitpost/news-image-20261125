// World News One Image — 25 November 2026.
// Entrypoint: validates the committed poster and copies it to the output.
//
// The poster was drawn by draw_poster.py (the drawing program in this
// repository) and committed as entry.png. The grader runs with the
// standard library only — no Python, no Pillow, no system fonts — so this
// entrypoint uses node:fs alone: it checks the committed PNG (signature,
// 1024x1024, at most 1 MiB) and copies it to the output directory. A
// copy is byte-identical on every run, so the image is deterministic.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(outDir, "entry.png");

// Validate the PNG before copying: 8-byte signature, then IHDR 1024x1024.
const png = readFileSync(source);
const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!png.subarray(0, 8).equals(signature)) {
  throw new Error("entry.png: bad PNG signature");
}
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png: expected 1024x1024, got ${width}x${height}`);
}
if (png.length > 1024 * 1024) {
  throw new Error(`entry.png: ${png.length} bytes exceeds the 1 MiB cap`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`entry.png written to ${target} (${png.length} bytes, ${width}x${height})`);
