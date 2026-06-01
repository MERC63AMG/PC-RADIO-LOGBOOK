FROM python:3.12-slim

WORKDIR /app

# Instalace systémových závislostí pro GUI
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libdbus-1-3 \
    libfontconfig1 \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# Kopírování projektových souborů
COPY requirements.txt .
COPY main.py .
COPY README.md .

# Instalace Python závislostí
RUN pip install --no-cache-dir -r requirements.txt

# Nastavení proměnné prostředí pro PyInstaller
ENV PYTHONUNBUFFERED=1

# Entry point - spustí aplikaci nebo build podle argumentu
ENTRYPOINT ["python"]
CMD ["main.py"]

# Pro stavbu EXE:
# docker build -t cb-pmr-logbook .
# docker run -v $(pwd)/dist:/app/dist cb-pmr-logbook -m PyInstaller.main -y --onefile main.py
