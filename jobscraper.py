from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
import scrapers
import argparse
import asyncio

import xlsoutput
import dbconnection

def saveJob(job, datasource):
    if(datasource == 1):
        xlsoutput.insertJob(job)

    if(datasource == 2):
        dbconnection.insertJob(job)

    

async def renderChildPage(link, datasource):
    miniSession = AsyncHTMLSession()
    scraper = scrapers.getParser(1)

    h = await miniSession.get(link)
    await h.html.arender(timeout=15, sleep=10)
    await miniSession.close()    
    job = scraper.parse(h, link)
    saveJob(job, datasource)
    return job

async def scrapWebsite(page, datasource):
    session = HTMLSession()
    r = session.get(f'https://www.occ.com.mx/empleos/trabajo-en-tecnologias-de-la-informacion-sistemas/?page={page}')
    links = list(filter(lambda x: "oferta" in x, r.html.links))
    session.close()

    #Async render 
    coros = [renderChildPage((f'https://www.occ.com.mx{link}'), datasource) for link in links]
    results = await asyncio.gather(*coros)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", help="which result page should we pick",
                    type=int)
    parser.add_argument("--jobsite", help="which jobsite should be parsed (OCC = 1, CT = 2)", type=int)
    parser.add_argument("--datasource", help="specify whether we should save the parse result on a database or an xml (DB=1,XML=2)", type=int)

    args = parser.parse_args()
    page = 1
    datasource = 1
    if(args.page):
        page = args.page

    if(args.datasource):
        datasource = args.datasource
    

    print(page)
    asyncio.run(scrapWebsite(page, datasource))


if __name__ == "__main__":
    main()