FROM nginx:1.25

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY config/nginx.conf /etc/nginx/conf.d/

# Expose the port nginx is running on
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]