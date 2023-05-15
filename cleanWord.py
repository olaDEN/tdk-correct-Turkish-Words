from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM

# Set the path to the Zemberek JAR file
ZEMBEREK_PATH = "zemberek-full.jar"

# Start the JVM 
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (ZEMBEREK_PATH))

# Loadıng the TurkishMorphology and TurkishSpellChecker classes
TurkishMorphology = JClass("zemberek.morphology.TurkishMorphology")
TurkishSpellChecker = JClass("zemberek.normalization.TurkishSpellChecker")

# Create instances of TurkishMorphology and TurkishSpellChecker
morphology = TurkishMorphology.createWithDefaults()
spell_checker = TurkishSpellChecker(morphology)

input_file_path = "input.txt"
output_file_path = "output.txt"

# Open the files for reading an writing
with open(input_file_path, "r", encoding="utf-8") as input_file, open(
    output_file_path, "w", encoding="utf-8"
) as output_file:
    
    unique = set()
    for line in input_file:
        # Strip any leading or trailing whitespace from the line
        line = line.strip()
        # Check if the line is empty
        if not line:
            # Skip
            continue
        words = line.split()
        corrected = []
        for word in words:
            if word in unique:
                continue
            if spell_checker.check(JString(word)):
                # If the word is spelled correctly, add it to the list 
                corrected.append(word)
                unique.add(word)
            else:
                # If the word is misspelled, suggest a correction
                suggestions = spell_checker.suggestForWord(JString(word))
                if suggestions.size() > 0:
                    corrected_word = str(suggestions.get(0))
                    corrected.append(corrected_word)
                    unique.add(corrected_word)
                    #print(f"Misspelled word '{word}' corrected to '{corrected_word}'")
                else:
                    # If no correction could be suggested, print a message to the console
                    # print(f"No suggestion for misspelled word '{word}'")
                    corrected.append(word)
                    unique.add(word)
        # Convert the word to lowercase if it starts with a capital letter
        if line[0].isupper():
            line = line.lower()
        # Write the corrected words to the output file
        if corrected:
            output_file.write("\n".join(corrected))
            output_file.write("\n")

# Shutdown the JVM
shutdownJVM()




# 