# TourismPulse — Verify Gold Execution (read-only)
$d = "C:\Users\Kaashvi\AppData\Local\Microsoft\WinGet\Packages\Databricks.DatabricksCLI_Microsoft.Winget.Source_8wekyb3d8bbwe\databricks.exe"
$WH = "699426b61c5cd41b"

function Exec-Sql([string]$sql) {
  $body = @{ warehouse_id=$WH; statement=$sql; wait_timeout="30s"; results_format="JSON_ARRAY" } | ConvertTo-Json -Compress
  $resp = & $d api post "/api/2.0/sql/statements" --json $body --profile TOURISMPULSE | ConvertFrom-Json
  return $resp
}

Write-Output "== UC tables in workspace.gold_layer =="
$resp = & $d api get "/api/2.1/unity-catalog/tables?catalog_name=workspace&schema_name=gold_layer" --profile TOURISMPULSE | ConvertFrom-Json
$tables = @()
if ($resp.tables) { $tables = $resp.tables | ForEach-Object { $_.name } }
$tables | Sort-Object
Write-Output "Table count: $($tables.Count)"

Write-Output ""
Write-Output "== Row counts and schemas =="
foreach ($t in $tables) {
  $full = "workspace.gold_layer.$t"
  $resp = Exec-Sql("SELECT COUNT(*) AS row_count FROM $full")
  if ($resp.status.state -eq "SUCCEEDED" -and $resp.result.data_array) {
    $rowCount = [int]$resp.result.data_array[0][0]
  } else {
    $rowCount = "ERROR: $($resp | ConvertTo-Json -Depth 3)"
  }
  Write-Output "$full : rows=$rowCount"

  $resp = Exec-Sql("SHOW COLUMNS FROM $full")
  if ($resp.status.state -eq "SUCCEEDED" -and $resp.result.data_array) {
    $cols = @()
    foreach ($row in $resp.result.data_array) { $cols += ($row[0], $row[1]) }
    $cols = $cols[0..([Math]::Min(12, $cols.Count-1))]
    Write-Output "  schema(sample): $($cols -join ", ")"
  }
}
