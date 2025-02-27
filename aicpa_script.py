from playwright.sync_api import sync_playwright, TimeoutError

def run(playwright):
    # Launch the browser in non-headless mode for visibility
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()  # Create a new browser context
    page = context.new_page()       # Open a new page in the context

    # Step 1: Navigate to the AICPA homepage
    page.goto("https://www.aicpa.org/")
    print("Loaded homepage:", page.url)

    # Step 2: Navigate to the AICPA-CIMA homepage
    page.goto("https://www.aicpa-cima.com/home")
    print("Loaded second page:", page.url)

    # Step 3: Click the "Accept All" button (for cookies, etc.)
    accept_all_button = page.locator("#onetrust-accept-btn-handler")
    accept_all_button.wait_for(state="visible", timeout=30000)
    accept_all_button.click()
    print("Clicked 'Accept All' button.")

    # Step 4: Click the "Register now" button and switch to the new page
    register_button = page.locator(
        'li.react-multi-carousel-item--active a[data-testid="button-button-welcome-block"] > span'
    )
    try:
        # Ensure the "Register now" button is visible
        register_button.wait_for(state="visible", timeout=30000)
        register_button.hover()

        # Expect a new page to open after clicking "Register now"
        with context.expect_page() as new_page_info:
            register_button.click()
        
        # Switch to the new page
        new_page = new_page_info.value
        new_page.wait_for_load_state()  # Wait for the page to fully load
        print("Switched to new page:", new_page.url)
    except TimeoutError:
        print("Timeout waiting for 'Register now' button or new page.")
        page.screenshot(path="error_register_button.png")
        browser.close()
        return
    except Exception as e:
        print(f"Failed to click 'Register now' button: {e}")
        page.screenshot(path="error_register_button.png")
        browser.close()
        return

    # Step 5: Click the "View options" button on the new page
    try:
        view_options_button = new_page.locator('[data-testid="button-view-options"]')
        view_options_button.wait_for(state="visible", timeout=60000)
        view_options_button.scroll_into_view_if_needed()  # Scroll if necessary
        view_options_button.click()
        print("Clicked 'View Options' button.")
    except TimeoutError:
        print("Timeout waiting for 'View options' button to become visible.")
        new_page.screenshot(path="error_view_options.png")
        browser.close()
        return
    except Exception as e:
        print(f"Failed to click 'View options' button: {e}")
        new_page.screenshot(path="error_view_options.png")
        browser.close()
        return

    # Click the radio button div
    try:
        radio_button = new_page.locator('div[data-testid="0-radio-styled-middle"]')
        radio_button.wait_for(state="visible", timeout=15000)
        radio_button.hover()
        radio_button.click()
        print('Clicked radio button with data-testid="0-radio-styled-middle".')
    except TimeoutError:
        print("Timeout waiting for radio button.")
        new_page.screenshot(path="error_radio_button.png")
        browser.close()
        return
    except Exception as e:
        print(f"Failed to click radio button: {e}")
        new_page.screenshot(path="error_radio_button.png")
        browser.close()
        return

    # Click "Add to Cart" button
    try:
        add_to_cart_button = new_page.locator('button[data-testid="button-purchase-summary-add-to-cart"]')
        add_to_cart_button.wait_for(state="visible", timeout=15000)
        add_to_cart_button.hover()
        add_to_cart_button.click()
        print('Clicked "Add to Cart" button.')
    except TimeoutError:
        print("Timeout waiting for add to cart button.")
        new_page.screenshot(path="error_add_to_cart.png")
        browser.close()
        return
    except Exception as e:
        print(f"Failed to click add to cart button: {e}")
        new_page.screenshot(path="error_add_to_cart.png")
        browser.close()
        return
    # Click "View in Cart" button
    try:
        view_cart_button = new_page.locator('button[data-testid="button-purchase-summary-add-to-cart"]:has-text("View in Cart")')
        view_cart_button.wait_for(state="visible", timeout=15000)
        view_cart_button.hover()
        view_cart_button.click()
        print('Clicked "View in Cart" button.')
    except TimeoutError:
        print("Timeout waiting for view in cart button.")
        new_page.screenshot(path="error_view_in_cart.png")
        browser.close()
        return
    except Exception as e:
        print(f"Failed to click view in cart button: {e}")
        new_page.screenshot(path="error_view_in_cart.png")
        browser.close()
        return

    # Navigate to the cart page
    new_page.goto('https://www.aicpa-cima.com/account/cart')
    new_page.wait_for_load_state('load')
    print('Navigated to cart page: https://www.aicpa-cima.com/account/cart')

    # Take a screenshot
    new_page.screenshot(path='cart-page.png', full_page=True)
    print('Screenshot saved as cart-page.png')

    # Scroll down the page
    new_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    print('Scrolled to the bottom of the cart page.')

    # Clean up
    browser.close()

# Run the script
with sync_playwright() as playwright:
    run(playwright)
