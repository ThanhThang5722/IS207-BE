# Reset DB script - drop and recreate public schema inside Postgres container
# WARNING: destructive. This will remove all tables and data in the public schema.

param(
    [string]$Container = "is207-be-db-1",
    [string]$DbName = "fastapi_db",
    [string]$DbUser = "user",
    [switch]$Force
)

if (-not $Force) {
    Write-Host "WARNING: This will DROP and RECREATE the public schema in database '$DbName' on container '$Container'." -ForegroundColor Yellow
    $confirm = Read-Host "Type 'yes' to continue"
    if ($confirm -ne 'yes') {
        Write-Host "Aborted." -ForegroundColor Cyan
        exit 1
    }
}

$sql = @"
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO public;

-- conditionally grant to the configured DB user (if that role exists) and to 'postgres' if present
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$DbUser') THEN
        EXECUTE 'GRANT ALL ON SCHEMA public TO "$DbUser"';
    END IF;

    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'postgres') THEN
        EXECUTE 'GRANT ALL ON SCHEMA public TO postgres';
    END IF;
END
$$;
"@

# Pipe the SQL into psql inside the container
$bytes = [System.Text.Encoding]::UTF8.GetBytes($sql)

$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = 'docker'
$processInfo.Arguments = "exec -i $Container psql -U $DbUser -d $DbName -v ON_ERROR_STOP=1"
$processInfo.RedirectStandardInput = $true
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true
$processInfo.UseShellExecute = $false

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $processInfo
$process.Start() | Out-Null
$process.StandardInput.BaseStream.Write($bytes,0,$bytes.Length)
$process.StandardInput.Close()
$out = $process.StandardOutput.ReadToEnd()
$err = $process.StandardError.ReadToEnd()
$process.WaitForExit()

if ($out) { Write-Host $out }
if ($err) { Write-Host $err -ForegroundColor Red }

if ($process.ExitCode -ne 0) {
    Write-Host "Reset failed with exit code $($process.ExitCode)." -ForegroundColor Red
    exit $process.ExitCode
}

Write-Host "Schema reset complete. You can now re-run your init SQL." -ForegroundColor Green
