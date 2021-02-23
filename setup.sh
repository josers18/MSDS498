mkdir -p ~/.streamlit/
echo "[general]
email = \"jsifontes@u.northwestern.edu\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
