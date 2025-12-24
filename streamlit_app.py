import json
import requests
import streamlit as st

API = "http://127.0.0.1:8000"

CSS = """
<style>
[data-testid="stAppViewContainer"]{
 background: #b1b7c0 !important;
}
[data-testid="stHeader"]{
  background: transparent !important;
}
.block-container{
  padding-top: 2rem !important;
  max-width: 920px !important;
}

.title{
  font-size: 40px;
  font-weight: 800;
  color: #111827;
  margin: 0 0 6px 0;
}
.sub{
  color: #374151;
  margin-bottom: 18px;
}

.card{
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 18px 18px 10px 18px;
  box-shadow: 0 10px 24px rgba(0,0,0,0.08);
  margin-bottom: 16px;
}

h2{
  color: #111827 !important;
  margin-top: 0;
}

label, p, span, div{
  color: #111827 !important;
}

[data-testid="stTextInput"] input{
  background: #ffffff !important;
  color: #111827 !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 12px !important;
}

[data-testid="stFileUploader"]{
  background: #ffffff !important;
  border: 1px dashed #cbd5e1 !important;
  border-radius: 14px !important;
  padding: 10px !important;
}

.stButton > button{
  background: #22c55e !important;
  color: #ffffff !important;
  border: 0 !important;
  border-radius: 12px !important;
  font-weight: 800 !important;
  padding: 10px 16px !important;
}
.stButton > button:hover{
  background: #16a34a !important;
}

.tokenBox{
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 10px 12px;
  color: #111827;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  overflow-wrap: anywhere;
}

.small{
  font-size: 13px;
  color: #374151;
  margin-top: 8px;
  margin-bottom: 6px;
}

[data-testid="stNotificationContentInfo"],
[data-testid="stNotificationContentSuccess"],
[data-testid="stNotificationContentError"]{
  color: #111827 !important;
}
</style>
"""

st.set_page_config(page_title="CSV Analysis Tool", page_icon="📊", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

if "token" not in st.session_state:
  st.session_state.token = ""

if "last_result" not in st.session_state:
  st.session_state.last_result = {}

def api_post_query(path: str, params: dict):
  url = f"{API}{path}"
  r = requests.post(url, params=params, timeout=12)
  try:
    data = r.json()
  except Exception:
    data = {"error": "Nije JSON odgovor", "text": r.text}
  return r.status_code, data

def api_upload_csv(file):
  url = f"{API}/upload-csv"
  files = {"file": (file.name, file.getvalue(), "text/csv")}
  r = requests.post(url, files=files, timeout=25)
  try:
    data = r.json()
  except Exception:
    data = {"error": "Nije JSON odgovor", "text": r.text}
  return r.status_code, data

st.markdown('<div class="title">CSV Analysis Tool</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub">Backend: {API}</div>', unsafe_allow_html=True)

with st.container():
  st.markdown('<div class="card"><h2>Register</h2>', unsafe_allow_html=True)

  reg_user = st.text_input("Username", key="reg_user", placeholder="npr. adrian")
  reg_pass = st.text_input("Password", key="reg_pass", type="password", placeholder="••••••••")

  reg_click = st.button("Register", key="btn_register")

  if reg_click:
    if not reg_user.strip() or not reg_pass.strip():
      st.error("Upiši username i password")
    else:
      try:
        code, data = api_post_query("/register", {"username": reg_user.strip(), "password": reg_pass.strip()})
        st.session_state.last_result = {"ok": code < 400, "status": code, "data": data}
        if code < 400:
          st.success("Registrovan ✅")
        else:
          st.error(data.get("detail") or f"Greška ({code})")
      except Exception:
        st.error("Greška: backend ne odgovara")

  st.markdown("</div>", unsafe_allow_html=True)

with st.container():
  st.markdown('<div class="card"><h2>Login</h2>', unsafe_allow_html=True)

  log_user = st.text_input("Username", key="log_user", placeholder="npr. adrian")
  log_pass = st.text_input("Password", key="log_pass", type="password", placeholder="••••••••")

  b1, b2 = st.columns([1, 1])
  with b1:
    login_click = st.button("Login", key="btn_login")
  with b2:
    logout_click = st.button("Logout", key="btn_logout")

  if login_click:
    if not log_user.strip() or not log_pass.strip():
      st.error("Upiši username i password")
    else:
      try:
        code, data = api_post_query("/login", {"username": log_user.strip(), "password": log_pass.strip()})
        st.session_state.last_result = {"ok": code < 400, "status": code, "data": data}
        if code < 400 and data.get("token"):
          st.session_state.token = data["token"]
          st.success("Ulogovan ✅")
        else:
          st.error(data.get("detail") or f"Login greška ({code})")
      except Exception:
        st.error("Greška: backend ne odgovara")

  if logout_click:
    st.session_state.token = ""
    st.success("Logout ✅")

  st.markdown('<div class="small">Token:</div>', unsafe_allow_html=True)
  if st.session_state.token:
    st.markdown(f'<div class="tokenBox">{st.session_state.token}</div>', unsafe_allow_html=True)
  else:
    st.markdown('<div class="tokenBox">nema</div>', unsafe_allow_html=True)

  st.markdown("</div>", unsafe_allow_html=True)

with st.container():
  st.markdown('<div class="card"><h2>Upload CSV + analiza</h2>', unsafe_allow_html=True)

  file = st.file_uploader("Izaberi CSV fajl", type=["csv"])
  upload_click = st.button("Upload & Analyze", key="btn_upload")

  if upload_click:
    if file is None:
      st.error("Izaberi CSV fajl")
    else:
      try:
        code, data = api_upload_csv(file)
        st.session_state.last_result = {"ok": code < 400, "status": code, "data": data}
        if code < 400:
          st.success("Upload + analiza ✅")
        else:
          st.error(data.get("detail") or f"Greška ({code})")
      except Exception:
        st.error("Greška: backend ne odgovara")

  st.markdown("</div>", unsafe_allow_html=True)

with st.container():
  st.markdown('<div class="card"><h2>Rezultat</h2>', unsafe_allow_html=True)
  st.code(json.dumps(st.session_state.last_result, indent=2, ensure_ascii=False), language="json")
  st.markdown("</div>", unsafe_allow_html=True)