# InshortsAPI
Inshorts is an app which provides news from different sources and presents them under 60 words. This API Scraps content from the Inshorts website and provides it in easy to use JSON Format.
Categories

Supports all categories as on the Inshorts Website. These include -

    ''// result in bad request
    national //Indian National News
    business
    sports
    world
    politics
    technology
    startup
    entertainment
    miscellaneous
    hatke // Unconventional
    science
    automobile
#
**Usage**
#
##
**1. GET Request**
##
Make a get request of the form

http://{site_address}/news?category={category_name}

Example - http://www.exampleapi.com/news?category=science

**2. POST Request**

Make a post request with the category, provided as either form or json data with name/key 'category' to the same route as above i.e '/news'.
Response Format


The response JSON Object looks something like this -
```
{"success": true, 
"category": "science", 
"data": [{"title": "\nScientist lets thousands of mosquitoes bite him daily for research\n", 
"imageUrl": "https://static.inshorts.com/inshorts/images/v1/variants/jpg/m/2020/10_oct/1_thu/img_1601530220620_633.jpg?", 
"url": "https://www.inshorts.com/en/news/scientist-lets-thousands-of-mosquitoes-bite-him-daily-for-research-1601532043669", 
"content": "An Australian scientist lets up to 5,000 mosquitoes bite his arm on a daily basis as part of his research to fight dengue fever. The insects Perran Ross feeds are infected with Wolbachia, a bacterium known to block the spread of dengue. His work involves infecting mosquito eggs with the bacterium and then breeding Wolbachia-carrying mosquitoes in the lab. ", 
"author": "Krishna Veera Vanamali", 
"date": "01 Oct 2020,Thursday", "time": "11:30 am", 
"readMoreUrl": "https://www.timesnownews.com/amp/the-buzz/article/scientist-deliberately-feeds-himself-to-thousands-of-mosquitoes-in-quest-to-find-a-cure-for-diseases-watch/660612?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts ", 
"videoUrl": "https://www.youtube.com/"}, 
{"title": "\nOur nasal spray reduced COVID-19 growth in ferrets by up to 96%: Aus firm\n", 
"imageUrl": "https://static.inshorts.com/inshorts/images/v1/variants/jpg/m/2020/09_sep/28_mon/img_1601268915206_761.jpg?", 
"url": "https://www.inshorts.com/en/news/our-nasal-spray-reduced-covid19-growth-in-ferrets-by-up-to-96-aus-firm-1601270162650", 
"content": "Australian biotech company Ena Respiratory has said a nasal spray that it is developing to improve human immune system to fight common cold and flu significantly reduced coronavirus growth in a recent study on animals. INNA-051 reduced COVID-19 viral replication by up to 96% in ferrets, the company said. The study was led by British government agency Public Health England.", 
"author": "Ankush Verma", 
"date": "28 Sep 2020,Monday", 
"time": "10:46 am", 
"readMoreUrl": "https://mobile.reuters.com/article/amp/idUSKBN26J04S?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts ", 
"videoUrl": "https://www.youtube.com/"},
```
Each response object has the following keys -

    success - true indicates the api ran successfully. Upon error the success value is false and the object includes an errorMessage key with the error message.

    {
        "category": "sciencedfg",
        "data": [],
        "errorMessage": "Invalid Category",
        "success": false
    }

    category - the category you requested for.

    data - An array of objects each containing a news item for the category. Each object contains
        title
        content
        author
        imageUrl
        readMoreUrl(link to original news article)
        date and time of publish
        url (link to inshorts page)
        videoUrl(hardcoded can be changed for specific usecase)
