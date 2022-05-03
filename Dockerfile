FROM python:3.6 

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install  -r requirements.txt

COPY . .

ENV SECRET_KEY="qwertyuiopasdfghjklzxcvbnmgenratedfjsdfjs"
ENV ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV NAME="ashutosh"
ENV EMAIL="ashutoshuniyal21@gmail.com"
ENV PASSWORD=9410197255
ENV URL="mysql://fynd_acad:fynd123@mysql_db:3306/fynd_acad"

CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port",  "8000"]


# CMD uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}  