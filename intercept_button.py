from mitmproxy import ctx, http
import csv
import os
from datetime import date
from bs4 import BeautifulSoup


class ResponseInterceptor:
    def __init__(self):
        self.base_url = "https://mops.twse.com.tw/mops/web/ajax_t05sr01_1"
        self.response_content = None

    def request(self, flow: http.HTTPFlow):
        if flow.request.url == self.base_url and flow.request.method == "POST":
            ctx.log.info(f"Intercepted POST request to: {self.base_url}")

    def response(self, flow: http.HTTPFlow):
        if flow.request.url == self.base_url and flow.request.method == "POST":
            ctx.log.info(f"Intercepted response from: {self.base_url}")
            self.response_content = flow.response.content

            # Get current date
            current_date = date.today().strftime("%Y-%m-%d")

            # Create directory if it doesn't exist
            output_directory = os.path.join(os.path.expanduser("~/Desktop"), "OTC_Company_Info", current_date)
            os.makedirs(output_directory, exist_ok=True)

            # Extract company code from response content
            company_code = extract_company_code(self.response_content.decode("utf-8"))

            # Create CSV file path
            csv_filename = f"company_code_{company_code}_detail_info.csv"
            csv_path = os.path.join(output_directory, csv_filename)

            # Use BeautifulSoup to extract relevant information
            response_html = self.response_content.decode("utf-8")
            soup = BeautifulSoup(response_html, "html.parser")
            content = soup.get_text(separator="\n")

            # Save extracted content to a CSV file
            with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["Response Content"])
                csvwriter.writerow([content])

            print(f"CSV has been saved to: {csv_path}")
            print("File saved successfully!")


def extract_company_code(response_content):
    lines = response_content.splitlines()
    company_code = ""
    for line in lines:
        if "(上市公司)" in line or "(上櫃公司)" in line:
            company_code = line.split()[1]
            break
    return company_code


addons = [
    ResponseInterceptor()
]
