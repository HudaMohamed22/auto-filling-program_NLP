import os
import tkinter as tk
import re

nPredictions = 7
options = [] 


def prepareData():
        #take dir path as input
        path = search_entry1.get()
        os.chdir(path)
        
        #read one file data 
        def read_files(file_path):
           with open(file_path, 'r', encoding='utf-8') as file:
              corpus = file.read()
              return corpus

        # Iterate over all the files in the directory
        dataset=""
        for file in os.listdir():
           if file.endswith('.txt'):
              # Create the filepath of each file
              file_path =f"{path}/{file}" 
              corpus= read_files(file_path)
           dataset+=corpus

        print("------------------------------------------------------------------------------------------")
      #  print(dataset)
        res = len(dataset.split())
        # total no of wordsin data sample
        print ("The number of words in string are : " + str(res))
        return dataset

# generate tokens of data for generating ngrams later
def tokenizeText(txt_sample):
    txt_sample = txt_sample.lower()
    # tokenizing text to work on arabic and english words and numbers
    txt_sample = re.sub('[^\sa-zA-Z0-9]', '', txt_sample)
    return txt_sample.split()


# divide n grams and get number of each in txt
def calculateCounter(sentence,ngrams_list):
    if sentence not in ngrams_list.keys():
        ngrams_list[sentence] = 1
    else:
        ngrams_list[sentence] += 1
    return ngrams_list

probabilities = {}   

def generateNGrams(words_list, n):
    # to store n_word_sentence
    
    sentenceArr = []
    x=n-1
    #join input+1_sentences   #will use to com probability
    ngrams_list={}
    for num in range(0, len(words_list)):
        sentence = ' '.join(words_list[num:num + n])
        ngrams_list= calculateCounter(sentence,ngrams_list)
        sentenceArr.append(sentence) 
        
      #join input_sentences     #will use to com probability
    pre_ngrams_list={}
    for counter in range(0, len(words_list)):
        sentence_1 =' '.join(words_list[counter:counter + x])
        pre_ngrams_list=calculateCounter(sentence_1,pre_ngrams_list)
    #print("t-------------------------",pre_ngrams_list)
    
    for sentence in sentenceArr:
        splitted_Words = sentence.split()
        sentence_1=" ".join(splitted_Words[:-1])
        if(len(sentence_1.split())<x):
            continue
        probabilities[sentence]= ngrams_list[sentence] / pre_ngrams_list[sentence_1]

   # print("t-------------------------",probabilities)
        

def splitSequence(seq):
    return seq.split(" ")


def getPredictions(sequence):
    predicted = []
    nPred = nPredictions
    inputSequence = splitSequence(sequence)
    for sentence in probabilities.keys():
        if sequence in sentence:
            outputSequence = splitSequence(sentence)
            cont = False
            for i in range(0, len(inputSequence)):
                if outputSequence[i] != inputSequence[i]:
                    cont = True
                    break
            if cont:
                continue
            predicted.append((sentence, probabilities[sentence]))
    predicted.sort(key=lambda x: x[1], reverse=True)

    if len(predicted) == 0:
        print("No predicted words")
        nPred=0
    else:
        if len(predicted) < nPredictions:
            nPred = len(predicted)

        for i in range(0, nPred):
            outputSequence = predicted[i][0].split(" ")
            options.append(outputSequence[len(inputSequence)])
        return options, nPred

#prepare N grams model

def model():
    dataset = prepareData()
    words = tokenizeText(dataset)
    seq = search_entry2.get()
    generateNGrams(words, len(splitSequence(seq)) + 1)
    options, nPred=getPredictions(seq.lower())
    print(" Option List :",options,"\n","Num of options=",nPred)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, f"Option List: \n")
    for i in options:
        text_area.insert(tk.END, f"{i}\n")
    text_area.insert(tk.END, f"Num of options: {nPred}")

# Create the Tkinter GUI window
root = tk.Tk()
root.geometry("800x500")
root.title('Google')
input_label = tk.Label(root, text="Enter DataSet path :")
input_label.pack()

# Create the search bar and text area widgets
search_var1 = tk.StringVar()
search_entry1 = tk.Entry(root, textvariable=search_var1)
search_entry1.pack(pady=10)


input_label = tk.Label(root, text="Enter Search Words :")
input_label.pack()

search_var2 = tk.StringVar()
search_entry2 = tk.Entry(root, textvariable=search_var2)
search_entry2.pack(pady=10)
input_label = tk.Label(root, text="Press Enter")
input_label.pack(pady=10) 

text_area = tk.Text(root)
text_area.pack()



if search_entry1.get() and search_entry2.get():
    model()
else:
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, "Please provide inputs in both search bars.")

# Bind the search bar to the main function so that it displays the input in the text area when the user presses Enter
search_entry2.bind('<Return>', lambda event: model())

# Start the Tkinter main loop
root.mainloop()
