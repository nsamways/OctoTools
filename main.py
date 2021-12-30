# This is the main octotools script file
import requests, random, math, os, csv, sys, json, configparser, glob
from dateutil import parser
        

def main():
    
    # set defaults
    output_path = os.curdir
    input_path = os.curdir
    
    # read in main config files 
    config_files = glob.glob(os.path.join(input_path, '*.ini'))

    config = configparser.ConfigParser()
    config.read(config_files)

    # set up output path
    write_path = os.path.join(output_path,"Results.csv")
    outfile_name = open(write_path,'w') 
    outfile_handle = csv.writer(outfile_name)

    row_headers = ["stim_file_name","name","min_x","min_y","max_x","max_y"]
    outfile_handle.writerow(row_headers)
    
    
    # collect the data from the Octopus server
    # compile the request string based on the config file
    
    targetURL = config['Main Parameters']['base address'] + config['Main Parameters']['MPAN'] + '/meters/' + config['Main Parameters']['meter serial']
    targetURL = targetURL + '/consumption/'
    
    URLParams = {'page_size' : config['Advanced']['page size']}
        
    r = requests.get(targetURL , auth=(config['Main Parameters']['API key'],'') , params=URLParams)
    
    #print(r.url)
    #print(r.status_code)   
    
    # Extract the JSON data
    JSONResults = r.json()
    
    # process the messy JSON object
    cleanResults = []
    singleEntry = []
    
    
    print('number of results returned is: '+ str( len(JSONResults['results'])))

    for entries in JSONResults['results']:
        
        st = parser.parse(entries['interval_start'])
        et = parser.parse(entries['interval_end'])       
        con = entries['consumption']
        
        singleEntry = [st, et, con]
    
        cleanResults.append(singleEntry)
        
        singleEntry = []
    
    for i in range(10):    
        #print(cleanResults[i])
        date_time = cleanResults[i][1].strftime("%m/%d/%Y_%H:%M:%S")
        print("on " + date_time + " Consumption was: " + str(cleanResults[i][2]))
           
    # write out
    
    currentRow = []
    
    for i in range(1000):
        #print the end date
        date_time = cleanResults[i][1].strftime("%m/%d-%H:%M")
        currentRow.append(date_time)      
        
        #print the consumption
        currentRow.append(str(cleanResults[i][2]))
        outfile_handle.writerow(currentRow)
        currentRow = []
    
    # close the file for writing
    outfile_name.close()
    
    # debug
if __name__ == "__main__":
    main()