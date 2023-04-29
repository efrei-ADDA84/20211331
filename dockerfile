FROM python:3.9
COPY openweather.py /app/
COPY .env /app/
WORKDIR /app
RUN pip install requests
RUN pip install --upgrade python-dotenv
CMD ["python", "openweather.py"]
