# setup-port-forwarding.ps1
# Execute como Administrador no PowerShell do Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Port Forwarding WSL 2 - Sistema PMNP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obter IP do WSL automaticamente
$wslIP = (wsl hostname -I).Trim()

Write-Host "IP do WSL detectado: $wslIP" -ForegroundColor Green
Write-Host ""

# Adicionar port forwarding
Write-Host "Configurando port forwarding..." -ForegroundColor Yellow

netsh interface portproxy add v4tov4 listenport=8501 listenaddress=0.0.0.0 connectport=8501 connectaddress=$wslIP
netsh interface portproxy add v4tov4 listenport=5678 listenaddress=0.0.0.0 connectport=5678 connectaddress=$wslIP

Write-Host "✓ Port forwarding configurado!" -ForegroundColor Green
Write-Host ""

# Liberar firewall
Write-Host "Configurando firewall..." -ForegroundColor Yellow

New-NetFirewallRule -DisplayName "WSL Streamlit" -Direction Inbound -LocalPort 8501 -Protocol TCP -Action Allow -ErrorAction SilentlyContinue
New-NetFirewallRule -DisplayName "WSL n8n" -Direction Inbound -LocalPort 5678 -Protocol TCP -Action Allow -ErrorAction SilentlyContinue

Write-Host "✓ Firewall configurado!" -ForegroundColor Green
Write-Host ""

# Mostrar regras ativas
Write-Host "Regras de port forwarding ativas:" -ForegroundColor Cyan
netsh interface portproxy show all

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Configuração concluída!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Acesse de outros computadores:" -ForegroundColor Yellow
Write-Host "  Streamlit: http://SEU_IP_WINDOWS:8501" -ForegroundColor White
Write-Host "  n8n:       http://SEU_IP_WINDOWS:5678" -ForegroundColor White
Write-Host ""
Write-Host "Para descobrir seu IP do Windows:" -ForegroundColor Yellow
Write-Host "  ipconfig" -ForegroundColor White
Write-Host ""
