import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# Impor modul Subtes 1, 2, dan 3
from subtests.subtest_1_se import render_subtest_1_se
from subtests.subtest_2_wa import render_subtest_2_wa
from subtests.subtest_3_an import render_subtest_3_an

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Portal Psikotes IST Bagian 1 - PT Bumi Mas Wahyu",
    page_icon="🧠",
    layout="wide"
)

RESULTS_FILE = "rekap_ist_bagian1.csv"
ADMIN_PASSWORD = "adminbmw"

# --- HELPER DOKUMEN SEMENTARA & TIMESTAMPS ---
def get_temp_filename(email):
    safe_id = "".join(c for c in email if c.isalnum()) if email else "default"
    return f"temp_state_{safe_id}.json"

def save_app_state(email, user_info, answers, subtest, start_times):
    if not email:
        return
    filename = get_temp_filename(email)
    data = {
        "user_info": user_info,
        "answers": {str(k): v for k, v in answers.items()},
        "current_subtest": subtest,
        "start_times": start_times
    }
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass

def load_app_state(email):
    if not email:
        return {}, {}, 1, {}
    filename = get_temp_filename(email)
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                answers = {int(k): v for k, v in data.get("answers", {}).items()}
                return (
                    data.get("user_info", {}),
                    answers,
                    data.get("current_subtest", 1),
                    data.get("start_times", {})
                )
        except Exception:
            pass
    return {}, {}, 1, {}

@st.cache_data(ttl=5)
def load_results_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';')
    return pd.DataFrame()

# --- KUNCI JAWABAN RESMI IST (SUBTES 1 - 3) ---
ANSWER_KEYS_MC = {
    # Subtes 1 (SE)
    1: "e) kewibawaan", 2: "c) boros", 3: "d) gempa bumi", 4: "d) khianat", 5: "d) kuku",
    6: "b) biasanya", 7: "c) lemak", 8: "a) lawan", 9: "e) hipotesis", 10: "b) sol",
    11: "c) kotak PPPK", 12: "d) 20", 13: "d) konservatif", 14: "e) selalu", 15: "c) 800",
    16: "a) kekuatan", 17: "b) biasanya", 18: "b) Bandung", 19: "c) kemungkinan menang", 20: "b) 130",

    # Subtes 2 (WA)
    21: "b) panah", 22: "b) memaki", 23: "d) isi", 24: "c) melepaskan", 25: "c) perjalanan",
    26: "c) tugas", 27: "c) payung", 28: "d) kasar", 29: "d) sepeda", 30: "a) biola",
    31: "e) lurus", 32: "a) jam", 33: "a) kebijaksanaan", 34: "b) berjalan", 35: "c) potret",
    36: "a) panjang", 37: "d) gunting", 38: "e) masyarakat", 39: "b) menasehati", 40: "c) bulu",

    # Subtes 3 (AN)
    41: "c) melupakan", 42: "e) sangkar", 43: "d) jalan raya", 44: "d) gelang", 45: "d) kubus",
    46: "a) menawarkan", 47: "d) tengik", 48: "b) sungai", 49: "e) pelindung", 50: "d) tukang emas",
    51: "c) nada", 52: "c) kelakar", 53: "c) suasana hati", 54: "c) sutra", 55: "d) panjang senar",
    56: "c) mutasi", 57: "c) es", 58: "d) dikikir", 59: "e) mikroskop", 60: "e) lautan api"
}

def calculate_scores():
    user_answers = st.session_state.get("answers", {})
    score_se = sum(1 for q_id in range(1, 21) if user_answers.get(q_id) == ANSWER_KEYS_MC.get(q_id))
    score_wa = sum(1 for q_id in range(21, 41) if user_answers.get(q_id) == ANSWER_KEYS_MC.get(q_id))
    score_an = sum(1 for q_id in range(41, 61) if user_answers.get(q_id) == ANSWER_KEYS_MC.get(q_id))
    
    total_raw = score_se + score_wa + score_an
    return {
        "Subtes_1_SE": score_se,
        "Subtes_2_WA": score_wa,
        "Subtes_3_AN": score_an,
        "Total_Raw_Score_Bagian1": total_raw
    }

# --- SINKRONISASI SESSION & QUERY PARAMS ---
params = st.query_params
param_email = params.get("email", "")

if "page" not in st.session_state:
    st.session_state.page = params.get("page", "register")
if "current_subtest" not in st.session_state:
    st.session_state.current_subtest = int(params.get("subtest", "1"))
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "start_times" not in st.session_state:
    st.session_state.start_times = {}
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "saved" not in st.session_state:
    st.session_state.saved = False

if param_email:
    u_info, u_ans, u_sub, u_times = load_app_state(param_email)
    if u_info:
        st.session_state.user_info.update(u_info)
    if u_ans:
        st.session_state.answers.update(u_ans)
    if u_times:
        st.session_state.start_times.update(u_times)

mode = st.sidebar.radio("Pilih Akses:", ["Portal Tes Pelamar", "Dashboard Admin HRD"])

if mode == "Portal Tes Pelamar":
    if st.session_state.page == "register":
        st.title("🏛️ PT Bumi Mas Wahyu")
        st.subheader("Portal Psikotes Online - IST Bagian 1 (Subtes 1 - 3)")
        st.info("Mohon isi data diri Anda dengan lengkap sebelum memulai ujian.")

        with st.form("form_registrasi_awal"):
            nama = st.text_input("Nama Lengkap:")
            email = st.text_input("Alamat Email:")
            no_hp = st.text_input("Nomor WhatsApp / HP:")
            posisi = st.text_input("Posisi yang Dilamar:", placeholder="Contoh: Staff Closing / Admin HR")

            btn_start = st.form_submit_button("Mulai Tes IST Bagian 1 🚀", type="primary")

            if btn_start:
                if not nama or not email or not no_hp or not posisi:
                    st.error("⚠️ Mohon isi seluruh data diri secara lengkap!")
                else:
                    st.session_state.user_info = {
                        "nama": nama,
                        "email": email,
                        "no_hp": no_hp,
                        "posisi": posisi,
                        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.page = "test"
                    st.session_state.current_subtest = 1
                    st.query_params["page"] = "test"
                    st.query_params["subtest"] = "1"
                    st.query_params["email"] = email
                    
                    save_app_state(email, st.session_state.user_info, st.session_state.answers, 1, st.session_state.start_times)
                    st.rerun()

    elif st.session_state.page == "test":
        st.caption(
            f"👤 Kandidat: **{st.session_state.user_info.get('nama', '')}** | "
            f"💼 Posisi: **{st.session_state.user_info.get('posisi', '')}**"
        )
        st.markdown("---")

        curr_sub = st.session_state.current_subtest
        if curr_sub == 1:
            render_subtest_1_se()
        elif curr_sub == 2:
            render_subtest_2_wa()
        elif curr_sub == 3:
            render_subtest_3_an()
        elif curr_sub >= 4:
            st.session_state.page = "result"
            st.query_params["page"] = "result"
            st.rerun()

    elif st.session_state.page == "result":
        st.title("✅ Psikotes IST Bagian 1 Selesai")
        st.success(f"Terima kasih **{st.session_state.user_info.get('nama', '')}**, jawaban Bagian 1 Anda telah disimpan.")

        if not st.session_state.saved:
            scores = calculate_scores()
            record = {**st.session_state.user_info, **scores}
            df_new = pd.DataFrame([record])

            if os.path.exists(RESULTS_FILE):
                df_old = pd.read_csv(RESULTS_FILE, sep=';')
                df_final = pd.concat([df_old, df_new], ignore_index=True)
            else:
                df_final = df_new

            df_final.to_csv(RESULTS_FILE, index=False, sep=';', encoding='utf-8-sig')
            st.session_state.saved = True
            st.cache_data.clear()

        st.info("Data hasil ujian Bagian 1 telah disinkronkan langsung ke Dashboard HRD.")

        st.markdown("---")
        # Tombol reset untuk membersihkan query URL & session state
        if st.button("🔄 Selesai & Kembali ke Halaman Registrasi Awal", type="primary"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()

elif mode == "Dashboard Admin HRD":
    st.title("🔐 Dashboard Rekrutmen HRD (Bagian 1) - PT Bumi Mas Wahyu")
    if not st.session_state.admin_logged_in:
        pwd = st.text_input("Masukkan Kata Sandi Admin HRD:", type="password")
        if st.button("Login HRD"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Kata sandi salah!")
    else:
        st.sidebar.button("Logout Admin", on_click=lambda: st.session_state.update({"admin_logged_in": False}))
        df_results = load_results_data(RESULTS_FILE)

        if df_results.empty:
            st.warning("Belum ada data kandidat yang menyelesaikan Bagian 1.")
        else:
            st.metric("Total Kandidat Tes", len(df_results))
            st.dataframe(df_results, use_container_width=True)
            csv_data = df_results.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button("📥 Unduh Rekap CSV", csv_data, f"rekap_ist_bagian1_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
