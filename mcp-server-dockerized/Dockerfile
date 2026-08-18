FROM python:3.11-slim

WORKDIR /app

#intall uv for faster package management
RUN pip install uv

# copy req file
COPY requirements.txt .

#intall dependencies using uv
RUN uv venv
RUN uv pip install -r requirements.txt

# copy app code
COPY server.py .
COPY client-sse.py .

#Expose the port the server runs on
EXPOSE 8000

# command to run the server
CMD ["uv", "run", "server.py"]