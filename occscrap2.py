from requests_html import HTMLSession
import xlsxwriter
import argparse


#column indexes
NUMERO = 0
TITULO_POSICION = 1
AREA = 2
ESPECIALIDAD = 3
DESCRIPCION_POSICION = 4
IDIOMA_1 = 5
NIVEL_IDIOMA_1 = 6
IDIOMA_2 = 7
NIVEL_IDIOMA_2 = 8
IDIOMA_3 = 9
NIVEL_IDIOMA_3 = 10
PAIS = 11
ESTADO = 12
CIUDAD = 13
TIPO_CONTRATACION = 14
JORNADA_LABORAL = 15
ANIOS_EXPERIENCIA = 16
MONEDA = 17
RANGO_SALARIAL = 18
MOSTRAR_SALARIO = 19
VIGENCIA_DIAS = 20
NOMBRE_EMPRESA = 21
DESCRIPCION_EMPRESA = 22
URL_ORIGINAL = 23



def openXlsxFile(filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Vacantes')

    
    # Write the dumbass header
    worksheet.write(1, NUMERO, '#')
    worksheet.write(1, TITULO_POSICION, 'Titulo de la posición')
    worksheet.write(1, AREA, 'Área')
    worksheet.write(1, ESPECIALIDAD, 'Especialidad')
    worksheet.write(1, DESCRIPCION_POSICION, 'Descripción de la posición')
    worksheet.write(1, IDIOMA_1, 'Idioma')
    worksheet.write(1, NIVEL_IDIOMA_1, 'Nivel')
    worksheet.write(1, IDIOMA_2, 'Idioma')
    worksheet.write(1, NIVEL_IDIOMA_2, 'Nivel')
    worksheet.write(1, IDIOMA_3, 'Idioma')
    worksheet.write(1, NIVEL_IDIOMA_3, 'Nivel')
    worksheet.write(1, PAIS, 'País')
    worksheet.write(1, ESTADO, 'Estado')
    worksheet.write(1, CIUDAD, 'Ciudad')
    worksheet.write(1, TIPO_CONTRATACION, 'Tipo de contratación')
    worksheet.write(1, JORNADA_LABORAL, 'Jornada laboral')
    worksheet.write(1, ANIOS_EXPERIENCIA, 'Años de experiencia')
    worksheet.write(1, MONEDA, 'Moneda')
    worksheet.write(1, RANGO_SALARIAL, 'Rango salarial')
    worksheet.write(1, MOSTRAR_SALARIO, 'Mostrar salario en anuncio')
    worksheet.write(1, VIGENCIA_DIAS, 'Vigencia (días)')
    worksheet.write(1, NOMBRE_EMPRESA, 'Nombre empresa')
    worksheet.write(1, DESCRIPCION_EMPRESA, 'Descripción empresa')
    worksheet.write(1, URL_ORIGINAL, 'URL original')

    return workbook

def writeOnXlsxFile(row, column, field, workbook):
    worksheet = workbook.get_worksheet_by_name('Vacantes')
    worksheet.write(row, column, field)

def closeXlsxFile(file):
    file.close()

async def getAbsoluteLink(session, link):
    h = await session.get(link)
    return h

def scrapWebsite(page):
    session = HTMLSession()
    r = session.get(f'https://www.occ.com.mx/empleos/trabajo-en-tecnologias-de-la-informacion-sistemas/?page={page}')
    links = list(filter(lambda x: "oferta" in x, r.html.links))
    session.close()

    workbook = openXlsxFile(f'vacantes_{page}.xlsx')

    row = 2
    for link in links:
        absoluteLink = (f'https://www.occ.com.mx{link}')
        microSession = HTMLSession()
        h = microSession.get(absoluteLink)
        h.html.render(sleep=10)
        print(absoluteLink)

        # Ciudad ? cityLink
        print('Ciudad')
        ciudad = h.html.find('#cityLink')
        if(len(ciudad) > 0):
            print(ciudad[0].text)
            writeOnXlsxFile(row, CIUDAD, ciudad[0].text, workbook)
        
        # Estado ? stateLink
        print('Estado')
        estado = h.html.find('#stateLink')
        if(len(estado) > 0):
            estado = estado[0].text
            estadoReplace = estado.replace(',', '')
            estadoTrim = estadoReplace.strip()
            print(estadoTrim)
            writeOnXlsxFile(row, ESTADO, estadoTrim, workbook)

        # Jornada laboral
        print('Jornada')
        if(h.html.search('Tiempo completo') != None):
            print('Tiempo Completo')
            writeOnXlsxFile(row, JORNADA_LABORAL, 'Tiempo Completo', workbook)

        if(h.html.search('Medio tiempo') != None):
            print('Medio Tiempo')
            writeOnXlsxFile(row, JORNADA_LABORAL, 'Medio Tiempo', workbook)
        
        # Contratacion
        print('Contratacion')
        if(h.html.search('Permanente') != None):
            print('Permanente')
            writeOnXlsxFile(row, TIPO_CONTRATACION, 'Permanente', workbook)

        if(h.html.search('De temporal') != None):
            print('Temporal')
            writeOnXlsxFile(row, TIPO_CONTRATACION, 'Temporal', workbook)

        # Categoría 1
        print('Categoria 1')
        categoria1 = h.html.find('.c01614.c01620.c01633.c01685')
        if(len(categoria1) > 0):
            print(categoria1[0].text)
            writeOnXlsxFile(row, AREA, categoria1[0].text, workbook)


        # Titulo de la vacante
        print('Titulo')
        titulo = h.html.find('.c01614.c01619.c01633.c01641.c01623')
        if(len(titulo) > 0):
            print(titulo[0].text)
            writeOnXlsxFile(row, TITULO_POSICION, titulo[0].text, workbook)

        # Salario
        print('Salario')
        salario = h.html.find('#salary')
        if(len(salario) > 0):
            print(salario[0].text)
            writeOnXlsxFile(row, RANGO_SALARIAL, salario[0].text, workbook)

        # Descripción
        print('Descripción')
        divDescripcion = h.html.find('#jobbody')
        if(len(divDescripcion) > 0):
            print(divDescripcion[0].text)
            writeOnXlsxFile(row, DESCRIPCION_POSICION, divDescripcion[0].text, workbook)

        writeOnXlsxFile(row, URL_ORIGINAL, absoluteLink, workbook)

        microSession.close()
        row = row + 1
    closeXlsxFile(workbook)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", help="la pinche pagina no mames",
                    type=int)
    args = parser.parse_args()
    page = 1
    if(args.page):
        page = args.page

    print(page)
    
    scrapWebsite(page)
    #writeXlsxFile()


if __name__ == "__main__":
    main()