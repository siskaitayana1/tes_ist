import streamlit as st
import streamlit.components.v1 as components
import time
import json
import os
from PIL import Image

def find_image(filename):
    target_lower = filename.lower()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    
    search_dirs = [
        root_dir,
        os.path.join(root_dir, "images"),
        os.path.join(root_dir, "subtests"),
        os.path.join(root_dir, "assets"),
        base_dir,
        os.getcwd()
    ]
    
    for folder in search_dirs:
        if os.path.exists(folder):
            try:
                for f in os.listdir(folder):
                    if f.lower() == target_lower:
                        return os.path.join(folder, f)
            except Exception:
                pass
    return None

def show_subtest_image(filename, caption_text):
    img_path = find_image(filename)
    if img_path:
        try:
            img = Image.open(img_path)
            st.image(img, caption=caption_text, use_container_width=True)
        except Exception as e:
            st.error(f"Gagal membuka file gambar `{filename}`: {e}")
    else:
        st.error(f"⚠️ Gambar `{filename}` tidak ditemukan di server.")
        st.info("💡 **Petunjuk:** Pastikan file gambar sudah di-upload ke GitHub (misal di folder `images/` atau folder utama).")

def save_state_disk(email):
    if not email:
        return
    safe_id = "".join(c for c in email if c.isalnum())
    filename = f"temp_state_{safe_id}.json"
    data = {
        "user_info": st.session_state.get("user_info", {}),
        "answers": {str(k): v for k, v in st.session_state.get("answers", {}).items()},
        "current_subtest": st.session_state.get("current_subtest", 8),
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
        ⏱️ SISA WAKTU SUBTES 8: <span id="timer_display">--:--</span>
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

def render_subtest_8_wu():
    if "step_sub8" not in st.session_state:
        st.session_state.step_sub8 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub8 == "instruction":
        st.title("📑 Petunjuk Subtes 8")
        st.info("💡 Bacalah petunjuk di bawah ini. **Timer belum berjalan di halaman ini.**")
        st.markdown("""
        ### Aturan Pengerjaan:
        Ditentukan 5 buah kubus (**a, b, c, d, e**). Setiap soal memperlihatkan salah satu kubus tersebut dalam kedudukan yang diputar atau digulingkan. Carilah kubus yang sesuai untuk setiap soal.
        """)

        # Tampilkan Gambar Petunjuk Subtes 8
        show_subtest_image("subtest_8_petunjuk.png", "Lembar Petunjuk & Contoh Subtes 8")

        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 8 🚀", type="primary"):
            st.session_state.step_sub8 = "test"
            if "sub8" not in st.session_state.start_times:
                st.session_state.start_times["sub8"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub8 == "test":
        st.title("🧠 Subtes 8")
        
        if "sub8" not in st.session_state.start_times:
            st.session_state.start_times["sub8"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub8"])
        remaining = max(0, 540 - elapsed) # 9 menit

        if remaining <= 0:
            st.warning("⏰ Waktu Subtes 8 telah habis! Pindah otomatis ke Subtes 9...")
            st.session_state.current_subtest = 9
            st.query_params["subtest"] = "9"
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer(remaining)

        # Tampilkan Gambar Soal Utama Subtes 8
        show_subtest_image("subtest_8_soal.png", "Lembar Soal Subtes 8 (No. 137 - 156)")

        st.markdown("### Pilih Jawaban untuk Soal No. 137 – 156:")

        for q_num in range(137, 157):
            curr_val = st.session_state.answers.get(q_num, "a")
            opts = ["a", "b", "c", "d", "e"]
            idx = opts.index(curr_val) if curr_val in opts else 0
            ans = st.radio(
                f"Soal No. {q_num}:",
                options=opts,
                index=idx,
                horizontal=True,
                key=f"sub8_{q_num}"
            )
            st.session_state.answers[q_num] = ans

        save_state_disk(email)

        if st.button("Simpan & Lanjut ke Subtes 9 ➔", type="primary"):
            st.session_state.current_subtest = 9
            st.query_params["subtest"] = "9"
            save_state_disk(email)
            st.rerun()
