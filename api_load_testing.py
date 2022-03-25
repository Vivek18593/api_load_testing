import threading, requests, time, openpyxl
from termcolor import colored
import os
os.system('color')

print('   ************************')
print('   *   API LOAD TESTING   *')
print('   ************************')

#-----TEST API-----#
response_code = [200,201,202,204]
passed = 0
failed = 0
def checking_response(result,count,api):
    global passed, failed
    if result in response_code:
        print(str(count)+' : '+colored(str(result),'green')+' '+str(api)+colored(' >> ','cyan')+colored('Success','green'))
        passed+=1
    else:
        print(str(count)+' : '+colored(str(result),'red')+' '+str(api)+colored(' >> ','cyan')+colored('Failed','red'))
        failed+=1

def api_params(api,i,count):
    global passed, failed
    api = api.replace('data', 'data'+str(i))
    if method == 'get':
        try:
            result = requests.get(api).status_code
            checking_response(result,count,api)
        except:
            print(str(count)+' Request Failed!')
            failed+=1
    elif method == 'post':
        try:
            result = requests.post(api).status_code
            checking_response(result,count,api)
        except:
            print(str(count)+' Request Failed!')
            failed+=1
#**************#

#--------API LOAD TESTING--------#
counter = 1
def start_api_load_test(api):
    global counter
    start_time = time.perf_counter()
    threads = []
    for i in range(int(number_of_times_the_test_execute)):
        t = threading.Thread(target=api_params, args=[api,i+1,counter])
        t.start()
        threads.append(t)
        counter+=1
    for thread in threads:
        thread.join()
    end_time = time.perf_counter()
    print('\n')
    print(colored('[T] Time Taken: ','cyan'),colored(end_time-start_time,'yellow'),colored('second(s)','yellow'))
    print('Passed Test: '+colored(str(passed),'green'))
    print('Failed Test: '+colored(str(failed),'red'))
#********************************#


"""---EXECUTE---"""
status = True
while status:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    excel_file = current_dir+'\\data.xlsx'
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active
    rowcount = sheet.max_row
    param = ''
    for row in range(2,rowcount+1):
        p = sheet.cell(row,2).value
        param = param+str(p)+str('&')
    baseUrl = sheet.cell(1,2).value
    api_link = baseUrl+param[:-1]
    print(api_link)
    mthd = True
    while mthd:
        method = input('Test method (GET/POST): ').lower()
        if method == 'get' or method == 'post':
            num = True
            while num:
                number_of_times_the_test_execute = input('Number of test executions: ')
                if number_of_times_the_test_execute.isdigit():
                    start_api_load_test(api_link)
                    nxt = str(input('\nDo you want to continue?(Y or N): ')).lower()
                    if nxt == 'y':
                        num = False
                        status = True
                        passed = 0
                        failed = 0
                        counter = 1
                    else:
                        num = False
                        mthd = False
                        status = False
                    print('\n')
                else:
                    print('Not a number! Try again..')
                    num = True
        else:
            print('Method Incorrect! Try again..')
            mthd = True
    
    


