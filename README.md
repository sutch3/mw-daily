# MW Daily

MW Daily is a small Streamlit app for Master of Wine exam preparation. It gives Sara one analytical MW-style question per day, lets her write and save an answer, reveals marking guidance, and tracks weak areas over time.

## Features

- Daily question mode
- Random question mode
- 50 original MW-style questions
- Categories covering viticulture, vinification, wine business, global wine regions, current issues, tasting logic, and research paper skills
- Warm-up, MW-style, and exam-pressure difficulty levels
- Saved written answers
- Model answer, marking points, common traps, and follow-up reading topics
- Progress page with answered questions, category coverage, time taken, and answer history

## Run locally

This app is built with Python and Streamlit.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app will open at the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Deploy with GitHub and Streamlit Community Cloud

1. Create a new GitHub repository.
2. Add these files to the repository and push them to GitHub.
3. Go to Streamlit Community Cloud.
4. Choose **New app**.
5. Select the GitHub repository.
6. Set the main file path to:

```text
app.py
```

7. Deploy.

Sara can then use the Streamlit app link directly.

## Hosted progress storage

For local development, answers are saved in:

```text
data/progress.json
```

For Streamlit hosting, add GitHub-backed storage so Sara's answers survive redeploys:

1. Create a fine-grained GitHub token with contents read/write access to this one repository.
2. In Streamlit Community Cloud, open the app settings.
3. Add secrets using this shape:

```toml
[github_storage]
token = "github_pat_replace_me"
repo = "your-github-username/mw-daily"
branch = "main"
path = "data/progress.json"
```

When those secrets are present, the app saves progress back to `data/progress.json` in GitHub. Sara does not need to log in or manage anything.

Keep `.streamlit/secrets.toml` private. Use `.streamlit/secrets.example.toml` only as a template.

## Updating the app

Make changes locally, commit them, and push to GitHub. Streamlit Community Cloud will redeploy from the GitHub repository.

## Project structure

```text
app.py                 # Daily/random question page
pages/2_Progress.py    # Progress dashboard
mw_daily/questions.py   # Question loading and daily selection
mw_daily/storage.py     # Answer persistence
mw_daily/analytics.py   # Progress and weak-area calculations
data/questions.json     # 50 original MW-style questions
data/progress.json      # Saved answer records
```
