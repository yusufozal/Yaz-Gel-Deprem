from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver'ı başlatma (Chrome)
driver = webdriver.Chrome()

# Web sayfasına gitme
driver.get("https://deprem.afad.gov.tr/event-catalog")

try:
    # Bekleme işlemi (10 saniyeye kadar)
    wait = WebDriverWait(driver, 10)

    # Filtreleme işlemi için zaman tanıma
    input("Lütfen tarih ve diğer filtreleri ayarlayın ve 'Filtrele' butonuna tıklayın. Devam etmek için Enter'a basın.")

    # Tabloyu kontrol etmeden önce kısa bir bekleme
    time.sleep(5)  # Bu bekleme süresini gerektiği gibi ayarlayabilirsiniz

    # Verilerin yüklendiğini kontrol etmek için "No records available" metninin kaybolmasını bekleme
    wait.until_not(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "No records available")]')))

    all_data = []

    while True:
        # Doğru XPath ile tabloyu bulma
        table_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainContent"]/div/div/div/div[2]/div[3]/div/div/kendo-grid/div/kendo-grid-list/div/div[1]/table')))

        # Tablo satırlarını bulma
        rows = table_element.find_elements(By.TAG_NAME, "tr")

        # Tablo verilerini toplama
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            all_data.append(row_data)

        # Sonraki butonunu bulma ve tıklama
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainContent"]/div/div/div/div[2]/div[3]/div/div/kendo-grid/kendo-pager/kendo-pager-next-buttons/a[1]/span')))
            next_button.click()
            time.sleep(2)  # Sayfanın yüklenmesi için kısa bir bekleme
        except:
            # Sonraki butonu yoksa döngüden çıkma
            break

    # Verileri dosyaya kaydetme
    with open("data.txt", "w") as file:
        for row_data in all_data:
            file.write("\t".join(row_data) + "\n")

finally:
    # Tarayıcıyı kapatma
    driver.quit()
