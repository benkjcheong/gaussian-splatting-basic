import cv2
import os

def extract_even_frames_from_folder(video_dir="../video", output_root="../photos", frames_per_video=150):
    video_dir = os.path.abspath(video_dir)
    output_root = os.path.abspath(output_root)

    print(f"📂 Looking for videos in: {video_dir}")
    print(f"📸 Output photos will go in: {output_root}")

    if not os.path.isdir(video_dir):
        print(f"❌ ERROR: Video folder not found at {video_dir}")
        return

    os.makedirs(output_root, exist_ok=True)

    video_files = [f for f in os.listdir(video_dir) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]

    if not video_files:
        print("⚠️ No video files found in the folder.")
        return

    for filename in video_files:
        video_path = os.path.join(video_dir, filename)
        video_name = os.path.splitext(filename)[0]
        output_dir = os.path.join(output_root, video_name)
        os.makedirs(output_dir, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames == 0:
            print(f"⚠️ Skipping {filename}: unreadable or empty.")
            cap.release()
            continue

        step = max(1, total_frames // frames_per_video)
        print(f"🎞️ Processing '{filename}' ({total_frames} frames), extracting every {step} frames...")

        frame_idx = 0
        saved = 0
        while saved < frames_per_video and cap.isOpened():
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                print(f"⚠️ Frame {frame_idx} could not be read. Stopping early.")
                break
            out_path = os.path.join(output_dir, f"{saved:05d}.png")
            cv2.imwrite(out_path, frame)
            saved += 1
            frame_idx += step

        cap.release()
        print(f"✅ {saved} frames saved to: {output_dir}\n")

if __name__ == "__main__":
    extract_even_frames_from_folder(video_dir="../video", output_root="../photos", frames_per_video=150)
