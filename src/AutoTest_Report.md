# Automated Functional Testing Report (Black Box)

**Date:** 2025-12-13 23:45:07
**Reference:** 'Aula - Testes de Software.pdf' & 'Tipos de Testes Automatizados.pdf'

## 1. Compliance & Traceability Matrix
This section details how each PDF requirement was mapped to a specific test suite implementation.

| Test Suite | PDF Requirement | Implementation Strategy (How it was covered) | Test Status |
| :--- | :--- | :--- | :--- |
| **AUTH** | **Security Testing (Teste de Segurança)**<br>*Aula - Testes de Software.pdf (Page 7)* | Simulated full OAuth2 flow: Login -> Extract JWT Token -> Access Protected Route. Verifies Authentication and Authorization layers. | -- |
| ↳ SEQ-01 | | Full Sequence Execution | ✅ PASS |
| **CAMINHOES** | **Equivalence Partitioning (Particionamento de Equivalências)**<br>*Aula - Testes de Software.pdf (Page 8)* | Partitioned inputs into Valid Enum members ('ativo') and Invalid members ('vendido'). Verifies strict type checking. | -- |
| ↳ TRK01 | | Active Truck | ❌ FAIL |
| ↳ TRK02 | | Inactive Truck | ❌ FAIL |
| ↳ TRK03 | | Maintenance Truck | ❌ FAIL |
| ↳ TRK04 | | Invalid Enum | ❌ FAIL |
| ↳ TRK05 | | Missing Placa | ❌ FAIL |
| **COMPLEX_MANIFESTO** | **Integration Testing (Teste de Integração)**<br>*Aula - Testes de Software.pdf (Page 4)* | Executed a dependent chain: Localidade -> Navio -> Manifesto -> Container. Verifies Foreign Key integrity and data flow between modules. | -- |
| ↳ SEQ-01 | | Full Sequence Execution | ❌ FAIL |
| **DASHBOARD** | **System Testing (Teste de Sistema)**<br>*Aula - Testes de Software.pdf (Page 4)* | State-based testing. Modified system state (Add Truck) and verified global KPI counter incremented from 0 to 1. | -- |
| ↳ SEQ-01 | | Full Sequence Execution | ❌ FAIL |
| **NAVIOS** | **Boundary Value Analysis (Análise de Valores Limites)**<br>*Aula - Testes de Software.pdf (Page 9)* | Tested boundary '0' (Valid) and '-100' (Invalid). Verifies system behavior at edges of the Integer domain. | -- |
| ↳ NAV01 | | Valid Creation | ✅ PASS |
| ↳ NAV02 | | Negative Capacity (Invalid) | ❌ FAIL |
| ↳ NAV03 | | Zero Capacity (Boundary) | ✅ PASS |
| ↳ NAV04 | | SQL Injection Name | ✅ PASS |
| ↳ NAV05 | | Missing Name | ❌ FAIL |

## 2. Summary of Failures
* **CAMINHOES / TRK01**: Active Truck - *status_code: Expected 200, Got 500*
* **CAMINHOES / TRK02**: Inactive Truck - *status_code: Expected 200, Got 500*
* **CAMINHOES / TRK03**: Maintenance Truck - *status_code: Expected 200, Got 500*
* **CAMINHOES / TRK04**: Invalid Enum - *status_code: Expected 422, Got 500*
* **CAMINHOES / TRK05**: Missing Placa - *status_code: Expected 422, Got 500*
* **COMPLEX_MANIFESTO / SEQ-01**: Full Sequence Execution - *status_code: Expected 200, Got 422*
* **DASHBOARD / SEQ-01**: Full Sequence Execution - *json_field: Expected 1, Got 0*
* **NAVIOS / NAV02**: Negative Capacity (Invalid) - *status_code: Expected 422, Got 200*
* **NAVIOS / NAV05**: Missing Name - *status_code: Expected 422, Got 200*
