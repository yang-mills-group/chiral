FROM ubuntu@sha256:562111b88caa79c71391c0c4d3c2114a7d5c35915c20561fd893cb1e07929e6b
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends bubblewrap python3 git ca-certificates libgmp10 libstdc++6 time && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /run/user
ENV PATH=/tools/bin:/usr/bin:/bin
WORKDIR /runcheck
