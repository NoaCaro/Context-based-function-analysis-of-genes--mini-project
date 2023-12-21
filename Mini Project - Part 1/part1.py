
### **Deciphering the functional role of a bacterial gene by colinearly conserved genomic neighborhood context**

Given a file of COG-spelled genomes, the parameters q, d and an unknown COG, the function find_words() finds all the strings of length d over the COG alphabet, that are conserved in ≥ q of the genomes in the database, such that the unknown COG appears at least once in each string.
"""

def find_words(q, d, unknown_cog):
  words_hash = dict() #hash map where the word is the key, and the value is a set of genomes' ids that contains the word
  with open('cog_words_bac.txt', 'r') as file:
      for line in file:
          fields = line.strip().split('\t')
          cogs = fields[1:] # skipping the first element in the parsed line to save just the cogs' numbers
          # check if the unknown cog is in the current line and if the cogs array contains less than d cogs - skip it since there won't be a word in length d
          if len(cogs) >= d and unknown_cog in cogs:
              genome_id = fields[0].split('#')[1] # after splitting the line by /t, split it by # to get the genome id, which is the first element
              # save the indexes of the unknown cog in the current line
              unknown_cog_indexes = []
              counter = 0
              for cog in cogs:
                if cog == unknown_cog:
                  unknown_cog_indexes.append(counter)
                counter += 1
              # find the valid words in length d that contain the unknown cog
              for cog_index in unknown_cog_indexes:
                # define the boundries for the words in size d while taking into consideration the array range
                start_index = cog_index-d+1 if cog_index-d+1>=0 else 0
                end_index = cog_index+d-1 if cog_index+d-1<len(cogs) else len(cogs)-1
                for i in range(start_index, end_index-d+2):
                  curr_word_array = cogs[i:i+d]
                  # add the word to the hash only if it isn't contain 'X'
                  if 'X' not in curr_word_array:
                    curr_word = "".join(cogs[i:i+d])
                    # add the current word to the words hash
                    if curr_word in words_hash:
                      words_hash[curr_word].add(genome_id)
                    else:
                      words_hash[curr_word] = {genome_id}

      # filter out the words that appear in less than q genomes and save the amount of genomes instead of the genomes set
      new_words_hash = {key: len(value) for key, value in words_hash.items() if len(value) >= q}
      return new_words_hash

"""The function process_and_display_results() calls the function find_words() with the parameter d varying from 3 to 25, as the longest word in the database.
Finally, it groups the results by their length, sort each group by decreasing quorum and prints the relevant words.
"""

def process_and_display_results():
  # calling the function find_words() with d=3 until d=25 (as the longest word in the file)
  for i in range(3,26):
    words_hash = find_words(10, i, "0488")
    # if the dict is not empty, sort by q and print
    if bool(words_hash):
      sorted_words_hash = dict(sorted(words_hash.items(), key=lambda x: x[1], reverse=True))
      print("\033[1m\033[4m\033[30m\033[7mThe words of length " + str(i) + " are:\033[0m")
      print()
      counter = 1
      for key, value in sorted_words_hash.items():
        print(str(counter) + ") The word: " + key)
        print("Amount of genomes the word appears in: " + str(value))
        counter += 1
        print()
        print()
    else: # if the dict is empty - there are no valid words of this length
      print("\033[1m\033[4m\033[30m\033[7mThere are no valid words of length " + str(i) + " and above" "\033[0m")
      print()
      return # return in order not to check longer words
    print()
    print("-"*200)
    print()

process_and_display_results()

"""________________________________________________________________________________
________________________________________________________________________________
________________________________________________________________________________


**EXTRA - Additional code to help analyze our COG**

Updated function process_and_display_results() to also print the cogs' description.

Using the function cogs_description() which parses the cog_info_table data.

"""

def cogs_description():
  cogs_hash = dict()
  with open('COG_INFO_TABLE.txt', 'r', encoding='ISO-8859-1') as file:
    for line in file:
      fields = line.split(';')
      cog = fields[0][3:] # removing the word "COG" to save only the identifier
      cog_info = fields[1:-1] # minus 1 to excluse the "\n"
      cogs_hash[cog] = cog_info
  return cogs_hash

def process_and_display_results():
  # add description to the cogs in each word
  cogs_hash = cogs_description()

  # calling the function find_words() with d=3 until d=25 (as the longest word in the file)
  for i in range(3,26):
    words_hash = find_words(10, i, "0488")
    # if the dict is not empty, sort by q and print
    if bool(words_hash):
      sorted_words_hash = dict(sorted(words_hash.items(), key=lambda x: x[1], reverse=True))
      print("\033[1m\033[4m\033[30m\033[7mThe words of length " + str(i) + " are:\033[0m")
      print()
      counter = 1
      for key, value in sorted_words_hash.items():
        print(str(counter) + ") The word: " + key)
        print("Amount of genomes the word appears in: " + str(value))
        print("Cogs analysis:")
        cogs_word = [key[i:i+4] for i in range(0, len(key), 4)]
        for cog in cogs_word:
          print(cog + ": " + str(cogs_hash[cog]))
        counter += 1
        print()
        print()
    else: # if the dict is empty - there are no valid words of this length
      print("\033[1m\033[4m\033[30m\033[7mThere are no valid words of length " + str(i) + " and above" "\033[0m")
      print()
      return # return in order not to check longer words
    print()
    print("-"*200)
    print()

process_and_display_results()
