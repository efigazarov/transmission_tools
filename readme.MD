# Transmission Resume Recovery & Reconfiguration

This guide outlines the process to restore `.resume` files, analyze them, and reconfigure torrent locations in a Transmission Docker setup.

## Prerequisites

- Docker installed
- Python 3 with `requests` module
- Your Transmission container uses persistent volumes mounted from `/home/efi/transmission`

---

## 🔁 Full Process

### 0. Stop and Remove the Current Transmission Docker Container

```bash
docker stop transmission && docker rm transmission
```

---

### 1. Backup Transmission Config Folder

```bash
cp -r ~/transmission/config ~/transmission/config-backup
```

---

### 2. Clear Current `.resume` Files

```bash
rm ~/transmission/config/resume/*.resume
```

---

### 3. Update `resume_analysis.py` Script

Make sure `resume_analysis.py` reads from the backup resume folder:

```python
resume_dir = "/home/efi/transmission/config-backup/resume"
```

---

### 4. Generate a Clean Resume Analysis

```bash
python3 resume_analysis.py > results.txt
```

This creates a structured summary of `.resume` files and their corresponding data paths.

---

### 5. Start a New Transmission Docker Container

```bash
sudo docker run -d \
  --name=transmission \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Israel \
  -e TRANSMISSION_WEB_HOME=/config/flood-for-transmission \
  -p 9091:9091 \
  -p 51413:51413 \
  -p 51413:51413/udp \
  -v /home/efi/transmission/config:/config \
  -v /media:/downloads \
  -v /home/efi/transmission/watch:/watch \
  --restart unless-stopped \
  linuxserver/transmission:latest
```

---

### 6. Stop All Downloads via Transmission GUI

Open Transmission Web UI at [http://localhost:9091](http://localhost:9091) and **pause all active downloads**.

---

### 7. Run the Location Setter Script

```bash
python3 set_locations_based_on_resume_analysis.py
```

This script reads `results.txt` and uses the Transmission RPC to reassign torrent data locations without moving files.

---

## Notes

- The `resume_analysis.py` script parses resume files into a human-readable format.
- The `set_locations_based_on_resume_analysis.py` script reads that output and configures Transmission.
- Ensure Transmission RPC credentials and endpoint match your container config.
