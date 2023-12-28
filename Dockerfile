FROM python:3.10.7-slim

# Install everything
RUN echo '\
platform=$(uname -m)\n\
echo "Plataforma detectada:" $platform\n\
\n\
while ! apt-get update -y; do\n\
    echo "Trying again apt-get update..."\n\
    sleep 5\n\
done\n\
\n\
if [[ "$platform" == "x86_64" ]]; then\n\
    while ! apt-get install -y --no-install-recommends --fix-missing --fix-broken libpq-dev gcc build-essential wget ca-certificates fontconfig libc6 libfreetype6 libjpeg62-turbo libpng16-16 libssl1.1 libstdc++6 libx11-6 libxcb1 libxext6 libxrender1 xfonts-75dpi xfonts-base zlib1g ; do\n\
        echo "Trying again apt-get install..."\n\
        sleep 5\n\
    done\n\
    wget -q https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb\n\
    dpkg -i wkhtmltox_0.12.5-1.buster_amd64.deb\n\
    cp /usr/local/bin/wkhtmltopdf /usr/bin/\n\
    cp /usr/local/bin/wkhtmltoimage /usr/bin/\n\
fi\n\
\n\
if [[ "$platform" == *"arm"* || "$platform" == *"arch"* ]]; then\n\
    while ! apt-get install -y --no-install-recommends --fix-missing --fix-broken libpq-dev gcc build-essential wkhtmltopdf ; do\n\
        echo "Trying again apt-get install..."\n\
        sleep 5\n\
    done\n\
fi\n\
' > /install-packages.sh
RUN bash install-packages.sh

# Setup project workdir and env vars
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip and wheel
RUN pip install --upgrade pip &&\
 pip install wheel

# Install project requirements
COPY requirements.txt .
COPY utils ./utils
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port 8000
EXPOSE 8000