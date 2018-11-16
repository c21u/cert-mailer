FROM python:3.7-alpine as base

FROM base as builder

RUN apk add zlib-dev jpeg-dev build-base

RUN mkdir /install
WORKDIR /install

COPY requirements.txt ./
RUN pip install --install-option="--prefix=/install" -r requirements.txt

FROM base

COPY --from=builder /install /usr/local

WORKDIR /app
COPY . .

CMD [ "bash" ]
