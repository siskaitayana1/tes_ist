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
        "current_subtest": st.session_state.get("current_subtest", 4),
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
        ⏱️ SISA WAKTU SUBTES 4: <span id="timer_display">--:--</span>
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

def render_subtest_4_ge():
    if "step_sub4" not in st.session_state:
        st.session_state.step_sub4 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub4 == "instruction":
        st.title("📑 Petunjuk Subtes 4")
        st.info("💡 Bacalah petunjuk di bawah ini. **Timer belum berjalan di halaman ini.**")
        st.markdown("""
        ### Aturan Pengerjaan:
        Ditentukan dua kata [3]. Carilah satu perkataan yang meliputi pengertian kedua kata tadi [3]. Tulislah perkataan itu pada kolom jawaban [3].

        ---
        ### Contoh 04:
        **Ayam – itik** [3]  
        *Penjelasan:* Perkataan "burung" dapat meliputi pengertian kedua kata itu [3]. Jawabannya ialah **burung** [3].

        ---
        ### Contoh Berikutnya:
        **Gaun – celana** [4]  
        *Penjelasan:* Jawabannya ialah **pakaian** [4].
        """)
        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 4 🚀", type="primary"):
            st.session_state.step_sub4 = "test"
            if "sub4" not in st.session_state.start_times:
                st.session_state.start_times["sub4"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub4 == "test":
        st.title("🧠 Subtes 4")
        
        if "sub4" not in st.session_state.start_times:
            st.session_state.start_times["sub4"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub4"])
        remaining = max(0, 480 - elapsed) # 8 menit

        if remaining <= 0:
            st.warning("⏰ Waktu Subtes 4 telah habis! Pindah otomatis ke Subtes 5...")
            st.session_state.current_subtest = 5
            st.query_params["subtest"] = "5"
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer(remaining)

        questions = [
            {"id": 61, "no": "61", "pair": "mawar – melati"},
            {"id": 62, "no": "62", "pair": "mata – telinga"},
            {"id": 63, "no": "63", "pair": "gula – intan"},
            {"id": 64, "no": "64", "pair": "hujan – salju"},
            {"id": 65, "no": "65", "pair": "pengantar surat – telepon"},
            {"id": 66, "no": "66", "pair": "kamera – kacamata"},
            {"id": 67, "no": "67", "pair": "lambung – usus"},
            {"id": 68, "no": "68", "pair": "banyak – sedikit"},
            {"id": 69, "no": "69", "pair": "telur – benih"},
            {"id": 70, "no": "70", "pair": "bendera – lencana"},
            {"id": 71, "no": "71", "pair": "rumput – gajah"},
            {"id": 72, "no": "72", "pair": "ember – kantong"},
            {"id": 73, "no": "73", "pair": "awal – akhir"},
            {"id": 74, "no": "74", "pair": "kikir – boros"},
            {"id": 75, "no": "75", "pair": "penawaran – permintaan"},
            {"id": 76, "no": "76", "pair": "atas – bawah"}
        ]

        for q in questions:
            st.markdown(f"**Soal {q['no']}.** {q['pair']}")
            curr_val = st.session_state.answers.get(q['id'], "")
            ans = st.text_input(
                f"Tuliskan satu kata persamaannya No. {q['no']}:",
                value=curr_val,
                key=f"sub4_{q['id']}"
            )
            st.session_state.answers[q['id']] = ans
            st.markdown("---")

        save_state_disk(email)

        if st.button("Simpan & Lanjut ke Subtes 5 ➔", type="primary"):
            st.session_state.current_subtest = 5
            st.query_params["subtest"] = "5"
            save_state_disk(email)
            st.rerun()
