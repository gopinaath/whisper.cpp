import re
import logging
import os

# Cleans up streaming output of transcript redirected to a file.  
# Example: ./stream -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000 > discussion-10-sample.txt
# Tested only on Mac. 

INPUT_FILE = "./whisper.cpp/discussion-10-sample.txt"
CLEAN_FILE = "./whisper.cpp/discussion-10-sample-clean.txt"

logging.basicConfig(level=logging.INFO)

out_file_lines = []

regexp = re.compile(b'\x1b*2K\n')

with open(INPUT_FILE, 'r') as file:
    for line in file:
        line_bytes = bytes(line, 'utf-8')
        logging.debug("line_bytes {}", line_bytes)

        if regexp.search(line_bytes):
            logging.debug("..NOT added to transcript")
        else:
            out_file_lines.append(line)
            logging.debug(".. added to transcript")

logging.debug(out_file_lines)
logging.debug(type(out_file_lines))

if os.path.isfile(CLEAN_FILE):
    logging.info(CLEAN_FILE + " already exists.")
    os.remove(CLEAN_FILE)
    logging.info(CLEAN_FILE + " deleted.")

# open file in write mode
with open(CLEAN_FILE, 'w') as file:
    for line in out_file_lines:
        # write each item on a new line
        file.write("%s" % line)
    logging.info('Done')
