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
        "current_subtest": st.session_state.get("current_subtest", 1),
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
        ⏱️ SISA WAKTU SUBTES 1: <span id="timer_display">--:--</span>
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

def render_subtest_1_se():
    if "step_sub1" not in st.session_state:
        st.session_state.step_sub1 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub1 == "instruction":
        st.title("📑 Petunjuk Subtes 1")
        st.info("💡 Bacalah petunjuk di bawah ini. **Timer belum berjalan di halaman ini.**")
        st.markdown("""
        ### Aturan Pengerjaan:
        Soal-soal 01–20 terdiri atas kalimat-kalimat. Pada setiap kalimat satu kata hilang dan disediakan 5 (lima) kata pilihan sebagai penggantinya.

        ---
        ### Contoh 01:
        **Seekor kuda mempunyai kesamaan terbanyak dengan seekor .....**  
        a) kucing | b) bajing | c) keledai | d) lembu | e) anjing  
        *Penjelasan:* Jawaban yang benar ialah **c) keledai**.

        ---
        ### Contoh Berikutnya:
        **Lawannya "harapan" ialah .....**  
        a) duka | b) putus asa | c) sengsara | d) cinta | e) benci  
        *Penjelasan:* Jawabannya ialah **b) putus asa**.
        """)
        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 1 🚀", type="primary"):
            st.session_state.step_sub1 = "test"
            if "sub1" not in st.session_state.start_times:
                st.session_state.start_times["sub1"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub1 == "test":
        st.title("🧠 Subtes 1")
        
        if "sub1" not in st.session_state.start_times:
            st.session_state.start_times["sub1"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub1"])
        remaining = max(0, 360 - elapsed) # 6 menit

        if remaining <= 0:
            st.warning("⏰ Waktu Subtes 1 telah habis! Pindah otomatis ke Subtes 2...")
            st.session_state.current_subtest = 2
            st.query_params["subtest"] = "2"
            save_state_disk(email)
            time.sleep(1)
            st.rerun()

        show_live_timer(remaining)

        questions = [
            {"id": 1, "no": "01", "q": "Pengaruh seseorang terhadap orang lain seharusnya bergantung pada .....", "opts": ["a) kekuasaan", "b) bujukan", "c) kekayaan", "d) keberanian", "e) kewibawaan"]},
            {"id": 2, "no": "02", "q": "Lawannya 'hemat' ialah .....", "opts": ["a) murah", "b) kikir", "c) boros", "d) bernilai", "e) kaya"]},
            {"id": 3, "no": "03", "q": "..... tidak termasuk cuaca", "opts": ["a) angin puyuh", "b) halilintar", "c) salju", "d) gempa bumi", "e) kabut"]},
            {"id": 4, "no": "04", "q": "Lawannya 'setia' ialah .....", "opts": ["a) cinta", "b) benci", "c) persahabatan", "d) khianat", "e) permusuhan"]},
            {"id": 5, "no": "05", "q": "Seekor kuda selalu mempunyai .....", "opts": ["a) kandang", "b) ladam", "c) pelana", "d) kuku", "e) surai"]},
            {"id": 6, "no": "06", "q": "Seorang paman ..... lebih tua dari kemenakannya.", "opts": ["a) jarang", "b) biasanya", "c) selalu", "d) tidak pernah", "e) kadang-kadang"]},
            {"id": 7, "no": "07", "q": "Pada jumlah yang sama, nilai kalori yang tertinggi terdapat pada .....", "opts": ["a) ikan", "b) daging", "c) lemak", "d) tahu", "e) sayuran"]},
            {"id": 8, "no": "08", "q": "Pada suatu pertandingan selalu terdapat .....", "opts": ["a) lawan", "b) wasit", "c) penonton", "d) sorak", "e) kemenangan"]},
            {"id": 9, "no": "09", "q": "Suatu pernyataan yang belum dipastikan dikatakan sebagai pernyataan yang .....", "opts": ["a) paradoks", "b) tergesa-gesa", "c) mempunyai arti rangkap", "d) menyesatkan", "e) hipotesis"]},
            {"id": 10, "no": "10", "q": "Pada sepatu selalu terdapat .....", "opts": ["a) kulit", "b) sol", "c) tali sepatu", "d) gesper", "e) lidah"]},
            {"id": 11, "no": "11", "q": "Suatu ..... tidak menyangkut persoalan pencegahan kecelakaan.", "opts": ["a) lampu lalu lintas", "b) kacamata pelindung", "c) kotak PPPK", "d) tanda peringatan", "e) palang kereta api"]},
            {"id": 12, "no": "12", "q": "Mata uang logam Rp 50,- tahun 1991, garis tengahnya ialah ..... mm.", "opts": ["a) 17", "b) 29", "c) 25", "d) 20", "e) 15"]},
            {"id": 13, "no": "13", "q": "Seseorang yang bersikap menyangsikan setiap kemajuan ialah seorang yang .....", "opts": ["a) demokratis", "b) radikal", "c) liberal", "d) konservatif", "e) anarkis"]},
            {"id": 14, "no": "14", "q": "Lawannya 'tidak pernah' ialah .....", "opts": ["a) sering", "b) kadang-kadang", "c) jarang", "d) kerap kali", "e) selalu"]},
            {"id": 15, "no": "15", "q": "Jarak antara Jakarta – Surabaya kira-kira ..... Km", "opts": ["a) 650", "b) 1000", "c) 800", "d) 600", "e) 950"]},
            {"id": 16, "no": "16", "q": "Untuk dapat membuat nada yang rendah dan mendalam, kita memerlukan banyak .....", "opts": ["a) kekuatan", "b) peranan", "c) ayunan", "d) berat", "e) suara"]},
            {"id": 17, "no": "17", "q": "Ayah ..... lebih berpengalaman dari pada anaknya", "opts": ["a) selalu", "b) biasanya", "c) jauh", "d) jarang", "e) pada dasarnya"]},
            {"id": 18, "no": "18", "q": "Diantara kota-kota berikut ini, maka kota ..... letaknya paling selatan.", "opts": ["a) Jakarta", "b) Bandung", "c) Cirebon", "d) Semarang", "e) Surabaya"]},
            {"id": 19, "no": "19", "q": "Jika kita mengetahui jumlah presentase nomor-nomor lotere yang tidak menang, maka kita dapat menghitung .....", "opts": ["a) jumlah nomor yang menang", "b) pajak lotere", "c) kemungkinan menang", "d) jumlah pengikut", "e) tinggi keuntungan"]},
            {"id": 20, "no": "20", "q": "Seorang anak yang berumur 10 tahun tingginya rata-rata ..... cm", "opts": ["a) 150", "b) 130", "c) 110", "d) 105", "e) 115"]}
        ]

        for q in questions:
            st.markdown(f"**Soal {q['no']}.** {q['q']}")
            ans = st.radio(
                f"Pilih Jawaban No. {q['no']}:",
                options=q['opts'],
                key=f"sub1_{q['id']}"
            )
            st.session_state.answers[q['id']] = ans
            st.markdown("---")

        save_state_disk(email)

        if st.button("Simpan & Lanjut ke Subtes 2 ➔", type="primary"):
            st.session_state.current_subtest = 2
            st.query_params["subtest"] = "2"
            save_state_disk(email)
            st.rerun()
