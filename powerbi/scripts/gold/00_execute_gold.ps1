# TourismPulse — Gold Layer Execution Script (SQL Warehouse)
# Proposed execution script. Runs SQL files in dependency order via Databricks SQL API.
# Does not execute anything yet. Review before running.

$d = "C:\Users\Kaashvi\AppData\Local\Microsoft\WinGet\Packages\Databricks.DatabricksCLI_Microsoft.Winget.Source_8wekyb3d8bbwe\databricks.exe"
$WH = "699426b61c5cd41b"

function Exec-Sql([string]$sql) {
  $body = @{ warehouse_id=$WH; statement=$sql; wait_timeout="30s"; results_format="JSON_ARRAY" } | ConvertTo-Json -Compress
  $resp = & $d api post "/api/2.0/sql/statements" --json $body --profile TOURISMPULSE | ConvertFrom-Json
  return $resp
}

# Create schema (idempotent)
$resp = Exec-Sql("CREATE SCHEMA IF NOT EXISTS workspace.gold_layer;")
if ($resp.status.state -ne "SUCCEEDED") { Write-Output "SCHEMA CREATE FAILED: $($resp.error)"; exit 1 }
Write-Output "Schema creation: OK"

$files = @(
    "01_dim_country.sql",
    "02_dim_date.sql",
    "03_fact_tourism_arrivals.sql",
    "04_fact_nights_spent.sql",
    "05_fact_hotel_performance.sql",
    "06_fact_hotel_occupancy.sql",
    "07_gold_analytics.sql",
    "08_gold_source_comparison.sql",
    "09_powerbi_preparation.sql"
)

$base = Split-Path $MyInvocation.MyCommand.Path

foreach ($f in $files) {
    $path = Join-Path $base $f
    if (-not (Test-Path $path)) { Write-Output "MISSING: $f"; exit 1 }
    $sql = Get-Content $path -Raw
    # Split on semicolons to support multi-statement files.
    $statements = $sql -split ';' | Where-Object { $_.Trim() }
    $ok = $true
    foreach ($stmt in $statements) {
        $resp = Exec-Sql($stmt.Trim())
        if ($resp.status.state -ne "SUCCEEDED") {
            Write-Output "$f : FAILED"
            Write-Output ($resp | ConvertTo-Json -Depth 5)
            $ok = $false
            break
        }
    }
    if ($ok) { Write-Output "$f : OK" } else { exit 1 }
}

Write-Output "All Gold scripts executed successfully."
