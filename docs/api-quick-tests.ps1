$base = "http://127.0.0.1:8000"

Write-Host "Health"
Invoke-RestMethod -Method Get -Uri "$base/health" | ConvertTo-Json

Write-Host "Analyze"
$analyzeBody = @{ text = "Could you help me understand what happened?" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$base/analyze" -ContentType "application/json" -Body $analyzeBody | ConvertTo-Json -Depth 5

Write-Host "SSML"
$ssmlBody = @{ text = "This is unbelievable news!" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$base/ssml" -ContentType "application/json" -Body $ssmlBody | ConvertTo-Json -Depth 5

Write-Host "Synthesize metadata"
$synthBody = @{ text = "I understand your frustration, and I am here to help." } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$base/synthesize" -ContentType "application/json" -Body $synthBody | ConvertTo-Json -Depth 5

Write-Host "Synthesize audio"
$audioResp = Invoke-WebRequest -Method Post -Uri "$base/synthesize/audio" -ContentType "application/json" -Body $synthBody -UseBasicParsing
Write-Host "Audio status: $($audioResp.StatusCode)"
Write-Host "Audio bytes:  $($audioResp.RawContentLength)"
