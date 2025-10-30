from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://127.0.0.1:5000/")

    # Check for the dark theme
    body = page.locator('body')
    expect(body).to_have_css('background-color', 'rgb(18, 18, 18)')
    expect(body).to_have_css('color', 'rgb(224, 224, 224)')

    page.screenshot(path="jules-scratch/verification/01_dark_theme.png")

    page.get_by_role("button", name="Start Quiz").click()

    # Wait for the quiz container to be visible and the question to appear
    quiz_container = page.locator('#quiz-container')
    expect(quiz_container).to_be_visible()
    question_header = quiz_container.locator('h2')
    expect(question_header).to_be_visible()

    page.screenshot(path="jules-scratch/verification/02_question_page.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
