param(
    [Parameter(Mandatory = $true)][string]$Domain,
    [string]$Owner  = 'wangshunlin45',
    [string]$Repo   = 'learning-tech-tree',
    [string]$Branch = 'main'
)

# Bind a custom domain to GitHub Pages through the REST API (no git push needed).
# Prereq in Aliyun DNS: CNAME  <sub>  ->  wangshunlin45.github.io

$ErrorActionPreference = 'Stop'
$Domain = $Domain.Trim().ToLowerInvariant()
$env:HTTPS_PROXY = 'http://127.0.0.1:7897'

function Get-GitHubToken {
    if ($env:GITHUB_TOKEN) { return $env:GITHUB_TOKEN }
    $code = @'
using System;
using System.Runtime.InteropServices;
public class Cred3 {
  [DllImport("advapi32.dll", SetLastError=true, CharSet=CharSet.Unicode)]
  public static extern bool CredRead(string target, int type, int flags, out IntPtr credential);
  [StructLayout(LayoutKind.Sequential, CharSet=CharSet.Unicode)]
  public struct CREDENTIAL {
    public int Flags; public int Type; public string TargetName; public string Comment;
    public System.Runtime.InteropServices.ComTypes.FILETIME LastWritten;
    public int CredentialBlobSize; public IntPtr CredentialBlob;
    public int Persist; public int AttributeCount; public IntPtr Attributes;
    public string TargetAlias; public string UserName;
  }
  public static string Get(string target){
    IntPtr p;
    if(!CredRead(target,1,0,out p)) return null;
    CREDENTIAL c = (CREDENTIAL)Marshal.PtrToStructure(p, typeof(CREDENTIAL));
    return c.CredentialBlobSize>0 ? Marshal.PtrToStringUni(c.CredentialBlob, c.CredentialBlobSize/2) : null;
  }
}
'@
    Add-Type -TypeDefinition $code
    return [Cred3]::Get('git:https://github.com')
}

$token = Get-GitHubToken
if (-not $token) { throw 'No GitHub token available (set $env:GITHUB_TOKEN)' }
$headers = @{ Authorization = "token $token"; 'User-Agent' = 'codex'; Accept = 'application/vnd.github+json' }
$api = "https://api.github.com/repos/$Owner/$Repo"

Write-Host '[1/4] write CNAME file into repo'
$sha = $null
try { $sha = (Invoke-RestMethod -Uri "$api/contents/CNAME" -Headers $headers).sha } catch { }
$body = @{ message = "chore: bind custom domain $Domain"; content = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($Domain)); branch = $Branch }
if ($sha) { $body.sha = $sha }
Invoke-RestMethod -Method Put -Uri "$api/contents/CNAME" -Headers $headers -Body ($body | ConvertTo-Json) -ContentType 'application/json' | Out-Null

Write-Host '[2/4] tell Pages the custom domain'
Invoke-RestMethod -Method Put -Uri "$api/pages" -Headers $headers -Body (@{ cname = $Domain; source = @{ branch = $Branch; path = '/' } } | ConvertTo-Json) -ContentType 'application/json' | Out-Null

Write-Host '[3/4] DNS check'
$ok = $false
foreach ($i in 1..12) {
    try {
        $r = Resolve-DnsName -Name $Domain -Type CNAME -ErrorAction Stop
        $target = ($r | Where-Object { $_.NameHost } | Select-Object -First 1).NameHost
        Write-Host ("  {0} -> {1}" -f $Domain, $target)
        if ($target -like '*github.io*') { $ok = $true; break }
    } catch { Write-Host "  pending ($i)" }
    Start-Sleep -Seconds 10
}

Write-Host '[4/4] result'
if ($ok) {
    Write-Host "OK. Certificate is issued within 1-15 min; then enable Enforce HTTPS."
    Write-Host "Site: https://$Domain/"
} else {
    Write-Host "CNAME not visible yet. Aliyun record must be: CNAME $Domain -> wangshunlin45.github.io"
}
