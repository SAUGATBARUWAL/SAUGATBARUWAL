from datetime import date
from pathlib import Path
import requests


# ============================================================
# CONFIGURATION
# ============================================================

BIRTH_DATE = date(2004, 2, 22)

GITHUB_USERNAME = "SAUGATBARUWAL"

TEMPLATE_FILE = Path("dark_mode_template.svg")
SVG_FILE = Path("dark_mode.svg")


# ============================================================
# CALCULATE AGE
# ============================================================

def calculate_age(birth_date):
    today = date.today()

    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        months -= 1

        if today.month == 1:
            previous_month = 12
            previous_year = today.year - 1
        else:
            previous_month = today.month - 1
            previous_year = today.year

        days_in_previous_month = (
            date(today.year, today.month, 1)
            - date(previous_year, previous_month, 1)
        ).days

        days += days_in_previous_month

    if months < 0:
        years -= 1
        months += 12

    return years, months, days


# ============================================================
# GET GITHUB REPOSITORY COUNT
# ============================================================

def get_github_repositories(username):

    url = f"https://api.github.com/users/{username}"

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["public_repos"]


# ============================================================
# UPDATE SVG
# ============================================================

def update_svg(age_text, repository_count):

    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {TEMPLATE_FILE}"
        )

    svg = TEMPLATE_FILE.read_text(
        encoding="utf-8"
    )

    # Replace dynamic values only
    svg = svg.replace(
        "__AGE__",
        age_text
    )

    svg = svg.replace(
        "__REPOSITORIES__",
        str(repository_count)
    )

    SVG_FILE.write_text(
        svg,
        encoding="utf-8"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    years, months, days = calculate_age(
        BIRTH_DATE
    )

    age_text = (
        f"{years} years, "
        f"{months} months, "
        f"{days} days"
    )

    print(f"Age: {age_text}")

    repository_count = get_github_repositories(
        GITHUB_USERNAME
    )

    print(
        f"GitHub repositories: "
        f"{repository_count}"
    )

    update_svg(
        age_text,
        repository_count
    )

    print(
        "dark_mode.svg updated successfully!"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()