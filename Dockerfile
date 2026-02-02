FROM mci-repo.unix.mci.ir:8088/python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -q -r requirements.txt \
    --index-url http://mci-repo.unix.mci.ir:8081/repository/pypi/simple \
    --trusted-host mci-repo.unix.mci.ir

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=manage.py

# Run migrations and start app
CMD flask db upgrade && python manage.py

