mkdir -p ~/.streamlit/
echo "
[general]n
email = "https://sof-test-1c6c58d57243.herokuapp.com"n
" > ~/.streamlit/credentials.toml
echo "
[server]n
headless = truen
enableCORS=falsen
port = $PORTn
" > ~/.streamlit/config.toml