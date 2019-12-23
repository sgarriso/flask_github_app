import requests
import json
import time
import sqllite_helper 
# note we could do 60 but for testing and throtting reasons we will do just 3
def get_github_loads(minpage=1,maxpage=3):
    parsed_data = []
    for i in range(minpage,maxpage,1):
        data = get_github_load(i)
        parsed_data.append(parse(data))
    return parsed_data

        
    
def get_github_load(page=1):
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&page='+str(page)+'&per_page=100'
    return requests.get(url).json()
def upload_data_db_records(records,conn):
    def upload_data(record,conn):
        sqllite_helper.insert_value(conn,list(record.keys()),list(record.values()))
    for record in records:
        upload_data(record,conn)
def upload_patched_data_db_records(records,repo_ids,conn):
    def upload_data(record,repo_id,conn):
        sqllite_helper.update_value(conn,list(record.keys()),list(record.values()),repo_id)
    for record,repo_id in zip(records,repo_ids):
            upload_data(record,repo_id,conn)
def parse(data):
    MAX=2000
    def check_len(values):
        lookup = ['name','description','url']
        for key in lookup:
            if values[key] and len(values[key]) > MAX:
                values[key] = values[key][0:2000]
        return values
    data_values = {}
    values = []
        #Store the list of repositories in a database table. 
    #The table must contain the 
    #repository ID
    #, name
    #, URL
    #, created date
    #, last push date
    #, description
    #, and number of stars.
    for bit in data['items']:
        
        data_values['repository_ID'] = bit['id']
        data_values['name'] = bit['name']
        data_values['description'] = bit['description']
        data_values['created_date'] = bit['created_at']
        data_values['last_push_date'] = bit['pushed_at']
        data_values['url'] = bit['url']
        data_values['stars'] = bit['stargazers_count']
        data_values=check_len(data_values)
        values.append(data_values)
        data_values = {}
    return values
def compare(server_data,github_data):
    def get_repo_ids(server_data):
        ids = []
        for record in server_data:
            #print(record)
            ids.append(int(record['repository_ID']))
        return ids
            
    patched_data = []
    new_data = []
    repo_ids = []
    ids=get_repo_ids(server_data)
    #print(ids)
    for page in github_data:
        for record in page:
            if (record["repository_ID"]) in ids :
                # compare values in github data and server if diff add to patch:
                data = {}
                id_loc = ids.index(record["repository_ID"])
                for key in record.keys():
                    if key != "repository_ID":
                        if record[key] != server_data[id_loc][key]:
                            data[key] = record[key]
                            # bug with description saying there is a diff might need to write my own string compare
                            #if key == "description":
                             #   print((server_data[id_loc][key]))
                             #   print((record[key]))
                             #   print(str(record[key]) != str(server_data[id_loc][key]))
                if data:
                    repo_ids.append(record["repository_ID"])
                    patched_data.append(data)
                        
            else:
                new_data.append(record)
    return patched_data,new_data,repo_ids
def get_db_data(conn):
    return sqllite_helper.get_values(conn)
def main():
    conn=sqllite_helper.setup()
    while True:
        parsed_data = get_github_loads()
        db_data = get_db_data(conn)
        #print(db_data)
        patched_data,new_data,repo_ids = compare(db_data,parsed_data)
        #print(patched_data,new_data,repo_ids)
        upload_data_db_records(new_data,conn)
        db_data = get_db_data(conn)
        #print(db_data)
        upload_patched_data_db_records(patched_data,repo_ids,conn)
        #exit()
        # seconds , mins, one hour
        time.sleep(60 * 60 * 1)
def test_parse():
    parsed_data=get_github_loads()
    server_data = get_server_data()
    #print(server_data)
    #upload_data_records(parsed_data)
#test_parse()
def test_compare():
    #parsed_data=get_github_loads()
    parsed_data = [[{
    "repository_ID": "83222441",
    "name": "system-design-primer",
    "url": "https://api.github.com/repos/donnemartin/system-design-primer",
    "created_date": "2017-02-26T16:15:28Z",
    "last_push_date": "2019-12-09T03:35:45Z",
    "description": "Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.",
    "stars": 5
},    {"repository_ID": "1",
    "name": "system-design-primer",
    "url": "https://api.github.com/repos/donnemartin/system-design-primer",
    "created_date": "2017-02-26T16:15:28Z",
    "last_push_date": "2019-12-09T03:35:45Z",
    "description": "Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.",
    "stars": 78179}]]
    #server_data = get_server_data()
   # print(server_data)
    server_data = [{
    "id": 2097,
    "repository_ID": "83222441",
    "name": "system-design-primer",
    "url": "https://api.github.com/repos/donnemartin/system-design-primer",
    "created_date": "2017-02-26T16:15:28Z",
    "last_push_date": "2019-12-09T03:35:45Z",
    "description": "Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.",
    "stars": 78178
}]
    patched_data,new_data,repo_ids=compare(server_data,parsed_data)
    print(patched_data,new_data,repo_ids)
    #upload_data_records(new_data)
    #upload_patched_data_records(patched_data,repo_ids)
main()
    
    
