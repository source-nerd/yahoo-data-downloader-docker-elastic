# YFinance Data Downloader - Docker and Kubernetes Cron Job

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

YFinance minute and daily data downloader, with Dockerfile and kubernetes pod yaml declaration. The Pod has restart policy on failure and can be run as a CROn job on daily basis. The downloaded data is written to elasticsearch - which is running in the same K8 environment and is connected via service.

> This project makes use of Github Actions to build and publish the docker image.

## Publishing image to GitHub Packages Manually
docker login docker.pkg.github.com -u USER_NAME -p PERSONAL_ACCESS_TOKEN

docker tag BUILD_IMAGE_ID docker.pkg.github.com/source-nerd/yahoo-data-downloader-docker-elastic/yahoo-data-downloader-docker-elastic:VERSION

docker build -t docker.pkg.github.com/source-nerd/yahoo-data-downloader-docker-elastic/yahoo-data-downloader-docker-elastic:VERSION .

docker push docker.pkg.github.com/source-nerd/yahoo-data-downloader-docker-elastic/yahoo-data-downloader-docker-elastic:VERSION


## Deploying to Kubernetes
1. Initialize the namespace
2. Install the creds - [REF HERE](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)
```shell
# Example:
kubectl create secret docker-registry regcred \
  --docker-server=$DOCKER_REGISTRY_SERVER \
  --docker-username=$DOCKER_USER \
  --docker-password=$DOCKER_PASSWORD \
  --docker-email=$DOCKER_EMAIL

# Actual
kubectl create secret docker-registry regcred --docker-server=docker.pkg.github.com --docker-username=source-nerd --docker-password=PERSONAL_ACCESS_TOKEN --docker-email=EMAIL
```

kubectl --kubeconfig KUBE_CONF_PATH -n NAMESPACE apply -f pod.yaml


## Feedback & Final Thoughts
The code may not be very optimized, so if you tend to find any bug fixes, feature requests, pull requests, feedback, etc., are welcome... If you like this project, please do give it a star.

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)

