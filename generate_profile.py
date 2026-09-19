from datetime import date
from pathlib import Path
import requests


# ============================================================
# CONFIGURATION
# ============================================================

# Your date of birth
BIRTH_DATE = date(2004, 2, 22)

# Your GitHub username
GITHUB_USERNAME = "SAUGATBARUWAL"

# SVG files
TEMPLATE_FILE = Path("dark_mode_template.svg")
OUTPUT_FILE = Path("dark_mode.svg")


# ============================================================
# CALCULATE AGE
# ============================================================

def calculate_age(birth_date):
    today = date.today()

    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    # Borrow days from the previous month
    if days < 0:
        months -= 1

        if today.month == 1:
            previous_month = 12
            previous_year = today.year - 1
        else:
            previous_month = today.month - 1
            previous_year = today.year

        # Find number of days in previous month
        if previous_month == 12:
            next_month = date(previous_year + 1, 1, 1)
        else:
            next_month = date(previous_year, previous_month + 1, 1)

        previous_month_date = date(
            previous_year,
            previous_month,
            1
        )

        days_in_previous_month = (
            next_month - previous_month_date
        ).days

        days += days_in_previous_month

    # Borrow one year
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

    # Stop if GitHub returns an error
    response.raise_for_status()

    data = response.json()

    return data["public_repos"]


# ============================================================
# GENERATE SVG
# ============================================================

def update_svg(age_text, repository_count):

    # Make sure template exists
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {TEMPLATE_FILE}"
        )

    # Read the ORIGINAL template
    svg = TEMPLATE_FILE.read_text(
        encoding="utf-8"
    )

    # Replace age placeholder
    svg = svg.replace(
        "__AGE__",
        age_text
    )

    # Replace GitHub repository placeholder
    svg = svg.replace(
        "__REPOSITORIES__",
        str(repository_count)
    )

    # Save the generated SVG
    OUTPUT_FILE.write_text(
        svg,
        encoding="utf-8"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Calculate age
    # --------------------------------------------------------

    years, months, days = calculate_age(
        BIRTH_DATE
    )

    age_text = (
        f"{years} years, "
        f"{months} months, "
        f"{days} days"
    )

    print(
        f"Age: {age_text}"
    )

    # --------------------------------------------------------
    # Get GitHub repository count
    # --------------------------------------------------------

    repository_count = get_github_repositories(
        GITHUB_USERNAME
    )

    print(
        f"GitHub repositories: "
        f"{repository_count}"
    )

    # --------------------------------------------------------
    # Generate SVG
    # --------------------------------------------------------

    update_svg(
        age_text,
        repository_count
    )

    print(
        "dark_mode.svg generated successfully!"
    )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()