import streamlit as st
import streamlit.components.v1 as components
import time
import json

def save_state_disk(email):
    if not email:
        return
    safe_id = "".join(c for c in email if c.isalnum())
    filename = f"temp_state_{safe_id}.json"
    data = {
        "user_info": st.session_state.get("user_info", {}),
        "answers": {str(k): v for k, v in st.session_state.get("answers", {}).items()},
        "current_subtest": st.session_state.get("current_subtest", 2),
        "start_times": st.session_state.get("start_times", {})
    }
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass

def show_live_timer(seconds_remaining):
    components.html(f"""
    <div style="font-family: Arial, sans-serif; font-size: 20px; font-weight: bold; color: #d9534f; 
                background-color: #fdf7f7; padding: 10px 15px; border: 2px solid #d9534f; 
                border-radius: 8px; text-align: center; margin-bottom: 10px;">
        ⏱️ SISA WAKTU SUBTES 2: <span id="timer_display">--:--</span>
    </div>
    <script>
        var timeLeft = {seconds_remaining};
        function updateDisplay() {{
            var m = Math.floor(timeLeft / 60);
            var s = timeLeft % 60;
            var displayM = m < 10 ? "0" + m : m;
            var displayS = s < 10 ? "0" + s : s;
            var elem = document.getElementById("timer_display");
            if (elem) {{ elem.innerHTML = displayM + ":" + displayS; }}
            if (timeLeft <= 0) {{ 
                if (elem) elem.innerHTML = "00:00 (WAKTU HABIS)"; 
                setTimeout(function() {{ window.top.location.reload(); }}, 500);
            }} else {{ 
                timeLeft--; 
            }}
        }}
        updateDisplay();
        setInterval(updateDisplay, 1000);
    </script>
    """, height=75)

def render_subtest_2_wa():
    if "step_sub2" not in st.session_state:
        st.session_state.step_sub2 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub2 == "instruction":
        st.title("📑 Petunjuk Subtes 2")
        st.info("💡 Bacalah petunjuk di bawah ini. **Timer belum berjalan di halaman ini.**")
        st.markdown("""
        ### Aturan Pengerjaan:
        Ditentukan 5 kata. Pada 4 dari 5 kata itu terdapat suatu kesamaan. Carilah kata yang kelima yang **tidak memiliki kesamaan**.

        ---
        ### Contoh 02:
        a) meja | b) kursi | c) burung | d) lemari | e) tempat tidur  
        *Penjelasan:* Jawaban yang benar adalah **c) burung**.

        ---
        ### Contoh Berikutnya:
        a) duduk | b) berbaring | c) berdiri | d) berjalan | e) berjongkok  
        *Penjelasan:* Jawaban yang benar ialah **d) berjalan**.
        """)
        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 2 🚀", type="primary"):
            st.session_state.step_sub2 = "test"
            if "sub2" not in st.session_state.start_times:
                st.session_state.start_times["sub2"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub2 == "test":
        st.title("🧠 Subtes 2")
        
        if "sub2" not in st.session_state.start_times:
            st.session_state.start_times["sub2"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub2"])
        remaining = max(0, 360 - elapsed) # 6 menit

        if remaining <= 0:
            st.warning("⏰ Waktu Subtes 2 telah habis! Pindah otomatis ke Subtes 3...")
            st.session_state.current_subtest = 3
            st.query_params["subtest"] = "3"
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer(remaining)

        questions = [
            {"id": 21, "no": "21", "opts": ["a) lingkungan", "b) panah", "c) elips", "d) busur", "e) lengkungan"]},
            {"id": 22, "no": "22", "opts": ["a) mengetuk", "b) memaki", "c) menjahit", "d) menggergaji", "e) memukul"]},
            {"id": 23, "no": "23", "opts": ["a) lebar", "b) keliling", "c) luas", "d) isi", "e) panjang"]},
            {"id": 24, "no": "24", "opts": ["a) mengikat", "b) menyatukan", "c) melepaskan", "d) mengaitkan", "e) melekatkan"]},
            {"id": 25, "no": "25", "opts": ["a) arah", "b) timur", "c) perjalanan", "d) tujuan", "e) selatan"]},
            {"id": 26, "no": "26", "opts": ["a) jarak", "b) perpisahan", "c) tugas", "d) batas", "e) perceraian"]},
            {"id": 27, "no": "27", "opts": ["a) saringan", "b) kelambu", "c) payung", "d) tapisan", "e) jala"]},
            {"id": 28, "no": "28", "opts": ["a) putih", "b) pucat", "c) buram", "d) kasar", "e) berkilauan"]},
            {"id": 29, "no": "29", "opts": ["a) otobis", "b) pesawat terbang", "c) sepeda motor", "d) sepeda", "e) kapal api"]},
            {"id": 30, "no": "30", "opts": ["a) biola", "b) seruling", "c) klarinet", "d) terompet", "e) saxophon"]},
            {"id": 31, "no": "31", "opts": ["a) bergelombang", "b) kasar", "c) berduri", "d) licin", "e) lurus"]},
            {"id": 32, "no": "32", "opts": ["a) jam", "b) kompas", "c) penunjuk jalan", "d) bintang pari", "e) arah"]},
            {"id": 33, "no": "33", "opts": ["a) kebijaksanaan", "b) pendidikan", "c) perencanaan", "d) penempatan", "e) pengerahan"]},
            {"id": 34, "no": "34", "opts": ["a) bermotor", "b) berjalan", "c) berlayar", "d) bersepeda", "e) berkuda"]},
            {"id": 35, "no": "35", "opts": ["a) gambar", "b) lukisan", "c) potret", "d) patung", "e) ukiran"]},
            {"id": 36, "no": "36", "opts": ["a) panjang", "b) lonjong", "c) runcing", "d) bulat", "e) bersudut"]},
            {"id": 37, "no": "37", "opts": ["a) kunci", "b) palang pintu", "c) gerendel", "d) gunting", "e) obeng"]},
            {"id": 38, "no": "38", "opts": ["a) jembatan", "b) batas", "c) perkawinan", "d) pagar", "e) masyarakat"]},
            {"id": 39, "no": "39", "opts": ["a) mengetam", "b) menasehati", "c) mengasah", "d) melicinkan", "e) menggosok"]},
            {"id": 40, "no": "40", "opts": ["a) batu", "b) baja", "c) bulu", "d) karet", "e) kayu"]}
        ]

        for q in questions:
            st.markdown(f"**Soal {q['no']}.** Pilih kata yang paling berbeda:")
            ans = st.radio(
                f"Pilihan Jawaban No. {q['no']}:",
                options=q['opts'],
                key=f"sub2_{q['id']}"
            )
            st.session_state.answers[q['id']] = ans
            st.markdown("---")

        save_state_disk(email)

        if st.button("Simpan & Lanjut ke Subtes 3 ➔", type="primary"):
            st.session_state.current_subtest = 3
            st.query_params["subtest"] = "3"
            save_state_disk(email)
            st.rerun()
