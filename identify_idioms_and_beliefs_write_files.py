#####################################################################################################################################
import os
import json
import mysql.connector
import re
from datetime import datetime, timedelta
import spacy
# TRF is accurate, and slow; good for production
#nlp = spacy.load("en_core_web_trf")

# sm is accurate enough, fast; good for development
nlp = spacy.load("en_core_web_sm")

# Stanford CoreNLP 4.5.3
#from stanfordcorenlp import StanfordCoreNLP
#nlp = StanfordCoreNLP('./stanford-corenlp-4.5.3')
#props = {'annotators': 'tokenize,ssplit,pos,lemma,ner,coref,depparse,parse,dcoref,openie,sentiment,kbp,natlog,quote,relation',
#         'pipelineLanguage': 'en',
#         'outputFormat': 'json'}

if os.path.exists("actions.txt"):
    os.remove("actions.txt")

if os.path.exists("sentences.txt"):
    os.remove("sentences.txt")



#beliefs = ["about", "afraid", "aligned", "and", "answer", "answers", "attention", "attach", "attached", "awesome", "believe", "belief", "but", "cause", "certainly", "choice", "choose", "chose", "commitment", "committed", "committing", "connect", "connected", "connecting", "contains", "cool", "curious", "desire", "energy", "energies", "exciting", "experience", "experiences", "expect", "expects", "expecting", "expected", "expression", "expressing", "expressed", "express", "fact", "facts", "fear", "fears", "feel", "feeling", "feels", "felt", "feminine", "forget", "for sure", "freaks me out", "from", "fun", "have", "head", "hope", "however", "i", "i am", "i can't", "i don't", "i haven't", "i know", "i'm", "i shouldn't", "i won't", "identity", "idea", "ideas", "impact", "important", "inclination", "inclined", "inside", "intention", "intentionally", "interesting", "is a", "it's", "know", "knowing", "knows", "let's be serious", "look", "looking", "looks", "love", "magical", "masculine", "memory", "mention", "mind", "moved towards", "move toward", "moving toward", "move towards", "moving towards", "move away", "moving away", "moved away", "need", "negative", "of", "one may", "philosophy", "positive", "prompt", "principle", "question", "questions", "questioning", "reason", "reminds", "scare", "scared", "scares", "sure", "tempt", "tempted", "tempting", "thought", "thoughts", "true", "try", "truth", "wound", "wounded", "wounding", "wish", "without", "within", "work", "working", "working toward", "working towards", "would", "want", "you know"]
from blessings import Terminal
t = Terminal()
from termcolor import colored

with open("my_words.txt", "r") as file:
    beliefs = [line.strip() for line in file.readlines()]

beliefs = sorted(set(beliefs))
#####################################################################################################################################

#####################################################################################################################################
def find_beliefs(text):
    doc = nlp(text)
    # Create a dictionary with an empty list for each belief phrase, and additional lists for non-belief sentences and all sentences
    beliefs = ["about", "afraid", "aligned", "and", "attach", "attached", "belief", "certainly", "commitment", "committed", "committing", "contains", "convince", "convinced", "conviction", "desire", "experience", "experiences", "fear", "feel", "feeling", "felt", "from", "head", "hope", "i", "i am", "i can't", "i don't", "i haven't", "i shouldn't", "i won't", "i'm", "idea", "ideas", "important", "inside", "intention", "intentionally", "is a", "it's", "know", "knowing", "knows", "love", "mind", "need", "of", "one may", "philosophy", "principle", "question", "thought", "thoughts", "true", "wound", "wounded", "wounding", "wish", "without", "within", "would", "want"]
    beliefs_dict = {phrase: [] for phrase in beliefs}

    # Loop through the sentences and append to the appropriate list
    for sent in doc.sents:

        for phrase in beliefs:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, sent.text.lower()):
                beliefs_dict[phrase].append(sent.text.strip())

    return beliefs_dict
#####################################################################################################################################


with open("question_words.txt", "r") as file:
    question_words = [line.strip() for line in file.readlines()]

import re
import spacy


# Assuming question_words are read from a file and stored in a global variable
# question_words = [...]

def find_questions_v2(text):
    doc = nlp(text)

    questions = {}

    for word in question_words:
        questions[word] = []

    questions["non_question_word_questions"] = []
    questions["all_questions"] = []
    questions["non_contextual_questions"] = []
    questions["matched_words"] = []

    current_question = None
    sentences_after_question = []
    sentences_counter = 0

    for sent in doc.sents:
        if sent.text.strip().endswith("?"):
            matched_word = False
            for word in question_words:
                if re.search(r'\b' + word + r'\b', sent.text.lower()):
                    current_question = sent.text.strip()
                    sentences_after_question = []
                    questions["all_questions"].append({"question": current_question, "sentences_after": []})
                    questions["matched_words"].append({"word": word, "question": current_question, "sentences_after": []})
                    matched_word = True
                    break
            if not matched_word:
                current_question = sent.text.strip()
                sentences_after_question = []
                questions["non_question_word_questions"].append({"question": current_question, "sentences_after": []})
                questions["all_questions"].append({"question": current_question, "sentences_after": []})
            sentences_counter = 0
        else:
            if current_question is not None:
                sentences_counter += 1
                if 1 <= sentences_counter <= 20:
                    sentences_after_question.append(sent.text.strip())
                if sentences_counter == 20:
                    if questions["all_questions"]:
                        questions["all_questions"][-1]["sentences_after"] = sentences_after_question
                    current_question = None
                    sentences_after_question = []

    if current_question is not None:
#        questions["non_question_word_questions"][-1]["sentences_after"] = sentences_after_question
#        questions["matched_words"][-1]["sentences_after"] = sentences_after_question




        if questions["all_questions"]:
            questions["all_questions"][-1]["sentences_after"] = sentences_after_question
        for word in question_words:
            if word in current_question.lower() and questions[word]:
                questions[word][-1]["sentences_after"] = sentences_after_question
                break

    questions["contextual_questions"] = [question for question in questions["all_questions"] if question["sentences_after"]]
    questions["non_contextual_questions"] = [question for question in questions["all_questions"] if not question["sentences_after"]]
    del questions["all_questions"]

    for key in list(questions.keys()):
        if key not in ["contextual_questions", "non_question_word_questions", "non_contextual_questions", "matched_words"] and not questions[key]:
            del questions[key]

    return questions





       





#####################################################################################################################################
def find_questions(text):

    doc = nlp(text)
    # Create a dictionary with an empty list for each question word, and additional lists for other questions and all questions
    question_words = ["are", "because", "can", "did", "does", "feeling", "have", "how", "i", "if", "is", "maybe", "my", "or", "our", "remember", "should", "since", "the", "they", "this", "want", "was", "we", "when", "where", "which", "who", "why", "will", "you", "your"]
    questions = {word: [] for word in question_words}
    questions["non_question_word_questions"] = []
    questions["all_questions"] = []

    # Loop through the sentences and append to the appropriate list
    for sent in doc.sents:
        if sent.text.strip().endswith("?"):
            matched_word = False
            for word in question_words:
                if word in sent.text.lower():
                    questions[word].append(sent.text.strip())
                    matched_word = True
            if not matched_word:
                questions["non_question_word_questions"].append(sent.text.strip())
                questions["all_questions"].append(sent.text.strip())
        else:
            for token in sent:
                if token.text.lower() in question_words:
                    questions[token.text.lower()].append(sent.text.strip())
                    questions["all_questions"].append(sent.text.strip())
                else:
                    questions["non_question_word_questions"].append(sent.text.strip())
                    questions["all_questions"].append(sent.text.strip())
    
    # Return the list of questions
    return questions
#####################################################################################################################################

#####################################################################################################################################
# ACTION / ME

def get_subjects(sentence):
    doc = nlp(sentence)
    subjects = []
    for token in doc:
        if token.dep_ == "nsubj":
            subjects.append(token.text)
        elif token.dep_ == "nsubjpass":
            subjects.append(token.text)
            for child in token.children:
                if child.dep_ == "punct" and child.text == "(":
                    start = child.i + 1
                elif child.dep_ == "punct" and child.text == ")":
                    end = child.i
                    subjects[-1] += " " + sentence[start:end]
    return subjects

'''
# STANFORD CORENLP 4.5.3 VERSION
def get_causes(sentence):
    doc = nlp(sentence)
    causes = {}
    for sent in doc.sentences:
        for word in sent.words:
            if word.dependency_relation == "nsubj":
                subject = word
                poss_token = None
                for child in subject.children:
                    if child.dependency_relation == "poss":
                        poss_token = child
                        break
                if subject.upos == "NOUN" and subject.parent.dependency_relation == "cop":
                    subject = subject.parent
                for ancestor in subject.parents:
                    if ancestor.upos == "VERB":
                        action = ancestor
                        obj = None
                        for child in action.children:
                            if child.dependency_relation == "dobj" or child.dependency_relation == "attr":
                                obj = child
                                break
                            elif child.dependency_relation == "prep":
                                for subchild in child.children:
                                    if subchild.dependency_relation == "pobj":
                                        obj = subchild
                                        break
                                if obj is None and child.text == "of":
                                    for subchild in child.children:
                                        if subchild.dependency_relation == "pobj":
                                            obj = subchild
                                            break
                            elif child.dependency_relation == "obl":
                                for subchild in child.children:
                                    if subchild.text == "of":
                                        obj = next(subchild.children)
                                        break
                        if obj is not None:
                            entities = {}
                            for child in action.children:
                                if child.dependency_relation == "prep":
                                    prep = child.text
                                    entity_tokens = []
                                    for subchild in child.children:
                                        if subchild.dependency_relation == "pobj":
                                            entity_tokens.append(subchild)
                                        elif subchild.dependency_relation == "compound":
                                            entity_tokens.append(subchild)
                                        elif subchild.dependency_relation == "conj" and subchild.upos == "NOUN":
                                            entity_tokens.append(subchild)
                                    for entity_token in entity_tokens:
                                        entity_text = entity_token.text
                                        if entity_token.upos == "PRON":
                                            for ancestor in entity_token.parents:
                                                if ancestor.upos == "NOUN":
                                                    entity_text = ancestor.text
                                                    break
                                        if len(list(entity_token.children)) > 0:
                                            entity_text = " ".join([entity_text] + [tok.text for tok in entity_token.children])
                                        if prep not in entities:
                                            entities[prep] = []
                                        entities[prep].append(entity_text)
                            if poss_token:
                                subject_text = f"{poss_token.text} {subject.text}"
                            else:
                                subject_text = subject.text
                            causes[action.text] = {
                                "subject": subject_text,
                                "object": obj.text,
                                "entities": entities
                            }
                            break
    return causes
'''



# SPACY VERSION
# BELOW IS GOLDEN CODE!!!!
def get_causes(sentence):
    doc = nlp(sentence)
    causes = {}
    for token in doc:
        if token.dep_ == "nsubj":
            subject = token
            poss_token = None
            for child in token.children:
                if child.dep_ == "poss":
                    poss_token = child
                    break
            if subject.pos_ == "NOUN" and subject.nbor().dep_ == "cop":
                subject = subject.nbor()
            for ancestor in token.ancestors:
                if ancestor.pos_ == "VERB":
                    action = ancestor
                    obj = None
                    for child in action.children:
                        if child.dep_ == "dobj" or child.dep_ == "attr":
                            obj = child
                            break
                        elif child.dep_ == "prep":
                            for subchild in child.children:
                                if subchild.dep_ == "pobj":
                                    obj = subchild
                                    break
                            if obj is None and child.text == "of":
                                for subchild in child.children:
                                    if subchild.dep_ == "pobj":
                                        obj = subchild
                                        break
                        elif child.dep_ == "obl":
                            for subchild in child.children:
                                if subchild.text == "of":
                                    obj = subchild.children.__next__()
                                    break
                    if obj is not None:
                        entities = {}
                        for child in action.children:
                            if child.dep_ == "prep":
                                prep = child.text
                                entity_tokens = []
                                for subchild in child.children:
                                    if subchild.dep_ == "pobj":
                                        entity_tokens.append(subchild)
                                    elif subchild.dep_ == "compound":
                                        entity_tokens.append(subchild)
                                    elif subchild.dep_ == "conj" and subchild.pos_ == "NOUN":
                                        entity_tokens.append(subchild)
                                for entity_token in entity_tokens:
                                    entity_text = entity_token.text
                                    if entity_token.pos_ == "PRON":
                                        for ancestor in entity_token.ancestors:
                                            if ancestor.pos_ == "NOUN":
                                                entity_text = ancestor.text
                                                break
                                    if entity_token.n_rights > 0:
                                        entity_text = " ".join([entity_text] + [tok.text for tok in entity_token.rights])
                                    if prep not in entities:
                                        entities[prep] = []
                                    entities[prep].append(entity_text)
                        if poss_token:
                            subject_text = f"{poss_token.text} {subject.text}"
                        else:
                            subject_text = subject.text
                        causes[action.text] = {
                            "subject": subject_text,
                            "object": obj.text,
                            "entities": entities
                        }
                        break

    return causes










'''
# STANFORD CORENLP 4.5.3 VERSION
def rank_beliefs(text):
    def get_sentences(parsed_text):
        return [sentence['tokens'] for sentence in parsed_text['sentences']]

    def join_sentence(sentence_tokens):
        return ' '.join(token['word'] for token in sentence_tokens)

    def split_sentences(text):
        output = nlp.annotate(text, properties={'annotators': 'ssplit', 'outputFormat': 'json'})
#        if not isinstance(output, dict):
#            raise Exception("Invalid output format. Please make sure the Stanford CoreNLP server is running and responding with JSON.")
        return [join_sentence(sentence['tokens']) for sentence in output['sentences']]


    hello_friend = {"actions": [], "sentences": []}
    sentences = split_sentences(text)

    for i, sent_text in enumerate(sentences):
        output = nlp.annotate(sent_text, properties={'annotators': 'tokenize,ssplit,pos,parse', 'outputFormat': 'json'})
#        if isinstance(output, str):
#            raise Exception("Invalid output format. Please make sure the Stanford CoreNLP server is running and responding with JSON.")
        parsed_sents = get_sentences(output)
        sent = parsed_sents[0]

        causes = get_causes(sent_text)
        for token in sent:
            if token['pos'] == "VB":
                for child in token['children']:
                    if child['text'] == "me":
                        action = token['text']
                        context_sents = sentences[max(0, i - 5) : i]
                        context = context_sents
                        hello_friend["actions"].append(
                            {
                                "action": action,
                                "object": child['text'],
                                "context": context,
                                "action_sentence": sent_text,
                                "actions": causes
                            }
                        )
                        break
        matched_beliefs = list(set([token['word'].lower() for token in sent if token['word'].lower() in beliefs]))
        if len(matched_beliefs) >= 4:
            context_sents = sentences[max(0, i - 5) : i]
            context = context_sents
            hello_friend["sentences"].append(
                {
                    "context": context,
                    "sentence_of_interest": sent_text,
                    "word_matches": matched_beliefs,
                    # "actions": causes,
                }
            )
        elif hello_friend["sentences"] and "word_matches" not in hello_friend["sentences"][-1]:
            # If no matched beliefs were found in the current sentence, but the previous
            # sentence in the list also did not have any matched beliefs, then remove the
            # previous dictionary from the list.
            hello_friend["sentences"].pop()
    hello_friend["sentences"] = sorted(
        hello_friend["sentences"], key=lambda x: -len(x.get("word_matches", []))
    )
    return hello_friend

'''









# SPACEY VERSION:
def rank_beliefs(text):
    hello_friend = {"actions": [], "sentences": []}
    doc = nlp(text)
    for i, sent in enumerate(doc.sents):
        causes = get_causes(sent.text)
        matched_beliefs = {}
        for token in sent:
            if token.lower_ in beliefs:
                matched_beliefs[token.lower_] = matched_beliefs.get(token.lower_, 0) + 1
        if matched_beliefs and len(matched_beliefs.keys()) >= 4:
            context_sents = list(doc.sents)[max(0, i - 5) : i]
            context = [sent.text for sent in context_sents]
            sorted_beliefs = dict(sorted(matched_beliefs.items(), key=lambda item: -item[1]))
            word_matches = {"words": sorted_beliefs, "number_of_matches": len(sorted_beliefs.keys()), "sum_of_matches": sum(sorted_beliefs.values())}
            hello_friend["sentences"].append(
                {
                    "context": context,
                    "sentence_of_interest": sent.text,
                    "word_matches": word_matches
                }
            )
        elif hello_friend["sentences"] and "word_matches" not in hello_friend["sentences"][-1]:
            hello_friend["sentences"].pop()
        for token in sent:
            if token.pos_ == "VERB":
                for child in token.children:
                    if child.text == "me":
                        action = token.text
                        context_sents = list(doc.sents)[max(0, i - 5) : i]
                        context = [sent.text for sent in context_sents]
                        hello_friend["actions"].append(
                            {
                                "action": action,
                                "object": child.text,
                                "context": context,
                                "action_sentence": sent.text,
                                "actions": causes
                            }
                        )
                        break
    hello_friend["sentences"] = sorted(
        hello_friend["sentences"], key=lambda x: -x["word_matches"]["sum_of_matches"]
    )
    return hello_friend








#####################################################################################################################################
# WORKS
def custom_dump(data, action_color='green', object_color='yellow'):
    term = Terminal()
    output = "{\n"

    def colored(text, color):
        return getattr(term, color)(text)

    for entry_idx, entry in enumerate(data):
        output += "    {\n"
        for key_idx, key in enumerate(entry):
            value = entry[key]

            if "action" in entry and "object" in entry:
                if key == "action":
                    value = colored(value, action_color)
                elif key == "object":
                    value = colored(value, object_color)
                elif key == "belief":
                    words = value.split(' ')
                    action_pattern = r'^{}$'.format(re.escape(entry["action"]))
                    object_pattern = r'^{}$'.format(re.escape(entry["object"]))

                    for idx, word in enumerate(words):
                        if re.match(action_pattern, word, re.IGNORECASE):
                            words[idx] = colored(word, action_color)
                        elif re.match(object_pattern, word, re.IGNORECASE):
                            words[idx] = colored(word, object_color)

                    value = ' '.join(words)

            # If the value is a list, format it with indentation
            if isinstance(value, list):
                output += f'        "{key}": [\n'
                for i, item in enumerate(value):
                    output += f'            "{item}"'
                    if i != len(value) - 1:
                        output += ","
                    output += "\n"
                output += "        ]"
            else:
                output += f'        "{key}": "{value}"'

            if key_idx != len(entry) - 1:
                output += ","
            output += "\n"

        output += "    }"
        if entry_idx != len(data) - 1:
            output += ","
        output += "\n"

    output += "}\n"

    return output














os.system('clear')
for filename in os.listdir('./Sandbox/JSON_sed'):
    print(f"FILE NAME: {filename}")
    with open('actions.txt', 'a+') as actions, open('sentences.txt', 'a+') as sentences:

        #####################################################################################################################################
        # Opening JSON file
        f = open(f'./Sandbox/JSON_sed/{filename}')
        json_data = json.load(f)
        f.close()
        #####################################################################################################################################

        #####################################################################################################################################
        date_regex = r"(\b\d{4}\b-\b\d{2}\b-\b\d{2}\b)"
        time_regex = r"(\b\d{2}\b-\b\d{2}\b-\b\d{2}\b)"

        date_match = re.search(date_regex, filename)
        time_match = re.search(time_regex, filename)

        date = date_match.group(1)
        time = time_match.group(1).replace("-", ":")

        datetime_str = f"{date} {time}"
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        actions.write('---------------------------------------------------------------------\n')
        actions.write(f"DATE: {date}\n")
        actions.write(f"TIME: {time}\n\n")

        sentences.write('---------------------------------------------------------------------\n')
        sentences.write(f"DATE: {date}\n")
        sentences.write(f"TIME: {time}\n\n")

 #       print(f"DATE: {date}")
 #       print(f"TIME: {time}")


        #####################################################################################################################################
        ranked_beliefs = rank_beliefs(json_data["text"])
#        print(f'BELIEFS:\n {json.dumps(ranked_beliefs, indent=4)}')

        # Keep track of unique sentences
        unique_actions = set()

        # Iterate over the list of data
        for action in ranked_beliefs['actions']:
            # Check if sentence has already been written to file
            if action['action_sentence'] not in unique_actions:
                # Write sentence to file
                actions.write(action['action_sentence'] + '\n')
                # Add sentence to set of unique sentences
                unique_actions.add(action['action_sentence'])

        # Keep track of unique sentences
        unique_sentences = set()
        # Iterate over the list of data
        for sentence in ranked_beliefs['sentences']:
            # Check if sentence has already been written to file
            if sentence['sentence_of_interest'] not in unique_sentences:
                # Write sentence to file
                sentences.write(sentence['sentence_of_interest'] + '\n')
                # Add sentence to set of unique sentences
                unique_sentences.add(sentence['sentence_of_interest'])
        actions.write('---------------------------------------------------------------------\n')
        sentences.write('---------------------------------------------------------------------\n')

    #print(f'BELIEFS:\n {custom_dump(rank_beliefs(json_data["text"]))}')
    #input("here")

    print(f'QUESTIONS:\n {json.dumps(find_questions_v2(json_data["text"]), indent=4)}')
    input("\nHERE\n")
'''
    sentiments = json_data["sentiment_analysis_results"]
    for sentiment in sentiments:
        beliefs_dict = find_beliefs(sentiment["text"])
        if beliefs_dict and any(beliefs_dict.values()):
            beliefs_dict_non_empty = {k: v for k, v in beliefs_dict.items() if v}
            if beliefs_dict_non_empty:
                print(f'BELIEFS:\n {json.dumps(beliefs_dict_non_empty, indent=4)}')        
                print(f'SENTIMENT : {sentiment["sentiment"]}')
                print(f'CONFIDENCE: {sentiment["confidence"]}')
'''


#    print(f'BELIEFS:\n {json.dumps(find_beliefs(json_data["text"]), indent=4)}')
    #print(f'QUESTIONS:\n {json.dumps(find_questions(json_data["text"]), indent=4)}')





#               LOOK UP THE SENTIMENT AND PROCESS THAT - THOSE ARE ALREADY SENTENCES 
#               * AND YOU WILL HAVE ADDITIONAL DATA *
