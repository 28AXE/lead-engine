# Lead Engine Docker Image
# Automated prospect sourcing and qualification system

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create output directories
RUN mkdir -p outputs .cache

# Environment variables for API keys
ENV VIBE_PROSPECTING_API_KEY=""
ENV WHOISXML_API_KEY=""
ENV HUNTER_IO_API_KEY=""
ENV PAPPERS_API_KEY=""
ENV META_AD_LIBRARY_TOKEN=""
ENV GOOGLE_MAPS_API_KEY=""
ENV APIFY_API_TOKEN=""
ENV GOOGLE_ADS_API_KEY=""
ENV LINKEDIN_JOBS_API_KEY=""

# Default command: dry-run mode
CMD ["python", "-m", "src.main", "--dry-run"]
