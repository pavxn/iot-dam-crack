FROM python:3.7

RUN pip install fastapi uvicorn pandas scikit-learn==1.2.1 numpy joblib

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" "--port", "8000"]
