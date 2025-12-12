# Example: How to update an organization

# Step 1: Login to get token
$loginBody = @{
    email = "admin@test.com"
    password = "your-password"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/admin/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $loginBody

# Step 2: Extract token
$token = $loginResponse.access_token
Write-Host "Token received: $($token.Substring(0, 20))..."

# Step 3: Update organization with token
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$updateBody = @{
    organization_name = "Your Current Org Name"  # Must match your current org name
    email = "newemail@test.com"
    password = "newpassword123"
    new_organization_name = "New Org Name"  # Optional - only if renaming
} | ConvertTo-Json

$updateResponse = Invoke-RestMethod -Uri "http://localhost:8000/org/update" `
    -Method PUT `
    -Headers $headers `
    -Body $updateBody

Write-Host "Organization updated successfully!"
Write-Host "New organization name: $($updateResponse.organization_name)"
Write-Host "New email: $($updateResponse.admin_email)"
