# Build a Docker image that can run from either AMD64 (Intel) or ARM64 (Apple) architectures.
# Run this script from the root of the repo to set the build context for the Dockerfile.
docker buildx build --platform linux/amd64,linux/arm64 -t ubkg-front-end -f docker/ubkg-api/Dockerfile .

