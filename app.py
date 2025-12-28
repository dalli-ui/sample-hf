

import gradio as gr
import glob

TMP_DIR = "/tmp"



def generate_video(duration, fps, width, height, blur):
    filename = os.path.join(TMP_DIR, f"video_{int(time.time())}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, int(fps), (int(width), int(height)))
    for i in range(int(fps * duration)):
        frame = np.random.randint(0, 256, (int(height), int(width), 3), dtype=np.uint8)
        if blur > 0:
            frame = cv2.GaussianBlur(frame, (blur, blur), 0)
        out.write(frame)
    out.release()
    return filename




def list_videos():
    files = sorted(glob.glob(os.path.join(TMP_DIR, "video_*.mp4")), reverse=True)
    return files

def get_video_options():
    files = list_videos()
    return [(os.path.basename(f), f) for f in files]

def play_video(video_path):
    return video_path

# Gradio UI for single video generation
def ui_generate_video(duration, fps, width, height, blur):
    path = generate_video(duration, fps, width, height, blur)
    return path

with gr.Blocks() as demo:
    gr.Markdown("# Video Generator\nGenerate a single video with custom settings.")
    with gr.Row():
        duration = gr.Slider(1, 30, value=5, step=1, label="Duration (seconds)")
        fps = gr.Slider(1, 60, value=24, step=1, label="FPS")
    with gr.Row():
        width = gr.Slider(64, 1920, value=640, step=16, label="Width")
        height = gr.Slider(64, 1080, value=480, step=16, label="Height")
    blur = gr.Slider(0, 31, value=0, step=2, label="Blur kernel size (odd, 0=none)")
    gen_btn = gr.Button("Generate Video")
    video_out = gr.Video()
    video_list = gr.Dropdown(choices=lambda: [(os.path.basename(f), f) for f in list_videos()], label="Saved Videos", interactive=True)
    video_player = gr.Video()
    refresh_btn = gr.Button("Refresh List")

    gen_btn.click(fn=ui_generate_video, inputs=[duration, fps, width, height, blur], outputs=video_out)
    video_list.change(fn=lambda f: f, inputs=video_list, outputs=video_player)
    refresh_btn.click(fn=lambda: gr.Dropdown.update(choices=[(os.path.basename(f), f) for f in list_videos()]), outputs=video_list)

port = int(os.getenv("PORT", 7860))
demo.launch(server_name="0.0.0.0", server_port=port)

if __name__ == "__main__":
    main()
