# -*- coding: utf-8 -*-
"""Karaoke-MASTER.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XKjLfHjSvkydv39JClASSqr4ErYwggrz

# Karaoke MASTER (ver. 2.1)

***

## GPT2-based Karaoke Melody Artificial Intelligence Model Creator/Trainer.

***

Credit for char-based GPT2 implementation used in this colab goes out to Andrej Karpathy: https://github.com/karpathy/minGPT

***

WARNING: This complete implementation is a functioning model of the Artificial Intelligence. Please excercise great humility, care, and respect.

***

##### Project Los Angeles

##### Tegridy Code 2021

***

# Setup Environment, clone needed repos, and install all required dependencies
"""

#@title Install all dependencies (run only once per session)

!git clone https://github.com/asigalov61/tegridy-tools
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio
!pip install wordcloud

#@title Import all needed modules

print('Loading needed modules. Please wait...')
import os

if not os.path.exists('/content/Dataset'):
    os.makedirs('/content/Dataset')

os.chdir('/content/tegridy-tools/tegridy-tools')
import TMIDI

os.chdir('/content/tegridy-tools/tegridy-tools/minGPT')
from minGPT import *

from midi2audio import FluidSynth
from IPython.display import display, Javascript, HTML, Audio

from wordcloud import WordCloud

from google.colab import output, drive

print('Loading complete. Enjoy! :)')

os.chdir('/content/')

"""# Download and process MIDI dataset"""

# Commented out IPython magic to ensure Python compatibility.
#@title Download Tiny Karaoke MIDI dataset

#@markdown Works best stand-alone/as-is for the optimal results
# %cd /content/Dataset/
!wget 'https://github.com/asigalov61/Tegridy-MIDI-Dataset/raw/master/Tiny-Karaoke-MIDI-Dataset-CC-BY-NC-SA.zip'
!unzip -j '/content/Dataset/Tiny-Karaoke-MIDI-Dataset-CC-BY-NC-SA.zip'
!rm '/content/Dataset/Tiny-Karaoke-MIDI-Dataset-CC-BY-NC-SA.zip'
# %cd /content/

"""# If you are not sure where to start or what settings to select, please use original defaults"""

# Commented out IPython magic to ensure Python compatibility.
#@title Process MIDIs to special MIDI dataset with Tegridy MIDI Processor

full_path_to_output_dataset_to = "/content/Karaoke-MASTER" #@param {type:"string"}
#@title Convert MIDI dataset to the Reduced TXT Karaoke dataset

#@markdown Make sure to select the right encoding for your language. Encoding is correct when you can properly and clearly read it in your language. Encodings list is located here: https://docs.python.org/3/library/codecs.html#standard-encodings

full_path_to_TXT_dataset = "/content/Karaoke-MASTER_TXT_Dataset.txt" #@param {type:"string"}
karaoke_language_encoding = "utf_8" #@param {type:"string"}
dataset_name = "DATASET=Karaoke-MASTER_TXT_Dataset"

# %cd /content/

print('TMIDI Processor')
print('Starting up...')

events_list = []
events_matrix = []

###########

files_count = 0

mev = 0
kev = 0

TXT = ''

chords_list_f = []
melody_list_f = []

all_words = ''
pitches_words_list = []

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "/content/Dataset/"
os.chdir(dataset_addr)
filez = os.listdir(dataset_addr)

print('Processing MIDI files. Please wait...')
for f in tqdm.auto.tqdm(filez):
  try:
    events_matrix, mev, kev, pwl, aw = TMIDI.Tegridy_Karaoke_MIDI_to_Reduced_TXT_Processor(f, karaoke_language_encoding)
    TXT += events_matrix
    pitches_words_list.extend(pwl)
    all_words += aw + ' '
    files_count += 1

  except:
    print('Problematic MIDI:', f)
    continue

TMIDI.Tegridy_TXT_Dataset_File_Writer(full_path_to_TXT_dataset, '', dataset_name + '\n' + TXT)

TMIDI.Tegridy_Karaoke_Pitches_Words_List_to_CSV_Writer(pitches_words_list, '/content/Karaoke-MASTER-Dataset-Pitches-Words.csv')

#@title Generate a nice Word Cloud of the processed dataset
wordcloud = WordCloud(width=1920, height=1068, margin=0, colormap='Blues').generate(all_words)

plt.figure(figsize=(19, 12))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

"""# Setup and Intialize the Model

## YOU MUST RUN THE CELL/CODE IN THE SECTION BELOW to init the model. Does not matter if the model is empty or pre-trained.

## DO NOT EXECUTE TRAIN CELL/CODE UNLESS YOU INTEND TO TRAIN FROM SCRATCH
"""

#@title Create/prepare GPT2 model and load the dataset

full_path_to_training_text_file = "/content/Karaoke-MASTER_TXT_Dataset.txt" #@param {type:"string"}
model_attention_span_in_tokens = 512 #@param {type:"slider", min:0, max:1024, step:16}
model_embed_size = 256 #@param {type:"slider", min:0, max:1024, step:64}
number_of_heads = 16 #@param {type:"slider", min:1, max:16, step:1}
number_of_layers = 4 #@param {type:"slider", min:1, max:16, step:1}
number_of_training_epochs = 2 #@param {type:"slider", min:1, max:5, step:1}
training_batch_size = 48 #@param {type:"slider", min:0, max:160, step:4}
model_learning_rate = 6e-4 #@param {type:"number"}

trainer, model, train_dataset = MainLoader(full_path_to_training_text_file,
                                          None,
                                          16,
                                          model_attention_span_in_tokens,
                                          model_embed_size,
                                          number_of_heads,
                                          number_of_layers,
                                          number_of_training_epochs,
                                          training_batch_size,
                                          model_learning_rate)

"""# Train the model or Load/Re-load the existing pre-trained model checkpoint"""

# Commented out IPython magic to ensure Python compatibility.
#@title (OPTION 1) Train the model
# %cd /content/
trainer.train()

#@title Plot Positional Embeddings

# visualize some of the learned positional embeddings, maybe they contain structure
PlotPositionalEmbeddings(model, model_attention_span_in_tokens)

# Commented out IPython magic to ensure Python compatibility.
#@title Save/Re-Save the model from memory
#@markdown Standard PyTorch AI models file extension is PTH
full_path_to_save_model_to = "/content/Karaoke-MASTER-Trained-Model.pth" #@param {type:"string"}
# %cd /content/
torch.save(model, full_path_to_save_model_to)

#@title (OPTION 2) Load existing model/checkpoint
full_path_to_model_checkpoint = "/content/Karaoke-MASTER-Trained-Model.pth" #@param {type:"string"}
model = torch.load(full_path_to_model_checkpoint)
model.eval()

"""# Generate, download, plot, and listen to the output"""

#@title Generate and download the composition as TXT file.
#@markdown PLEASE NOTE IMPORTANT POINTS: 

#@markdown 0) If you are not sure where to start/what settings to set, please use original defaults.

#@markdown 1) Model primes from the dataset !!!

#@markdown 2) Model's first output may be empty or garbled so please try several times before discarting the model

print('Karaoke MASTER Model Generator')
print('Starting up...')
number_of_tokens_to_generate = 2048 #@param {type:"slider", min:0, max:32768, step:128}
creativity_temperature = 0.8 #@param {type:"slider", min:0.05, max:4, step:0.05}
top_k_prob = 4 #@param {type:"slider", min:0, max:50, step:1}
input_prompt = "Love" #@param {type:"string"}

debug = False 

os.chdir('/content/')

completion = Generate(model,
                      train_dataset,
                      trainer,
                      number_of_tokens_to_generate,
                      creativity_temperature,
                      top_k_prob,
                      input_prompt)

fname = TMIDI.Tegridy_File_Time_Stamp('/content/Karaoke-MASTER-Composition-')

print('Done!')
print('Saving to', str(fname + '.txt'))
with open(fname + '.txt', "w") as text_file:
    print(completion, file=text_file)

print('Downloading TXT file...')
from google.colab import files
files.download(fname + '.txt')

#@title Convert generated Karaoke TXT file to the Karaoke MIDI file
text_encoding = "utf_8" #@param {type:"string"}

print('Karaoke TXT to Karaoke MIDI Processor')
print('Making your file. Please stand-by...')

KAR_ev = 0
song_name = ''
lyrics = ''

print('Converting Karaoke TXT to Song...')
song_name, song, lyrics, KAR_ev = TMIDI.Tegridy_Karaoke_TXT_to_MIDI_Processor(completion, text_encoding)

print('Saving your Karaoke MIDI file...')
TMIDI.Tegridy_SONG_to_MIDI_Converter(song, output_file_name=fname, output_signature='Karaoke-MASTER', track_name=song_name, text_encoding=text_encoding)

print('Downloading your Karaoke MIDI file...')
from google.colab import files
files.download(fname + '.mid')

print('Task complete! Enjoy :)')

#@title Show generated Karaoke lyrics and its word cloud
from pprint import pprint
pprint(lyrics)

#@title Generate a nice Word Cloud of the processed dataset
wordcloud = WordCloud(width=1920, height=1068, margin=0, colormap='Blues').generate(lyrics)

plt.figure(figsize=(19, 12))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

#@title Listen to the last generated composition
#@markdown NOTE: May be very slow with the long compositions
print('Synthesizing the last output MIDI. Please stand-by... ')

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
Audio(str(fname + '.wav'), rate=16000)

"""## Congrats! :) You did it :)"""