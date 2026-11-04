import streamlit as st
import streamlit.components.v1 as components
import time
import json
import os

def save_state_disk(email):
    if not email:
        return
    safe_id = "".join(c for c in email if c.isalnum())
    filename = f"temp_state_{safe_id}.json"
    data = {
        "user_info": st.session_state.get("user_info", {}),
        "answers": {str(k): v for k, v in st.session_state.get("answers", {}).items()},
        "current_subtest": st.session_state.get("current_subtest", 7),
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
        ⏱️ SISA WAKTU SUBTES 7: <span id="timer_display">--:--</span>
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

def render_subtest_7_fa():
    if "step_sub7" not in st.session_state:
        st.session_state.step_sub7 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub7 == "instruction":
        st.title("📑 Petunjuk Subtes 7")
        st.info("💡 Bacalah petunjuk di bawah ini. **Timer belum berjalan di halaman ini.**")
        st.markdown("""
        ### Aturan Pengerjaan:
        Setiap soal memperlihatkan suatu bentuk tertentu yang terpotong menjadi beberapa bagian. Carilah di antara bentuk pilihan (**a, b, c, d, e**) bentuk yang dapat dibangun dengan menyusun potongan-potongan tersebut tanpa ada kelebihan sudut atau ruang.
        """)

        # Tampilkan Gambar Petunjuk jika tersedia
        for path in ["subtest_7_petunjuk.png", "assets/subtest_7_petunjuk.png", "subtests/subtest_7_petunjuk.png"]:
            if os.path.exists(path):
                st.image(path, caption="Petunjuk & Contoh Subtes 7", use_container_width=True)
                break

        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 7 🚀", type="primary"):
            st.session_state.step_sub7 = "test"
            if "sub7" not in st.session_state.start_times:
                st.session_state.start_times["sub7"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub7 == "test":
        st.title("🧠 Subtes 7")
        
        if "sub7" not in st.session_state.start_times:
            st.session_state.start_times["sub7"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub7"])
        remaining = max(0, 420 - elapsed) # 7 menit

        if remaining <= 0:
            st.warning("⏰ Waktu Subtes 7 telah habis! Pindah otomatis ke Subtes 8...")
            st.session_state.current_subtest = 8
            st.query_params["subtest"] = "8"
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer(remaining)

        # Tampilkan Gambar Soal Utama jika tersedia
        for path in ["subtest_7_soal.png", "assets/subtest_7_soal.png", "subtests/subtest_7_soal.png"]:
            if os.path.exists(path):
                st.image(path, caption="Lembar Soal Subtes 7 (No. 117 - 136)", use_container_width=True)
                break

        st.markdown("### Pilih Jawaban untuk Soal No. 117 – 136:")

        for q_num in range(117, 137):
            curr_val = st.session_state.answers.get(q_num, "a")
            opts = ["a", "b", "c", "d", "e"]
            idx = opts.index(curr_val) if curr_val in opts else 0
            ans = st.radio(
                f"Soal No. {q_num}:",
                options=opts,
                index=idx,
                horizontal=True,
                key=f"sub7_{q_num}"
            )
            st.session_state.answers[q_num] = ans

        save_state_disk(email)

        if st.button("Simpan & Lanjut ke Subtes 8 ➔", type="primary"):
            st.session_state.current_subtest = 8
            st.query_params["subtest"] = "8"
            save_state_disk(email)
            st.rerun()
