FROM nginx

COPY ./default.conf /etc/nginx/conf.d/default.conf

COPY ./localhost.crt /etc/nginx/localhost.crt
COPY ./localhost.key /etc/nginx/localhost_private.key

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
