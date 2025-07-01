import subprocess
from pathlib import Path

# === CONFIGURATION ===
image_dir = Path("../photos")               # Folder containing all PNG images
output_dir = Path("../output")              # Output base directory
database_path = output_dir / "database.db"
sparse_dir = output_dir / "sparse/0"     # Sparse model folder

# === HELPER ===
def run_colmap_command(command: list[str]):
    """Run a COLMAP command with logging."""
    print(f"\n▶ Running: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running COLMAP command: {e}")
        exit(1)

# === MAIN PIPELINE ===
def run_colmap_pipeline():
    # Make sure output folders exist
    output_dir.mkdir(parents=True, exist_ok=True)
    sparse_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Feature extraction
    run_colmap_command([
        "colmap", "feature_extractor",
        "--database_path", str(database_path),
        "--image_path", str(image_dir),
        "--ImageReader.single_camera", "1",
        "--ImageReader.camera_model", "PINHOLE"
    ])

    # Step 2: Matching
    run_colmap_command([
        "colmap", "exhaustive_matcher",
        "--database_path", str(database_path)
    ])

    # Step 3: Sparse reconstruction
    run_colmap_command([
        "colmap", "mapper",
        "--database_path", str(database_path),
        "--image_path", str(image_dir),
        "--output_path", str(sparse_dir)
    ])

    print("\n✅ COLMAP pipeline complete.")
    print(f"• Database: {database_path}")
    print(f"• Sparse model: {sparse_dir}")

# === ENTRY POINT ===
if __name__ == "__main__":
    run_colmap_pipeline()
