FROM python:3.12-slim

RUN sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's/security.debian.org/mirror.yandex.ru\/debian-security/g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update && apt-get install -y --fix-missing wget gnupg unzip curl && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --fix-missing fonts-liberation xdg-utils && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --fix-missing \
    libatk-bridge2.0-0 libatk1.0-0 libgtk-3-0 \
    libcups2 libdbus-1-3 libnspr4 libnss3 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --fix-missing \
    libdrm2 libgbm1 \
    libxcomposite1 libxdamage1 libxfixes3 \
    libxkbcommon0 libxrandr2 \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y firefox-esr && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-edge.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-edge.gpg] https://packages.microsoft.com/repos/edge stable main" >> /etc/apt/sources.list.d/microsoft-edge.list \
    && apt-get update \
    && apt-get install -y microsoft-edge-stable \
    && rm -rf /var/lib/apt/lists/*

RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+' | head -1) \
    && wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux64

RUN GECKO_VERSION="v0.36.0" \
    && GECKO_VERSION_WITHOUT_V="0.36.0" \
    && wget -q "https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-linux64.tar.gz" \
    && tar -xzf geckodriver-${GECKO_VERSION}-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-${GECKO_VERSION}-linux64.tar.gz

RUN EDGE_VERSION=$(microsoft-edge-stable --version 2>/dev/null || true) \
    && EDGE_VERSION=$(echo $EDGE_VERSION | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -1) \
    && if [ -z "$EDGE_VERSION" ]; then \
        echo "ERROR: Could not determine Edge version" && exit 1; \
    fi \
    && wget -q --tries=3 --timeout=30 "https://msedgedriver.microsoft.com/${EDGE_VERSION}/edgedriver_linux64.zip" -O edgedriver.zip \
    && unzip -q edgedriver.zip \
    && mv msedgedriver /usr/local/bin/edgedriver \
    && chmod +x /usr/local/bin/edgedriver \
    && rm edgedriver.zip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p allure-results logs

RUN echo '#!/bin/bash\n\
echo "=========================================="\n\
echo "Запуск тестов PrestaShop"\n\
echo "Получены аргументы: $@"\n\
echo "=========================================="\n\
pytest tests/ --alluredir=allure-results --clean-alluredir "$@"\n\
' > /app/run_tests.sh && chmod +x /app/run_tests.sh

ENTRYPOINT ["/app/run_tests.sh"]