import os

# Root directory = wherever this script is run
ROOT = os.getcwd()

# Full directory tree for the project
DIRECTORIES = [
    # Core repo structure
    "site",
    "content",
    "scripts",
    "data",

    # SvelteKit expected sub-structure (created early for clarity)
    "site/src",
    "site/src/routes",
    "site/src/lib",
    "site/static",

    # Content structure (museum-style archive)
    "content/pages",
    "content/timelines",
    "content/timelines/eras",
    "content/timelines/events",
    "content/frameworks",
    "content/frameworks/power",
    "content/frameworks/governance",
    "content/community-impact",
    "content/legislative-process",
    "content/constitutions",
    "content/tags",
    "content/sources",
    "content/provenance",

    # Data outputs (generated at build time)
    "data/indexes",
    "data/manifests",
    "data/logs",

    # Build & utility scripts
    "scripts/build",
    "scripts/utils",
]

def create_directories():
    print("Initializing Arkansas Political History project structure...\n")

    for path in DIRECTORIES:
        full_path = os.path.join(ROOT, path)
        try:
            os.makedirs(full_path, exist_ok=True)
            print(f"✔ Created: {path}")
        except Exception as e:
            print(f"✖ Failed to create {path}: {e}")

    print("\nProject folder structure complete.")
    print(f"Root directory: {ROOT}")

if __name__ == "__main__":
    create_directories()
