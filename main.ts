// main.ts — entrypoint for the news-image-20261123 v5 entry.
//
// The front page is rendered by draw.py (PIL) into entry.png in this
// directory. This entrypoint's only job is to place that image where
// the make.fun grader looks for it: $MAKEFUN_OUTPUT_DIR/entry.png.
//
// Build the image first (from this directory):
//   python3 draw.py
// which writes entry.png (1024x1024, deterministic, < 1 MiB).
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR;
if (!out) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}

mkdirSync(out, { recursive: true });

const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png not found next to main.ts — run python3 draw.py first");
}
copyFileSync(src, join(out, "entry.png"));
console.log("entry.png copied to " + out);
