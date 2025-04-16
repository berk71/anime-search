from flask import Flask, render_template_string, request
from duckduckgo_search import DDGS

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Anime Image Search</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(to right, #f5f7fa, #c3cfe2);
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        h1 {
            margin-top: 40px;
            font-size: 2.5em;
            color: #2c3e50;
        }
        form {
            margin: 20px 0;
        }
        input[type="text"] {
            padding: 10px 15px;
            border: 1px solid #ccc;
            border-radius: 25px;
            width: 300px;
            max-width: 90%;
            font-size: 16px;
            outline: none;
            transition: 0.3s;
        }
        input[type="text"]:focus {
            border-color: #7f8c8d;
        }
        button {
            padding: 10px 20px;
            margin-left: 10px;
            border: none;
            border-radius: 25px;
            background-color: #3498db;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background-color: #2980b9;
        }
        .info {
            margin: 15px 0;
            font-size: 14px;
            color: #555;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            width: 90%;
            max-width: 1000px;
            padding: 20px;
        }
        .gallery img {
            width: 100%;
            max-height: 200px;
            object-fit: cover;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .gallery img:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <h1>Anime Image Search</h1>
    <form method="post">
        <input type="text" name="query" placeholder="Enter anime character" required>
        <button type="submit">Search</button>
    </form>
    {% if status %}
        <div class="info">Request: {{ request_url }}<br>Status Code: {{ status }}</div>
    {% endif %}
    {% if images %}
        <div class="gallery">
            {% for img in images %}
                <div><img src="{{ img }}" loading="lazy"></div>
            {% endfor %}
        </div>
    {% elif status == 200 %}
        <div class="info">No images found.</div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    images = []
    status = None
    request_url = ''
    if request.method == 'POST':
        query = request.form['query']
        request_url = f"image search for: {query}"
        try:
            with DDGS() as ddgs:
                results = ddgs.images(query, max_results=20)
                images = [r['image'] for r in results if 'image' in r]
                status = 200
        except Exception as e:
            print(f"Error: {e}")
            status = 500
    return render_template_string(HTML_TEMPLATE, images=images, status=status, request_url=request_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
