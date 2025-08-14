from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)
CORS(app)

# === GMAIL AYARLARI ===
EMAIL = "boyacicomtr@gmail.com"
PASSWORD = "abhe jxjy jwmb ilzs"  # ← 16 haneli Gmail uygulama şifren
TO_EMAIL = "boyacicomtr@gmail.com"

@app.route("/")
def home():
    return """
    <h3>✅ Form Sunucusu Çalışıyor</h3>
    <p><strong>/submit</strong> adresine POST isteği gönderin.</p>
    <p><em>Sunucu tarihi: {}</em></p>
    """.format(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

@app.route("/submit", methods=["POST"])
def handle_form():
    try:
        data = request.form.to_dict()
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # E-posta konusu: Hangi form?
        form_turu = "Bilinmeyen Form"
        if "parkeTipi" in data:
            form_turu = "Parke Döşeme Talebi"
        elif "seramikTuru" in data:
            form_turu = "Seramik Döşeme Talebi"
        else:
            form_turu = "Boya Badana Talebi"

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = TO_EMAIL
        msg["Subject"] = f"Yeni {form_turu}"

        # Tüm alanları e-postaya yaz
        body_lines = [f"Yeni bir form gönderildi:\n"]
        for key, value in data.items():
            label = {
                "isim": "İsim",
                "telefon": "Telefon",
                "ilIlce": "Bölge",
                "esyaliMi": "Eşyalı mı?",
                "odaSayisi": "Oda Sayısı",
                "metreKare": "Metrekare",
                "malzeme": "Malzeme",
                "parkeTipi": "Parke Tipi",
                "mmSecimi": "Parke Kalınlığı",
                "yuzeyDurumu": "Yüzey Durumu",
                "seramikTuru": "Seramik Türü",
                "seramikBoyutu": "Seramik Boyutu",
                "tahminiFiyat": "Tahmini Fiyat"
            }.get(key, key.replace("_", " ").title())

            body_lines.append(f"{label}: {value}")

        body_lines.append(f"\nTarih: {tarih}")
        body = "\n".join(body_lines)

        msg.attach(MIMEText(body.strip(), "plain", "utf-8"))

        # Gmail'e bağlan ve gönder
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
        server.quit()

        print(f"✅ Gönderildi: {data.get('isim', 'Bilinmeyen')} - {form_turu}")
        response = jsonify({"success": True})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        return response

    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        response = jsonify({"success": False, "error": str(e)})
        response.status_code = 500
        response.headers["Content-Type"] = "application/json"
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)