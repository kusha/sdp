FROM nginx:1.27.1

COPY nginx-default.conf.template /etc/nginx/conf.d/default.conf.template

COPY entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
