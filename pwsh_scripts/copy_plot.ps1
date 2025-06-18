param (
    [string]$ContainerName = "38e1087136eea9b9c6011bec7079827aed9444cd237de6be84a2d10049f92761",
    [string]$LocalPath = "C:\Users\tcvin\OneDrive\Documents\pubPoint\Plots",
    [string]$ContainerFilePath = "/tmp/plot.png",
    [string]$FileName = "plot"
)

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed or not in your PATH."
    exit 1
}

# Ensure FileName ends with .png
if (-not $FileName.ToLower().EndsWith(".png")) {
    $FileName += ".png"
}

# Make sure LocalPath exists
if (-not (Test-Path $LocalPath)) {
    New-Item -ItemType Directory -Path $LocalPath | Out-Null
}

# Build paths
$FullLocalFilePath = Join-Path $LocalPath $FileName
$DockerSource = "$ContainerName`:$ContainerFilePath"

# Copy file
docker cp "$DockerSource" "$FullLocalFilePath"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Image successfully copied to $FullLocalFilePath"
} else {
    Write-Error "❌ docker cp failed. The file might not exist in the container or the container ID is wrong."
    exit $LASTEXITCODE
}
