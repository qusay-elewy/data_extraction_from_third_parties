from bs4 import BeautifulSoup
import requests
from csv import writer
import pandas as pd
import os


def save_data(data, columns):
    """
    Saves extracted data to a CSV file.

    Args:
        data: The data list to be saved in a .csv file
        columns: The columns list to be passed to the defined daraframe
    Returns:
        A dataframe storing the extracted data
    """

    # Create a dataframe using the passed dataset, and save it to a csv file on the disk
    print("saving data...")
    df = pd.DataFrame(data, columns=columns)
    # Check if the output folder exists and if not create it and form the full path
    file_name = 'housing.csv'
    outdir = './output'
    if not os.path.exists(outdir):
       os.mkdir(outdir)
    full_path = os.path.join(outdir, file_name)
    df.to_csv(full_path, encoding='utf-8')
    return df


def scrape_page(url, page_number):
    """
    Scrapes the speified page of the passed URL (i.e., handles paginated scrapping).

    Args:
        url: The url of the website from which data will be scrapped (i.e. https://housinganywhere.com/s/Berlin--Germany)
        This URL is to be combined with page_number during execution
        page_number: The number of the page to be scrapped from the specified URL. The website displays its data in pages where user navigates through them through the provided pager, where page_number is passed with the URL in a query string to retrieve the corresponding page data
    Returns:
        A bytes array representing extracted page content

    """

    page_url = f"{url}?page={page_number}"
    print(f"Scrapping page {page_url}")
    response = requests.get(page_url)
    if response.status_code == 200:
        return response.content


def scrape_pages(url, start_page, end_page):
    """
    Scrapes multiple pages from a website all at once.
    Args:
        url: The url of the website from which data will be scrapped (i.e. https://housinganywhere.com/s/Berlin--Germany). To be combined with the page number during execution
        start_page: The page index at which the application will start data extraction
        end_page: The page index at which the application will stop data extraction (inclusive)
    Returns:
        A list of extracted content. Each item in this list represents a bytes array of the content extractced from one page
    """

    # Validate passed arguments
    if start_page > 0 and end_page > 0 and end_page >= start_page:
        page_count = end_page - start_page
        # Set value to to the index of the start page and take it from there
        page_number = start_page
        pages_content = []
        for page in range(0, (page_count + 1)):
            pages_content.append(scrape_page(url, page_number))
            page_number += 1
        return pages_content


def parse_content(content):
    """
    Args:
        content: A list of content extracted from the specified pages
        Each item in this list represents the data extracted from one page
    Returns:
        A list of parsed elements. Each item in this list represents the elements tags extractced from one page
    """

    parsed_data = []
    if content is not None:
        for item in content:
            soup = BeautifulSoup(item, "html.parser")

            # The root section that encompasses all the data elements we are interested in
            tags = soup.find_all("div", class_="MuiGrid-root")

            # Loop through retrieved elements to extract data we are interested in
            for tag in tags:
                hyperlinkSection = tag.find(
                    "a", class_="makeStyles-cardLink-214 makeStyles-link-24"
                )

                if hyperlinkSection is not None:
                    # Retrieved URL ends with "?page=page_number" so we need to remove this
                    href = hyperlinkSection.attrs["href"].split("?")[0]
                    hyperlink = f"https://housinganywhere.com{href}"

                    # Get property Id from the extracted hyperlink. 4th element from the end
                    id = href.split("/")[-4]

                    # Retrieve the values displayed underneath the property photo
                    attributes = tag.find("ul", class_="MuiList-root")
                    price = attributes.contents[0].text
                    specs = attributes.contents[1].text
                    availability = attributes.contents[2].text

                    # Create a row using extracted data and add it to a list if it is not there already
                    row = [id, hyperlink, price, specs, availability]
                    if row not in parsed_data:
                        parsed_data.append(row)
        return parsed_data


def process_pages(url, start_page, end_page):
    """
    Abstracts the data extraction and parsing logic, as well as user interface updates.
    Args:
        url: The url of the website from which data will be scrapped (i.e. https://housinganywhere.com/s/Berlin--Germany). To be combined with the page number during execution
        start_page: The page index at which the application will start data extraction
        end_page: The page index at which the application will stop data extraction (inclusive)
    Returns:
        None
    """

    print("Extracting content...")
    pages_content = scrape_pages(url, start_page, end_page)
    if pages_content is not None:
        print("Data extraction completed.")
        print("Parsing extracted content...")
        data = parse_content(pages_content)
        if data is not None:
            columns = ["Id", "URL", "Price", "Specs", "Availability"]
            df = save_data(data, columns)
            if df is not None:
                print("Data scrapping completed successfully")
                print(f"Number of processed properties: {len(df)}")
                print("Printing sample data")
                print("*" * 150)
                print(df.head(5))
            else:
                print("Could not save data")
        else:
            print("Could not parse content")
    else:
        print("Could not extract page data")


def main():

    url = "https://housinganywhere.com/s/Berlin--Germany"
    try:
        # Process pages 11-20 of the aforementioned URL
        process_pages(url, 11, 20)
    except Exception as ex:
        print(f"Something went wrong!\n{ex}")

if __name__ == "__main__":
    main()
