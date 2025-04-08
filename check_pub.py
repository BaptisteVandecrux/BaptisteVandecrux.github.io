import os
import yaml

folders = ["_publications", "_datasets"]

for folder in folders:
    for filename in os.listdir(folder):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        if lines[0].strip() != "---":
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

        # Update permalink
        base = os.path.splitext(filename)[0]
        expected_permalink = f"/publication/{base}" if folder == "_publication" else f"/datasets/{base}"
        current_permalink = meta.get("permalink", "").strip()
        if current_permalink != expected_permalink:
            meta["permalink"] = expected_permalink
            print(f"✅ Updated: {filename} → {expected_permalink}")

            # Rebuild file
            new_content = "---\n" + yaml.dump(meta, sort_keys=False) + "---\n" + "".join(rest_of_file)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
