
### **Genome Analysis and COG Deciphering:**
### **Improving Results through Mutation-Aware Algorithmic Approach**

The function **find_words()** was also used in part A – it finds all the strings of length d over the COG alphabet, such that the unknown COG appears in. In part A it returns only the valid words that appear in at least q genomes, but now this function also returns the words that appear in less than q genomes.
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

      # save the amount of genomes instead of the genomes set
      new_words_hash = {key: len(value) for key, value in words_hash.items()}
      return new_words_hash

"""The function **find_extensions()** looks for valid extensions for the base_words.
It uses the functions:
* **find_k()** - given d (the length of the word), find k (the maximum amount of insertions allowed), which is d/4
* **compare_words()** - check if filtered_out_word is a valid extension of curr_base_word - meaning no more than k insertions
"""

# given d (the length of the word), find k (the maximum amount of insertions)
def find_k(d):
    # k is defined as quarter of the d,
    # therefore we will divide d by 4 and round it using %4,
    # since d%4=2 if d/4=0.5
    if(d%4 <2):
        k  = int(d/4)
    else:
        k = int(d/4)+1
    return k



# check if filtered_out_word is a valid extension of curr_base_word - meaning no more than k insertions,
# return 0 if filtered_out_word is a valid extension, and -1 if it is not
def compare_words(curr_base_word, filtered_out_word, k):
  num_of_insertions = 0
  # for convenience - split the words to array - each cog in a different cell
  base_word_array = [curr_base_word[i:i+4] for i in range(0, len(curr_base_word), 4)]
  filtered_word_array = [filtered_out_word[i:i+4] for i in range(0, len(filtered_out_word), 4)]
  base_word_len = len(base_word_array)
  filtered_word_len = len(filtered_word_array)
  base_word_index = 0
  filtered_word_index = 0
  while (base_word_index < base_word_len and filtered_word_index < filtered_word_len and num_of_insertions <= k):
    # if the currect cog is identical, continue to check the next cog
    if (base_word_array[base_word_index] == filtered_word_array[filtered_word_index]):
      base_word_index += 1
      filtered_word_index += 1
    # if the currect cog is different:
    # - check if it is the first cog / last cog - since insertions can be only in the middle of the base word in a valid extension
    # - check if num_of_insertions is already == k
    elif (base_word_index==0 or base_word_index==base_word_len-1 or num_of_insertions == k):
      return -1
    # if the currect cog is different but the current insertion is valid
    else:
      num_of_insertions += 1
      filtered_word_index += 1

  # check if filtered_out_word is a valid extension of curr_base_word -
  # meaning we reached the end of these words while comparing the cogs and verifying no more than k insertions were made in the middle of base_word
  if (base_word_index == base_word_len and filtered_word_index == filtered_word_len and num_of_insertions <= k):
    return 0

  else:
    return -1



# look for valid extensions for the base_words
def find_extensions(base_words, filtered_out_words, extension_words):
  for d in range(3,26):
    curr_base_words_dict = base_words[d]
    k = find_k(d) # find k (the maximum amount of insertions), which is d/4
    for curr_base_word in curr_base_words_dict.keys():
      # go over the possible extensions to the current base word, while the extension word's length can be d+1 until d+k as the maximum amount of insertions
      for filtered_out_words_dict in filtered_out_words[d+1:d+k+1]:
          for filtered_out_word in filtered_out_words_dict.keys():
            # check if filtered_out_word is a valid extension of curr_base_word
            valid = compare_words(curr_base_word, filtered_out_word, k)
            if (valid==0): # valid extension
              # add to the extension_words the extension word we just found
              extension_words[curr_base_word].append(filtered_out_word)
  return extension_words

"""The function **main()** :
- Calls the function find_words() with the parameter d varying from 3 to 25 in order to find words in the desired length that contains the unknown COG.
- Than it calls the function find_extensions() in order to look for valid extensions for the base_words which allow until k insertions.
- Prints the base words found and their exttensions

"""

def main():
  ### initializations ###
  # extension_words is a dict in which the key is the base word (string), and the value is an array that contains the extension words this base word appears in
  extension_words = {}

  # base_words is an array of the valid words found, which appear in >= q genomes (the words used in part 1 of the mini project)
  # for convenient, the array size is 26, in order that cell d will represent the length d
  base_words = [0]*26
 # filtered_out_words is an array of words that contains the COG but appear in < q genomes (these words were filtered out in part 1 of the mini project)
  filtered_out_words = [0]*26

  # here we used q=10 and COG=0488 (can be modified)
  q = 10
  unknown_cog = "0488"


  ### call find_words() with varying d ###
  for d in range(3,26): # d=3 until d=25 (as the longest word in the file)
    temp_words_hash = find_words(q, d, unknown_cog)

    # break if there are no valid words of length d
    if (len(temp_words_hash)==0):
      break

    # split temp_words_hash returned from find_words() to words that appear in more/less than q genomes
    base_words[d] = {key: value for key, value in temp_words_hash.items() if value >= q}
    filtered_out_words[d] = {key: value for key, value in temp_words_hash.items() if value < q}

    # save the base words (strings) as the keys of extension_words
    for base_word in base_words[d]:
      extension_words[base_word] = []

  ### look for valid extensions for the base_words ###
  extension_words = find_extensions(base_words, filtered_out_words, extension_words)

  ### print the base words and the extension words found ###
  for d in range(3,26):
    curr_base_words = base_words[d]

    # if it is empty - there are no base words of this length or more
    if (len(curr_base_words)==0):
      print("\033[1m\033[4m\033[30m\033[7mThere are no valid words of length " + str(d) + " and above" "\033[0m")
      print()
      return # return in order not to check longer words

    # else - print the base words and their extensions
    curr_base_words_sorted = sorted(curr_base_words, key=curr_base_words.get, reverse=True) # sort the base words in decreasing order of q
    print("\033[1m\033[4m\033[30m\033[7mThe words of length " + str(d) + " are:\033[0m")
    base_counter = 1
    for base_word in curr_base_words_sorted:
      print()
      print(str(base_counter) + ") " + "\033[1m\033[4m\033[30m\033[7mThe base word\033[0m" + ": " + base_word)

      print("Amount of genomes the word appears in: " + str(curr_base_words[base_word]))
      base_counter += 1

      base_word_extensions = extension_words[base_word]
      if (len(base_word_extensions)==0):
        print("\033[1m\033[30m\033[7mThere are no valid extensions words\033[0m")
        print()
      else:
        extension_counter = 1
        print("\033[1m\033[30m\033[7mThe extension words found are:\033[0m")
        for extension in base_word_extensions:
          print("  " + str(extension_counter) + ". " + extension)
          extension_len = int(len(extension)/4)
          print("     Amount of genomes the extension word appears in: " + str(filtered_out_words[extension_len][extension]))
          extension_counter += 1

    print()
    print("-"*200)
    print()

main()

"""________________________________________________________________________________
________________________________________________________________________________
________________________________________________________________________________


**EXTRA - Additional code to help analyze our COG**

Updated **main()** to also print the cogs' description.

Using the function **cogs_description()** which parses the cog_info_table data.

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



def main():
  ### initializations ###
  # extension_words is a dict in which the key is the base word (string), and the value is an array that contains the extension words this base word appears in
  extension_words = {}

  # base_words is an array of the valid words found, which appear in >= q genomes (the words used in part 1 of the mini project)
  # for convenient, the array size is 26, in order that cell d will represent the length d
  base_words = [0]*26
 # filtered_out_words is an array of words that contains the COG but appear in < q genomes (these words were filtered out in part 1 of the mini project)
  filtered_out_words = [0]*26

  # here we used q=10 and COG=0488 (can be modified)
  q = 10
  unknown_cog = "0488"

  # create cogs_hash in order to add description to the cogs in each word
  cogs_hash = cogs_description()


  ### call find_words() with varying d ###
  for d in range(3,26): # d=3 until d=25 (as the longest word in the file)
    temp_words_hash = find_words(q, d, unknown_cog)

    # break if there are no valid words of length d
    if (len(temp_words_hash)==0):
      break

    # split temp_words_hash returned from find_words() to words that appear in more/less than q genomes
    base_words[d] = {key: value for key, value in temp_words_hash.items() if value >= q}
    filtered_out_words[d] = {key: value for key, value in temp_words_hash.items() if value < q}

    # save the base words (strings) as the keys of extension_words
    for base_word in base_words[d]:
      extension_words[base_word] = []


  ### look for valid extensions for the base_words ###
  extension_words = find_extensions(base_words, filtered_out_words, extension_words)

  ### print the base words and the extension words found ###
  for d in range(3,26):
    curr_base_words = base_words[d]

    # if it is empty - there are no base words of this length or more
    if (len(curr_base_words)==0):
      print("\033[1m\033[4m\033[30m\033[7mThere are no valid words of length " + str(d) + " and above" "\033[0m")
      print()
      return # return in order not to check longer words

    # else - print the base words and their extensions
    curr_base_words_sorted = sorted(curr_base_words, key=curr_base_words.get, reverse=True) # sort the base words in decreasing order of q
    print("\033[1m\033[4m\033[30m\033[7mThe words of length " + str(d) + " are:\033[0m")
    base_counter = 1
    for base_word in curr_base_words_sorted:
      print()
      print(str(base_counter) + ") " + "\033[1m\033[4m\033[30m\033[7mThe base word\033[0m" + ": " + base_word)

      print("  * Amount of genomes the word appears in: " + str(base_words[d][base_word]))
      print("  * " + "\033[1m\033[30m\033[7mCogs analysis:\033[0m")
      cogs_word = [base_word[i:i+4] for i in range(0, len(base_word), 4)]
      for cog in cogs_word:
        print("     " + cog + ": " + str(cogs_hash[cog]))
      base_counter += 1

      base_word_extensions = extension_words[base_word]
      if (len(base_word_extensions)==0):
        print("  * " + "\033[1m\033[30m\033[7mThere are no valid extensions words\033[0m")
        print()
      else:
        extension_counter = 1
        print("  * " + "\033[1m\033[30m\033[7mThe extension words found are:\033[0m")
        for extension in base_word_extensions:
          print("    " + str(extension_counter) + ". " + extension)
          extension_len = int(len(extension)/4)
          print("     Amount of genomes the extension word appears in: " + str(filtered_out_words[extension_len][extension]))
          print("     " + "\033[1m\033[30m\033[7mCogs analysis:\033[0m")
          cogs_word = [extension[i:i+4] for i in range(0, len(extension), 4)]
          for cog in cogs_word:
            print("      " + cog + ": " + str(cogs_hash[cog]))
          print()
          extension_counter += 1

    print()
    print("-"*200)
    print()

main()
