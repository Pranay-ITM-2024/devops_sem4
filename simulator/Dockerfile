FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir requests
COPY simulator.py .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
CMD ["python", "simulator.py"]
