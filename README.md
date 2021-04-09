# opencv-python

## Deployment To Azure Web App
![제목 없음-1](https://user-images.githubusercontent.com/55523155/114118485-db795880-9923-11eb-820e-9482fd1eeed9.png)
> [startup.sh][DeploymentCommandLink]

[DeploymentCommandLink]: #deployment-command

## Deployment Command
```shell
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```
