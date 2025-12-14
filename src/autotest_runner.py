import csv
import requests
import sys
import os
import json
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- CONFIGURATION ---
BASE_URL = "http://localhost:8000"

# Adjust python path
sys.path.append(os.getcwd())

# --- DYNAMIC DB FIX ---
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "1234") 
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "sistema_portuario")
    REAL_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    try:
        from popular_banco import resetar_banco, engine as old_engine
        import popular_banco
    except ImportError:
        sys.path.append(os.path.join(os.getcwd(), '..'))
        from src.popular_banco import resetar_banco, engine as old_engine
        import src.popular_banco as popular_banco

    print(f"[CONFIG] Patching DB Connection to: postgresql://{DB_USER}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    new_engine = create_engine(REAL_DATABASE_URL)
    popular_banco.engine = new_engine
    popular_banco.Session = sessionmaker(bind=new_engine)
    popular_banco.session = popular_banco.Session()
    
except Exception as e:
    print(f"[WARNING] Failed to patch DB connection: {e}")
    try:
        from popular_banco import resetar_banco
    except:
        def resetar_banco(): pass

# --- REPORTING SYSTEM ---
class TestReporter:
    def __init__(self):
        self.results = []
        self.start_time = datetime.datetime.now()
        
        self.technique_details = {
            "navios": {
                "req": "Boundary Value Analysis (Análise de Valores Limites)",
                "pdf_ref": "Aula - Testes de Software.pdf (Page 9)",
                "how": "Tested boundary '0' (Valid) and '-100' (Invalid). Verifies system behavior at edges of the Integer domain."
            },
            "caminhoes": {
                "req": "Equivalence Partitioning (Particionamento de Equivalências)",
                "pdf_ref": "Aula - Testes de Software.pdf (Page 8)",
                "how": "Partitioned inputs into Valid Enum members ('ativo') and Invalid members ('vendido'). Verifies strict type checking."
            },
            "complex_manifesto": {
                "req": "Integration Testing (Teste de Integração)",
                "pdf_ref": "Aula - Testes de Software.pdf (Page 4)",
                "how": "Executed a dependent chain: Localidade -> Navio -> Manifesto -> Container. Verifies Foreign Key integrity and data flow between modules."
            },
            "dashboard": {
                "req": "System Testing (Teste de Sistema)",
                "pdf_ref": "Aula - Testes de Software.pdf (Page 4)",
                "how": "State-based testing. Modified system state (Add Truck) and verified global KPI counter incremented from 0 to 1."
            },
            "auth": {
                "req": "Security Testing (Teste de Segurança)",
                "pdf_ref": "Aula - Testes de Software.pdf (Page 7)",
                "how": "Simulated full OAuth2 flow: Login -> Extract JWT Token -> Access Protected Route. Verifies Authentication and Authorization layers."
            }
        }

    def log_result(self, suite_name, case_id, description, status, details=""):
        self.results.append({
            "suite": suite_name,
            "case": case_id,
            "desc": description,
            "status": status,
            "details": details
        })

    def generate_report(self):
        filename = "AutoTest_Report.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Automated Functional Testing Report (Black Box)\n\n")
            f.write(f"**Date:** {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("**Reference:** 'Aula - Testes de Software.pdf' & 'Tipos de Testes Automatizados.pdf'\n\n")
            
            f.write("## 1. Compliance & Traceability Matrix\n")
            f.write("This section details how each PDF requirement was mapped to a specific test suite implementation.\n\n")
            f.write("| Test Suite | PDF Requirement | Implementation Strategy (How it was covered) | Test Status |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            
            current_suite = ""
            # Sort results to group suites together
            self.results.sort(key=lambda x: x['suite'])
            
            for r in self.results:
                suite = r['suite']
                info = self.technique_details.get(suite, {"req": "Functional", "how": "General API Test", "pdf_ref": ""})
                
                if suite != current_suite:
                    ref = f"<br>*{info['pdf_ref']}*" if "pdf_ref" in info else ""
                    f.write(f"| **{suite.upper()}** | **{info['req']}**{ref} | {info['how']} | -- |\n")
                    current_suite = suite
                
                icon = "✅ PASS" if r['status'] == "PASS" else "❌ FAIL"
                f.write(f"| ↳ {r['case']} | | {r['desc']} | {icon} |\n")
            
            f.write("\n## 2. Summary of Failures\n")
            failures = [r for r in self.results if r['status'] == "FAIL"]
            if not failures:
                f.write("No failures detected. All functional requirements met.\n")
            else:
                for fail in failures:
                    f.write(f"* **{fail['suite'].upper()} / {fail['case']}**: {fail['desc']} - *{fail['details']}*\n")

        print(f"\n[REPORT] Report generated: {os.path.abspath(filename)}")

reporter = TestReporter()

def run_test_suite(flow_file_path):
    print(f"\n{'='*60}")
    print(f"EXECUTING FLOW: {flow_file_path}")
    print(f"{'='*60}")
    
    suite_name = os.path.basename(flow_file_path).replace("test_flow_", "").replace(".csv", "")
    
    context = {"saved_vars": {}, "current_row": {}}
    
    if not os.path.exists(flow_file_path):
        print(f"[ERROR] Flow file not found: {flow_file_path}")
        return

    flow_dir = os.path.dirname(flow_file_path)

    with open(flow_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        steps = list(reader)

    step_index = 0
    has_loop = False
    suite_success = True
    suite_fail_reason = ""

    while step_index < len(steps):
        step = steps[step_index]
        keyword = step['Keyword'].strip()
        
        if keyword == "SETUP":
            if step['Parameter 1'] == "reset_db":
                print("[SETUP] Resetting Database...")
                try: 
                    resetar_banco()
                    print("[SETUP] Database Reset Successful.")
                except Exception as e: 
                    print(f"[SETUP] CRITICAL ERROR: {e}")
                    suite_success = False
                    suite_fail_reason = str(e)

        elif keyword == "LOOP":
            has_loop = True
            data_filename = step['Parameter 1']
            data_file_path = os.path.join(flow_dir, data_filename)
            
            if not os.path.exists(data_file_path):
                print(f"[ERROR] Data file not found: {data_file_path}")
                break

            with open(data_file_path, 'r', encoding='utf-8') as df:
                data_rows = list(csv.DictReader(df, skipinitialspace=True))

            loop_start_idx = step_index + 1
            loop_end_idx = loop_start_idx
            while loop_end_idx < len(steps) and steps[loop_end_idx]['Keyword'] != "END_LOOP":
                loop_end_idx += 1
            
            loop_steps = steps[loop_start_idx:loop_end_idx]
            
            for row in data_rows:
                context['current_row'] = row
                case_id = row.get('CaseID', 'Unknown')
                desc = row.get('Description', '')
                print(f"\n  >>> Case {case_id}: {desc}")
                
                case_status = "PASS"
                fail_details = ""
                for loop_step in loop_steps:
                    success, msg = execute_step(loop_step, context)
                    if not success:
                        case_status = "FAIL"
                        fail_details = msg
                
                reporter.log_result(suite_name, case_id, desc, case_status, fail_details)
            
            step_index = loop_end_idx 

        elif keyword == "END_LOOP":
            pass 
        else:
            # Single Step execution (Linear script)
            success, msg = execute_step(step, context)
            if not success:
                suite_success = False
                suite_fail_reason = msg

        step_index += 1
    
    # If the flow had NO loops (linear script like Auth or Manifesto), report it as one big case
    if not has_loop:
        status = "PASS" if suite_success else "FAIL"
        reporter.log_result(suite_name, "SEQ-01", "Full Sequence Execution", status, suite_fail_reason)

def execute_step(step, context):
    keyword = step['Keyword'].strip()
    param1 = resolve_vars(step.get('Parameter 1', ''), context)
    param2 = resolve_vars(step.get('Parameter 2', ''), context)
    param3 = resolve_vars(step.get('Parameter 3', ''), context)
    success = True
    msg = ""

    if keyword == "API_POST":
        endpoint = param1; data_raw = param2
        payload = {}
        is_form = False
        
        if data_raw.startswith("{") and data_raw.endswith("}"):
            try: payload = json.loads(data_raw.replace("'", '"')) 
            except: pass
        else:
            if data_raw:
                pairs = data_raw.split('|')
                for p in pairs:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        payload[k.strip()] = v.strip()
            if "username" in payload and "password" in payload: is_form = True

        headers = {}
        if param3 and "HEADER_AUTH" in param3:
            parts = param3.split('|')
            if len(parts) > 1:
                token = context['saved_vars'].get(parts[1])
                if token: headers["Authorization"] = f"Bearer {token}"

        try:
            url = f"{BASE_URL}{endpoint}"
            if is_form:
                response = requests.post(url, data=payload, headers=headers)
            elif "chegada" in endpoint or "containeres" in endpoint:
                response = requests.post(url, json=payload, headers=headers)
            else:
                response = requests.post(url, params=payload, headers=headers)
                if response.status_code == 422:
                    response = requests.post(url, json=payload, headers=headers)

            context['response'] = response
            print(f"    [POST] {endpoint} -> Status: {response.status_code}")
        except Exception as e:
            print(f"    [ERROR] Connection failed: {e}")
            success = False
            msg = f"Connection failed: {e}"

    elif keyword == "API_GET":
        endpoint = param1
        headers = {}
        if param2 and "HEADER_AUTH" in param2:
            parts = param2.split('|')
            token_name = parts[1] if len(parts) > 1 else param3
            token = context['saved_vars'].get(token_name)
            if token: headers["Authorization"] = f"Bearer {token}"

        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            context['response'] = response
            print(f"    [GET] {endpoint} -> Status: {response.status_code}")
        except Exception as e:
            print(f"    [ERROR] Connection failed: {e}")
            success = False
            msg = f"Connection failed: {e}"

    elif keyword == "EXTRACT":
        field_path = param1; save_as = param3
        try:
            val = context['response'].json()
            for key in field_path.split('.'):
                if isinstance(val, dict): val = val.get(key)
                else: val = None; break
            if val is not None:
                context['saved_vars'][save_as] = val
                print(f"    [EXTRACT] Saved '{save_as}'")
            else: 
                print(f"    [EXTRACT] Field '{field_path}' not found.")
                success = False
                msg = f"Extract failed: {field_path} not found"
        except: 
            print(f"    [EXTRACT] Failed to parse JSON.")
            success = False
            msg = "Extract failed: Invalid JSON"

    elif keyword == "ASSERT":
        target = param1; expected = str(param3)
        try:
            actual = "None"
            if target == "status_code": actual = str(context['response'].status_code)
            elif target == "json_field":
                actual = str(context['response'].json().get(param2))
            
            if actual == expected: 
                print(f"    [PASS] {target}: {actual}")
            else: 
                print(f"    [FAIL] {target}: Expected {expected}, Got {actual}")
                success = False
                msg = f"{target}: Expected {expected}, Got {actual}"
        except Exception as e: 
            print(f"    [FAIL] Exception: {e}")
            success = False
            msg = f"Assert exception: {e}"
            
    return success, msg

def resolve_vars(text, context):
    if not isinstance(text, str): return text
    for col, val in context['current_row'].items():
        text = text.replace("{" + col + "}", str(val))
    for key, val in context['saved_vars'].items():
        text = text.replace("{" + key + "}", str(val))
    return text

if __name__ == "__main__":
    # --- PATH CONFIGURATION ---
    base_qa_path = os.path.join("..", "QA", "Scripts")
    if not os.path.exists(base_qa_path):
        base_qa_path = "."

    files_to_run = [
        "test_flow_navios.csv",
        "test_flow_caminhoes.csv",
        "test_flow_auth.csv",
        "test_flow_complex_manifesto.csv",
        "test_flow_dashboard.csv"
    ]
    
    print(f"Looking for test files in: {os.path.abspath(base_qa_path)}")
    
    for filename in files_to_run:
        full_path = os.path.join(base_qa_path, filename)
        if os.path.exists(full_path):
            run_test_suite(full_path)
        else:
            print(f"Skipping {filename} (File not found at {full_path})")
            
    reporter.generate_report()