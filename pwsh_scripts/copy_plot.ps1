param (
    [string]$ContainerName = "pubpoint-backend-1",
    [string]$LocalPath = "C:\Users\tcvin\OneDrive\Documents\pubPoint\Plots",
    [string]$ContainerFilePath = "/tmp/plot",
    [string]$FileName = "plot"
)

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed or not in your PATH."
    exit 1
}

# Make sure LocalPath exists
if (-not (Test-Path $LocalPath)) {
    New-Item -ItemType Directory -Path $LocalPath | Out-Null
}

# Build paths
$FullLocalFilePath = Join-Path $LocalPath "$FileName.png"
$DockerSource = "$ContainerName`:$ContainerFilePath.png"
$FullLocalFilePathMap = Join-Path $LocalPath "$FileName-map.png"
$DockerSourceMap = "$ContainerName`:$ContainerFilePath-map.png"

# Copy file
docker cp "$DockerSource" "$FullLocalFilePath"
docker cp "$DockerSourceMap" "$FullLocalFilePathMap"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Image successfully copied to $FullLocalFilePath"
} else {
    Write-Error "❌ docker cp failed. The file might not exist in the container or the container ID is wrong."
    exit $LASTEXITCODE
}
