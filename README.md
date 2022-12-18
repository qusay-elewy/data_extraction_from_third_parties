# Extracting Data from Third-Party Data Sources

### Project Summary
Today, we live in a digital world where there is a myriad of new data being generated every second. We can say that data is the new oil, and the ability to gather and process this data can lead to a lot of innovations and business opportunities. Beyond the standard data sources such as spreadsheets and databases, there is a plethora of other data sources that can be used for both business and research purposes. This includes a countless number of webpages on the Internet, as well as data offered by organizations to its clients and business partners through web services and APIs.

In this project, we will show how to extract data from several non-database data sources using techniques like web scrapping, and through APIs

For the web scrapping part, we use Python and the BeautifulSoup library to extract some housing data from www.housinganywhere.com, a website that allows people to rent houses in Europe. The module goes through the advertised properties and inspect the underlying HTML code of these pages to extract some interesting information such as the property type (apartment, studio, rooms...), size, rent, etc. Then, this data is saved to a .csv file using Pandas so that it can be analyzed and used later.
