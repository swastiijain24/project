import json
import os
from typing import Dict, List

from django.utils.text import slugify


def _collect_seed_skills(profile, recent_posts) -> List[str]:
    skills = set()
    if profile.workingat:
        skills.add(profile.workingat.strip())
    if profile.education:
        skills.add(profile.education.strip())
    for post in recent_posts:
        for tag in post.tags.all():
            if tag.name:
                skills.add(tag.name.strip())
    cleaned = [s for s in skills if s]
    return cleaned[:8]


def _fallback_resume_content(profile, recent_posts) -> Dict[str, str]:
    first_name = (profile.user_id.first_name or profile.user_id.username).strip()
    role = (profile.workingat or "Aspiring Software Developer").strip()
    location = (profile.location or "Remote").strip()
    education = (profile.education or "Lifelong learner").strip()
    skills = _collect_seed_skills(profile, recent_posts)
    skill_text = ", ".join(skills) if skills else "Python, Django, Problem Solving"

    about = (
        f"I am {first_name}, a builder focused on creating practical digital products. "
        f"I currently work as {role} and enjoy turning real user problems into clean web experiences. "
        f"Based in {location}, I combine strong fundamentals with rapid iteration and continuous learning. "
        f"My background includes {education}, and my current stack focuses on {skill_text}."
    )

    tagline = f"{role} | Building AI-powered social experiences"

    return {
        "about": about,
        "tagline": tagline[:255],
        "skills": skill_text,
    }


def _build_prompt(profile, recent_posts) -> str:
    tag_text = []
    captions = []
    for post in recent_posts:
        post_tags = [tag.name for tag in post.tags.all()[:6]]
        if post_tags:
            tag_text.extend(post_tags)
        if post.caption:
            captions.append(post.caption[:200])

    prompt_payload = {
        "name": f"{profile.user_id.first_name} {profile.user_id.last_name}".strip(),
        "username": profile.user_id.username,
        "bio": profile.bio,
        "location": profile.location,
        "workingat": profile.workingat,
        "education": profile.education,
        "recent_post_captions": captions[:5],
        "recent_tags": tag_text[:12],
        "task": "Generate a resume-ready personal brand snippet.",
        "output_format": {
            "about": "2-4 lines, first person, achievement-oriented",
            "tagline": "single line under 80 chars",
            "skills": "comma-separated top 8 skills"
        }
    }

    return (
        "You are a career branding assistant. Return only valid JSON with keys: "
        "about, tagline, skills. No markdown.\n\n"
        f"INPUT:\n{json.dumps(prompt_payload, ensure_ascii=True)}"
    )


def generate_resume_ai_content(profile, recent_posts) -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    if not api_key:
        return _fallback_resume_content(profile, recent_posts)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            input=[{"role": "user", "content": _build_prompt(profile, recent_posts)}],
            temperature=0.5,
            max_output_tokens=400,
        )

        text = (response.output_text or "").strip()
        if not text:
            return _fallback_resume_content(profile, recent_posts)

        data = json.loads(text)
        about = str(data.get("about", "")).strip()
        tagline = str(data.get("tagline", "")).strip()
        skills = str(data.get("skills", "")).strip()

        if not about or not tagline:
            return _fallback_resume_content(profile, recent_posts)

        normalized_skills = ", ".join(
            [s.strip() for s in skills.split(",") if s.strip()]
        )

        return {
            "about": about,
            "tagline": tagline[:255],
            "skills": normalized_skills[:255],
        }
    except Exception:
        return _fallback_resume_content(profile, recent_posts)


def build_portfolio_slug(profile) -> str:
    base = profile.user_id.username or "profile"
    return slugify(base) or "profile"
