FROM postgres:16-alpine

# Set environment variables
ENV POSTGRES_DB=salon_db
ENV POSTGRES_USER=salon_user
ENV POSTGRES_PASSWORD=salon_password

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

# Default command from base image
CMD ["postgres"]
