#!/bin/env python
# add your header here
#
"""Cloned on the repository and recieved as template by Asmita Gautam
Assignment 09: Data Quality checking
Data Quality checking for a given meterologoical datasets
And ploting the comparision of each variables before and after quality checking
Modified for comments on 2020-03-08
"""
# Importing the required module
import pandas as pd
import numpy as np

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')

   
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF)
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    DataDF=DataDF.replace([-999],np.NaN)  #Using numpy module to replace -999 with NaN
    ReplacedValuesDF.loc['1. No Data',:]=DataDF.isna().sum()
    #Used to count no of nan in the each column

    return( DataDF, ReplacedValuesDF )

def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
    DataDF.Precip[(DataDF['Precip']>25) | (DataDF['Precip']<0)]=np.nan  #Replacing precipitation out of range 0<P>25 with nan
    DataDF['Wind Speed'][(DataDF['Wind Speed']>10) | (DataDF['Wind Speed']<0)]=np.nan 
    DataDF.loc[(DataDF['Max Temp']>35),['Max Temp']]=np.nan
    DataDF.loc[(DataDF['Min Temp']<-25),['Min Temp']]=np.nan
    DataDF.loc[(DataDF['Min Temp']>35),['Min Temp']]=np.nan
    DataDF.loc[(DataDF['Max Temp']<-25),['Max Temp']]=np.nan
    ReplacedValuesDF.loc['2. Gross Error',:]=DataDF.isna().sum()- ReplacedValuesDF.sum()
    #Use to count the no of nan in each column
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    DataDF.loc[DataDF['Min Temp']>DataDF['Max Temp'],['Min Temp','Max Temp']]= np.nan 
    #Replacing the min and max temp datapoints where maximum temp is lower than minimum temp 
    
    ReplacedValuesDF.loc['3. Swapped',:]=DataDF.isna().sum()- ReplacedValuesDF.sum()
    # adding the count as a column in the replacedvaluesdf with a row index as 3.Swapped
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""

    DataDF.loc[(DataDF['Max Temp']-DataDF['Min Temp']>25),['Max Temp','Min Temp']]=np.nan  #Replacing the datapoint of max and min temp with nan
    ReplacedValuesDF.loc['4. Range', :]=DataDF.isna().sum()-ReplacedValuesDF.sum()
    # adding the count as a column in the replacedvaluesdf with a row index as 4.Rangefail
    return( DataDF, ReplacedValuesDF )
    
if __name__ == '__main__':
    
    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    
    ###Creating comparision plots
     ##Reopening the datafile for the raw data to compare
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']
    RawData = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    RawData = RawData.set_index('Date')
    
    import matplotlib.pyplot as plt #Importing the required module
    """Precipitation correction comparision figure"""
    f1=plt.figure()
    ax1=f1.add_subplot(1,1,1)        
    ax1.plot(DataDF.index,RawData['Precip'],'r',label='Raw Data')
    ax1.plot(DataDF.index,DataDF['Precip'],'g',label='After Correlation')
    plt.legend(loc="lower left") #deciding the loaction to show legend
    plt.ylabel('Precipitation (mm)')
    plt.xlabel('Date')
    plt.title('Preciptation Raw vs QC')              
    plt.savefig('Precipitation.pdf')
    plt.show()
    plt.close()
    """Maximum temp correction comparision figure"""
    f2=plt.figure()
    ax2=f2.add_subplot(1,1,1)
    ax2.plot(DataDF.index,RawData['Max Temp'],'r',label='Raw Data')
    ax2.plot(DataDF.index,DataDF['Max Temp'],'g',label='After Correlation')
    plt.legend(loc="lower left")
    plt.ylabel('Maximum Temp (Celcius)')
    plt.xlabel('Date')
    plt.title('Maximum Temp Raw vs QC')
    plt.savefig('MaxTemp_plot.pdf')     #Saving figure to pdf
    plt.show()
    plt.close()

    """Minimum temp correction comparision fig"""
    f3=plt.figure()
    ax3=f3.add_subplot(1,1,1)
    ax3.plot(DataDF.index,RawData['Min Temp'],'r',label='Raw Data')
    ax3.plot(DataDF.index,DataDF['Min Temp'],'g',label='After Correlation')
    plt.legend(loc="lower left")
    plt.ylabel('Minimum Temp (Celcius)')
    plt.xlabel('Date')
    plt.title('Minimum Temp Raw vs QC')               
    plt.savefig('MinTemp_plot.pdf')     #Saving figure to pdf
    """Wind Speed correction comparaision figure"""
    f4=plt.figure()
    ax4=f4.add_subplot(1,1,1)
    ax4.plot(DataDF.index,RawData['Wind Speed'],'r',label='Raw Data')
    ax4.plot(DataDF.index,DataDF['Wind Speed'],'g',label='After Correlation')
    plt.legend(loc="upper right")
    plt.ylabel('Wind Speed (m/s)')
    plt.xlabel('Date')
    plt.title('Wind Speed Raw vs QC')               
    plt.savefig('Wind Speed_plot.pdf')     #Saving figure to pdf
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    """Data Output"""
    DataDF.to_csv('Quality_Checked_Data.txt',sep='\t', index=True)#To save quality checked data to txt file
    ReplacedValuesDF.to_csv('Replaced_Values_info.txt', sep = '\t', index= True)# To save the corrected data info to tab deliminated files
    
    