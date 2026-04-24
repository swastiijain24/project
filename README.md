# GenAI Social Portfolio (Django)

A resume-ready GenAI social platform where users build a public profile and use AI to generate a professional personal brand summary.

## Why This Is A GenAI Project

This project includes an AI-powered profile enhancement feature that:
- analyzes profile metadata (bio, location, work, education)
- uses recent posts and tags as signal for interests/skills
- generates a resume-ready About section
- generates a concise professional tagline
- extracts and formats top skills for portfolio display

If an API key is unavailable, the system uses a deterministic fallback generator so the feature still works in demos.

## Key Features

- Django-based social feed with posts, likes, follows, tags
- AI Resume Assistant integrated into account settings
- AI-generated content visible directly on public profile
- Media upload support for profile and posts
- MySQL-backed persistent storage

## Tech Stack

- Python + Django
- MySQL
- OpenAI Python SDK
- Bootstrap + custom CSS

## Setup

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
copy .env.example .env
```

Set `OPENAI_API_KEY` in `.env` (or your shell environment).

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Run server:

```bash
python manage.py runserver
```

## How To Demo GenAI Feature

1. Sign in and go to Account Settings.
2. Add some basic profile info and create a few tagged posts.
3. Click `Generate with AI`.
4. Open your profile page to show generated:
- AI Tagline
- AI About summary
- AI Skills

## Resume Bullet Ideas

- Built a GenAI-powered social portfolio app using Django and OpenAI APIs, generating personalized resume summaries, taglines, and skill clusters from user activity signals.
- Designed fallback AI generation logic for deterministic offline demos, improving feature reliability without external API dependence.
- Implemented end-to-end profile intelligence workflow: prompt construction, model output parsing, persistence, and frontend visualization.
