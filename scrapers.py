import requests_html
from models import JobListing


class OccParser:
    def parse(self, response, url):
        ciudad = response.html.find('#cityLink')


        estado = response.html.find('#stateLink')
        jornada = self.__getJornada(response)
        contratacion = self.__getContratacion(response)
        title = response.html.xpath('(//h1)[1]/text()')
        salary = response.html.find('#salary')
        description = response.html.find('#jobbody')

        return JobListing(url=url, 
                          city=ciudad[0].text if len(ciudad) > 0 else "",
                          state=estado[0].text if len(estado) > 0 else "",
                          salaryString=salary[0].text if len(salary) > 0 else "",
                          description=description[0].text if len(description) > 0 else "")

    def __getJornada(self, response):
        if(response.html.search('Tiempo completo') != None):
            return "Tiempo Completo"

        if(response.html.search('Medio tiempo') != None):
            return "Medio Tiempo"

        return ""

    def __getContratacion(self, response):
        if(response.html.search('Permanente') != None):
            return "Permanente"

        if(response.html.search('Temporal') != None):
            return "Temporal"

        return ""

        

        

        



