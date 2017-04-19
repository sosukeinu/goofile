# Basic

This is an update of [https://code.google.com/archive/p/goofile/](https://code.google.com/archive/p/goofile/) for Python 3, with the addition of a setup.py file for easy pip installation.

To install, download or clone repository:

    git clone https://github.com/sosukeinu/goofile.git goofile
    
then `cd` into the resulting directory

    cd goofile
    
then, install using pip

    pip install .
    
You can then run the script from anywhere on your system using:

    goofile -d {domain to search} -f {filetype, i.e. pdf}
    
for example

    goofile -d kali.org -f pdf
    
# Enhancements

The above technique might trigger Google's Bot detection after too many requests. To work around this, you can set up a [Custom Site Search Engine](https://developers.google.com/custom-search/json-api/v1/introduction)

In order to get this new method to work, it requires some setup. You must follow the process below to create and configure a Custom Search Engine, and retrieve an API key and Search Engine ID, which you will then pass along with your request.

**First** get an API Key from [Custom Site Search Engine Intro Page](https://developers.google.com/custom-search/json-api/v1/introduction)

select "Get a key"

![](https://cloud.githubusercontent.com/assets/1004903/25198500/bf72a15e-2515-11e7-85db-325ed669181b.png)

create a project

![](https://cloud.githubusercontent.com/assets/1004903/25198504/bf7481cc-2515-11e7-91c6-b7090c76f199.png)

copy the API key, and keep this in a safe place for use

![](https://cloud.githubusercontent.com/assets/1004903/25198502/bf73aa72-2515-11e7-97f7-7457b5fc5069.png)

****


**Then** return to [Custom Site Search Engine Intro Page](https://developers.google.com/custom-search/json-api/v1/introduction) and Click on "Custom Search Engine"

![](https://cloud.githubusercontent.com/assets/1004903/25198503/bf73ff36-2515-11e7-8a86-d1adcbd306c1.png)

on the next page, click "Create a custom search engine"

![](https://cloud.githubusercontent.com/assets/1004903/25198501/bf73aad6-2515-11e7-8148-707a57dbaf62.png)

give the search engine a site to search (this can be anything) and select "Create"

![](https://cloud.githubusercontent.com/assets/1004903/25198505/bf755fd4-2515-11e7-8b61-b7ff1cfc1aa7.png)

this redirects you to [your dashboard](https://cse.google.com/manage/all)

![](https://cloud.githubusercontent.com/assets/1004903/25198507/bf821c60-2515-11e7-82be-22b2a6bcee64.png)

grab your search engine ID, and put this in a safe place for use.

![](https://cloud.githubusercontent.com/assets/1004903/25198506/bf822b9c-2515-11e7-91e9-bac47dbf59cb.png)

**Lastly** be sure to set this to search the entire web, or you'll get no results

![](https://cloud.githubusercontent.com/assets/1004903/25198508/bf838f1e-2515-11e7-854a-8cc38fff9e5e.png)

Once you've configured your search Engine as above, you can run the file search by passing the API Key and Search Engine ID along with the request, as below:

    goofile -d kali.org -f pdf -k {your-api-key} -e {search-engine-id}
    
Further, you can do things like pass a search term along with the query

    goofile -d scp.nrc.gov -f pdf -k {your-api-key} -e {search-engine-id} -q detonation

    
**Note:** The free account is limited to 100 queries per day.

You can always manage your projects here: [Dashboard](https://cse.google.com/manage/all)
