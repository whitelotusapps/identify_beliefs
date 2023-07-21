# identify_beliefs
This code base is used to analyze transcribed text for beliefs. Initially developed to analyze the "text" key from AssemblyAI JSON transcriptions.

You can read about these scripts from the below articles, they are the same article, provided on two different platforms:

LinkedIn:
[So, You Want to Be a Data Scientist, Huh? Pub: 2](https://www.linkedin.com/pulse/so-you-want-data-scientist-huh-pub-2-zack-olinger/)

Medium
[So, You Want to Be a Data Scientist, Huh? Part 2](https://medium.com/@therealzackolinger/so-you-want-to-be-a-data-scientist-huh-9a3d63f16f96)


# Requirements

1. As of 2023-07-21, the code is expecting the files to have a specific file naming convention:

`YYYY-mmm-dd - HH-mm-ss`

For example:

```
2021-03-10 - 02-14-00 - audio journal.json
```

* The `YYYY-mmm-dd - HH-mm-ss` format is what the script is looking for to determine the date and time of the transcript. Overall, this is not necessary for identifying beliefs and will be removed from future versions of the code.

2. The `my_words.txt` file is required. This is a list of words that mean something to the person who is having their beliefs analyzed. This is a personal lexicon/idiolect. Words and phrases that have a specific, impactful meaning to the individual being analyzed go into this file.

## Script variants

* `identify_idioms_and_beliefs_npyscreen.py` is a terminal menu driven version of this script; it will provide a list of AssemblyAI JSON files to process beliefs from.

* `identify_idioms_and_beliefs_text_files.py` does not contain a menu, and is meant to ready only the raw text transcription and displays the output to the terminal. This version can be used on ANY text transcription, not just AssemblyAI.

* `identify_idioms_and_beliefs_write_files.py` is meant to write the belief data to output files without displaying the content to the screen

* `identify_idioms_and_beliefs.py` this is the original script, and is much like the `identify_idioms_and_beliefs_npyscreen.py` and `identify_idioms_and_beliefs_text_files.py` scripts. This script is meant to read in AssemblyAI JSON files and display the beliefs on the screen, without the use of a menu to select the file to be processed.
## Usage

The main thing to ensure is that the script knows where to pull the text data to analyze. In the code you made see references to the below folder locations:

```
./Sandbox/CLEAN_UP
./Sandbox/TXT
./Sandbox/JSON_sed
```

The `./Sandbox/TXT` location is where plain text files are located. If you have text files that are just plain text, then change the folder location in the script to point to that folder.

Instances of where `./Sandbox/CLEAN_UP` or `./Sandbox/JSON_sed` are where AssemblyAI JSON output files are stored. If you have AssemblyAI JSON output files, change the location to where your files are located.

## Example Output

### Actions
```
"action": "reminds",                                                                                                                                                                                                        
"object": "me",                                                                                                                                                                                                              
"context": [                                                                                                                                                                                                                 
	"I know I told <edit> for sure.",                                                                                                                                                                                      
	"I was like, I had just been thinking about your grandma.",                                                                                                                                                              
	"I was like, I wonder how she's doing, you know?",                                                                                                                                                                       
	"And then that was probably a few days before you did your life, and then you do your live",                                                                                                                             
	"and yeah, I go to bed every night, <edit>."                                                                                                                                                                             
],                                                                                                                                                                                                                           
"action_sentence": "I go to bed every night and I tell you I love you and I want to hold you, and I think about hugging you, and I think about when I'm driving in my car, because every time I get in my car not every      
time, but a lot, my car totally reminds me of you.",                                                                                                                                                                                     
"actions": {                                                                                                                                                                                                                 
	"go": {                                                                                                                                                                                                                  
		"subject": "I",                                                                                                                                                                                                      
		"object": "bed",                                                                                                                                                                                                     
		"entities": {                                                                                                                                                                                                        
			"to": [                                                                                                                                                                                                          
				"bed"                                                                                                                                                                                                        
			]                                                                                                                                                                                                                
		}                                                                                                                                                                                                                    
	},                                                                                                                                                                                                                       
	"tell": {                                                                                                                                                                                                                
		"subject": "I",                                                                                                                                                                                                      
		"object": "you",                                                                                                                                                                                                     
		"entities": {}                                                                                                                                                                                                       
	},                                                                                                                                                                                                                       
	"love": {                                                                                                                                                                                                                
		"subject": "I",                                                                                                                                                                                                      
		"object": "you",                                                                                                                                                                                                     
		"entities": {}                                                                                                                                                                                                       
	},                                                                                                                                                                                                                       
	"driving": {                                                                                                                                                                                                             
		"subject": "I",                                                                                                                                                                                                      
		"object": "car",                                                                                                                                                                                                     
		"entities": {                                                                                                                                                                                                        
			"in": [                                                                                                                                                                                                          
				"car"                                                                                                                                                                                                        
			]                                                                                                                                                                                                                
		}                                                                                                                                                                                                                    
	},                                                                                                                                                                                                                       
	"get": {                                                                                                                                                                                                                 
		"subject": "I",                                                                                                                                                                                                      
		"object": "car",                                                                                                                                                                                                     
		"entities": {                                                                                                                                                                                                        
			"in": [                                                                                                                                                                                                          
				"car"                                                                                                                                                                                                        
			]                                                                                                                                                                                                                
		}                                                                                                                                                                                                                    
	},                                                                                                                                                                                                                       
	"reminds": {                                                                                                                                                                                                             
		"subject": "my car",                                                                                                                                                                                                 
		"object": "me",                                                                                                                                                                                                      
		"entities": {                                                                                                                                                                                                        
			"of": [                                                                                                                                                                                                          
				"you"                                                                                                                                                                                                        
			] 
```


### Sentences of Interest
```
"sentences": [                                                                                                                                                                                                                      
	{                                                                                                                                                                                                                                
		"context": [                                                                                                                                                                                                                 
			"I know I told <edit> for sure.",                                                                                                                                                                                      
			"I was like, I had just been thinking about your grandma.",                                                                                                                                                              
			"I was like, I wonder how she's doing, you know?",                                                                                                                                                                       
			"And then that was probably a few days before you did your life, and then you do your live",                                                                                                                             
			"and yeah, I go to bed every night, <edit>."   
		],                                                                                                                                                                                                                           
		"sentence_of_interest": "I go to bed every night and I tell you I love you and I want to hold you, and I think about hugging you, and I think about when I'm driving in my car, because every time I get in my car not       
every time, but a lot, my car totally reminds me of you.",                                                                                                                                                                               
		"word_matches": {                                                                                                                                                                                                            
			"words": {                                                                                                                                                                                                               
				"about": 2,                                                                                                                                                                                                          
				"i want": 2,                                                                                                                                                                                                         
				"time": 2,                                                                                                                                                                                                           
				"a lot": 1,                                                                                                                                                                                                          
				"reminds": 1,                                                                                                                                                                                                        
				"when i": 1,                                                                                                                                                                                                         
				"tell": 1,                                                                                                                                                                                                           
				"love": 1,                                                                                                                                                                                                           
				"because": 1,                                                                                                                                                                                                        
				"i'm": 1,                                                                                                                                                                                                            
				"hold": 1                                                                                                                                                                                                            
			},                                                                                                                                                                                                                       
			"number_of_matches": 11,                                                                                                                                                                                                 
			"sum_of_matches": 14                                                                                                                                                                                                     
		}                                                                                                                                                                                                                            
	} 
```
