FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xvf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib \
    && ./configure --prefix=/usr \
    && make \
    && sudo make install

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py"]