# 3D Gaussian Splatting Pipeline

## Repositories

- [INRIA Official: gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting)
- [Camenduru Colab Fork](https://github.com/camenduru/gaussian-splatting)
- [GS-SDF (HKU-MARS)](https://github.com/hku-mars/GS-SDF)
- [Colab-Friendly: 3DGaussianSplatting-INRIA-Method](https://github.com/YassGan/3DGaussianSplatting-INRIA-Method-Colab)

> ⚠️ **Note**: Requires a **T4 GPU** for optimal performance.

---

## Hugging Face Setup
- Add your HuggingFace token to the `.env` file.

### Resources:
- **Model**: [bcben/gaussian-splat](https://huggingface.co/bcben/gaussian-splat)

---

## Pipeline Steps

1. **Convert Video to Photos** (Run Locally)
   - Use the provided script in the `src` folder to extract frames from the input video.
   - Example (Python/OpenCV based):
     ```bash
     python src/video_to_frames.py --input my_video.mp4 --output frames/
     ```

2. **Generate COLMAP Data from Photos** (Run Locally)
   - Use COLMAP-related scripts in the `src` folder to reconstruct sparse/dense point cloud from frames.
   - Make sure COLMAP is installed and accessible.
   - Example:
     ```bash
     python src/run_colmap.py --images frames/ --output colmap_output/
     ```

3. **Generate Gaussian Splatting Model on Google Colab**
   - Upload the `frames/` and `colmap_output/` folders to Colab.
   - Use one of the Colab-ready notebooks (e.g., [YassGan’s Colab repo](https://github.com/YassGan/3DGaussianSplatting-INRIA-Method-Colab)) to train the Gaussian splatting model.

4. **Upload and View in Three.js**
   - Export the trained model in compatible format (e.g., `.ply`, `.json`, or splats format).
   - Integrate it into your Three.js application for web visualization.
   - Example with Three.js loader:
     ```javascript
     const loader = new THREE.PointsLoader();
     loader.load('model.splats', function (points) {
       scene.add(points);
     });
     ```
