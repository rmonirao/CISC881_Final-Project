"""
CISC881 - Final Project
Katya Dunets and Monica Rao
Queen's University, School of Computing

This program pre-processed lung CT scans and saves a 4D array of cropped 3D images
as well as an associated array of classifications in order to be used for modeling
"""

import pandas as pd
import SimpleITK as sitk
import skimage as sk
import numpy as np 
import csv
import os 

def csv_cleaning():
    """
    This function filters through the CSV file of candidate locations and keeps only the 
    locations with images that were downloaded. It also takes a random sample of 1420
    non-nodule images in order to reduce the number of coordinates.
    """
    
    data_path = "/Users/katyadunets/Desktop/CISC881Project/Project_Data/All_Data"
    files = os.listdir(data_path)
    
    image_name_list = []
    
    for item in files:
        item_name = item[0:64]
        image_name_list.append(item_name)
        
        
    with open("/Users/katyadunets/Desktop/CISC881Project/Project_Data/candidates.csv", "r+") as csvfile:
        
        all_data = pd.read_csv(csvfile)
        cleansed_data = all_data[all_data['seriesuid'].isin(image_name_list)]
        cleansed_data.to_csv("cleansed_data.csv", index = False, encoding = "utf8")
        
    with open("/Users/katyadunets/Desktop/cleansed_data.csv") as csvfile:
        
        all_data = pd.read_csv(csvfile)
        
        nodule_data = all_data[all_data["class"] == 1]
        non_nodule_data = all_data[all_data["class"] == 0]
        
        small_non_subset = non_nodule_data.sample(n=1420)
        
        nodule_data.to_csv("nodule_data.csv", index = False, encoding = "utf8" )
        small_non_subset.to_csv("subset_non_nodule_data.csv", index = False, encoding = "utf8" )

def resample(newSpacing):
    """
    The following function resamples each image given a new voxel spacing
    and outputs the resampled images to a new directory
    """

    originalDirectory = "/Users/katyadunets/Desktop/CISC881Project/Project_Data/All_Data"
    files = os.listdir(originalDirectory)
    
    for file in files:
        if file[0] != '.' and file.endswith("mhd"): #this skips the .DS_Store files

            filePath = os.path.join(originalDirectory, file)
            fileName = file
            
            inputImage = sitk.ReadImage(filePath)
            oldSpacing = inputImage.GetSpacing()
            
            castImageFilter = sitk.CastImageFilter()
            inputImage = castImageFilter.Execute(inputImage)
        
            oldSize = inputImage.GetSize()
            oldSpacing= inputImage.GetSpacing()
            newWidth = oldSpacing[0]/newSpacing[0]* oldSize[0]
            newHeight = oldSpacing[1] / newSpacing[1] * oldSize[1]
            newDepth = oldSpacing[2] / newSpacing[2] * oldSize[2]
            newSize = [int(newWidth), int(newHeight), int(newDepth)]
        
            filter = sitk.ResampleImageFilter()
            
            inputImage.GetSpacing()
            filter.SetOutputSpacing(newSpacing)
            filter.SetInterpolator(sitk.sitkLinear)
            filter.SetOutputOrigin(inputImage.GetOrigin())
            filter.SetOutputDirection(inputImage.GetDirection())
            filter.SetSize(newSize)
            
            outImage = filter.Execute(inputImage)
            
            print(outImage.GetSpacing())
            
            outDirectory = os.path.join("/Users/katyadunets/Desktop/CISC881Project/Resampled_Project_Data/")
            outDirectory = os.path.join(outDirectory + fileName)
            
            sitk.WriteImage(outImage, outDirectory)
            
            """
            Lines 68-82 are sourced from: 
            https://github.com/FNNDSC/pl-neuproseg/blob/baae51ad910e436c6e4fa2be0e59037cbe74c8e8/neuproseg/utils.py    
            """
            
def readCSV(filePath):
    """
    This function reads in the candidate CSV file and returns a list of rows 
    from the file
    """
    lines = []
    with open(filePath, "r") as f:
        csvReader = csv.reader(f)
        for line in csvReader:
            lines.append(line)
    
    return lines

def cropImage(cand, sitkImage):
    """
    This function crops an image with size 40X40X40, given an image and candidate
    location
    """
    
    worldCoord = np.asarray([float(cand[1]),float(cand[2]),float(cand[3])])
    
    voxelWidth = 40
                    
    x, y, z = sitkImage.TransformPhysicalPointToIndex(worldCoord)
                    
    x = int(x)
    y = int(y)
    z = int(z)
                    
    patch = sitkImage[x - voxelWidth // 2:x + voxelWidth // 2, y - voxelWidth // 2:y + voxelWidth // 2, z - voxelWidth // 2:z + voxelWidth // 2]
                    
    numpyImage = sitk.GetArrayFromImage(patch)
                    
    maxHU = 400.
    minHU = -1000.
    normalizedImage = (numpyImage - minHU) / (maxHU - minHU)
    normalizedImage[numpyImage>1] = 1.
    normalizedImage[numpyImage<0] = 0.
    
    print(normalizedImage.shape)
    
    return normalizedImage

def createArray(folder, candidateLines): 
    """
    This function creates a 4D array of slices (with augmentations for each image)
    """
    
    originalDirectory = folder
    files = os.listdir(originalDirectory)
    
    large_array = np.empty((0, 40, 40, 40)) 
    class_array = []
    
    for file in files:
        if file[0] != "." and file.endswith(".mhd"):
            filePath = os.path.join(originalDirectory, file)
            fileName = file.split(".mhd")[0]
            
            try:
                sitkImage = sitk.ReadImage(filePath)
                
                for cand in candidateLines:
                    if cand[0] == fileName:
                        
                        normalizedImage = cropImage(cand, sitkImage)
                        
                        large_array = np.append(large_array, [normalizedImage], axis = 0)
                        
                        if cand[4] == "1":
                            print("nodule!")
                            class_array.append(1)
                        
                        else:
                            class_array.append(0)
                            print("non-nodule!")
                            
                        if cand[4] == "1":
                            rotation = np.rot90(normalizedImage, k = 1, axes = (0,1))
                            large_array = np.append(large_array, [rotation], axis = 0)
                            class_array.append(1)
                            
                            rotation2 = np.rot90(normalizedImage, k = 2, axes = (0,1))
                            large_array = np.append(large_array, [rotation2], axis = 0)
                            class_array.append(1)
                            
                            rotation3 = np.rot90(normalizedImage, k = 3, axes = (0,1))
                            large_array = np.append(large_array, [rotation3], axis = 0)
                            class_array.append(1)
                            
                            rotation4 = sk.util.random_noise(normalizedImage)
                            large_array = np.append(large_array, [rotation4], axis = 0)
                            class_array.append(1)
                            
                            rotation5 = sk.util.random_noise(normalizedImage)
                            large_array = np.append(large_array, [rotation5], axis = 0)
                            class_array.append(1)
                        
                        if cand[4] == "0":
                            rotation = np.rot90(normalizedImage, k = 1, axes = (0,1))
                            large_array = np.append(large_array, [rotation], axis = 0)
                            class_array.append(0)
                            
                            rotation2 = np.rot90(normalizedImage, k = 2, axes = (0,1))
                            large_array = np.append(large_array, [rotation2], axis = 0)
                            class_array.append(0)
                            
                            
                        print(large_array.shape)
            
            except (RuntimeError, ValueError):
                print("Runtime error or Value Error")
                
    return large_array, class_array

def process_data(array):
    """
    The following function processes an array to have zero-mean and unit-variance
    """
    array = (array - array.mean(axis=0)) / array.std(axis=0)
    
    return array

def main():
    """
    The main function calls the pre-processing functions and saves the two final 
    arrays: array of patches and array of classifications
    """
    csv_cleaning()
    newSpacing = (0.7, 0.7, 2.5)
    resample(newSpacing)
    
    csvPath = "/Users/katyadunets/Desktop/CISC881_Project_Code/final_data.csv" #path to clean CSV file
    folder = "/Users/katyadunets/Desktop/CISC881Project/Resampled_Project_Data" #path to resampled images
    
    candidateLines = readCSV(csvPath)
    final_array, final_classes = createArray(folder, candidateLines)
    
    np.save("/Users/katyadunets/Desktop/classes.npy", final_classes) #save the class array
    
    processed_data = process_data(final_array) #process the final_array
    np.save("/Users/katyadunets/Desktop/processed_3D_array.npy", processed_data) #save the final_array
    
    
    
    
    
    
    
    
    