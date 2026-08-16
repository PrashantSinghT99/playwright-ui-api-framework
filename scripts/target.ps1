[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("setup", "start", "status", "stop")]
    [string]$Action = "status",

    [string]$Ref = "d36bd3f8647a091d406e53bad463c5e3e5d2ece1"
)

$ErrorActionPreference = "Stop"
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$targetRoot = [IO.Path]::GetFullPath((Join-Path $workspace ".target\restful-booker-platform"))

if (-not $targetRoot.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar)) {
    throw "Target directory must remain inside the workspace."
}

function Assert-TargetExists {
    if (-not (Test-Path -LiteralPath (Join-Path $targetRoot ".git"))) {
        throw "Local target is not installed. Run: .\scripts\target.ps1 setup"
    }
}

switch ($Action) {
    "setup" {
        if (Test-Path -LiteralPath (Join-Path $targetRoot ".git")) {
            git -C $targetRoot fetch --depth 1 origin $Ref
        }
        else {
            New-Item -ItemType Directory -Force -Path (Split-Path $targetRoot) | Out-Null
            git clone --no-checkout --filter=blob:none `
                https://github.com/mwinteringham/restful-booker-platform.git $targetRoot
            git -C $targetRoot fetch --depth 1 origin $Ref
        }
        git -C $targetRoot checkout --detach $Ref
        Write-Host "Pinned Restful Booker Platform at $Ref"
    }
    "start" {
        Assert-TargetExists
        Push-Location $targetRoot
        try {
            & .\build_locally.cmd
        }
        finally {
            Pop-Location
        }
    }
    "status" {
        Assert-TargetExists
        docker compose --project-directory $targetRoot ps
    }
    "stop" {
        Assert-TargetExists
        docker compose --project-directory $targetRoot down
    }
}
