import os
import time
import cv2
import numpy as np

from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TMP_DIR = "/tmp"
VIDEO_DURATION = 14  # seconds (increase duration)
FPS = 30  # higher frame rate
FRAME_SIZE = (1920, 1080)  # Full HD for heavy usage
NUM_THREADS = 4  # Number of parallel video generators


def generate_video(filename):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, FPS, FRAME_SIZE)
    for i in range(FPS * VIDEO_DURATION):
        # Heavy computation: apply random noise and a blur
        frame = np.random.randint(0, 256, (FRAME_SIZE[1], FRAME_SIZE[0], 3), dtype=np.uint8)
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        out.write(frame)
    out.release()


def main():
    autocreate = "1"
    idx = 0

    def video_loop(thread_id):
        nonlocal idx
        while autocreate:
            filename = os.path.join(TMP_DIR, f"video_{int(time.time())}_{idx}_t{thread_id}.mp4")
            print(f"[Thread {thread_id}] Generating {filename}")
            generate_video(filename)
            idx += 1
            # No sleep for max resource usage

    # Start multiple video generation threads for heavy usage
    if autocreate:
        for t in range(NUM_THREADS):
            Thread(target=video_loop, args=(t,), daemon=True).start()

    # Minimal HTTP server for Hugging Face Spaces
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Video generator running')

    port = int(os.getenv("PORT", 7860))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Serving HTTP on port {port}")
    server.serve_forever()  

if __name__ == "__main__":
    main()
