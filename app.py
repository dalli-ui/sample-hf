import os
import time
import cv2
import numpy as np

from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TMP_DIR = "/tmp"
VIDEO_DURATION = 2  # seconds
FPS = 10
FRAME_SIZE = (320, 240)


def generate_video(filename):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, FPS, FRAME_SIZE)
    for i in range(FPS * VIDEO_DURATION):
        frame = np.random.randint(0, 256, (FRAME_SIZE[1], FRAME_SIZE[0], 3), dtype=np.uint8)
        out.write(frame)
    out.release()


def main():
    autocreate = os.getenv("AUTO_CREATE", "0") == "1"
    idx = 0

    def video_loop():
        nonlocal idx
        while autocreate:
            filename = os.path.join(TMP_DIR, f"video_{int(time.time())}_{idx}.mp4")
            print(f"Generating {filename}")
            generate_video(filename)
            idx += 1
            time.sleep(1)

    # Start video generation in a background thread
    if autocreate:
        Thread(target=video_loop, daemon=True).start()

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
