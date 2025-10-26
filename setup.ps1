param(
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

Write-Host "[setup] 初始化作品集通用环境..." -ForegroundColor Cyan

$pythonProjects = @(
    'global-price-sentinel',
    'event-relay-hub',
    'doc-knowledge-forge',
    'insight-viz-studio'
)

$nodeProjects = @(
    'saas-northstar-dashboard',
    'a11y-component-atlas'
)

function Ensure-PythonEnv {
    param(
        [string]$ProjectPath
    )

    $venvPath = Join-Path $ProjectPath '.venv'
    if (Test-Path $venvPath -and -not $Force) {
        Write-Host "[setup] 跳过 $ProjectPath (已存在虚拟环境)" -ForegroundColor Yellow
        return
    }

    if (Test-Path $venvPath) {
        Remove-Item $venvPath -Recurse -Force
    }

    Write-Host "[setup] 创建虚拟环境: $ProjectPath" -ForegroundColor Green
    python -m venv $venvPath
    $pip = Join-Path $venvPath 'Scripts/pip.exe'
    $reqFile = Join-Path $ProjectPath 'requirements.txt'
    if (Test-Path $reqFile) {
        & $pip install --upgrade pip
        & $pip install -r $reqFile
    }
}

function Install-NodeDeps {
    param(
        [string]$ProjectPath
    )

    if (-not (Test-Path (Join-Path $ProjectPath 'package.json'))) {
        Write-Host "[setup] package.json 未找到: $ProjectPath" -ForegroundColor Yellow
        return
    }

    Write-Host "[setup] 安装 Node 依赖: $ProjectPath" -ForegroundColor Green
    Push-Location $ProjectPath
    try {
        if (Test-Path 'pnpm-lock.yaml') {
            pnpm install
        } elseif (Test-Path 'yarn.lock') {
            yarn install
        } else {
            npm install
        }
    }
    finally {
        Pop-Location
    }
}

$root = Get-Location

foreach ($proj in $pythonProjects) {
    $path = Join-Path $root $proj
    if (-not (Test-Path $path)) {
        Write-Host "[setup] 跳过缺失目录: $proj" -ForegroundColor Yellow
        continue
    }
    Ensure-PythonEnv -ProjectPath $path
}

foreach ($proj in $nodeProjects) {
    $path = Join-Path $root $proj
    if (-not (Test-Path $path)) {
        Write-Host "[setup] 跳过缺失目录: $proj" -ForegroundColor Yellow
        continue
    }
    Install-NodeDeps -ProjectPath $path
}

Write-Host "[setup] 完成" -ForegroundColor Cyan

