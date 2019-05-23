#Alex Greenman
#873392313
#this Python script counts the frequencies of characters in a text file. It also
#parses command line arguments that can be utilized to change what characters are
#counted
import sys
from string import ascii_lowercase
def add_frequencies(d,file_name,remove_case):
    '''This function counts character frequencies in the file
    and adds them to a dictionary. The remove_case parameter takes a boolean;
    when true, all characters in the file are converted lowercase and counted.
    When false, character count is case sensitive'''
    #open file and remove all spaces and newline characters, store in text
    with open(file_name, "r") as file:
        text = file.read()
        text=text.replace(" ", "")
        text=text.replace('\n',"")
    #conditional executed if remove_case parameter is 'True'
    if remove_case == True:
        #convert all characters to lowercase
        text=text.lower()
        #iterate over characters in text
        for character in text:
            #if character already in d, add one to its frequency count
            if character in d:
                d[character]+=1
            #if character not already in d, frequency count is one
            else:
                d[character]=1
    #conditional executed if remove_case parameter is 'False'
    else:
        for character in text:
            if character in d:
                d[character]+=1
            else:
                d[character]=1

def main():
    '''This function parses command line arguments. The command line arguments are
    processed and then the desired character frequencies are returned, for one
    or multiple files'''
    #set default parameters
    remove_case=True
    d={}
    empty_string=''
    #process the arguments
    argi=1
    while argi < len(sys.argv):
        #extract an argument
        arg=sys.argv[argi]
        #if argument does not start with '-', then break out of while loop
        if arg[0] != '-':
          break
        if arg=='-c':
            #adjust remove_case parameter so character count is case sensitive
            remove_case=False
        elif arg=='-z':
            #iterate over ascii_lowercase letters and set their frequency counts to zero
            for character in ascii_lowercase:
                d[character]=0
        elif arg == '-l':
            #increment argi by one and store the letters user wants counted in empty_string
            empty_string+=sys.argv[argi+1]
            argi+=1
        else:
            #if user passes in an unrecognized flag, make them aware
            print(f'Unrecognized Flag \'{arg}\'')
            argi+=1
        argi+=1

    #iterate over the remainder of sys.argv list, allowing for multiple files
    #to be processed
    for file_name in sys.argv[argi:]:
        #call add_frequencies to count frequencies based on flags
        add_frequencies(d, file_name, remove_case)

    for k, v in d.items():
        #if '-l' is in sys.argv, only print the letters that the user wants counted
        #in CSV format
        if '-l' in sys.argv:
            if k in empty_string:
                print(f'\"{k}\",{v}')
        #otherwise, just print the key value pairs in d in CSV format
        else:
            print(f'\"{k}\",{v}')

main()
