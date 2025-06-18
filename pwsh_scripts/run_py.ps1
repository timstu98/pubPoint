param (
    [string]$pythonScriptPath,
    [string[]]$scriptArgs = $null
)

$joinedArgs = if ($scriptArgs) { $scriptArgs -join ' ' } else { "" }

docker exec -it pubpoint-backend-1 python $pythonScriptPath $joinedArgs
