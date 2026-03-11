import os
# Vercel সার্ভারে ফাইল সেভ করার জন্য /tmp ফোল্ডার পারমিশন দেওয়া হলো
os.environ['U2NET_HOME'] = '/tmp'

from flask import Flask, request, send_file
from rembg import remove, new_session
import io

app = Flask(__name__)

# u2netp হলো একটি লাইটওয়েট AI মডেল, যা ফ্রি সার্ভারে খুব দ্রুত কাজ করে
session = new_session("u2netp")

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400
        
    file = request.files['file']
    input_data = file.read()
    
    try:
        # AI এর মাধ্যমে ব্যাকগ্রাউন্ড রিমুভ করা হচ্ছে
        output_data = remove(input_data, session=session)
        
        # প্রসেস করা ছবিটি ব্রাউজারে ফেরত পাঠানো হচ্ছে
        return send_file(
            io.BytesIO(output_data),
            mimetype='image/png',
            as_attachment=False
        )
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
