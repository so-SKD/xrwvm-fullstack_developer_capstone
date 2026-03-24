FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app

WORKDIR $APP

# Install dependencies
COPY requirements.txt $APP
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . $APP

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Build frontend (ensure 'frontend/build' exists)
WORKDIR $APP/frontend
RUN npm install
RUN npm run build

# Copy the React build to Django's static folder
COPY frontend/build /app/static  

# Back to app folder
WORKDIR $APP

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port
EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi:application"]
