# 0) (one-time) Identify yourself to Git if you haven't before
git config --global user.name "Your Name"
git config --global user.email "youremail@berkeley.edu"

# 1) Initialize a repo in the current folder
git init

# 2) Optional: add a .gitignore to keep junk out of the repo
printf ".ipynb_checkpoints/\n__pycache__/\n*.pyc\n.env\n" > .gitignore

# 3) (Recommended) minimal requirements for Streamlit app
printf "streamlit\npandas\nnumpy\nmatplotlib\nopenpyxl\n" > requirements.txt

# 4) Stage + commit everything
git add -A
git commit -m "Initial commit: EEP105 dashboard + notebook"

# 5) Connect to your GitHub repo (replace with your actual URL)
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git

# 6) Push to GitHub
git push -u origin main
