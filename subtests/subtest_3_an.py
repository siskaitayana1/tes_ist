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
        "current_subtest": st.session_state.get("current_subtest", 3),
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
        ⏱️ SISA WAKTU SUBTES 3: <span id="timer_display">--:--</span>
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

def render_subtest_3_an():
    if "step_sub3" not in st.session_state:
        st.session_state.step_sub3 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub3 == "instruction":
        st.title("📑 Petunjuk Subtes 3")
        st.info("💡 Bacalah petunjuk di bawah ini. **Timer belum berjalan di halaman ini.**")
        st.markdown("""
        ### Aturan Pengerjaan:
        Ditentukan 3 (tiga) kata. Carilah kata pilihan yang memiliki hubungan yang sama dengan dua kata awal.

        ---
        ### Contoh 03:
        **Hutan : pohon = tembok : ?**  
        *Penjelasan:* Jawaban yang benar ialah **a) batu bata**.

        ---
        ### Contoh Berikutnya:
        **Gelap : terang = basah : ?**  
        *Penjelasan:* Jawaban yang benar ialah **e) kering**.
        """)
        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 3 🚀", type="primary"):
            st.session_state.step_sub3 = "test"
            if "sub3" not in st.session_state.start_times:
                st.session_state.start_times["sub3"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub3 == "test":
        st.title("🧠 Subtes 3")
        
        if "sub3" not in st.session_state.start_times:
            st.session_state.start_times["sub3"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub3"])
        remaining = max(0, 420 - elapsed) # 7 menit

        if remaining <= 0:
            st.warning("⏰ Waktu Subtes 3 telah habis! Pindah otomatis ke Subtes 4...")
            st.session_state.current_subtest = 4
            st.query_params["subtest"] = "4"
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer(remaining)

        questions = [
            {"id": 41, "no": "41", "q": "Menemukan : menghilangkan = Mengingat : ?", "opts": ["a) menghapal", "b) mengenai", "c) melupakan", "d) berpikir", "e) memimpikan"]},
            {"id": 42, "no": "42", "q": "Bunga : jambangan = Burung : ?", "opts": ["a) sarang", "b) langit", "c) pagar", "d) pohon", "e) sangkar"]},
            {"id": 43, "no": "43", "q": "Kereta api : rel = Otobis : ?", "opts": ["a) roda", "b) poros", "c) ban", "d) jalan raya", "e) kecepatan"]},
            {"id": 44, "no": "44", "q": "Perak : emas = Cincin : ?", "opts": ["a) arloji", "b) berlian", "c) permata", "d) gelang", "e) platina"]},
            {"id": 45, "no": "45", "q": "Lingkaran : bola = Bujur sangkar : ?", "opts": ["a) bentuk", "b) gambar", "c) segi empat", "d) kubus", "e) piramida"]},
            {"id": 46, "no": "46", "q": "Saran : kepustakaan = Merundingkan : ?", "opts": ["a) menawarkan", "b) menentukan", "c) menilai", "d) menimbang", "e) merenungkan"]},
            {"id": 47, "no": "47", "q": "Lidah : asam = Hidung : ?", "opts": ["a) mencium", "b) bernapas", "c) mengecap", "d) tengik", "e) asin"]},
            {"id": 48, "no": "48", "q": "Darah : pembuluh = Air : ?", "opts": ["a) pintu air", "b) sungai", "c) talang", "d) hujan", "e) ember"]},
            {"id": 49, "no": "49", "q": "Saraf : penyalur = Pupil : ?", "opts": ["a) penyinaran", "b) mata", "c) melihat", "d) cahaya", "e) pelindung"]},
            {"id": 50, "no": "50", "q": "Pengantar surat : pengantar telegram = Pandai besi : ?", "opts": ["a) palu godam", "b) pedagang besi", "c) api", "d) tukang emas", "e) besi tempa"]},
            {"id": 51, "no": "51", "q": "Buta : warna = Tuli : ?", "opts": ["a) pendengaran", "b) mendengar", "c) nada", "d) kata", "e) telinga"]},
            {"id": 52, "no": "52", "q": "Makanan : bumbu = Ceramah : ?", "opts": ["a) penghinaan", "b) pidato", "c) kelakar", "d) kesan", "e) ayat"]},
            {"id": 53, "no": "53", "q": "Marah : emosi = Duka cita : ?", "opts": ["a) suka cita", "b) sakit hati", "c) suasana hati", "d) sedih", "e) rindu"]},
            {"id": 54, "no": "54", "q": "Mantel : jubah = wool : ?", "opts": ["a) bahan sandang", "b) domba", "c) sutra", "d) jas", "e) tekstil"]},
            {"id": 55, "no": "55", "q": "Ketinggian puncak : tekanan udara = ketinggian nada : ?", "opts": ["a) garpu tala", "b) sopran", "c) nyanyian", "d) panjang senar", "e) suara"]},
            {"id": 56, "no": "56", "q": "Negara : revolusi = Hidup : ?", "opts": ["a) biologi", "b) keturunan", "c) mutasi", "d) seleksi", "e) ilmu hewan"]},
            {"id": 57, "no": "57", "q": "Kekurangan : penemuan = Panas : ?", "opts": ["a) haus", "b) khatulistiwa", "c) es", "d) matahari", "e) dingin"]},
            {"id": 58, "no": "58", "q": "Kayu : diketam = Besi : ?", "opts": ["a) dipalu", "b) digergaji", "c) dituang", "d) dikikir", "e) ditempa"]},
            {"id": 59, "no": "59", "q": "Olahragawan : lembing = Cendekiawan : ?", "opts": ["a) perpustakaan", "b) penelitian", "c) karya", "d) studi", "e) mikroskop"]},
            {"id": 60, "no": "60", "q": "Keledai : kuda pacuan = Pembakaran : ?", "opts": ["a) pemadam api", "b) obor", "c) letupan", "d) korek api", "e) lautan api"]}
        ]

        for q in questions:
            st.markdown(f"**Soal {q['no']}.** {q['q']}")
            ans = st.radio(
                f"Pilih Jawaban No. {q['no']}:",
                options=q['opts'],
                key=f"sub3_{q['id']}"
            )
            st.session_state.answers[q['id']] = ans
            st.markdown("---")

        save_state_disk(email)

        if st.button("Simpan & Lanjut ke Subtes 4 ➔", type="primary"):
            st.session_state.current_subtest = 4
            st.query_params["subtest"] = "4"
            save_state_disk(email)
            st.rerun()
