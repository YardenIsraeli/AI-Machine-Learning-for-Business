#!/usr/local/bin/python3.6

import boto3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image  

if __name__ == "__main__":    
    
    #Setting
    collection = '2018WorldCup'
    bucket = 'bucket4awslab'
    similarity_threshold = 80    
    client=boto3.client('rekognition')
    
    #Create Collection
    print('Create a collection in an AWS Region')    
    response_create_collection = client.create_collection(CollectionId='collection')  
    #print response
    print('Collection ARN: ' + response_create_collection['CollectionArn'])
    print('FaceModelVersion: ' + response_create_collection['FaceModelVersion'])
    print('Status code: ' + str(response_create_collection['StatusCode']))
    print('Done...')
    
    #Detect Brazil national team players in 2018 World Cup and Add them to the collection
    print('Add faces to the collection')    
    response_index_faces = client.index_faces(
            CollectionId = collection,
            DetectionAttributes=['DEFAULT'],
            ExternalImageId='Brazil_id',
            Image={
                    'S3Object': {
                            'Bucket': bucket,
                            'Name': 'BrazilNationalFootballTeam2018.jpg'},
                            },
    )
    collectionSize = len(response_index_faces['FaceRecords'])
    print("%s faces were added to %s collection" % (collectionSize, collection))

    #Create orederd list of Brazil national team players
    players_list = ["Alisson", "Coutinho", "Marquinhos", "Fermino", "Casermino",
                   "Neymar", "Marcelo", "Paulinho", "Alvas", "Augusto", "Miranda"]
    
    #Get metadata for the faces in our collection
    print("metadata of faces in our collection:\n")
    response_list_faces = client.list_faces(CollectionId = collection)    
    list_faces = response_list_faces['Faces']
    print(list_faces)
    
    #Show Detection of Brazil national team players in 2018 World Cup 
    img = Image.open('BrazilNationalFootballTeam2018.jpg')
    X , Y = img.size
    #Create figure and axes
    fig,ax = plt.subplots(1)
    #Display the image
    ax.imshow(img)
    #Create a Rectangle patch
    for i in range(0,11):
        BB = list_faces[i]['BoundingBox']
        rect = patches.Rectangle(
                xy=(BB[u'Left']*X,BB[u'Top']*Y),
                width=BB[u'Width']*X,
                height=BB[u'Height']*Y,linewidth=2,edgecolor='r',facecolor='none')
        #Add the patch to the Axes
        ax.add_patch(rect)
        ax.text(rect.get_x(),rect.get_y()-30,players_list[i],
        horizontalalignment='center',
        verticalalignment='top',
        color='Red', fontsize=8, fontweight = 'bold')    
    #fig.savefig(BrazilNationalFootballTeam2018_withBB.jpg')
    
    #Search for faces in our collection     
    #Hold players Ids in a list
    id_list = [d['FaceId'] for d in list_faces]
      
    #searching Marcelo   
    fileName='Marcelo.jpeg'
    maxFaces = 1    
    response_match = client.search_faces_by_image(CollectionId = collection,
                                Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                FaceMatchThreshold = similarity_threshold,
                                MaxFaces = maxFaces)                                
    faceMatches = response_match['FaceMatches']

    #Display the match   
    img_marcelo = Image.open('Marcelo.jpeg')
    X , Y = img_marcelo.size
    # Create figure and axes
    fig,ax = plt.subplots(1)
    #Show input image
    ax.imshow(img_marcelo)    
    #Get bounded box of the matcing face in the input image
    BB = response_match['SearchedFaceBoundingBox']
    rect = patches.Rectangle(
            xy=(BB[u'Left']*X,BB[u'Top']*Y),
            width=BB[u'Width']*X,
            height=BB[u'Height']*Y,linewidth=2,edgecolor='r',facecolor='none')
    #Add the patch to the Axes
    ax.add_patch(rect)
    #find the name of the player in the input image    
    player_ind = id_list.index(faceMatches[0]['Face']['FaceId'])
    player_name = players_list[player_ind]
    #get match similarity
    player_similarity = "{:.2f}".format(faceMatches[0]['Similarity']) + "%"
    #draw player name & match similarity
    ax.text(rect.get_x(),rect.get_y()-30, player_name + ',' + player_similarity,
    horizontalalignment='center',
    verticalalignment='top',
    color='Red', fontsize=8, fontweight = 'bold')  

    #searching Neymar  
    fileName='Neymar.jpg'
    maxFaces = 1    
    response_match = client.search_faces_by_image(CollectionId = collection,
                                Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                FaceMatchThreshold = similarity_threshold,
                                MaxFaces = maxFaces)                                
    faceMatches = response_match['FaceMatches']

    #Display the match   
    img_neymar = Image.open(fileName)
    X , Y = img_neymar.size
    # Create figure and axes
    fig,ax = plt.subplots(1)
    #Show input image
    ax.imshow(img_neymar)    
    #Get bounded box of the matcing face in the input image
    BB = response_match['SearchedFaceBoundingBox']
    rect = patches.Rectangle(
            xy=(BB[u'Left']*X,BB[u'Top']*Y),
            width=BB[u'Width']*X,
            height=BB[u'Height']*Y,linewidth=2,edgecolor='r',facecolor='none')
    #Add the patch to the Axes
    ax.add_patch(rect)
    #find the name of the player in the input image    
    player_ind = id_list.index(faceMatches[0]['Face']['FaceId'])
    player_name = players_list[player_ind]
    #get match similarity
    player_similarity = "{:.2f}".format(faceMatches[0]['Similarity']) + "%"
    #draw player name & match similarity
    ax.text(rect.get_x(),rect.get_y()-30, player_name + ',' + player_similarity,
    horizontalalignment='center',
    verticalalignment='top',
    color='Red', fontsize=8, fontweight = 'bold')    
    




