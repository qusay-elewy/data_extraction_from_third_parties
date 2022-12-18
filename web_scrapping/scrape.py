from bs4 import BeautifulSoup
import requests
from csv import writer
import pandas as pd


def save_data(data, columns):
    """
    Saves data to a CSV file.

    Args:
        data: the data list to be saved
        columns: the columns list
    Returns:
        None

    """
    # Create a dataframe using the passed dataset, and save it to a csv file on the disk
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("output/housing.csv")
    print("\nData scrapping completed successfully.")
    print(f"Number of extracted properties: {len(df)}\n")

    # Show some sample data to the user
    print("Sample data")
    print("*****************************************")
    print(df.head(5))


def scrapePage(base_url):
    """
    Scrapes a webpage.
    Args:
        base_url: the url of the webpage to be scraped. To be combined with the page number during execution.
    Returns:
        None
    """
    data = []
    print("Scrapping data. Please wait.")

    try:
        # Scrape 50 pages from the website
        for pageNumber in range(1, 2):
            print(f"Scrapping page {pageNumber}...")
            pageUrl = f"{base_url}?page={pageNumber}"
            response = requests.get(pageUrl)

            # Successful request
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                # The root section that encompasses all the data elements we are interested in
                list = soup.find_all("div", class_="MuiGrid-root")

                # Loop through retrieved items to extract data we are interested in
                for item in list:
                    hyperlinkSection = item.find(
                        "a", class_="makeStyles-cardLink-214 makeStyles-link-24"
                    )

                    if hyperlinkSection is not None:
                        # Retrieved URL ends with "?page=page_number" so we need to remove this
                        href = hyperlinkSection.attrs["href"].split("?")[0]
                        hyperlink = f"https://housinganywhere.com{href}"

                        # Get property Id from the extracted hyperlink. 4th element from the end
                        id = href.split("/")[-4]

                        # Retrieve the values displayed underneath the property photo
                        attributes = item.find("ul", class_="MuiList-root")
                        price = attributes.contents[0].text
                        specs = attributes.contents[1].text
                        availability = attributes.contents[2].text

                        # Create a row using extracted data and add it to a list if not there already
                        row = [id, hyperlink, price, specs, availability]
                        if row not in data:
                            data.append(row)

                # Write extracted data to a CSV file
                columns = ["Id", "URL", "Price", "Specs", "Availability"]
                save_data(data, columns)
            else:
                print("Attept to access page data failed.")

    except Exception as ex:
        print("Something went wrong!\n" + str(ex))


def main():
    url = "https://housinganywhere.com/s/Berlin--Germany"
    scrapePage(url)


if __name__ == "__main__":
    main()
