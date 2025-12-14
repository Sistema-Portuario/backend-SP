# Structural Testing Report (White Box)

**Reference:** 'Aula - Testes de Software.pdf' (Pages 10-11)

## Coverage Matrix
| PDF Requirement | Test Scenario | How it was Covered |
| :--- | :--- | :--- |
| Teste de Comandos | Navio Creation | Executed creation lines by sending valid POST request. |
| Teste de Ramos | Navio Read (False/Else branch) | Forced execution of 'if not navio' block by requesting non-existent UUID. |
| Teste de Condições | Login (True OR True) | Tested User Exists AND Password Correct -> Result: Success |
| Teste de Condições | Login (True OR False) | Tested User Exists AND Password Wrong -> Result: Fail |
| Teste de Condições | Login (False OR ...) | Tested User Does Not Exist -> Result: Fail (Short-circuit logic) |
| Teste de Caminhos | Step 1: Create | Executed Path Start (POST) |
| Teste de Caminhos | Step 2: Update | Executed Path Middle (PUT) |
| Teste de Caminhos | Step 3: Delete | Executed Path End (DELETE) |
| Teste de Caminhos | Step 4: Verify | Confirmed data no longer exists (404) to complete path. |


**Note:** See 'pytest --cov' output for exact line-by-line statement coverage %.