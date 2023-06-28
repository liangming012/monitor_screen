FROM node:19.7.0 as build-stage

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:stable-perl as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY --from=build-stage /app/default.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/oasgames.com.crt /etc/nginx/conf.d/ssl/oasgames.com.crt

COPY --from=build-stage /app/oasgames.com.key /etc/nginx/conf.d/ssl/oasgames.com.key

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# 生成镜像命令         docker build -t monitor_screen_frontend:v1.0.0 .
# 使用镜像运行容器命令   docker run -d --name monitor_screen_frontend -p 8081:80 monitor_screen_frontend:v1.0.0