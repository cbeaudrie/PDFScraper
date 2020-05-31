def getPDFs( browser, pdfLinks ):
    import time

    current_window = browser.current_window_handle

    i=1
    
    for pdf in pdfLinks:
        print(i, ' of ', len(pdfLinks), ' downloading...')

        href = pdf.get_attribute('href')

        if href:
            browser.execute_script('window.open(arguments[0]);', href)
        else:
            link.click()

        time.sleep(3)
        new_window = [window for window in browser.window_handles if window != current_window][0]
        time.sleep(3)
        browser.switch_to.window(new_window)
        time.sleep(3)

        browser.switch_to.frame("pdfIframe")

        openButton = browser.find_element_by_id('open-button')
        openButton.click()

        browser.close()
        browser.switch_to.window(current_window)
        print(i, ' DONE')
        i=i+1

    print('FINISHED Getting PDFs')
    return