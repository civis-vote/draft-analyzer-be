FROM postgres:17

# Install required tools and pgvector
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-17 \
    make \
    gcc \
    g++ \
    git \
  && git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git \
  && cd pgvector && make && make install \
  && cd .. && rm -rf pgvector \
  && apt-get remove --purge -y git gcc g++ make \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
