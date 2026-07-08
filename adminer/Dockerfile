FROM adminer:latest

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080 || exit 1

# Default command
CMD ["php", "-S", "0.0.0.0:8080", "-t", "/var/www/html"]
