FROM nginx:stable

COPY nginx.conf.dev /etc/nginx/nginx.conf
ENTRYPOINT [ "nginx", "-g", "daemon off;" ]