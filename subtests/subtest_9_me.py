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
        "current_subtest": st.session_state.get("current_subtest", 9),
        "start_times": st.session_state.get("start_times", {})
    }
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass

def show_live_timer_memorize(seconds_remaining):
    components.html(f"""
    <div style="font-family: Arial, sans-serif; font-size: 20px; font-weight: bold; color: #1e40af; 
                background-color: #eff6ff; padding: 12px 15px; border: 2px solid #2563eb; 
                border-radius: 8px; text-align: center; margin-bottom: 10px;">
        ⏱️ SISA WAKTU MENGHAFAL KATA: <span id="timer_mem">--:--</span>
    </div>
    <script>
        var timeLeft = {seconds_remaining};
        function updateDisplay() {{
            var m = Math.floor(timeLeft / 60);
            var s = timeLeft % 60;
            var displayM = m < 10 ? "0" + m : m;
            var displayS = s < 10 ? "0" + s : s;
            var elem = document.getElementById("timer_mem");
            if (elem) {{ elem.innerHTML = displayM + ":" + displayS; }}
            if (timeLeft <= 0) {{ 
                if (elem) elem.innerHTML = "00:00 (WAKTU MENGHAFAL HABIS)"; 
                setTimeout(function() {{ window.top.location.reload(); }}, 500);
            }} else {{ 
                timeLeft--; 
            }}
        }}
        updateDisplay();
        setInterval(updateDisplay, 1000);
    </script>
    """, height=80)

def show_live_timer_test(seconds_remaining):
    components.html(f"""
    <div style="font-family: Arial, sans-serif; font-size: 20px; font-weight: bold; color: #dc2626; 
                background-color: #fef2f2; padding: 10px 15px; border: 2px solid #dc2626; 
                border-radius: 8px; text-align: center; margin-bottom: 10px;">
        ⏱️ SISA WAKTU SOAL SUBTES 9: <span id="timer_test">--:--</span>
    </div>
    <script>
        var timeLeft = {seconds_remaining};
        function updateDisplay() {{
            var m = Math.floor(timeLeft / 60);
            var s = timeLeft % 60;
            var displayM = m < 10 ? "0" + m : m;
            var displayS = s < 10 ? "0" + s : s;
            var elem = document.getElementById("timer_test");
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

def render_subtest_9_me():
    if "step_sub9" not in st.session_state:
        st.session_state.step_sub9 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub9 == "instruction":
        st.title("📑 Petunjuk Subtes 9 (Mengingat Kata)")
        st.info("💡 Bacalah petunjuk di bawah ini sebelum memulai **tahap mengingat (3 menit)**.")
        st.markdown("""
        ### Aturan Pengerjaan:
        Pada subtes ini, Anda akan diberikan daftar kata yang dikelompokkan dalam 5 kategori (**Bunga, Perkakas, Burung, Kesenian, Binatang**).
        
        1. Anda diberi waktu tepat **3 MENIT** untuk **menghafal** kata-kata tersebut.
        2. Setelah waktu menghafal habis, daftar kata akan ditutup dan Anda akan menjawab 20 soal selama **6 MENIT** berdasarkan kata yang telah dihafal.
        """)
        st.markdown("---")
        if st.button("Mulai Tahap Menghafal (3 Menit) 🚀", type="primary"):
            st.session_state.step_sub9 = "memorize"
            if "sub9_mem" not in st.session_state.start_times:
                st.session_state.start_times["sub9_mem"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub9 == "memorize":
        st.title("📌 Tahap Menghafal Kata (3 Menit)")
        
        if "sub9_mem" not in st.session_state.start_times:
            st.session_state.start_times["sub9_mem"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub9_mem"])
        remaining = max(0, 180 - elapsed) # 3 menit (180 detik)

        if remaining <= 0:
            st.warning("⏰ Waktu menghafal 3 menit telah selesai! Mengalihkan ke lembar soal Subtes 9...")
            st.session_state.step_sub9 = "test"
            if "sub9_test" not in st.session_state.start_times:
                st.session_state.start_times["sub9_test"] = time.time()
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer_memorize(remaining)

        st.success("Hafalkan kata-kata di bawah ini secara cermat!")
        
        # Kotak Hafalan dengan Kontras Tinggi & Warna Teks Terkunci Eksplisit
        st.markdown("""
        <div style="background-color: #f8fafc; color: #0f172a; padding: 20px; border-radius: 10px; border: 2px solid #2563eb; font-size: 18px; line-height: 1.8;">
            <p style="color: #0f172a; margin-bottom: 8px;"><b>BUNGA</b> : SOKA, LARAT, FLAMBOYAN, YASMIN, DAHLIA</p>
            <p style="color: #0f172a; margin-bottom: 8px;"><b>PERKAKAS</b> : WAJAN, JARUM, KIKIR, CANGKUL, PALU</p>
            <p style="color: #0f172a; margin-bottom: 8px;"><b>BURUNG</b> : ITIK, ELANG, WALET, TEKUKUR, NURI</p>
            <p style="color: #0f172a; margin-bottom: 8px;"><b>KESENIAN</b> : QUINTET, ARCA, OPERA, UKIRAN, GAMELAN</p>
            <p style="color: #0f172a; margin-bottom: 0px;"><b>BINATANG</b> : RUSA, MUSANG, BERUANG, HARIMAU, ZEBRA</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Sudah Hafal & Lanjut ke Soal ➔", type="primary"):
            st.session_state.step_sub9 = "test"
            if "sub9_test" not in st.session_state.start_times:
                st.session_state.start_times["sub9_test"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub9 == "test":
        st.title("🧠 Subtes 9")
        
        if "sub9_test" not in st.session_state.start_times:
            st.session_state.start_times["sub9_test"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub9_test"])
        remaining = max(0, 360 - elapsed) # 6 menit pengerjaan (360 detik)

        if remaining <= 0:
            st.warning("⏰ Waktu Subtes 9 telah habis! Menyelesaikan seluruh psikotes...")
            st.session_state.current_subtest = 10
            st.query_params["subtest"] = "10"
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer_test(remaining)

        opts = ["a) Bunga", "b) Perkakas", "c) Burung", "d) Kesenian", "e) Binatang"]
        questions = [
            {"id": 157, "no": "157", "letter": "A"},
            {"id": 158, "no": "158", "letter": "B"},
            {"id": 159, "no": "159", "letter": "C"},
            {"id": 160, "no": "160", "letter": "D"},
            {"id": 161, "no": "161", "letter": "E"},
            {"id": 162, "no": "162", "letter": "F"},
            {"id": 163, "no": "163", "letter": "G"},
            {"id": 164, "no": "164", "letter": "H"},
            {"id": 165, "no": "165", "letter": "I"},
            {"id": 166, "no": "166", "letter": "J"},
            {"id": 167, "no": "167", "letter": "K"},
            {"id": 168, "no": "168", "letter": "L"},
            {"id": 169, "no": "169", "letter": "M"},
            {"id": 170, "no": "170", "letter": "N"},
            {"id": 171, "no": "171", "letter": "O"},
            {"id": 172, "no": "172", "letter": "P"},
            {"id": 173, "no": "173", "letter": "R"},
            {"id": 174, "no": "174", "letter": "S"},
            {"id": 175, "no": "175", "letter": "T"},
            {"id": 176, "no": "176", "letter": "U"}
        ]

        for q in questions:
            st.markdown(f"**Soal {q['no']}.** Kata yang mempunyai huruf permulaan – **{q['letter']}** – adalah .......")
            curr_val = st.session_state.answers.get(q['id'], opts)
            idx = opts.index(curr_val) if curr_val in opts else 0
            ans = st.radio(
                f"Pilih Jawaban No. {q['no']}:",
                options=opts,
                index=idx,
                key=f"sub9_{q['id']}"
            )
            st.session_state.answers[q['id']] = ans
            st.markdown("---")

        save_state_disk(email)

        if st.button("Simpan & Selesaikan Psikotes 🏁", type="primary"):
            st.session_state.current_subtest = 10
            st.query_params["subtest"] = "10"
            save_state_disk(email)
            st.rerun()
