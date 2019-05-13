import couchdb
from couchdb import design
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from math import ceil

couch=couchdb.Server('http://admin:admin@172.26.37.214:5984/')
db1 = couch['marvel_tweets']
db2 = couch['marvel_user_timelines']
db3 = couch['got_tweets']
db4 = couch['got_user_timelines']

map_function_realted = """function (doc) {
  emit(doc.user_screen_name, doc.sentiment_score);
}"""

map_function_all = """function (doc) {
  emit(doc.user, doc.sentiment);
}"""

map_function_month = """function (doc) {
  emit(doc.month, doc.sentiment_score);
}"""

map_function_year = """function (doc) {
  emit(doc.year, doc.sentiment_score);
}"""

reduce_function = """function (keys, values, rereduce) {
return sum(values)/values.length
}"""


# delete existing disign docs with the same name
def deleteDesignDocUser(db):
    db.delete(db['_design/user_senti'])


def deleteDesignDocTime(db):
    db.delete(db['_design/time_senti'])


# create view for our marvel_topic2
def create_views_year(db):
    view = design.ViewDefinition('time_senti', 'mapreduce', map_function_year, reduce_function)
    view.sync(db)


# create view for our game of thrones_topic2
def create_views_month(db):
    view = design.ViewDefinition('time_senti', 'mapreduce', map_function_month, reduce_function)
    view.sync(db)
    row1s = db3.view('time_senti/mapreduce', descending=True, group=True)
    for row1 in row1s:
        print(row1)


#create views for marvel_topic1 and game of thrones_topic1
def create_views_related(db):
    map_tweets = map_function_realted
    reduce_senti = reduce_function
    view = design.ViewDefinition('user_senti', 'mapreduce', map_tweets, reduce_senti)
    view.sync(db)


def create_views_all(db):
    map_tweets = map_function_all
    reduce_senti = reduce_function
    view = design.ViewDefinition('user_senti', 'mapreduce', map_tweets, reduce_senti)
    view.sync(db)


# # get month in a specific year
# def conbineyearmonth():
#     # dbtest.delete(dbtest['special/special'])
#     map_fun_special = '''function(doc){
#      emit(doc.id, doc.user_screen_name);
#      }'''
#     view = design.ViewDefinition('special', 'special', map_fun_special)
#     view.sync(dbtest)
#     for row in dbtest.view('special/special', descending=True):
#         doc = dbtest[row.id]
#         doc['month'] = dbtest[row.id]['year']+dbtest[row.id]['month']
#         dbtest.delete(dbtest[row.id])
#         dbtest.save(doc)


# create all the views
def createforall():
    deleteDesignDocUser(db1)
    deleteDesignDocUser(db2)
    create_views_related(db1)
    create_views_all(db2)
    deleteDesignDocUser(db3)
    deleteDesignDocUser(db4)
    create_views_related(db3)
    create_views_all(db4)
    deleteDesignDocTime(db1)
    create_views_year(db1)
    deleteDesignDocTime(db3)
    create_views_month(db3)


# produce the marvelyear.html with a line chart in it
def get_result_for_year():
    dict1 = {}
    row1s = db1.view('time_senti/mapreduce', descending=True, group=True)
    for row1 in row1s:
        if int(row1['key']) >= 2015 :
            dict1[row1['key']] = float(row1['value'])
    for key, value in dict1.items():
        print('{key}:{value}'.format(key=key, value=value))
    d = {}
    for key in sorted(dict1.keys()):
        d[key] = round(dict1[key],3)
    # d = sorted(dict1.items(), key=lambda k: k[0])
    print(d)
    line = Line()
    line.add_xaxis(list(d.keys())) \
        .add_yaxis('Average Sentiment', list(d.values()), symbol = 'circle', symbol_size = 10) \
        .set_global_opts(
        title_opts=opts.TitleOpts(pos_bottom='0%', pos_left='center', title='Average Sentiment Related to Marvel Movies')
    )
    line.render(path='./templates/marvelyear.html')
    print('successful!!!')


#  produce the gotmonth.html with a line chart in it
def get_result_for_month():
    dict1 = {}
    row1s = db3.view('time_senti/mapreduce', descending=True, group=True)
    for row1 in row1s:
        print(row1)
        if row1['key'] == 'Jan':
            dict1[1] = float(row1['value'])
        if row1['key'] == 'Feb':
            dict1[2] =  float(row1['value'])
        if row1['key'] == 'Mar':
            dict1[3] = float(row1['value'])
        if row1['key'] == 'Apr':
            dict1[4] =  float(row1['value'])
        if row1['key'] == 'May':
            dict1[5] = float(row1['value'])
    for key, value in dict1.items():
        print('{key}:{value}'.format(key=key, value=value))
    d = {}
    for key in sorted(dict1.keys()):
        d[key] = round(dict1[key], 3)
    # d = sorted(dict1.items(), key=lambda k: k[0])
    print(d)
    line = Line()
    line.add_xaxis(['January','February','March','April','May']) \
        .add_yaxis('Average Sentiment', list(d.values()), symbol = 'circle', symbol_size = 10) \
        .set_global_opts(
        title_opts=opts.TitleOpts(pos_bottom='0%', pos_left='center', title='Average Sentiment Related to Game of Thrones')
    )
    line.render(path='./templates/gotmonth.html')
    print('successful!!!')


# produce the html files for marvel&got topic1 with bar charts in them
def calcule_result_for_user(db_first, db_second, pathfile, yname, titlename):
    dict1 = {}
    dict2 = {}
    row1s = db_first.view('user_senti/mapreduce', descending=True, group=True)
    row2s = db_second.view('user_senti/mapreduce', descending=True, group=True)
    i = 0
    for row1 in row1s:
        dict1[row1['key']] = float(row1['value'])
        # for key, value in dict1.items():
        #     print('{key}:{value}'.format(key=key, value=value))
    for row2 in row2s:
        dict2[row2['key']] = float(row2['value'])
        # for key, value in dict2.items():
        #     print('{key}:{value}'.format(key=key, value=value))
    for key, value in dict2.copy().items():
        if key in dict1.keys():
                dict2[key] = abs(dict1[key]-dict2[key])
                print(i)
                i += 1
        else:
                dict2.pop(key)
    for key, value in dict2.items():
        print('{key}:{value}'.format(key=key, value=value))
    dict = dict2
    bar = Bar()
    lista = list(dict.values())
    print(lista)
    for i in range(len(lista)):
        lista[i] = ceil(10 * round(lista[i], 2)) / 10
    print(sorted(lista))
    count_dict = {}
    for item in sorted(lista):
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    total = sum(count_dict.values())
    for key in count_dict.keys():
        count_dict[key] = 100 * round(float(count_dict[key]) / total, 2)
    print(list(count_dict.values()))
    bar.add_xaxis(list(count_dict.keys())) \
        .add_yaxis(yname, list(count_dict.values()),label_opts=opts.LabelOpts(formatter='{c}%')) \
        .set_global_opts(
        title_opts=opts.TitleOpts(pos_bottom='0%', pos_left='center', title=titlename)
        )
    bar.render(path = pathfile)
    print('successful!!!')

if __name__ == '__main__':

    createforall()

    calcule_result_for_user(db1, db2, './templates/marveluser.html','Percentage of All Marvel Users', 'Sentiment Changes When mention Marvel Related Content')
    calcule_result_for_user(db3, db4, './templates/gotuser.html','Percentage of All GOT Users', 'Sentiment Changes When mention Game of Thrones Related Content')

    get_result_for_year()
    get_result_for_month()

