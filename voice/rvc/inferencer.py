import subprocess
import os

RVC_PATH = "rvc"
MODEL_PATH = "rvc/weights/alisa.pth"
INDEX_PATH = "rvc/index/alisa.index"

def convert(input_wav, output_wav):
    cmd = [
        "python", "infer.py",
        "--model_path", MODEL_PATH,
        "--index_path", INDEX_PATH,
        "--input_path", input_wav,
        "--output_path", output_wav
    ]
    subprocess.run(cmd, cwd=RVC_PATH, check=True)
