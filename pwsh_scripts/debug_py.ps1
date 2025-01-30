param (
    [string]$pythonScriptPath
)

docker exec -it pubpoint-backend-1 python -m debugpy --listen 0.0.0.0:5678 --wait-for-client $pythonScriptPath