# GitHub and public deployment

GitHub can host your code publicly, but GitHub Pages cannot run this app by itself because this is a Python Streamlit app.

The easiest public deployment path is:

1. Create a public GitHub repository.
2. Push this `Robot Maintenance` folder to that repository.
3. Go to Streamlit Community Cloud.
4. Connect your GitHub account.
5. Choose the repo.
6. Set the main file to `app.py`.
7. Deploy.

After that, you can submit both links:

- GitHub repo link
- Streamlit public app link

## commands from this folder

```bash
git init
git add .
git commit -m "build robot predictive maintenance dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## local run command

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## what not to upload

Do not upload `.venv`. It is just the local Python environment with downloaded packages. GitHub and Streamlit install fresh packages from `requirements.txt`.
