from math import ceil
from flask import Flask
from datetime import datetime as dt
from pytz import timezone
app = Flask(__name__)
restemp = ['Geonameid', 'Name', 'Ascii name', 'Alternate names', 'Latitude', 'Longitude', 
        'Feature class', 'Feature code', 'Country code', 'Country code 2', 'Admin1 code', 'Admin2 code', 
        'Admin3 code', 'Admin4 code', 'Population', 'Elevation', 'DEM', 'Timezone', 'Modification date']
@app.route('/')
def hello_world():
    return 'Начальная страница, скрипт запущен =)'

@app.route('/geonameid/<geonameid>')
def objectinfo(geonameid):
        with open('RU.txt', mode='r') as data:
                res = ''
                for record in data:
                        prsdstr = record.split('\t')
                        if prsdstr[0] == geonameid:
                                if prsdstr[6] == 'P':
                                        for i in range(1, len(restemp)):
                                                if prsdstr[i] != '':
                                                        res += f'{restemp[i]}: {prsdstr[i]}<br>'
                                                elif prsdstr[i] == '':
                                                        res += f'{restemp[i]}: -<br>'
                                        return res
                                elif prsdstr[6] != 'P':
                                        res += 'Это, конечно, не город =), но вот информация:<br>'
                                        for i in range(1, len(restemp)):
                                                if prsdstr[i] != '':
                                                        res += f'{restemp[i]}: {prsdstr[i]}<br>'
                                                elif prsdstr[i] == '':
                                                        res += f'{restemp[i]}: -<br>'
                                        return res


@app.route('/page/<p>/<n>')
def page(p, n):
        with open('RU.txt', mode='r') as data:
                c = 0
                cities = []
                for record in data:
                        if record.split('\t')[6] == 'P':
                                c += 1
                                cities.append(record.split('\t'))
                nint = int(n)
                pint = int(p)
                pagenum = ceil(c / nint)
                np = cities[(pint-1) * nint : ((pint-1) * nint) + nint]
                res = ''
                for i in np:
                        recres = ''
                        for r in range(len(restemp)):
                                if i[r] != '':
                                        if r < len(restemp) - 1:
                                                recres += f'{restemp[r]}: {i[r]}, '
                                        elif r == len(restemp) - 1:
                                                recres += f'{restemp[r]}: {i[r]}<br>'
                                elif i[r] == '':
                                        if r < len(restemp) - 1:
                                                recres += f'{restemp[r]}: -, '
                                        elif r == len(restemp) - 1:
                                                recres += f'{restemp[r]}: -<br>'
                        res += recres
                return res

@app.route('/cities/<frst>/<scnd>')
def cities(frst,scnd):
        slovar = {'ый':'yy','ье':"ye",'ое':'oye','ае':'aye','ее':'eye',
        'ие':'iye','уе':'uye','ые':'yye','а':'a','б':'b','в':'v',
        'г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i',
        'й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
        'с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh',
        'щ':'shch','ъ':'','ы':'y','э':'e','ю':'yu','я':'ya', 'А':'A',
        'Б':'B','В':'V','Г':'G','Д':'D','Е':'Ye','Ё':'Yo','Ж':'Zh','З':'Z','И':'I',
        'Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R',
        'С':'S','Т':'T','У':'U','Ф':'F','Х':'H','Ц':'Ts','Ч':'Ch','Ш':'Sh',
        'Щ':'Shch','Ъ':'','Ы':'y','Э':'E','Ю':'Yu','Я':'Ya',' ':' ',
        ',':'','?':'','~':'','!':'','@':'','#':'','$':'','%':'','^':'',
        '&':'','*':'','(':'',')':'','-':'','=':'','+':'',':':'',';':'','<':'',
        '>':'','\'':'','"':'','\\':'','/':'','№':'','[':'',']':'','{':'',
        '}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i','Є':'e', '—':'','ь':''}
        with open('RU.txt', mode='r') as data:
                cities = []
                for record in data:
                        if record.split('\t')[6] == 'P':
                                cities.append(record.split('\t'))
                altnames = []
                noaltnames = []
                for c in cities:
                        if c[3] != '':
                                altnames.append(c)
                        elif c[3] == '':
                                noaltnames.append(c)
                neededfrst = []
                neededscnd = []
                final = []
                frstorig = frst
                scndorig = scnd              
                for key in slovar:
                        frst = frst.replace(key, slovar[key])
                        scnd = scnd.replace(key, slovar[key])
                for city in altnames:
                        if frstorig == city[3].split(',')[-1] or frst == city[3].split(',')[-1]:
                                neededfrst.append(city)
                        elif scndorig == city[3].split(',')[-1] or scnd == city[3].split(',')[-1]:
                                neededscnd.append(city)
                for cit in noaltnames:
                        if frst == cit[2].replace("'", ""):
                                neededfrst.append(cit)
                        elif scnd == cit[2].replace("'", ""):
                                neededscnd.append(cit)
                if len(neededfrst) != 0 and len(neededfrst) > 1:
                        pop = []
                        for i in neededfrst:
                                pop.append(int(i[-5]))
                        final.append(neededfrst[pop.index(max(pop))])
                        neededfrst.remove(neededfrst[pop.index(max(pop))])
                        if frstorig == scndorig:
                                pop = []
                                for i in neededfrst:
                                        pop.append(int(i[-5]))
                                neededscnd.append(neededfrst[pop.index(max(pop))])
                elif len(neededfrst) == 1:
                        final.append(neededfrst[0])
                        if frstorig == scndorig:
                                return 'К сожалению город с таким названием в базе только один.'
                if len(neededscnd) != 0 and len(neededscnd) > 1:
                        pop = []
                        for i in neededscnd:
                                pop.append(int(i[-5]))
                        final.append(neededscnd[pop.index(max(pop))])
                elif len(neededscnd) == 1:
                        final.append(neededscnd[0])
                if len(neededfrst) != 0 and len(neededscnd) != 0:
                        date = dt.now()
                        tz1 = timezone(final[0][-2])
                        tz2 = timezone(final[1][-2])
                        tzdiff = int((tz1.localize(date) - tz2.localize(date).astimezone(tz1)).seconds/3600)
                        if tzdiff <= 12:
                                tzdiff = tzdiff
                        elif tzdiff > 12:
                                tzdiff = 24 - tzdiff
                        if float(final[0][4]) > float(final[1][4]):
                                final.append(f'Первый город ({frstorig}) севернее второго ({scndorig}).')
                        elif float(final[0][4]) < float(final[1][4]):
                                final.append(f'Второй город ({scndorig}) севернее первого ({frstorig}).')
                        if final[0][-2] == final[1][-2]:
                                final.append(f'Оба города находятся в одной временной зоне: {final[0][-2]}.')
                        elif final[0][-2] != final[1][-2]:
                                final.append(f'Города находятся в разных временных зонах.<br>'
                                f'Первый в зоне {final[0][-2]}, второй в зоне {final[1][-2]}, '
                                f'а разница между ними составляет {tzdiff} ч.')
                        res = ''
                        for i in range(len(final)):
                                if i == 0:
                                        res += f'<p>{frstorig}:<br>'
                                        for it in range(len(final[i])):
                                                if it < len(final[i]) - 1:
                                                        res += f'{restemp[it]}: {final[i][it]}<br>'
                                                elif it == len(final[i]) - 1:
                                                        res += f'{restemp[it]}: {final[i][it]}</p>'
                                elif i == 1:
                                        res += f'<p>{scndorig}:<br>'
                                        for it in range(len(final[i])):
                                                if it < len(final[i]) - 1:
                                                        res += f'{restemp[it]}: {final[i][it]}<br>'
                                                elif it == len(final[i]) - 1:
                                                        res += f'{restemp[it]}: {final[i][it]}</p>'
                                elif i == 2 or i == 3:
                                        res += f'<p>{final[i]}</p>'
                        return res
                elif len(neededfrst) == 0 and len(neededscnd) == 0:
                        return 'Таких городов нет в базе или же это и не города вовсе.'
                elif len(neededfrst) == 0 and len(neededscnd) != 0:
                        return 'Первого города нет в базе или это не город.'
                elif len(neededfrst) != 0 and len(neededscnd) == 0:
                        return 'Второго города нет в базе или это не город.'



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)