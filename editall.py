import os
import re

# Folder tempat file HTML disimpan
folder_path = "chapter"  # ubah ke lokasi folder kamu

# Regex untuk menghapus style & script lama
style_pattern = re.compile(r"<style.*?>.*?</style>", re.DOTALL)
old_darkmode_pattern = re.compile(r"<script.*?>.*?</script>", re.DOTALL)

# HTML tombol yang akan ditambahkan
buttons_html = """
    <button id="darkModeBtn" title="Toggle Dark Mode">🌙</button>
    <button id="scrollTopBtn" onclick="scrollToTop()">↑</button>
"""

for root, _, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith(".html"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Hapus style lama
            content = re.sub(style_pattern, "", content)

            # Hapus script dark mode lama
            content = re.sub(old_darkmode_pattern, "", content)

            # Tambah <link> di <head> kalau belum ada
            if '<link rel="stylesheet" href="../style.css">' not in content:
                content = content.replace(
                    "<head>",
                    "<head>\n    <link rel=\"stylesheet\" href=\"../style.css\">"
                )

            # Tambah tombol di dalam <body>
            if "id=\"darkModeBtn\"" not in content:
                if "id=\"scrollTopBtn\"" in content:
                    # Sisipkan dark mode button sebelum scrollTopBtn
                    content = content.replace(
                        '<button id="scrollTopBtn"',
                        '<button id="darkModeBtn" title="Toggle Dark Mode">🌙</button>\n    <button id="scrollTopBtn"'
                    )
                else:
                    # Kalau belum ada scrollTopBtn, tambahkan kedua tombol
                    buttons_html = """
                <button id="darkModeBtn" title="Toggle Dark Mode">🌙</button>
                <button id="scrollTopBtn" onclick="scrollToTop()">↑</button>
            """
                    content = content.replace(
                        "<body>",
                        f"<body>\n{buttons_html}"
                    )


            # Tambah <script> sebelum </body> kalau belum ada
            if '<script src="script.js"></script>' not in content:
                content = content.replace(
                    "</body>",
                    "    <script src=\"../script.js\"></script>\n</body>"
                )

            # Simpan jika ada perubahan
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated: {file_path}")

print("Selesai! Semua file HTML sudah diperbarui.")
