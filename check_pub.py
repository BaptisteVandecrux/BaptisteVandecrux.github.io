import os
import yaml

folders = ["_publications", "_datasets"]

for folder in folders:
    for filename in os.listdir(folder):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(folder, filename)

        # Force fallback decode for full safety
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="cp1252", errors="replace") as f:
                lines = f.readlines()
            print(f"⚠️ Re-decoding with cp1252: {filename}")

        if not lines or lines[0].strip() != "---":
            print(f"{filename}: missing front matter")
            continue

        # Extract YAML front matter
        front_matter = []
        rest_of_file = []
        inside_yaml = False
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if inside_yaml:
                    rest_of_file = lines[i+1:]
                    break
                else:
                    inside_yaml = True
                    continue
            if inside_yaml:
                front_matter.append(line)

        try:
            meta = yaml.safe_load("".join(front_matter))
        except Exception as e:
            print(f"{filename}: YAML error - {e}")
            continue

        # Build expected permalink
        base = os.path.splitext(filename)[0]
        expected_permalink = f"/publication/{base}" if folder == "_publications" else f"/datasets/{base}"
        current_permalink = meta.get("permalink", "").strip()

        changed = False
        if current_permalink != expected_permalink:
            meta["permalink"] = expected_permalink
            changed = True
            print(f"✅ Updated permalink: {filename} → {expected_permalink}")

        # Rebuild and overwrite (always) in UTF-8
        rebuilt = "---\n" + yaml.dump(meta, sort_keys=False, allow_unicode=True) + "---\n" + "".join(rest_of_file)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(rebuilt)
        if not changed:
            print(f"🧼 Cleaned encoding only: {filename}")
