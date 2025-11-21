#!/usr/bin/env python3
import os, json, base64, mimetypes

def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_files(dir_path, exts=None):
    files_data = []
    for file in os.listdir(dir_path):
        if exts and not any(file.endswith(e) for e in exts):
            continue
        path = os.path.join(dir_path, file)
        if os.path.isdir(path):
            continue
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        mime_type, _ = mimetypes.guess_type(path)
        if not mime_type:
            mime_type = "application/octet-stream"
        files_data.append({"name": file, "type": mime_type, "contents": b64, "display_logo": True})
    return files_data

config = json.load(open("config/config.json"))
scripts = [{"name": f.split(".")[0], "contents": read_text(os.path.join("scripts", f))}
           for f in os.listdir("scripts") if f.endswith(".py")]
manual = [{"name": f.split(".")[0], "contents": read_text(os.path.join("manual", f))}
          for f in os.listdir("manual") if f.endswith(".md")]
images = read_files("images")
change_log = {"contents": read_text("CHANGELOG.md")}

latest = {
    "config": config,
    "scripts": scripts,
    "images": images,
    "manual": manual,
    "change_log": change_log
}

with open("latest.json", "w") as f:
    json.dump(latest, f, indent=2)

print("latest.json built")
