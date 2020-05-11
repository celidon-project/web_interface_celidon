FROM alpine:latest as build-stage

RUN apk update && apk add bash yarn \
 && yarn global add @vue/cli @vue/cli-service-global
WORKDIR /app
COPY celidon_ui/package.json ./
RUN yarn
COPY ./celidon_ui .
RUN yarn build


FROM build-stage as dev
ENTRYPOINT [ "bash", "-c", "yarn && exec yarn serve" ]


FROM nginx:stable as prod
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx/nginx.conf.prod /etc/nginx/nginx.conf
ENTRYPOINT [ "nginx", "-g", "daemon off;" ]