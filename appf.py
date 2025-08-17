# 1. Initialize git in your project folder
git init

# 2. Connect your local folder to GitHub (replace with your repo URL)
git remote add origin https://github.com/your-username/your-repo-name.git

# 3. Check remote to confirm it’s linked
git remote -v

# 4. Stage all files in the folder
git add .

# 5. Make your first commit with a message
git commit -m "First commit - project upload"

# 6. Rename default branch to main (if needed)
git branch -M main

# 7. Push everything to GitHub
git push -u origin main
