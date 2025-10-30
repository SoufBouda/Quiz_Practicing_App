from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://127.0.0.1:5000/")
    page.screenshot(path="jules-scratch/verification/01_start_page.png")
    page.get_by_role("button", name="Start Quiz").click()
    page.wait_for_selector("h2")
    page.screenshot(path="jules-scratch/verification/02_question_page.png")
    page.get_by_label("Berlin").check()
    page.screenshot(path="jules-scratch/verification/03_answer_selected.png")
    page.get_by_role("button", name="Next").click()
    page.wait_for_selector("h2")
    page.screenshot(path="jules-scratch/verification/04_next_question.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
