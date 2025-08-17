# Navigate to your project folder
cd /mount/src/eep105-groupdashboard

# Initialize git repo
git init
git remote add origin https://github.com/<YOUR-USERNAME>/eep105-final.git

# Add your file
git add appfinal.py

# Commit changes
git commit -m "Add final Streamlit app"

# Push to GitHub
git branch -M main
git push -u origin main
