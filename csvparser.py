## **********************************************************************
## Console Spreadsheet Evaluator
## Version: 1.0.2
## Author: Steven Chuob
## Date: 10/23/2015
## email: schuob@gmail.com
##
## Description
## This script will parse a CSV file from the arguments during execution.
##
## Expected values in each cell is either: integer/float, cell reference
## or a mathematical operation written in postfix format.
##
## required python libraries
## csv - for handling of csv files and to read it as a dict for easier
## easier handling
##
## re - for regular expressions
## collections - for OrderedDict
## **********************************************************************
import csv
import re
from collections import OrderedDict

## debug flag
debug = False


## **********************************************************************
## Operators for POSTFIX form (RPN) calculations
## **********************************************************************
OP_SPACE= ' '
OP_EQUAL = '='
OP_PLUS = '+'
OP_MINUS = '-'
OP_MULT = '*'
OP_DIV = '/'
OP_ATTR = {
	OP_PLUS: {'prcd': 1, 'fn': lambda a, b: a + b},
	OP_MINUS: {'prcd': 1, 'fn': lambda a, b: a - b},
	OP_MULT: {'prcd': 2, 'fn': lambda a, b: a * b},
	OP_DIV: {'prcd': 2, 'fn': lambda a, b: a / b},
}

## **********************************************************************
## Creating a regex expression pattern to use for matching purposes
## **********************************************************************
sep_re = re.compile(r'\s*(%s|%s|%s|%s|%s|%s)\s*' % (
    re.escape(OP_SPACE),
    re.escape(OP_EQUAL),
	re.escape(OP_PLUS),
	re.escape(OP_MINUS),
	re.escape(OP_MULT),
	re.escape(OP_DIV)))

## **********************************************************************
## @tokenize(string)
## Using the regular expression pattern created, split the values into
## single value and storing them into a list
## **********************************************************************
def tokenize(expr):
	return [t.strip() for t in sep_re.split(expr.strip()) if t]


## **********************************************************************
## @calc_postfix(array)
## Calculator to do simple mathmatical operations: + - * /
## **********************************************************************
def calc_postfix(tokens):
    result, stack = 0, []
    
    ## taking each value in the token to execute math operations
    for tok in tokens:
        if tok in OP_ATTR:
            op1, op2, result = stack.pop(), stack.pop(), 0
            try:
                stack.append(OP_ATTR[tok]['fn'](op2, op1))
            except ZeroDivisionError:
                raise ValueError('%s %s %s ?!' % (op2, tok, op1))
        else:
            stack.append(float(tok))

    if len(stack) != 1:
        raise ValueError("invalid expression, operatiors and operands don't match")
    
    ## debug options
    if debug == True:
        print 'math output: ', stack.pop()

    return stack.pop()

## **********************************************************************
## @calculate(string)
## Prepping the value extracted for calculation or it will return an
## integer or string for further determination
## **********************************************************************
def calculate(expr):
    tokens = tokenize(expr)
    
    ## debug options
    if debug == True:
        print 'value',expr,tokens
    
    ## Checking for '=' and empty spaces in the array and destroying them
    ## from the array so that it does not get included in the calculation
    tok_counter = 0
    for tok in tokens:
        if tok == '=' or tok == '':
            tokens.pop(tok_counter)
        tok_counter = tok_counter + 1

    ## Once the '=' and empty_space have been destory we are left with
    ## a few outcome.
    ##
    ## An array with the size == 1 or size > 1
    ## If the array's size == 1 that means the value is an integer or
    ## string. This will be returned to the main function, if it's a
    ## string value additional checks will be done.
    ##
    ## If the array's size > 1 that means the value is a postfix
    ## mathmatical operation. The value will be handled by
    ## @calc_postfix.
    if len(tokens) == 1:
        try:
            float(tokens[len(tokens)-1])
            return float(tokens[len(tokens)-1])
        except:
            return str(tokens[len(tokens)-1])
    else:
        return calc_postfix(tokens)

## **********************************************************************
## @csvparser(string)
## Taking the CSV file and updating the keys to match an excel
## spreadsheet columns, this will allow searching by rows and keys.
## 
## We will also drop all empty cells and rows, also this function will
## sort the dictionary by using OrderDict as Python's Dictionary does
## not sort..
## **********************************************************************
def csvparser(file):
    ## new array for the rows
    tmp_dict = {}
    counter =1
    
    ## opening the csv and reading row by row, delimiting on ','
    with open(file, 'rb') as csvfile:
        csvdata = csv.DictReader(csvfile, delimiter=',', dialect=csv.excel_tab)
        for row in csvdata:
            tmp_row = {}
            
            ## debug options
            if debug == True:
                print 'row',counter,row
            
            ## the assumption here is that there is a header row in place
            ## ranging from A-Z.
            for key,value in row.items():
                ## updating the key so we don't have duplicare keys, by
                ## default DictReader will take the header and use it as
                ## the key per row. Instead we want the keys to be similar
                ## to excel cells: A1, A2
                tmp_row.update({str(key)+str(counter):value})
                
                ## Dropping empty cells
                drop_empty_columns = dict((k, v) for k, v in tmp_row.iteritems() if v)
                if debug == True:
                    print 'drop_empty_columns',drop_empty_columns
                
                ## ensuring the row is sorted properly
                sort_dict = OrderedDict(sorted(drop_empty_columns.items()))
            
            tmp_dict.update({str(counter):sort_dict})
            counter = counter + 1
            
            ## Dropping empty rows
            drop_empty_row = dict((k, v) for k, v in tmp_dict.iteritems() if v)
            parse_results = OrderedDict(sorted(drop_empty_row.items()))

    return parse_results

## **********************************************************************
## @csvref()
## **********************************************************************
def csvref(data, ref):
    
    ## breaking the reference number into LETTER and ROW for easier search
    ref_array = re.split('(\d+)',ref)
    ref_array.pop(2)
    col = ref_array[0]
    row = ref_array[1]
    
    try:
        expr = (data[row][ref])
        return calculate(expr)
    except KeyError:
        return 'null'

## **********************************************************************
##  @main()
## **********************************************************************
if '__main__' == __name__:
    import sys
    output = {}
        
    ## Extracting the filename from the parameter and sending it to
    ## the csv parser for cleaning up.
    if len(sys.argv) == 2:
        file = sys.argv[1]
        results = csvparser(file)
        
        ## debug options
        if debug == True:
            print 'data',results

        ## Taking the parse data and figuring out what to do with the
        ## cell values..
        for row_num in results:
            tmp_output_row = []
            row_data = results[row_num]
        
            ## Looping through each row's cell and extracting the
            ## value for each cell for calculation
            for key in row_data:
                expr = row_data[key]
                result = calculate(expr)
            
                ## @result should only return 2 types for consideration
                ## Expected values of results are going to be:
                ## string or an integer/float
                ##
                ## If it's a string, that means the cell value is referencing
                ## another cell and additional checks need to be done before
                ## it's placed into the array.
                ##
                ## If it's an integer/float it will add the out into a temp
                ## array for printing later.
                if str(type(result)) == "<type 'str'>":
                    ref_result = csvref(results,result)
                    out = str(key) + '=>' + str(ref_result)
                    tmp_output_row.append(out)
                else:
                    out = str(key)+ '=>' + str(result)
                    tmp_output_row.append(out)

            ## Output the original row's value, then calculation done for those
            ## values. The calculation format: cell#=> value of calculation
            print 'original: ',row_data.values(),',','calculation:',tmp_output_row
    else:
        print 'Error, no csv file has been specify or more then one file was specify'
        print '\n'
        print 'Usage: python csvcalculator.py csvfile_path'