FROM python:3.10-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install -v --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "main.py"]

# CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
# CMD ["sh", "-c", "gunicorn -b 0.0.0.0:\${PORT} main:app"]
