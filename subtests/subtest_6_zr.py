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
        "current_subtest": st.session_state.get("current_subtest", 6),
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
        ⏱️ SISA WAKTU SUBTES 6: <span id="timer_display">--:--</span>
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

def render_subtest_6_zr():
    if "step_sub6" not in st.session_state:
        st.session_state.step_sub6 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub6 == "instruction":
        st.title("📑 Petunjuk Subtes 6")
        st.info("💡 Bacalah petunjuk di bawah ini. **Timer belum berjalan di halaman ini.**")
        st.markdown("""
        ### Aturan Pengerjaan:
        Pada persoalan berikut akan diberikan deret angka [7]. Setiap deret tersusun menurut suatu aturan tertentu dan dapat dilanjutkan menurut aturan itu [7]. Carilah angka berikutnya untuk setiap deret [7].

        ---
        ### Contoh 06:
        **2 4 6 8 10 12 14 ?** [7]  
        *Penjelasan:* Angka berikutnya didapat jika angka di depannya ditambah 2 [7]. Jawabannya ialah **16** [7].

        ---
        ### Contoh Berikutnya:
        **9 7 10 8 11 9 12 ?** [8]  
        *Penjelasan:* Aturannya dikurangi 2 lalu ditambah 3 [8]. Jawabannya ialah **10** [8].
        """)
        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 6 🚀", type="primary"):
            st.session_state.step_sub6 = "test"
            if "sub6" not in st.session_state.start_times:
                st.session_state.start_times["sub6"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub6 == "test":
        st.title("🧠 Subtes 6")
        
        if "sub6" not in st.session_state.start_times:
            st.session_state.start_times["sub6"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub6"])
        remaining = max(0, 600 - elapsed) # 10 menit

        if remaining <= 0:
            st.warning("⏰ Waktu Subtes 6 telah habis! Menyelesaikan seluruh tes...")
            st.session_state.current_subtest = 7
            st.query_params["subtest"] = "7"
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer(remaining)

        questions = [
            {"id": 97, "no": "97", "series": "6 9 12 15 18 21 24 ?"},
            {"id": 98, "no": "98", "series": "15 16 18 19 21 22 24 ?"},
            {"id": 99, "no": "99", "series": "19 18 22 21 25 24 28 ?"},
            {"id": 100, "no": "100", "series": "16 12 17 13 18 14 19 ?"},
            {"id": 101, "no": "101", "series": "2 4 8 10 20 22 44 ?"},
            {"id": 102, "no": "102", "series": "15 13 16 12 17 11 18 ?"},
            {"id": 103, "no": "103", "series": "25 22 11 33 30 15 45 ?"},
            {"id": 104, "no": "104", "series": "49 51 54 27 9 11 14 ?"},
            {"id": 105, "no": "105", "series": "2 3 1 3 4 2 4 ?"},
            {"id": 106, "no": "106", "series": "19 17 20 16 21 15 22 ?"},
            {"id": 107, "no": "107", "series": "94 92 46 44 22 20 10 ?"},
            {"id": 108, "no": "108", "series": "5 8 9 8 11 12 11 ?"},
            {"id": 109, "no": "109", "series": "12 15 19 23 28 33 39 ?"},
            {"id": 110, "no": "110", "series": "7 5 10 7 21 17 68 ?"},
            {"id": 111, "no": "111", "series": "11 15 18 9 13 16 8 ?"},
            {"id": 112, "no": "112", "series": "3 8 15 24 35 48 63 ?"},
            {"id": 113, "no": "113", "series": "4 5 7 4 8 13 7 ?"},
            {"id": 114, "no": "114", "series": "8 5 15 18 6 3 9 ?"},
            {"id": 115, "no": "115", "series": "15 6 18 10 30 23 69 ?"},
            {"id": 116, "no": "116", "series": "5 35 28 4 11 77 70 ?"}
        ]

        for q in questions:
            st.markdown(f"**Soal {q['no']}.** {q['series']}")
            curr_val = st.session_state.answers.get(q['id'], "")
            ans = st.text_input(
                f"Angka Berikutnya No. {q['no']}:",
                value=curr_val,
                key=f"sub6_{q['id']}"
            )
            st.session_state.answers[q['id']] = ans
            st.markdown("---")

        save_state_disk(email)

        if st.button("Simpan & Selesaikan Ujian 🏁", type="primary"):
            st.session_state.current_subtest = 7
            st.query_params["subtest"] = "7"
            save_state_disk(email)
            st.rerun()
